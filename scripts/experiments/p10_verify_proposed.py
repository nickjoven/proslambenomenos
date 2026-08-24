#!/usr/bin/env python3
"""Proposed verify script for P-10 (Myrheim-Meyer dimension from pure
order). Written by the p10 task; the integrator moves it into
scripts/verify/ if a claim is filed. Self-contained, stdlib only,
fixed seed, ~2 s.

Checks (see PREDICTIONS.md P-10 and scripts/experiments/p10_symbolic.py):
  1. d=2 related-pair fraction re-derived from scratch: in lightcone
     coordinates the interval is the unit square and the ordered-pair
     probability is int int (1-u)(1-v) du dv = 1/4 (exact rationals),
     so the related fraction is 1/2; cross-checked against the Gamma
     form Gamma(d+1)Gamma(d/2)/(2 Gamma(3d/2)) at d = 1..4
     (1, 1/2, 8/35, 1/10).
  2. A small fixed-seed sprinkle grid at d = 4 (N = 1024, M = 10):
     mean d_hat must land within 0.15 of 4 (the derived 4-sigma band
     is 0.049; 0.15 is deliberately loose so the pass leg is robust).
  3. Acceptance rate of the interval sampler matches the derived
     volume fraction pi/24 within 4 binomial sigma.

--mutant shuffled-order re-runs leg 2 with the time coordinate
randomly permuted across points (order destroyed, point set marginals
kept). Derived scrambled null: d* = 4.23 (p10_symbolic EQ 27), so the
mean d_hat moves ~0.23 above 4 and the 0.15 gate must FAIL (exit 1,
FAIL line, no traceback).
"""
import math
import random
import sys
from fractions import Fraction as Fr
from math import lgamma, sqrt

SEED = 20260824
MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else True
KNOWN = {"shuffled-order"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


def gamma_related(d):
    """Related-pair fraction, Gamma form (= 2x ordered form)."""
    return 0.5 * math.exp(lgamma(d + 1) + lgamma(d / 2) - lgamma(1.5 * d))


def invert(fv, lo=1.0, hi=24.0):
    if fv >= gamma_related(lo):
        return lo
    if fv <= gamma_related(hi):
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if gamma_related(mid) > fv:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> int:
    ok = True
    # --- leg 1: d=2 fraction from scratch, exact ---
    # int_0^1 (1-u) du = 1/2 for each lightcone coordinate; the
    # ordered-pair probability is the product, the related fraction 2x.
    half = Fr(1, 1) - Fr(1, 2)                 # int (1-u) du, exact
    p_ord = half * half
    f2 = 2 * p_ord
    if f2 != Fr(1, 2):
        print(f"FAIL d=2 derivation: related fraction {f2} != 1/2")
        ok = False
    targets = {1: Fr(1), 2: Fr(1, 2), 3: Fr(8, 35), 4: Fr(1, 10)}
    for d, tv in targets.items():
        if abs(gamma_related(d) - float(tv)) > 1e-12:
            print(f"FAIL Gamma form at d={d}: {gamma_related(d)} != {tv}")
            ok = False
    print(f"d=2 fraction re-derived: {f2}; Gamma form matches "
          f"{{1, 1/2, 8/35, 1/10}} at d=1..4: {ok}")

    # --- legs 2+3: fixed-seed sprinkle at d=4 ---
    d, N, M = 4, 1024, 10
    p_vol = math.pi / 24.0
    dhats = []
    acc_n = acc_tr = 0
    for run in range(M):
        rng = random.Random(f"{SEED}:verify:{run}")
        T, X, Y, Z = [], [], [], []
        while len(T) < N:
            acc_tr += 1
            t = rng.random()
            x = rng.random() - 0.5
            y = rng.random() - 0.5
            z = rng.random() - 0.5
            m = t if t < 0.5 else 1.0 - t
            if x * x + y * y + z * z < m * m:
                T.append(t)
                X.append(x)
                Y.append(y)
                Z.append(z)
        acc_n += N
        if MUTANT == "shuffled-order":
            mrng = random.Random(f"{SEED}:verify-mutant:{run}")
            mrng.shuffle(T)
        order = sorted(range(N), key=T.__getitem__)
        t_ = [T[i] for i in order]
        x_ = [X[i] for i in order]
        y_ = [Y[i] for i in order]
        z_ = [Z[i] for i in order]
        cnt = 0
        for i in range(N - 1):
            ti, xi, yi, zi = t_[i], x_[i], y_[i], z_[i]
            for j in range(i + 1, N):
                dt = t_[j] - ti
                dx = x_[j] - xi
                dy = y_[j] - yi
                dz = z_[j] - zi
                if dt * dt > dx * dx + dy * dy + dz * dz:
                    cnt += 1
        dhats.append(invert(cnt / (N * (N - 1) / 2.0)))
    mean = sum(dhats) / M
    rate = acc_n / acc_tr
    acc_tol = 4 * sqrt(p_vol * (1 - p_vol) / acc_tr)
    if abs(rate - p_vol) > acc_tol:
        print(f"FAIL acceptance rate {rate:.4f} vs pi/24 = {p_vol:.4f} "
              f"(tol {acc_tol:.4f})")
        ok = False
    err = abs(mean - d)
    print(f"d=4 sprinkle N={N} M={M}: mean d_hat = {mean:.4f} "
          f"(gate |mean-4| <= 0.15), acceptance {rate:.4f} vs {p_vol:.4f}")
    if err > 0.15:
        print(f"FAIL dimension recovery: |{mean:.4f} - 4| = {err:.4f} > 0.15")
        ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException as e:               # falsifier contract: no traceback
        print(f"FAIL unexpected error: {type(e).__name__}: {e}")
        sys.exit(1)
