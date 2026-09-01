#!/usr/bin/env python3
"""P-38 registered run: evaluate the five registered clauses
against the derive-layer instruments (PREDICTIONS.md P-38 fixed
before this ran). The independent reimplementation lives in
scripts/verify/p38_switch_bridge.py, not here.

Run: python3 scripts/experiments/p38_bridge.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p38_derive import eq1_eq4, eq2_eq3  # noqa: E402


def main():
    r14 = eq1_eq4()
    r23 = eq2_eq3()
    pats = r14["patterns"]
    a = all(p["worst_forbidden"] <= 1e-14
            and abs(p["total"] - 1.0) <= 1e-12 for p in pats)
    b = (pats[0]["n_allowed"] == 32
         and abs(pats[0]["min_allowed"] - 1 / 32) <= 1e-12
         and abs(pats[0]["max_allowed"] - 1 / 32) <= 1e-12
         and all(p["n_allowed"] == 8
                 and abs(p["min_allowed"] - 1 / 8) <= 1e-12
                 and abs(p["max_allowed"] - 1 / 8) <= 1e-12
                 for p in pats[1:]))
    c = (r23["max_conditions_satisfied"] == 3
         and r23["histogram"] == {1: 2048, 3: 2048})
    d = (r23["mermin_classical_max"] == 2
         and r23["mermin_algebraic_max"] == 4)
    fe = r14["nulls"]["definite_FE_violation_mass"]
    e = (r14["nulls"]["nosig_A_worst"] <= 1e-12
         and fe[0] == 0
         and all(abs(v - 0.5) <= 1e-12 for v in fe[1:]))
    out = {"clauses": {"a": a, "b": b, "c": c, "d": d, "e": e},
           "EQ1_EQ4": r14, "EQ2_EQ3": r23}
    with open(os.path.join(HERE, "p38_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])


if __name__ == "__main__":
    main()
