#!/usr/bin/env python3
"""P-40 registered run: the eight registered cells (q in {34, 55,
89, 144} x lambda in {1.0, 2.0}) plus clause evaluation
(PREDICTIONS.md P-40 fixed before this ran).

Run: python3 scripts/experiments/p40_gaps.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p40_derive import (FIBS, bands_and_gaps, eq2_trace_map,  # noqa: E402
                        fib_word, labels)

CELLS = [(8, lam) for lam in (1.0, 2.0)] + \
        [(9, lam) for lam in (1.0, 2.0)] + \
        [(10, lam) for lam in (1.0, 2.0)] + \
        [(11, lam) for lam in (1.0, 2.0)]
FLOOR = 1e-6


def main():
    out = {"cells": {}, "labels": {}, "trace": {}}
    ok_a = ok_b = True
    for m, lam in CELLS:
        q = FIBS[m]
        w = fib_word(m)
        edges, bands, gaps = bands_and_gaps(w, lam, q)
        key = f"q{q}_lam{lam}"
        if gaps is None:
            out["cells"][key] = {"edges_found": len(edges),
                                 "expected": 2 * q, "ok": False}
            ok_a = False
            print(key, "INTEGRITY FAIL", len(edges), "edges",
                  flush=True)
            continue
        widths = sorted(hi - lo for lo, hi in gaps)
        open_ok = widths[0] > FLOOR
        ok_b = ok_b and open_ok
        out["cells"][key] = {
            "edges_found": len(edges), "n_gaps": len(gaps),
            "min_gap": widths[0], "median_gap":
            widths[len(widths) // 2], "max_gap": widths[-1],
            "all_open_above_floor": open_ok}
        print(f"{key}: {len(gaps)} gaps, min {widths[0]:.3e} "
              f"median {widths[len(widths)//2]:.3e} "
              f"max {widths[-1]:.3e} open {open_ok}", flush=True)
    ok_c = True
    for m, _ in CELLS[::2]:
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
    with open(os.path.join(HERE, "p40_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])


if __name__ == "__main__":
    main()
