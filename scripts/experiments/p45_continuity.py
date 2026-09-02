#!/usr/bin/env python3
"""P-45 registered runner: the site-energy continuity identity on
the P-35/P-36 inertial pi ring. Clauses and cells fixed in
PREDICTIONS.md P-45 before this ran; definitions (site energy,
bond current, residual bound, the Euler-Cromer bookkeeping and the
order-discrimination ladder verdict) imported from the derive
layer p45_derive.py, whose validation cells are NOT rerun here.

Cells:
  (a)-(c) one million random states at N = 64, f = the slip-cell
      load, gamma = 0.02: control and twisted rings at the band
      velocity scale vmax = 2 (400k each) and the rotor scale
      vmax = 100 (100k each); seed 20260902.
  (d) the P-36 grid pre-onset: {control, twist0, twist1} x
      N in {64, 96, 128}, f = fold(cell) - 0.10, soft ramp 200,
      hold 100, the dt = 0.02 / 0.01 / 0.005 ladder.
  (e) the slip cell: twist0, N = 64, f = fold + 0.005 (the first
      P-36 grid level above the derived fold - no equilibrium
      exists there, so the event's existence is dt-independent),
      soft ramp 200, run to the P-36 event plus 40 units (hold cap
      200), the dt = 0.001 / 0.0005 / 0.00025 ladder
      (dt0 f / gamma = 0.098 rad per step at the rotor speed).

Run: python3 scripts/experiments/p45_continuity.py [--quick]
"""
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc  # noqa: E402
from p45_derive import GAMMA, ORDER_BAND, ensemble, first_order, ladder  # noqa: E402


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    N = 64
    fold_t0 = fold_fc(N, -math.pi)
    f_slip = fold_t0 + 0.005
    out = {"seed": 20260902, "gamma": GAMMA, "f_slip_cell": f_slip,
           "order_band": list(ORDER_BAND)}

    # (a)-(c): the identity at random states
    rng = random.Random(20260902)
    plan = [(False, 2.0, 400000), (True, 2.0, 400000),
            (False, 100.0, 100000), (True, 100.0, 100000)]
    if quick:
        plan = [(tw, vm, M // 100) for tw, vm, M in plan]
    ens = []
    for twisted, vmax, M in plan:
        e = ensemble(rng, N, twisted, vmax, M, f_slip)
        ens.append(e)
        print("ensemble twisted=%s vmax=%g M=%d: site %.3f seam %.3f "
              "global %.3f tele %.3f (abs site %.1e global %.1e)"
              % (twisted, vmax, M, e["worst_site_ratio"], e["worst_seam_ratio"],
                 e["worst_global_ratio"], e["worst_telescoping_ratio"],
                 e["worst_site_abs"], e["worst_global_abs"]), flush=True)
    out["ensembles"] = ens
    a_holds = all(e["worst_site_ratio"] <= 1.0 for e in ens)
    b_holds = all(e["worst_global_ratio"] <= 1.0
                  and e["worst_telescoping_ratio"] <= 1.0 for e in ens)
    c_holds = all(e["worst_seam_ratio"] <= 1.0 for e in ens if e["twisted"])
    out["states_total"] = sum(e["M"] for e in ens)

    # (d): the P-36 grid pre-onset, the dt = 0.02 ladder
    cells = {}
    Ns = [64] if quick else [64, 96, 128]
    for n in Ns:
        for tag, tw, sec in (("control", False, 0), ("twist0", True, 0),
                             ("twist1", True, 1)):
            total = ((2 * sec - 1) * math.pi) if tw else 0.0
            fold = fold_fc(n, total)
            t1 = time.time()
            L = ladder(n, tw, sec, GAMMA, fold - 0.10, 0.02,
                       t_ramp=200.0, t_hold=100.0)
            rec = {k: v for k, v in L.items() if k != "runs"}
            rec.update({"N": n, "f": fold - 0.10, "fold": fold,
                        "seconds": time.time() - t1})
            key = "%s_N%d" % (tag, n)
            cells[key] = rec
            print(key, "D_global", ["%.3e" % x for x in L["global_defects"]],
                  "r %.4f %.4f" % (L["r1_global"], L["r2_global"]),
                  "D_local", ["%.3e" % x for x in L["local_defects"]],
                  "r %.4f %.4f" % (L["r1_local"], L["r2_local"]),
                  "first-order", L["first_order_global"], L["first_order_local"],
                  flush=True)
    out["ladder_cells"] = cells
    d_holds = all(c["first_order_global"] and c["first_order_local"]
                  for c in cells.values())

    # (e): the slip cell
    dt0 = 0.02 if quick else 0.001
    t1 = time.time()
    L = ladder(N, True, 0, GAMMA, f_slip, dt0, t_ramp=200.0, t_hold=200.0,
               after_event=40.0)
    slip = {k: v for k, v in L.items() if k != "runs"}
    slip.update({"N": N, "f": f_slip, "fold": fold_t0, "dt0": dt0,
                 "rad_per_step_at_f_over_gamma": dt0 * f_slip / GAMMA,
                 "seconds": time.time() - t1,
                 "footprint_by_dt": [r["footprint"] for r in L["runs"]],
                 "site_b_by_dt": [r["site_decomposition_b"] for r in L["runs"]],
                 "global_by_dt": [{"E_change": r["E_change"], "injected": r["injected"],
                                   "dissipated": r["dissipated"]} for r in L["runs"]]})
    out["slip_cell"] = slip
    e_event = all(t is not None for t in L["event_t"])
    e_holds = e_event and L["first_order_global"] and L["first_order_local"]
    print("slip cell: events", L["event_t"],
          "D_global", ["%.3e" % x for x in L["global_defects"]],
          "r %.4f %.4f" % (L["r1_global"], L["r2_global"]),
          "D_local", ["%.3e" % x for x in L["local_defects"]],
          "r %.4f %.4f" % (L["r1_local"], L["r2_local"]),
          "first-order", L["first_order_global"], L["first_order_local"], flush=True)
    print("  footprint at dt0:", json.dumps(L["runs"][0]["footprint"]))
    print("  loaded site at dt0:", json.dumps(L["runs"][0]["site_decomposition_b"]))

    out["clauses"] = {"a_holds": a_holds, "b_holds": b_holds, "c_holds": c_holds,
                      "d_holds": d_holds, "e_event_at_every_dt": e_event,
                      "e_holds": e_holds}
    out["seconds_total"] = time.time() - t0
    name = "p45_results%s.json" % ("_quick" if quick else "")
    with open(os.path.join(HERE, name), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out["clauses"]), "in %.0f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
