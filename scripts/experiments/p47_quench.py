#!/usr/bin/env python3
"""P-47 registered runner: classical Kibble-Zurek quenches of the free
pi ring with exact half-sector counting. Clauses and cells fixed in
PREDICTIONS.md P-47 before this ran; the shared density, the
Langevin ring and the statistics imported from p47_derive.py (its
validation cells are not rerun here).

Cells: N = 64, J = 1, gamma = 1, T_i = 2, dt = 0.05, burn 20,
settle 20; tau_Q ladder {0, 5, 20, 80, 320}; M = 200 realizations
per ring per rung, control and twisted, seed 20260903.

Run: python3 scripts/experiments/p47_quench.py [--quick]
"""
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p47_derive import (TAU, bond_moments, inner_prob, lattice_moments,  # noqa: E402
                        model_se, predict_tw_from_c, quench_sample, stats)


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    N = 64
    gamma, T_i, dt = 1.0, 2.0, 0.05
    ladder = [0.0, 5.0, 20.0, 80.0, 320.0]
    M = 20 if quick else 200
    Ts = [0.03, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0, 1.5, 2.0]
    rng = random.Random(20260903)
    u2 = bond_moments(T_i)
    fast_null = N * u2 / TAU ** 2
    out = {"N": N, "gamma": gamma, "T_i": T_i, "dt": dt, "M": M,
           "fast_null_iid": fast_null, "seed": 20260903, "rungs": {}}
    verdict = {"a": True, "b": True, "c": True, "d": True}
    for tau in ladder:
        t1 = time.time()
        rec = {"tau_Q": tau}
        for tw in (False, True):
            Ws, Wr, offs = [], [], []
            for _ in range(M):
                W, W_ramp, off = quench_sample(N, tw, gamma, T_i, tau, dt, rng)
                Ws.append(W)
                Wr.append(W_ramp if W_ramp is not None else W)
                offs.append(off)
            st = stats(Ws)
            st["ramp_end"] = stats(Wr)
            st["changed_in_settle"] = sum(1 for a, b in zip(Ws, Wr) if abs(a - b) > 0.25)
            st["worst_lattice_off"] = max(offs)
            st["min_W2"] = min(w * w for w in Ws)
            rec["twisted" if tw else "control"] = st
        # (a) exact lattice at every sample; (d) the half-quantum floor
        a_ok = (rec["control"]["worst_lattice_off"] <= 1e-12
                and rec["twisted"]["worst_lattice_off"] <= 1e-12)
        d_ok = rec["twisted"]["min_W2"] >= 0.25 - 1e-12
        # (b) the fast null on the ramp-end count at tau_Q = 0
        if tau == 0.0:
            for key in ("control", "twisted"):
                re_ = rec[key]["ramp_end"]
                re_["fast_null"] = fast_null
                re_["z_fast"] = (re_["E"] - fast_null) / re_["SE"]
                re_["holds"] = abs(re_["z_fast"]) <= 3.0
                verdict["b"] &= re_["holds"]
        # (c) the shared density: twisted predicted from control
        Ec = rec["control"]["E"]
        Teff, Et_pred = predict_tw_from_c(N, Ec, Ts)
        _, _, Pc_eff, Pt_eff = lattice_moments(N, Teff)
        Ec_up = Ec + rec["control"]["SE"]
        _, Et_up = predict_tw_from_c(N, Ec_up, Ts)
        se_comb = math.sqrt(model_se(Pt_eff, M) ** 2 + (Et_up - Et_pred) ** 2)
        z = (rec["twisted"]["E"] - Et_pred) / se_comb
        p_pred = inner_prob(Pt_eff)
        p_meas = rec["twisted"]["p_inner"]
        se_p = math.sqrt(max(p_pred * (1 - p_pred), 1e-9) / M)
        # propagate the control's error into p_pred as well
        _, _, _, Pt_up = lattice_moments(N, predict_tw_from_c(N, Ec_up, Ts)[0])
        se_p_comb = math.sqrt(se_p ** 2 + (inner_prob(Pt_up) - p_pred) ** 2)
        rec["shared_density"] = {
            "T_eff_from_control": Teff, "E_tw_pred": Et_pred, "SE_combined": se_comb,
            "z": z, "E_holds": abs(z) <= 3.0,
            "p_inner_pred": p_pred, "p_inner_meas": p_meas, "SE_p_combined": se_p_comb,
            "z_p": (p_meas - p_pred) / se_p_comb,
            "p_holds": abs(p_meas - p_pred) <= 3.0 * se_p_comb,
            "P_tw_pred": {str(k): v for k, v in Pt_eff.items() if v > 1e-6},
            "P_c_pred": {str(k): v for k, v in Pc_eff.items() if v > 1e-6}}
        c_ok = rec["shared_density"]["E_holds"] and rec["shared_density"]["p_holds"]
        rec["a_holds"], rec["c_holds"], rec["d_holds"] = a_ok, c_ok, d_ok
        verdict["a"] &= a_ok
        verdict["c"] &= c_ok
        verdict["d"] &= d_ok
        rec["seconds"] = time.time() - t1
        out["rungs"][str(tau)] = rec
        print("tau_Q %g: control E %.3f+-%.3f (ramp-end %.3f) twisted E %.3f+-%.3f (ramp-end %.3f); "
              "T_eff %.3f pred %.3f z %.2f; p_inner %.3f vs %.3f z %.2f; lattice %.1e; a %s c %s d %s (%.0f s)"
              % (tau, Ec, rec["control"]["SE"], rec["control"]["ramp_end"]["E"],
                 rec["twisted"]["E"], rec["twisted"]["SE"], rec["twisted"]["ramp_end"]["E"],
                 Teff, Et_pred, z, p_meas, p_pred, rec["shared_density"]["z_p"],
                 max(rec["control"]["worst_lattice_off"], rec["twisted"]["worst_lattice_off"]),
                 a_ok, c_ok, d_ok, rec["seconds"]), flush=True)
    # (e) ordering: the instantaneous quench holds more winding than the slowest
    r0, rs = out["rungs"]["0.0"]["control"], out["rungs"][str(ladder[-1])]["control"]
    gap = r0["E"] - rs["E"]
    se_gap = math.sqrt(r0["SE"] ** 2 + rs["SE"] ** 2)
    out["ordering"] = {"E_fast": r0["E"], "E_slow": rs["E"], "gap": gap,
                       "SE": se_gap, "z": gap / se_gap, "holds": gap > 3.0 * se_gap}
    verdict["e"] = out["ordering"]["holds"]
    # reported: local exponents of the control's final count
    keys = [k for k in ladder if k > 0]
    ex = []
    for a, b in zip(keys, keys[1:]):
        Ea, Eb = out["rungs"][str(a)]["control"]["E"], out["rungs"][str(b)]["control"]["E"]
        ex.append({"from": a, "to": b, "exponent": -math.log(Eb / Ea) / math.log(b / a)})
    out["local_exponents_unregistered"] = ex
    print("ordering fast vs slow: %.3f vs %.3f (z %.2f) holds %s; local exponents %s"
          % (r0["E"], rs["E"], out["ordering"]["z"], out["ordering"]["holds"],
             [(e["from"], e["to"], round(e["exponent"], 3)) for e in ex]))
    out["clauses"] = {k + "_holds": v for k, v in verdict.items()}
    out["seconds_total"] = time.time() - t0
    name = "p47_results%s.json" % ("_quick" if quick else "")
    with open(os.path.join(HERE, name), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out["clauses"]), "in %.0f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
