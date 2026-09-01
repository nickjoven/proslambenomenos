#!/usr/bin/env python3
"""P-43 registered run: clause evaluation (PREDICTIONS.md P-43
fixed before this ran).

Run: python3 scripts/experiments/p43_bodies.py
"""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p43_derive import (affine_dim, causal_points,  # noqa: E402
                        causal_shadow, chsh_quantum_reach,
                        chsh_shadow, local_points)


def main():
    lp = local_points()
    cp = causal_points()
    a = len(set(lp)) == 16 and affine_dim(lp) == 8
    dimc, vc = affine_dim(cp), len(cp)
    b = vc == 2368 and dimc == 24
    c = (dimc != 8) and (vc != 16)
    cs = causal_shadow(cp)
    xs = chsh_shadow()
    half = Fraction(1, 2)
    ce = sorted(p for p in cs
                if (p[0] - half) ** 2 + (p[1] - half) ** 2
                == Fraction(1, 4))
    xe = sorted(p for p in xs if p[0] ** 2 + p[1] ** 2 == 1)
    T = lambda p: ((p[0] + 1) / 2, (p[1] + 1) / 2)
    reach = chsh_quantum_reach()
    d = (len(ce) == 4 and len(xe) == 4
         and sorted(T(p) for p in xe) == ce
         and reach["worst_settings_error"] <= 1e-12)
    out = {"clauses": {"a": a, "b": b, "c": c, "d": d},
           "local": {"V": len(set(lp)), "dim": affine_dim(lp)},
           "causal": {"V": vc, "dim": dimc},
           "shadow": {"causal_extremes": [tuple(map(str, p))
                                          for p in ce],
                      "chsh_extremes": [tuple(map(str, p))
                                        for p in xe],
                      "reach": reach}}
    with open(os.path.join(HERE, "p43_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])


if __name__ == "__main__":
    main()
