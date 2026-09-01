#!/usr/bin/env python3
"""P-39 registered run: evaluate the four registered clauses
(PREDICTIONS.md P-39 fixed before this ran). Independent
reimplementation lives in scripts/verify/p39_alpha_family.py.

Run: python3 scripts/experiments/p39_family.py
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p39_derive import ALPHAS, eq1, eq2_eq3, eq4  # noqa: E402


def main():
    r1 = eq1()
    r23 = eq2_eq3()
    r4 = eq4(r1, r23)
    a = (r1["all_equal"] and r1["extremes_present"]
         and r1["n_points"] == 9)
    b = all(v["spec_ok"] and v["trace_ok"] and v["loop_ok"]
            for v in r23["validity"].values())
    c = all(abs(d["gap"]) <= 1e-11 for d in r23["achieve"].values())
    adv = r4["advantage"]
    d = (max(r4["radius_residuals"]) <= 1e-12
         and r4["adv_zero_at_0"]
         and all(adv[str(al)] > 0 for al in ALPHAS
                 if al > 0)
         and r4["adv_max_at_1"]
         and r4["adv_at_1_vs_closed"] <= 1e-12)
    out = {"clauses": {"a": a, "b": b, "c": c, "d": d},
           "EQ1": r1, "EQ2_EQ3": r23, "EQ4": r4}
    with open(os.path.join(HERE, "p39_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])


if __name__ == "__main__":
    main()
