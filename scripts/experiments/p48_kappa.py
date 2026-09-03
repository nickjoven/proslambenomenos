#!/usr/bin/env python3
"""P-48 registered runner: the stiffness clock and the tail law
toward the band edge. Clauses and cells fixed in PREDICTIONS.md P-48
before this ran; every definition (the kappa map, the identity
residual, the trajectory comparison, the P-46 instrument with both
references, the mixing floor) imported from p48_derive.py, whose
validation numbers are pinned in p48_derive.json and not rerun here.

Cells (twisted sector 0, N = 64, reduced load f/kappa = fold + 0.005,
ramp 200, dt = 0.001 at kappa = 1):
  (a) the one-step map identity at kappa in {0.5, 2, 3}, two velocity
      scales, 20000 states each, seed 20260903;
  (a2) dyadic kappa in {1/4, 4}: the trajectories through the slip
      are bit-identical to the unit-stiffness run;
  (b) kappa in {0.5, 2, 3}: identical event steps, phase deviation
      within 32 eps x steps x max|theta|;
  (c) the gamma ladder at kappa = 1, gamma in {0.2, 0.35, 0.45,
      0.5, 0.6, 0.8}: the tail law under the rotor-phase reference;
  reported: the bond-phase reference beside it, gamma = 1 (in band),
      the Omega/2 content, the rotor's slowing, the event times.

Run: python3 scripts/experiments/p48_kappa.py [--quick]
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
from p48_derive import (EPS, OPS, gamma_ladder_cell, one_step_identity,  # noqa: E402
                        trajectory_scaling)

LADDER = (0.2, 0.35, 0.45, 0.5, 0.6, 0.8)


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    N = 64
    fold = fold_fc(N, -math.pi)
    f1 = fold + 0.005
    out = {"seed": 20260903, "N": N, "fold": fold, "f1": f1, "eps": EPS, "ops": OPS}
    verdict = {}

    # (a) the map identity
    rng = random.Random(20260903)
    M = 200 if quick else 20000
    ids = {}
    a_ok = True
    for kappa in (0.5, 2.0, 3.0):
        for vmax in (2.0, 100.0):
            r = one_step_identity(rng, N, M, 0.1, kappa * f1, kappa, 0.001, vmax)
            ids["kappa_%g_vmax_%g" % (kappa, vmax)] = r
            a_ok &= r["worst_v_ratio"] <= 1.0 and r["worst_theta_ratio"] <= 1.0
            print("(a) kappa %g vmax %g: v %.3f theta %.3f" % (kappa, vmax, r["worst_v_ratio"], r["worst_theta_ratio"]), flush=True)
    out["one_step"] = ids
    verdict["a_holds"] = a_ok

    # (a2) dyadic, (b) non-dyadic trajectories through the slip
    traj = {}
    a2_ok = True
    b_ok = True
    dt = 0.01 if quick else 0.001
    for kappa in (0.25, 4.0, 0.5, 2.0, 3.0):
        r = trajectory_scaling(N, 0.1, f1, kappa, dt)
        # the derived deviation bound: per-step rounding on the largest
        # phase reached, accumulated linearly over the run's steps
        r["bound_dtheta"] = OPS * EPS * r["n_steps"] * r["theta_max"]
        r.pop("profile", None)
        same = (r["event_step_A"] is not None and r["event_step_A"] == r["event_step_B"])
        if kappa in (0.25, 4.0):
            r["bit_identical"] = same and r["max_dtheta"] == 0.0 and r["max_dv"] == 0.0
            a2_ok &= r["bit_identical"]
        else:
            r["within_bound"] = same and r["max_dtheta"] <= r["bound_dtheta"]
            b_ok &= r["within_bound"]
        traj["kappa_%g" % kappa] = r
        print("(a2/b) kappa %g: events %s/%s max dtheta %.2e (bound %.1e) max dv %.2e (%.0f s)"
              % (kappa, r["event_step_A"], r["event_step_B"], r["max_dtheta"], r["bound_dtheta"], r["max_dv"], r["seconds"]), flush=True)
    out["trajectories"] = traj
    verdict["a2_holds"] = a2_ok
    verdict["b_holds"] = b_ok

    # (c), (d) the gamma ladder, both references
    ladder = {}
    c_ok = True
    gammas = (0.5,) if quick else LADDER + (1.0,)
    for g in gammas:
        cell = gamma_ladder_cell(N, f1, g, dt=dt)
        ladder["gamma_%g" % g] = cell
        if cell.get("empty"):
            print("gamma %g: EMPTY (event %s)" % (g, cell["event_t"]), flush=True)
            if g in LADDER:
                c_ok = False
            continue
        ck = cell["checks"]
        registered = g in LADDER
        if registered:
            c_ok &= ck["ratio21_rotor_in_band"]
        print("gamma %g%s: event %.1f Omega %.3f | (c) ratio21 rotor %.4e in band %s | (d) A1 bond in band %s (rel %+.1e), bond excess covered %s (excess %+.1f%%, mixing %.1f%% of A2) | smear %.3f | Omega/2 at 4 over floor %.1f (%.0f s)"
              % (g, "" if registered else " [reported]", cell["event_t"], cell["Omega_measured"],
                 ck["ratio21_rotor"], ck["ratio21_rotor_in_band"], ck["A1_bond_in_band"], ck["A1_bond_rel_to_band"],
                 ck["bond_excess_covered"], 100 * ck["ratio21_bond_excess_over_top"], 100 * ck["mixing_over_A2_bond"],
                 ck["smear_rotor_ref_A1"], cell["subharmonic"]["half_at_4_over_floor"], cell["seconds"]), flush=True)
    out["gamma_ladder"] = ladder
    verdict["c_holds"] = c_ok
    # the two references, REPORTED (the derive layer read the bond-
    # reference excess non-monotone along the ladder: 4, 24, 23, 27,
    # 16, 4 percent - no clause; the mechanism is a candidate)
    cells = [ladder["gamma_%g" % g] for g in LADDER if not ladder["gamma_%g" % g].get("empty")]
    out["reference_comparison_unregistered"] = {
        "gammas": list(LADDER),
        "bond_excess_over_top": [c["checks"]["ratio21_bond_excess_over_top"] for c in cells],
        "rotor_ref_smear_A1": [c["checks"]["smear_rotor_ref_A1"] for c in cells],
        "first_order_mixing_over_A2": [c["checks"]["mixing_over_A2_bond"] for c in cells],
        "A1_bond_rel_to_band": [c["checks"]["A1_bond_rel_to_band"] for c in cells],
        "Omega_over_terminal": [c["Omega_over_terminal"] for c in cells],
        "event_t": [c["event_t"] for c in cells]}
    print("reported: bond excess", ["%+.3f" % c["checks"]["ratio21_bond_excess_over_top"] for c in cells],
          "smear", ["%.3f" % c["checks"]["smear_rotor_ref_A1"] for c in cells])
    out["clauses"] = verdict
    out["seconds_total"] = time.time() - t0
    name = "p48_results%s.json" % ("_quick" if quick else "")
    with open(os.path.join(HERE, name), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(verdict), "in %.0f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
