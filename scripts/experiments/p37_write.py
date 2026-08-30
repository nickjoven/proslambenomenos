#!/usr/bin/env python3
"""P-37 registered cells: the (work, error) surface of writing one
bit on rung 2. Protocol, grids, seeds, bands all fixed in
PREDICTIONS.md P-37 and p37_registration.json BEFORE this ran.

Run: python3 scripts/experiments/p37_write.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p37_derive import (H, eq_density, floor_W,  # noqa: E402
                        quantiles_from_pdf, run_cell, w2_circle)

GRIDS = {0.22: [1, 2, 4, 8, 16, 32], 0.28: [1, 2, 4, 8, 12]}
WALL = [(0.22, 16), (0.22, 55), (0.28, 12), (0.28, 32)]
SEED0 = 20260830
M_MAIN, M_WALL = 1500, 6000


def w2_emp(D, finals, m=160):
    xs, pdf = eq_density(D, 0.0, 4000)
    qa = quantiles_from_pdf(xs, pdf, m)
    fin = sorted(finals)
    M = len(fin)
    qb = [fin[min(int((i + 0.5) / m * M), M - 1)] for i in range(m)]
    return w2_circle(qa, qb)


def main():
    out = {"cells": {}, "nulls": {}}
    idx = 0
    cells = []
    for D in (0.22, 0.28):
        for a in (1.2, 2.4):
            for tau in GRIDS[D]:
                cells.append((D, a, tau, M_MAIN, "main"))
    for D, tau in WALL:
        cells.append((D, 2.4, tau, M_WALL, "wall"))
    for D, a, tau, M, kind in cells:
        idx += 1
        r = run_cell(D, a, float(tau), M, 0.002, SEED0 + idx,
                     record_final=True)
        w2 = w2_emp(D, r["final"])
        fl = floor_W(D, r["p"])
        both = fl + w2 / tau
        key = "%s_a%s_t%s_%s" % (D, a, tau, kind)
        out["cells"][key] = {
            "W": r["W_mean"], "W_se": r["W_se"], "p": r["p"],
            "p_se": r["p_se"], "w2": w2, "floor": fl,
            "floor_plus_sl": both,
            "b_holds": r["W_mean"] >= fl - 3 * r["W_se"],
            "c_holds": r["W_mean"] >= both - 3 * r["W_se"]}
        print(key, "W %.4f(%.4f) p %.4f(%.4f) floor %.4f +sl %.4f b:%s c:%s"
              % (r["W_mean"], r["W_se"], r["p"], r["p_se"], fl, both,
                 out["cells"][key]["b_holds"],
                 out["cells"][key]["c_holds"]), flush=True)

    # clause (a): the two Jarzynski nulls and the dt/2 cell
    for D in (0.22, 0.28):
        idx += 1
        n = run_cell(D, 0.5, 6.0, 2000, 0.002, SEED0 + idx)
        out["nulls"][str(D)] = {
            "jarz": n["jarz"], "jarz_se": n["jarz_se"],
            "holds": abs(n["jarz"] - 1) <= 3 * n["jarz_se"],
            "W": n["W_mean"], "W_se": n["W_se"]}
        print("null D=%s jarz %.4f(%.4f) holds %s"
              % (D, n["jarz"], n["jarz_se"],
                 out["nulls"][str(D)]["holds"]), flush=True)
    idx += 1
    nh = run_cell(0.28, 0.5, 6.0, 2000, 0.001, SEED0 + idx)
    band = 3 * math.sqrt(2) * max(nh["W_se"],
                                  out["nulls"]["0.28"]["W_se"])
    out["nulls"]["dt_half"] = {
        "W": nh["W_mean"], "band": band,
        "holds": abs(nh["W_mean"] - out["nulls"]["0.28"]["W"]) <= band}
    print("dt/2 W %.4f vs %.4f band %.4f holds %s"
          % (nh["W_mean"], out["nulls"]["0.28"]["W"], band,
             out["nulls"]["dt_half"]["holds"]), flush=True)

    # clause (d): the wall pairs
    out["wall"] = {}
    for D, t_best, t_wall in ((0.22, 16, 55), (0.28, 12, 32)):
        cb = out["cells"]["%s_a2.4_t%s_wall" % (D, t_best)]
        cw = out["cells"]["%s_a2.4_t%s_wall" % (D, t_wall)]
        gap = cw["p"] - cb["p"]
        sig = math.sqrt(cw["p_se"] ** 2 + cb["p_se"] ** 2)
        out["wall"][str(D)] = {
            "p_best": cb["p"], "p_wall": cw["p"], "gap": gap,
            "sigma": sig, "holds": gap >= 3 * sig}
        print("wall D=%s best %.4f wall %.4f gap %.4f (3sig %.4f) %s"
              % (D, cb["p"], cw["p"], gap, 3 * sig,
                 out["wall"][str(D)]["holds"]), flush=True)

    ok_b = all(c["b_holds"] for c in out["cells"].values())
    ok_c = all(c["c_holds"] for c in out["cells"].values())
    ok_a = (out["nulls"]["0.22"]["holds"] and out["nulls"]["0.28"]["holds"]
            and out["nulls"]["dt_half"]["holds"])
    ok_d = all(w["holds"] for w in out["wall"].values())
    out["clauses"] = {"a": ok_a, "b": ok_b, "c": ok_c, "d": ok_d}
    # strip finals from the saved file (bulky); keep per-cell stats
    with open(os.path.join(HERE, "p37_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])


if __name__ == "__main__":
    main()
