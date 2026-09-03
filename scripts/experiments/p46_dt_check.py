#!/usr/bin/env python3
"""p46_dt_check.py - the R-45b check on P-46 clause (c): does the
neighbour's amplitude A_1 resolve the difference between the exact
Euler-Cromer discrete response and the continuous-time response?

Reads the registered run (dt = 0.001, p46_results.json) and the
dt-halving rerun (dt = 0.0005, p46_results_dt0.0005.json, produced by
P46_DT=0.0005 python3 p46_aftermath.py). For each registered window
it evaluates both responses over the window's Omega and stiffness
ranges (p46_derive.evanescent with and without dt), and reports:
the measured A_1 at each dt, the discrete band at each dt, the
continuum band, the discrete-continuum gap, the lock-in floor, and
the shift of A_1 under dt halving against the floor. Writes
p46_dt_check.json. No verdicts are registered here; this is a
reading in support of a correction entry.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p46_derive import evanescent  # noqa: E402


def bands(w, gamma, dt):
    vals = [abs(evanescent(om, c, gamma, dt)[1])
            for om in w["omega_range"] for c in w["c_range"]]
    return [min(vals), max(vals)]


def main():
    reg = json.load(open(os.path.join(HERE, "p46_results.json")))
    half = json.load(open(os.path.join(HERE, "p46_results_dt0.0005.json")))
    out = {"dt_registered": reg["dt"], "dt_half": half["dt"], "cells": {}}
    for key, cell in reg["cells"].items():
        g = cell["gamma"]
        rows = []
        for w, wh in zip(cell["windows"], half["cells"][key]["windows"]):
            om = w["omega_bar"]
            d1 = bands(w, g, reg["dt"])
            d2 = bands(wh, g, half["dt"])
            c1 = bands(w, g, None)
            a1, a2 = w["A"]["1"], wh["A"]["1"]
            floor = w["offset1"]["floor"] / d1[0]
            row = {"window": w["window"], "omega_bar": om,
                   "dt_omega_sq": (reg["dt"] * om) ** 2,
                   "A1": a1, "A1_half": a2,
                   "discrete_band": d1, "discrete_band_half": d2,
                   "continuum_band": c1,
                   "gap_discrete_minus_continuum_rel": d1[0] / c1[0] - 1.0,
                   "gap_over_dt_omega_sq": (d1[0] / c1[0] - 1.0) / (reg["dt"] * om) ** 2,
                   "floor_rel": floor,
                   "A1_rel_to_discrete": a1 / d1[0] - 1.0,
                   "A1_rel_to_continuum": a1 / c1[0] - 1.0,
                   "A1_half_rel_to_discrete_half": a2 / d2[0] - 1.0,
                   "A1_half_rel_to_continuum": a2 / c1[0] - 1.0,
                   "A1_shift_rel": a2 / a1 - 1.0,
                   "shift_within_floor": abs(a2 / a1 - 1.0) <= floor,
                   "gap_within_floor": abs(d1[0] / c1[0] - 1.0) <= floor}
            rows.append(row)
            print("gamma %-5g Omega %6.2f (dt Om)^2 %.2e gap %+.2e (= (dt Om)^2 x %.4f) "
                  "floor %.1e | A1 rel disc %+.2e cont %+.2e | dt/2: rel disc %+.2e cont %+.2e "
                  "shift %+.2e within floor %s"
                  % (g, om, row["dt_omega_sq"], row["gap_discrete_minus_continuum_rel"],
                     row["gap_over_dt_omega_sq"], floor, row["A1_rel_to_discrete"],
                     row["A1_rel_to_continuum"], row["A1_half_rel_to_discrete_half"],
                     row["A1_half_rel_to_continuum"], row["A1_shift_rel"],
                     row["shift_within_floor"]))
        out["cells"][key] = {"gamma": g, "windows": rows}
    out["all_gaps_within_floor"] = all(r["gap_within_floor"]
                                       for c in out["cells"].values() for r in c["windows"])
    out["all_shifts_within_floor"] = all(r["shift_within_floor"]
                                         for c in out["cells"].values() for r in c["windows"])
    with open(os.path.join(HERE, "p46_dt_check.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "cells"}))


if __name__ == "__main__":
    main()
