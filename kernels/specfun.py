#!/usr/bin/env python3
"""Special-function kernels: the scaled exponential integral e^x E1(x)
(series + Lentz continued fraction), the K0 integral representation,
the Bessel ratio I1/I0 by continued fraction, and Euler-averaged
accelerated alternating series. Extracted, not rewritten.

Admission (two-artifact rule):
  expint_e1_scaled  scripts/experiments/p16_derive.py:91-118,
                    scripts/verify/p16_two_dimensions.py:37-57
  k0                scripts/experiments/p16_derive.py:67-75 (EQ1)
                    (cross-checked there against the series route;
                    the K0 kernel is the link between the sprinkled
                    causet operators and their closed forms)
  bessel_ratio      scripts/experiments/p23_derive.py:44-49,
                    scripts/verify/p22_locking_skeleton.py:75-79
                    (the halved-argument form with the loop stopping
                    at k = 2 is P-15's instrument,
                    scripts/experiments/p15_derive.py:71-78; both
                    forms are cross-checked in --selftest)
  alt_series_accel  scripts/experiments/p7_derive.py:178-190 (EQ4,
                    Catalan); the same repeated-averaging pattern
                    backs the imported-constant audits (LC-14)

Selftest anchors:
  - e^x E1(x): E1(1) = 0.2193839343955203 (A&S 5.1) through both the
    series (x <= 1) and the continued fraction (x > 1) branches
    joined at their crossover; UV check x f(x) -> 1.
  - K0(1) = 0.421024438240708333 (A&S 9.8; p16_derive.py EQ1).
  - I1/I0 continued fraction = von Mises quadrature at kappa = 5/3
    to 1e-12 (p23_derive.py EQ1); the P-15 halved form agrees to 1e-13.
  - accelerated series: Catalan G = 0.9159655941772190 with two depths
    agreeing to 1e-13 (p7_derive.py EQ4); eta(1) = ln 2; beta(2) = G.

stdlib only; floating-point operation order preserved from the
verify-script sources (the falsifiers that import these must keep
byte-identical PASS lines).
"""
import math

EULER_G = 0.5772156649015328606


def expint_e1_scaled(x):
    """f(x) = e^x E1(x), stable for all x > 0: the alternating series
    below x = 1, the Lentz continued fraction above
    (scripts/verify/p16_two_dimensions.py:37 e1_scaled;
    p16_derive.py:91 is the same arithmetic)."""
    if x <= 1.0:
        s = -EULER_G - math.log(x)
        term, k, val = x, 1, x
        while abs(term) > 1e-18 * (abs(val) + 1):
            k += 1
            term *= -x * (k - 1) / (k * k)
            val += term
        return math.exp(x) * (s + val)
    tiny = 1e-30
    f, C, D = tiny, tiny, 0.0
    for k in range(0, 200):
        a = 1.0 if k == 0 else -k * k
        b = x + 2 * k + 1
        D = 1.0 / (b + a * D if b + a * D != 0 else tiny)
        C = b + a / C if C != 0 else tiny
        delta = C * D
        f *= delta
        if abs(delta - 1) < 1e-15:
            break
    return f


def k0(x, n=3000, tmax=None):
    """K0(x) = int_0^inf e^{-x cosh t} dt, truncated adaptively
    (p16_derive.py:67, EQ1)."""
    if tmax is None:
        tmax = math.acosh(max(40.0 / x, 2.0)) + 2.0
    h = tmax / n
    s = 0.5 * (math.exp(-x) + math.exp(-x * math.cosh(tmax)))
    for i in range(1, n):
        s += math.exp(-x * math.cosh(i * h))
    return s * h


def bessel_ratio(x, depth=60):
    """I1(x)/I0(x) by the continued fraction built from the bottom up,
    stopping at k = 2 (scripts/verify/p22_locking_skeleton.py:75;
    p23_derive.py:44 is the same recursion with a zero guard)."""
    r = 0.0
    for k in range(depth, 1, -1):
        r = x / (2 * k + x * r)
    return x / (2 + x * r)


def bessel_ratio_p15(x, depth=80):
    """The P-15 instrument's halved-argument form of the same fraction:
    I1/I0 = (x/2)/(1 + (x^2/4)/(2 + (x^2/4)/(3 + ...))), tail built
    bottom-up, stopping at k = 2 (p15_derive.py:71)."""
    q = 0.0
    for k in range(depth, 1, -1):
        q = (x * x / 4) / (k + q)
    return (x / 2) / (1 + q)


def alt_series_accel(term, n_terms=4000, depth=80):
    """Sum of the alternating series sum_n term(n) by repeated
    averaging of the tail of partial sums (Euler acceleration),
    exactly the p7_derive.py:178 catalan() pattern generalized to any
    term function."""
    ps, s = [], 0.0
    for n in range(n_terms):
        s += term(n)
        ps.append(s)
    tail = ps[-(depth + 1):]
    while len(tail) > 1:
        tail = [0.5 * (a + b) for a, b in zip(tail, tail[1:])]
    return tail[0]


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True

    # anchor 1: E1(1) known digits through the series branch, and the
    # CF branch at x = 1 + 1e-12 lands beside it
    E1_1 = 0.2193839343955203
    a = expint_e1_scaled(1.0) - math.e * E1_1
    b = expint_e1_scaled(1.0 + 1e-12) - math.e * E1_1
    good = abs(a) < 1e-14 and abs(b) < 1e-11
    ok &= good
    print(f"e^x E1(x) at 1: series dev {abs(a):.1e}, CF dev {abs(b):.1e} "
          f"{'ok' if good else 'FAIL'}")
    uv = 400.0 * expint_e1_scaled(400.0)
    good = abs(uv - 1) < 5e-3
    ok &= good
    print(f"UV x f(x) at 400: {uv:.5f} vs 1 {'ok' if good else 'FAIL'}")

    # anchor 2: K0(1) reference and depth split (p16_derive.py EQ1)
    K0_1_REF = 0.421024438240708333
    d1 = abs(k0(1.0) - K0_1_REF)
    d2 = abs(k0(1.0, n=6000) - k0(1.0, n=3000))
    good = d1 < 1e-10 and d2 < 1e-12
    ok &= good
    print(f"K0(1): |dev| {d1:.1e}, depth split {d2:.1e} "
          f"{'ok' if good else 'FAIL'}")

    # anchor 3: I1/I0 CF vs von Mises quadrature at kappa = 5/3
    # (p23_derive.py EQ1) and vs the P-15 halved form
    kappa = 5.0 / 3.0
    n = 20000
    h = 2 * math.pi / n
    num = den = 0.0
    for i in range(n):
        t = -math.pi + (i + 0.5) * h
        w = math.exp(kappa * (math.cos(2 * t) - 1.0))
        num += math.cos(2 * t) * w
        den += w
    qd = num / den
    cf = bessel_ratio(kappa)
    d15 = abs(cf - bessel_ratio_p15(kappa))
    good = abs(cf - qd) < 1e-12 and d15 < 1e-13
    ok &= good
    print(f"I1/I0(5/3): CF {cf:.10f} vs quad {qd:.10f}, P-15 form dev "
          f"{d15:.1e} {'ok' if good else 'FAIL'}")

    # anchor 4: accelerated series - Catalan two depths, eta(1), beta(2)
    G1 = alt_series_accel(lambda n: (-1) ** n / (2 * n + 1) ** 2, depth=40)
    G2 = alt_series_accel(lambda n: (-1) ** n / (2 * n + 1) ** 2, depth=80)
    eta1 = alt_series_accel(lambda n: (-1) ** n / (n + 1))
    good = (abs(G1 - G2) < 1e-13 and abs(G2 - 0.9159655941772190) < 1e-12
            and abs(eta1 - math.log(2)) < 1e-13)
    ok &= good
    print(f"accelerated series: G = {G2:.15f} (depth split {abs(G1 - G2):.1e}), "
          f"eta(1) dev {abs(eta1 - math.log(2)):.1e} {'ok' if good else 'FAIL'}")

    print("specfun selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
