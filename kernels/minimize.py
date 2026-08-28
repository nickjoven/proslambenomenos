#!/usr/bin/env python3
"""Optimizer kernels: golden-section maximization, Nelder-Mead
(maximizing, classic coefficients), and the constrained uniform
relaxation used for the ring saddle. Extracted, not rewritten.

Admission (two-artifact rule):
  golden_max    scripts/experiments/p21_hardy.py:105-120,
                scripts/experiments/p11_derive.py:96-106 (the 0.382 /
                0.618 gauge search norm_A_gauged is the same section
                pattern)
  nelder_mead   scripts/experiments/p21_hardy.py:65-102 (the P-21
                agent's implementation); reused by that file's
                maximally-entangled-slice polish (two independent call
                sites in the landed registered computation)
  relax_rest    scripts/experiments/p24_derive.py:155-167 (EQ3's
                numeric check that the relaxed rest of the ring is
                uniform); the same constrained-relaxation move backs
                the p24 falsifier's saddle identity

Selftest anchors:
  - golden_max on the Hardy envelope p_env(k) = k^2 (1-k)^2 /
    ((1+k^2)(k^2-k+1)^2) lands on the pinned maximum
    (5 sqrt 5 - 11)/2 to 1e-12 (p21_derive.py EQ5 lineage; the pin is
    p21_registration.json's pinned_max 0.09016994374947...).
  - nelder_mead recovers the same envelope maximum from a flat start,
    and the minimum of a shifted quadratic to 1e-8.
  - relax_rest at the ring saddle: clamping Delta* = pi(N-3)/(N-2)
    and relaxing the rest lands on the closed-form energy
    E(Delta*) = K(1-cos Delta*) + K(N-1)(1-cos((2pi-Delta*)/(N-1)))
    with the free bonds uniform (p24_derive.py EQ3).

stdlib only; floating-point operation order preserved from the sources.
"""
import math
import random


def golden_max(f, lo, hi, tol=1e-12):
    """Golden-section maximization of a unimodal f on [lo, hi]
    (p21_hardy.py:105). Returns (x, f(x))."""
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    x1, x2 = b - g * (b - a), a + g * (b - a)
    f1, f2 = f(x1), f(x2)
    while b - a > tol:
        if f1 < f2:
            a, x1, f1 = x1, x2, f2
            x2 = a + g * (b - a)
            f2 = f(x2)
        else:
            b, x2, f2 = x2, x1, f1
            x1 = b - g * (b - a)
            f1 = f(x1)
    x = 0.5 * (a + b)
    return x, f(x)


def nelder_mead(f, x0, step, iters=500, ftol=1e-14, xtol=1e-11):
    """Maximize f from simplex seed x0 with the classic coefficients
    (1, 2, 0.5, 0.5) (p21_hardy.py:65). Returns (x_best, f_best)."""
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
        if fs[0] - fs[-1] < ftol and max(
                abs(simplex[j][i] - simplex[0][i])
                for j in range(1, n + 1) for i in range(n)) < xtol:
            break
        cent = [sum(simplex[j][i] for j in range(n)) / n for i in range(n)]
        xr = [cent[i] + (cent[i] - simplex[-1][i]) for i in range(n)]
        fr = f(xr)
        if fr > fs[0]:
            xe = [cent[i] + 2 * (cent[i] - simplex[-1][i]) for i in range(n)]
            fe = f(xe)
            simplex[-1], fs[-1] = (xe, fe) if fe > fr else (xr, fr)
        elif fr > fs[-2]:
            simplex[-1], fs[-1] = xr, fr
        else:
            xc = [cent[i] + 0.5 * (simplex[-1][i] - cent[i]) for i in range(n)]
            fc = f(xc)
            if fc > fs[-1]:
                simplex[-1], fs[-1] = xc, fc
            else:
                for j in range(1, n + 1):
                    simplex[j] = [0.5 * (simplex[j][i] + simplex[0][i])
                                  for i in range(n)]
                    fs[j] = f(simplex[j])
    best = max(range(n + 1), key=lambda i: fs[i])
    return simplex[best], fs[best]


def relax_rest(N, Delta, iters=40000, lr=0.02, kick=0.3, seed=7, K=1.0):
    """Ring of N bonds with bond 0 clamped at Delta; relax the free
    N-1 bonds under E = K sum(1 - cos b) subject to sum b = 2 pi
    (projected gradient descent from a kicked start). Returns
    (E_total, free bonds) (p24_derive.py:155)."""
    rng = random.Random(seed)
    free = N - 1
    b = [(2 * math.pi - Delta) / free + kick * (rng.random() - 0.5) for _ in range(free)]
    s = sum(b)
    b = [x + (2 * math.pi - Delta - s) / free for x in b]
    for _ in range(iters):
        g = [math.sin(x) for x in b]
        gm = sum(g) / free
        b = [x - lr * (gx - gm) for gx, x in zip(g, b)]
    return K * (1 - math.cos(Delta)) + K * sum(1 - math.cos(x) for x in b), b


# ---------------------------------------------------------------- selftest
def _p_env(k):
    """The Hardy envelope (p21_hardy.py:59, from p21_derive EQ5)."""
    return k * k * (1 - k) ** 2 / ((1 + k * k) * (k * k - k + 1) ** 2)


def _selftest():
    ok = True
    pin = (5 * math.sqrt(5) - 11) / 2   # the P-21 closed-form maximum

    # anchor 1: golden section on the Hardy envelope
    k_star, p_star = golden_max(_p_env, 1e-3, 0.999)
    good = abs(p_star - pin) < 1e-12
    ok &= good
    print(f"golden_max p_env: {p_star:.15f} vs (5 sqrt5 - 11)/2 = "
          f"{pin:.15f} {'ok' if good else 'FAIL'}")

    # anchor 2: Nelder-Mead on the same envelope and on a quadratic
    xs, p_nm = nelder_mead(lambda v: _p_env(v[0]), [0.3], step=0.1)
    g1 = abs(p_nm - pin) < 1e-10
    xq, fq = nelder_mead(lambda v: -((v[0] - 1.5) ** 2 + (v[1] + 2.0) ** 2),
                         [0.0, 0.0], step=0.5)
    g2 = abs(xq[0] - 1.5) < 1e-6 and abs(xq[1] + 2.0) < 1e-6
    ok &= g1 and g2
    print(f"nelder_mead: envelope dev {abs(p_nm - pin):.1e}, quadratic "
          f"argmax dev {max(abs(xq[0] - 1.5), abs(xq[1] + 2.0)):.1e} "
          f"{'ok' if g1 and g2 else 'FAIL'}")

    # anchor 3: the ring saddle - relaxed rest is uniform at Delta*
    # (p24_derive.py EQ3: Delta* = pi(N-3)/(N-2))
    K = 1.0
    for N in (8, 16):
        ds = math.pi * (N - 3) / (N - 2)
        Erelax, b = relax_rest(N, ds)
        Eclosed = K * (1 - math.cos(ds)) + K * (N - 1) * \
            (1 - math.cos((2 * math.pi - ds) / (N - 1)))
        spread = max(b) - min(b)
        good = abs(Erelax - Eclosed) < 1e-6 and spread < 1e-3
        ok &= good
        print(f"relax_rest N={N}: E {Erelax:.8f} vs closed {Eclosed:.8f}, "
              f"spread {spread:.1e} {'ok' if good else 'FAIL'}")

    print("minimize selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
