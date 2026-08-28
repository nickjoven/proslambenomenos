#!/usr/bin/env python3
"""Verification for the P-31 claim second-bridge-skeleton-
distinction, by independent live reimplementation: orbits by
HIGH-PRECISION DECIMAL arithmetic (60 digits, rounded-key set
closure - a different route than the experiment's exact Q(beta)
polynomials), rationals by its own Fraction BFS. Nothing read from
results files.

Checks: (1) the golden boundary orbit closes at size 4 and the
supergolden (s_2) orbit at size 6, by the decimal route; (2) the
tribonacci orbit closes at size 8; (3) the mediant 4/7 diverges
with denominator certificate > 1e6; (4) the Fibonacci convergent
13/21 diverges likewise.

--mutant mediant-lands  asserts the orbit at 4/7 closes; the
    denominator certificate kills it.
--mutant open-edge      treats g1's domain as OPEN at its left
    edge (x > 1 - t strictly), so g1(1 - t) = 0 never joins the
    golden orbit and its size reads 3, not 4; the golden anchor
    kills it - the closed-edge subtlety of the derivation,
    weaponized.
"""
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"mediant-lands", "open-edge"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

getcontext().prec = 60
EPS = Decimal(10) ** -40


def decimal_root(poly, lo, hi):
    """poly: high-to-low int coeffs; bisection in Decimal."""
    lo, hi = Decimal(lo), Decimal(hi)

    def f(x):
        acc = Decimal(0)
        for c in poly:
            acc = acc * x + c
        return acc
    flo = f(lo)
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def orbit_decimal(beta, cap=5000):
    """Multivalued BFS with rounded-key closure detection."""
    t = 1 / beta
    one = Decimal(1)

    def key(x):
        return str(x.quantize(Decimal(10) ** -45))

    strict_left = (MUTANT == "open-edge")
    seen = {}
    start = [1 - t, t]
    for x in start:
        seen[key(x)] = x
    frontier = start
    while frontier:
        if len(seen) > cap:
            return False, len(seen)
        nxt = []
        for x in frontier:
            kids = []
            if -EPS <= x <= t + EPS:
                kids.append(beta * x)
            left_ok = (x > 1 - t + EPS) if strict_left \
                else (x >= 1 - t - EPS)
            if left_ok and x <= one + EPS:
                kids.append(beta * x + 1 - beta)
            for k in kids:
                kk = key(k)
                if kk not in seen:
                    seen[kk] = k
                    nxt.append(k)
        frontier = nxt
    return True, len(seen)


def rational_diverges(t, den_cap=10 ** 6, cap=20000):
    beta = 1 / t
    seen = {1 - t, t}
    frontier = [1 - t, t]
    max_den = max(x.denominator for x in frontier)
    while frontier:
        if max_den > den_cap:
            return True, max_den
        if len(seen) > cap:
            return True, max_den
        nxt = []
        for x in frontier:
            kids = []
            if 0 <= x <= t:
                kids.append(beta * x)
            if 1 - t <= x <= 1:
                kids.append(beta * x + 1 - beta)
            for k in kids:
                if k not in seen:
                    seen.add(k)
                    nxt.append(k)
                    max_den = max(max_den, k.denominator)
        frontier = nxt
    return False, max_den


def main():
    failures = []

    phi = decimal_root([1, -1, -1], 1, 2)
    closed, size = orbit_decimal(phi)
    print(f"golden orbit (decimal route): closed={closed} size={size}")
    if not (closed and size == 4):
        print("FAIL: golden orbit is not size 4")
        failures.append("golden")

    # x^3 - 2x^2 + x - 1, high-to-low
    psi2 = decimal_root([1, -2, 1, -1], Decimal("1.5"), 2)
    closed, size = orbit_decimal(psi2)
    print(f"supergolden orbit: closed={closed} size={size}")
    if not (closed and size == 6):
        print("FAIL: supergolden orbit is not size 6")
        failures.append("supergolden")

    tri = decimal_root([1, -1, -1, -1], 1, 2)
    closed, size = orbit_decimal(tri)
    print(f"tribonacci orbit: closed={closed} size={size}")
    if not (closed and size == 8):
        print("FAIL: tribonacci orbit is not size 8")
        failures.append("tribonacci")

    for p, q, name in ((4, 7, "mediant 4/7"),
                       (13, 21, "convergent 13/21")):
        div, md = rational_diverges(Fraction(p, q))
        print(f"{name}: diverges={div} (max den {md})")
        want_diverge = not (MUTANT == "mediant-lands" and q == 7)
        if MUTANT == "mediant-lands" and q == 7:
            if div:
                print("FAIL: asserted closure at 4/7 but the "
                      "denominator certificate fired")
                failures.append("mediant")
        elif not div or md <= 10 ** 6:
            print(f"FAIL: {name} did not certify divergence")
            failures.append("rational")
        _ = want_diverge

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p31 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
