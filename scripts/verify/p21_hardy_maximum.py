#!/usr/bin/env python3
"""Verification for the P-21 claim hardy-maximum-is-phi-fifth, by
independent live reimplementation - nothing read from the experiment's
registration or results files:

  1. the closed form re-derived here: the three Hardy zero-constraints
     eliminated into tangents (a, -k/a, -k^2/a, ka), checked against
     directly computed amplitudes at random points; the square
     identity D - (1+k^3)^2 = k^2 (a - k/a)^2 checked numerically;
     the envelope p_env(k) = k^2(1-k)^2/((1+k^2)(1-k+k^2)^2) checked
     against the amplitude-level probability at a = sqrt(k);
  2. the maximum re-derived in exact Q(sqrt 5) arithmetic (own
     implementation): y* = (3+sqrt5)/2 solves y^2 - 3y + 1 = 0 and
     (y*-2)/(y*(y*-1)^2) = (5 sqrt5 - 11)/2 = phi^5 as identities on
     pairs of rationals;
  3. a fresh smaller seeded search: 40 Nelder-Mead starts (own
     implementation, seed 20260827 - different from the experiment's
     20260826) over the full 5-parameter space with the penalty
     schedule, polished on the envelope; the found maximum must land
     within 1e-8 of (5 sqrt5 - 11)/2.

--mutant maximally-entangled-best  asserts the c = s slice reaches at
    least phi^5/2 and must FAIL: the constrained paradox probability
    at the maximally entangled state is zero.
--mutant flat-landscape  asserts the maximum is degenerate in the
    Schmidt angle - p_env at theta* +/- 0.1 within 1e-6 of the
    maximum - and must FAIL: the golden optimum is isolated
    (curvature moves p by ~1.2e-2 at 0.1 rad).
"""
import math
import random
import sys
from fractions import Fraction

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"maximally-entangled-best", "flat-landscape"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

PHI5 = (5 * math.sqrt(5) - 11) / 2


def amp(c, s, ta, tb, ap, bp):
    ua = (math.cos(ta), math.sin(ta)) if ap else (-math.sin(ta), math.cos(ta))
    ub = (math.cos(tb), math.sin(tb)) if bp else (-math.sin(tb), math.cos(tb))
    return c * ua[0] * ub[0] + s * ua[1] * ub[1]


def hardy(x):
    th, a0, a1, b0, b1 = x
    c, s = math.cos(th), math.sin(th)
    z1 = amp(c, s, a0, b0, True, True) ** 2
    z2 = amp(c, s, a1, b0, True, False) ** 2
    z3 = amp(c, s, a0, b1, False, True) ** 2
    return amp(c, s, a1, b1, True, True) ** 2, (z1, z2, z3)


def reduced_x(k, a):
    """The constraint-eliminating parametrization, re-derived here:
    tan a0 = a, tan b0 = -k/a, tan a1 = -k^2/a, tan b1 = k a, with
    theta = atan2(1, k) so that c/s = k."""
    return (math.atan2(1.0, k), math.atan(a), math.atan(-k * k / a),
            math.atan(-k / a), math.atan(k * a))


def p_env(k):
    return k * k * (1 - k) ** 2 / ((1 + k * k) * (k * k - k + 1) ** 2)


def me_slice_max():
    """Constrained paradox probability on the c = s state, maximized
    over the remaining measurement freedom (grid + refinement)."""
    best = 0.0
    for i in range(2001):
        a = 10 ** (-3 + 6 * i / 2000)
        p, _ = hardy(reduced_x(1.0, a))
        best = max(best, p)
    return best


def nelder_mead(f, x0, step, iters=400):
    n = len(x0)
    simplex = [list(x0)]
    for i in range(n):
        v = list(x0)
        v[i] += step
        simplex.append(v)
    fs = [f(v) for v in simplex]
    for _ in range(iters):
        order = sorted(range(n + 1), key=lambda i: -fs[i])
        simplex = [simplex[i] for i in order]
        fs = [fs[i] for i in order]
        if fs[0] - fs[-1] < 1e-14:
            break
        cent = [sum(simplex[j][i] for j in range(n)) / n for i in range(n)]
        xr = [2 * cent[i] - simplex[-1][i] for i in range(n)]
        fr = f(xr)
        if fr > fs[0]:
            xe = [3 * cent[i] - 2 * simplex[-1][i] for i in range(n)]
            fe = f(xe)
            simplex[-1], fs[-1] = (xe, fe) if fe > fr else (xr, fr)
        elif fr > fs[-2]:
            simplex[-1], fs[-1] = xr, fr
        else:
            xc = [0.5 * (cent[i] + simplex[-1][i]) for i in range(n)]
            fc = f(xc)
            if fc > fs[-1]:
                simplex[-1], fs[-1] = xc, fc
            else:
                for j in range(1, n + 1):
                    simplex[j] = [0.5 * (simplex[j][i] + simplex[0][i])
                                  for i in range(n)]
                    fs[j] = f(simplex[j])
    b = max(range(n + 1), key=lambda i: fs[i])
    return simplex[b], fs[b]


def main():
    # 1a. constraint elimination checked against direct amplitudes
    rng = random.Random(11)
    worst = 0.0
    for _ in range(400):
        k = rng.uniform(0.15, 0.9)
        a = rng.choice([-1, 1]) * rng.uniform(0.2, 2.5)
        p, zs = hardy(reduced_x(k, a))
        worst = max(worst, max(zs))
        pred = (k * k * (1 - k * k) ** 2
                / ((1 + k * k) * (1 + k ** 4 / a ** 2) * (1 + k * k * a * a)))
        worst = max(worst, abs(p - pred))
        gap = ((1 + k ** 4 / a ** 2) * (1 + k * k * a * a) - (1 + k ** 3) ** 2
               - k * k * (a - k / a) ** 2)
        worst = max(worst, abs(gap))
        pe = hardy(reduced_x(k, math.sqrt(k)))[0]
        worst = max(worst, abs(pe - p_env(k)))
    if worst > 1e-12:
        print(f"FAIL: constraint elimination / closed form off by {worst:.2e}")
        return 1

    # 2. the maximum in exact Q(sqrt5) arithmetic (a + b sqrt5 pairs)
    def mulq(x, y):
        return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def invq(x):
        n = x[0] * x[0] - 5 * x[1] * x[1]
        return (x[0] / n, -x[1] / n)

    h = Fraction(1, 2)
    ystar = (3 * h, h)
    root = (mulq(ystar, ystar)[0] - 3 * ystar[0] + 1,
            mulq(ystar, ystar)[1] - 3 * ystar[1])
    y1 = (ystar[0] - 1, ystar[1])
    y2 = (ystar[0] - 2, ystar[1])
    pstar = mulq(y2, invq(mulq(ystar, mulq(y1, y1))))
    phi = (-h, h)
    phi5 = mulq(phi, mulq(phi, mulq(phi, mulq(phi, phi))))
    if root != (0, 0) or pstar != phi5 or pstar != (-11 * h, 5 * h):
        print(f"FAIL: exact algebra: root {root}, p* {pstar}, phi^5 {phi5}")
        return 1

    # mutants (both must FAIL against the physics)
    if MUTANT == "maximally-entangled-best":
        best = me_slice_max()
        if best < PHI5 / 2:
            print(f"FAIL: the maximally entangled slice tops out at "
                  f"{best:.2e}, nowhere near phi^5/2 = {PHI5 / 2:.4f} - "
                  f"Hardy's paradox dies at c = s")
            return 1
        print("mutant claim held (it should not have)")
        return 0

    theta_star = math.atan2(1.0, 0.4643126)  # from the quartic root
    if MUTANT == "flat-landscape":
        pk = max(p_env(1 / math.tan(theta_star + 0.1)),
                 p_env(1 / math.tan(theta_star - 0.1)))
        pmax = p_env(1 / math.tan(theta_star))
        if abs(pmax - pk) > 1e-6:
            print(f"FAIL: the maximum is not degenerate in the Schmidt "
                  f"angle: p_env moves by {abs(pmax - pk):.2e} at "
                  f"theta* +/- 0.1 (bar 1e-6)")
            return 1
        print("mutant claim held (it should not have)")
        return 0

    # 3. fresh smaller seeded search, different seed
    rng = random.Random(20260827)
    best_p = -1.0
    for _ in range(40):
        x = [rng.uniform(0.02, math.pi / 2 - 0.02)] + \
            [rng.uniform(-math.pi / 2, math.pi / 2) for _ in range(4)]
        for lam in (1e3, 1e5, 1e7, 1e9):
            x, _ = nelder_mead(
                lambda v: hardy(v)[0]
                - lam * sum(z * z for z in hardy(v)[1]), x,
                step=0.25 if lam == 1e3 else 0.02)
        p, zs = hardy(x)
        pen = p - 1e9 * sum(z * z for z in zs)
        best_p = max(best_p, pen)
    # envelope polish (golden-section in k, own implementation)
    g = (math.sqrt(5) - 1) / 2
    lo, hi = 1e-3, 0.999
    while hi - lo > 1e-12:
        x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
        if p_env(x1) < p_env(x2):
            lo = x1
        else:
            hi = x2
    found = p_env(0.5 * (lo + hi))
    if best_p < PHI5 - 1e-4:
        print(f"FAIL: 40-start search stalled at penalized {best_p:.8f}, "
              f"more than 1e-4 below (5 sqrt5 - 11)/2")
        return 1
    if abs(found - PHI5) > 1e-8:
        print(f"FAIL: polished maximum {found:.15f} differs from "
              f"(5 sqrt5 - 11)/2 = {PHI5:.15f} by {abs(found - PHI5):.2e}")
        return 1
    # the slice must stay dead in the base run too
    if me_slice_max() > 1e-12:
        print(f"FAIL: maximally entangled slice above 1e-12")
        return 1
    print(f"p21 hardy maximum verified live: closed form re-derived, "
          f"Q(sqrt5) algebra reproduced, 40-start seed-20260827 search "
          f"polished to {found:.15f} (pinned {PHI5:.15f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
