#!/usr/bin/env python3
"""Refutation of twisted-sector-complex-structure and verification of
its replacement, half-shift-squares-by-x-parity.

Flat Klein bottle, base x-period 1, glide f(x+1, y) = -f(x, 1-y) on
the orientation (twisted) bundle and +f(x, 1-y) on the trivial one;
J = translation by 1/2 in x. For each mode e^{2 pi i m x} g(y), g in
{cos, sin}(2 pi n y), m in {0, 1/2, 1, 3/2, 2}, n = 1, the script
determines (i) which bundle the mode belongs to from the glide
condition and (ii) the sign of J^2 = translation by 1. It then checks:

  REFUTED claim: "J^2 = -I on the twisted sector and +I on the
  untwisted sector". Counterexamples: (m = 1, sin) is twisted with
  J^2 = +1; (m = 1/2, sin) is untwisted with J^2 = -1.

  REPLACEMENT: J^2 = (-1)^{2m} on every mode - the sign depends on
  the x-parity class alone, and each bundle contains both signs.
  Equivalently J^2 = (bundle sign) * R_y, R_y the y-reflection.

Exit 0 iff the counterexamples exist and the replacement holds on all
10 modes at random points, tolerance 1e-12."""

import cmath
import math
import random
import sys

random.seed(11)
MUTANT = sys.argv[sys.argv.index("--mutant") + 1] if "--mutant" in sys.argv and sys.argv.index("--mutant") + 1 < len(sys.argv) else ("--mutant" in sys.argv or None)
KNOWN_MUTANTS = {"bundle-decides"}
if MUTANT is not None and MUTANT not in KNOWN_MUTANTS:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN_MUTANTS)}")
    sys.exit(2)


def mode(m, n, br):
    g = (lambda y: math.cos(2 * math.pi * n * y)) if br == "cos" else \
        (lambda y: math.sin(2 * math.pi * n * y))
    return lambda x, y: cmath.exp(2j * math.pi * m * x) * g(y)


def bundle(f):
    for _ in range(30):
        x, y = random.random(), random.random()
        b = f(x, 1 - y)
        if abs(b) < 1e-6:
            continue
        r = f(x + 1, y) / b
        if abs(r - 1) < 1e-12:
            return "untwisted"
        if abs(r + 1) < 1e-12:
            return "twisted"
        return "neither"
    return "neither"


def j2(f):
    x, y = random.random(), random.random()
    r = f(x + 1, y) / f(x, y)
    return round(r.real) if abs(r.imag) < 1e-12 and abs(abs(r.real) - 1) < 1e-12 else None


def main() -> int:
    rows = []
    for m in (0, 0.5, 1, 1.5, 2):
        for br in ("cos", "sin"):
            f = mode(m, 1, br)
            rows.append((m, br, bundle(f), j2(f)))
            print(f"m={m:<4} {br}  {rows[-1][2]:<9}  J^2={rows[-1][3]:+d}")
    if MUTANT == "bundle-decides":
        # LAW-11 mutant: the refuted statement - J^2 = -1 iff twisted bundle
        replacement = all(s == (-1 if b == "twisted" else 1) for _, _, b, s in rows)
    else:
        replacement = all(s == (1 if float(m).is_integer() else -1) for m, _, _, s in rows)
    twisted_plus = any(b == "twisted" and s == +1 for _, _, b, s in rows)
    untwisted_minus = any(b == "untwisted" and s == -1 for _, _, b, s in rows)
    print(f"replacement J^2 = (-1)^(2m) on all modes: {replacement}")
    print(f"counterexample twisted with J^2=+1: {twisted_plus}; "
          f"untwisted with J^2=-1: {untwisted_minus}")
    ok = replacement and twisted_plus and untwisted_minus
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
