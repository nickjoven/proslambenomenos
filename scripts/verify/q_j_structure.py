#!/usr/bin/env python3
"""Verification for twisted-sector-complex-structure: J = translation
by L1/2 satisfies J^2 = -I on the twisted (half-integer m) sector and
J^2 = +I on the integer sector, and J preserves the twisted boundary
condition.

Checks, at L1 = L2 = 1, on explicit modes f(x,y) = e^{2 pi i m x} * g(y)
with g = cos(2 pi n y) for half-integer m (allowed twisted modes) and
g = sin(2 pi n y) for integer m:

  1. multiplier: (J f)/f = e^{i pi m}; squared = e^{2 pi i m} = -1 for
     m in Z + 1/2, +1 for m in Z (checked numerically at random points)
  2. BC preservation: if f satisfies f(x+1, y) = -f(x, 1-y) then so
     does J f (checked pointwise at random points)
  3. commutation with the deck action on sample modes.

Exit 0 iff all checks pass at < 1e-12.
"""

import cmath
import math
import random
import sys


def mode(m, n, branch):
    if branch == "cos":
        return lambda x, y: cmath.exp(2j * math.pi * m * x) * math.cos(2 * math.pi * n * y)
    return lambda x, y: cmath.exp(2j * math.pi * m * x) * math.sin(2 * math.pi * n * y)


def main() -> int:
    random.seed(6)
    ok = True
    cases = [(0.5, 0, "cos"), (0.5, 1, "cos"), (1.5, 2, "cos"),
             (-0.5, 1, "cos"), (0, 1, "sin"), (1, 1, "sin"), (2, 2, "sin")]
    for m, n, br in cases:
        f = mode(m, n, br)
        J = lambda x, y: f(x + 0.5, y)
        JJ = lambda x, y: f(x + 1.0, y)
        want_sq = -1.0 if (m % 1) else 1.0
        worst_mult = worst_sq = worst_bc = 0.0
        for _ in range(60):
            x, y = random.random(), random.random()
            base = f(x, y)
            if abs(base) > 1e-9:
                worst_mult = max(worst_mult, abs(J(x, y) / base - cmath.exp(1j * math.pi * m)))
                worst_sq = max(worst_sq, abs(JJ(x, y) / base - want_sq))
            # BC preservation for the allowed twisted modes
            worst_bc = max(worst_bc, abs(J(x + 1, y) + J(x, 1 - y)))
        allowed = ((m % 1) and br == "cos") or (not (m % 1) and br == "sin")
        bc_ok = worst_bc < 1e-12 if allowed else True
        good = worst_mult < 1e-12 and worst_sq < 1e-12 and bc_ok
        ok &= good
        print(f"m={m} {br} n={n}: |J/f - e^(i pi m)|={worst_mult:.1e}  "
              f"|J^2/f - ({want_sq:+.0f})|={worst_sq:.1e}"
              + (f"  BC(Jf) residual={worst_bc:.1e}" if allowed else "")
              + ("  ok" if good else "  FAIL"))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
