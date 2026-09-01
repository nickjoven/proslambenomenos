#!/usr/bin/env python3
"""P-41 registered run: the eight cells with the eigen-route
detector (PREDICTIONS.md P-41 fixed before this ran). Band edges
are the eigenvalues of the periodic and antiperiodic operators -
certified complete - with the P-40 discriminant retained as a
cross-check only.

Run: python3 scripts/experiments/p41_gaps.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from p40_derive import (FIBS, disc, eq2_trace_map, fib_word,  # noqa: E402
                        labels)
from kernels.eig import eigh  # noqa: E402

CELLS = [(m, lam) for m in (8, 9, 10, 11) for lam in (1.0, 2.0)]
FLOOR = 1e-6


def edge_matrix(word, lam, corner):
    q = len(word)
    A = [[0.0] * q for _ in range(q)]
    for n in range(q):
        A[n][n] = lam * word[n]
        A[n][(n + 1) % q] += 1.0 if n + 1 < q else corner
        A[(n + 1) % q][n] += 1.0 if n + 1 < q else corner
    return A


def cell(m, lam):
    q = FIBS[m]
    w = fib_word(m)
    per = eigh(edge_matrix(w, lam, +1.0))
    anti = eigh(edge_matrix(w, lam, -1.0))
    edges = sorted(list(per) + list(anti))
    bands = [(edges[2 * i], edges[2 * i + 1]) for i in range(q)]
    gaps = [(bands[i][1], bands[i + 1][0]) for i in range(q - 1)]
    # cross-checks against the discriminant
    xc = 0.0
    for e in per:
        xc = max(xc, abs(disc(w, lam, e) - 2.0))
    for e in anti:
        xc = max(xc, abs(disc(w, lam, e) + 2.0))
    mid_ok = True
    for lo, hi in bands:
        if hi < lo - 1e-12:
            mid_ok = False
        if abs(disc(w, lam, 0.5 * (lo + hi))) > 2 + 1e-9:
            mid_ok = False
    for lo, hi in gaps:
        if hi - lo > 1e-9 and abs(disc(w, lam, 0.5 * (lo + hi))) < 2 - 1e-9:
            mid_ok = False
    widths = sorted(hi - lo for lo, hi in gaps)
    return {"n_edges": len(edges), "disc_xcheck_worst": xc,
            "midpoints_ok": mid_ok, "min_gap": widths[0],
            "median_gap": widths[len(widths) // 2],
            "max_gap": widths[-1],
            "all_open_above_floor": widths[0] > FLOOR}


def main():
    out = {"cells": {}, "labels": {}, "trace": {}}
    ok_a = ok_b = True
    for m, lam in CELLS:
        q = FIBS[m]
        r = cell(m, lam)
        key = f"q{q}_lam{lam}"
        out["cells"][key] = r
        a_ok = (r["n_edges"] == 2 * q and r["midpoints_ok"]
                and r["disc_xcheck_worst"] < 1e-6)
        ok_a = ok_a and a_ok
        ok_b = ok_b and r["all_open_above_floor"]
        print(f"{key}: edges {r['n_edges']}/{2*q} xcheck "
              f"{r['disc_xcheck_worst']:.1e} min {r['min_gap']:.3e} "
              f"median {r['median_gap']:.3e} a:{a_ok} "
              f"b:{r['all_open_above_floor']}", flush=True)
    ok_c = True
    for m in (8, 9, 10, 11):
        q = FIBS[m]
        lab = labels(m)
        bij = (len(set(lab.values())) == q - 1
               and all(abs(s) <= q // 2 for s in lab.values()))
        ok_c = ok_c and bij
        out["labels"][str(q)] = {"bijection_in_range": bij}
    ok_d = True
    for lam, E in ((1.0, 0.3), (2.0, -0.7), (1.0, 1.9)):
        r = eq2_trace_map(lam, E)
        out["trace"][f"lam{lam}_E{E}"] = r
        ok_d = ok_d and (r["recursion_worst"] < 1e-9
                         and r["rotation_tie_worst"] < 1e-9)
    out["clauses"] = {"a": ok_a, "b": ok_b, "c": ok_c, "d": ok_d}
    with open(os.path.join(HERE, "p41_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])


if __name__ == "__main__":
    main()
