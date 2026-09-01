#!/usr/bin/env python3
"""P-42 registered run: clause evaluation (PREDICTIONS.md P-42
fixed before this ran).

Run: python3 scripts/experiments/p42_identity.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p42_derive import (avn_rank, factorization_check,  # noqa: E402
                        ghz_model, ring_section, switch_marginals)


def main():
    g = ghz_model()
    sm, joints = switch_marginals()
    worst = 0.0
    for ctx in g:
        for os_ in itertools.product((0, 1), repeat=3):
            worst = max(worst, abs(g[ctx].get(os_, 0.0)
                                   - sm[ctx].get(os_, 0.0)))
    fac = factorization_check(joints)
    av = avn_rank()
    rs = ring_section()
    a = worst <= 1e-14
    b = (fac["factorizes"] and fac["worst_nonuniformity"] <= 1e-14
         and fac["detail"]["XXX"]["completions_each"] == 8
         and all(fac["detail"][c]["completions_each"] == 2
                 for c in ("XYY", "YXY", "YYX")))
    c = av["rank_A"] == 3 and av["rank_aug"] == 4
    d = (rs["strain_spread"] <= 1e-12
         and abs(rs["winding"] + 0.5) <= 1e-12)
    out = {"clauses": {"a": a, "b": b, "c": c, "d": d},
           "worst_model_diff": worst, "factorization": fac,
           "avn": av, "ring": rs}
    with open(os.path.join(HERE, "p42_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])


if __name__ == "__main__":
    main()
