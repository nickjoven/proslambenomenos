#!/usr/bin/env python3
"""Verification for the P-22/P-23 claims two-photon-locking-z2-skeleton
and locking-protects-mod-pi-observable, by independent live
reimplementation: its own Euler-Maruyama integrator with fresh seeds,
its own Bessel continued fraction, its own mini mobility quadrature -
nothing read from any results file.

Checks: (1) deterministic beat at delta = 1.5, eps = 1 lands on
sqrt(1.25) within a band that includes the winding-quantization term
2 pi/T (the R-17 lesson, built in); (2) bistability - two starts a
pi apart in the two-photon equation both lock and stay pi apart;
(3) noisy mobility at one cell against this file's own quadrature;
(4) the protected observable at (eps, D) = (1, 0.3): live ensemble
mean of <cos 2 theta> beside its I1/I0(kappa) value with
|<cos theta>| small while hops occur.

--mutant single-phase-lock  asserts the two pi-separated starts
    converge to the SAME locked phase mod 2 pi and must FAIL.
--mutant tongue-squared     asserts the lock range scales as eps^2,
    i.e. that (delta, eps) = (0.3, 0.5) slips; it locks, so FAIL.
--mutant bessel-blind       asserts the mod-pi equilibrium is
    D-independent (equal at D = 0.3 and 0.15 within 0.02); the
    Bessel ratio moves by ~0.19, so FAIL.
"""
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"single-phase-lock", "tongue-squared", "bessel-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

DT = 0.002


def em(theta0, delta, eps, D, T, k, seed):
    rng = random.Random(seed)
    g = rng.gauss
    s = math.sin
    n = int(T / DT)
    amp = math.sqrt(2 * D * DT)
    th = theta0
    for _ in range(n):
        th += (delta - eps * s(k * th)) * DT + (amp * g(0.0, 1.0) if D > 0 else 0.0)
    return th


def em_avg(eps, D, T, seed):
    rng = random.Random(seed)
    g = rng.gauss
    s = math.sin
    c = math.cos
    n = int(T / DT)
    amp = math.sqrt(2 * D * DT)
    th = 0.0
    well = 0
    hops = 0
    c1 = c2 = 0.0
    for _ in range(n):
        th += (-eps * s(2 * th)) * DT + amp * g(0.0, 1.0)
        w = round(th / math.pi)
        if w != well and abs(th - math.pi * w) < math.pi / 4:
            hops += 1
            well = w
        c1 += c(th)
        c2 += c(2 * th)
    return c1 / n, c2 / n, hops


def bessel_ratio(x, depth=60):
    r = 0.0
    for k in range(depth, 1, -1):
        r = x / (2 * k + x * r)
    return x / (2 + x * r)


def mobility_quad(delta, eps, D, n=1600):
    h = 2 * math.pi / n
    Us = [(-delta * (i * h) - eps * math.cos(i * h)) / D for i in range(2 * n + 1)]
    terms = []
    for i in range(n + 1):
        w = Us[i:i + n + 1]
        m = max(w)
        s = 0.5 * (math.exp(w[0] - m) + math.exp(w[-1] - m))
        s += sum(math.exp(x - m) for x in w[1:-1])
        terms.append(-Us[i] + m + math.log(s * h))
    tmax = max(terms)
    tot = 0.5 * (math.exp(terms[0] - tmax) + math.exp(terms[-1] - tmax))
    tot += sum(math.exp(t - tmax) for t in terms[1:-1])
    return 2 * math.pi * D * (-math.expm1(-2 * math.pi * delta / D)) * \
        math.exp(-(tmax + math.log(tot * h)))


def main():
    # (1) deterministic beat with the quantization-aware band
    T = 1200.0
    v = (em(0.1, 1.5, 1.0, 0.0, T, 1, 1) - 0.1) / T
    tgt = math.sqrt(1.25)
    band = 1e-3 * tgt + 1.5 * 2 * math.pi / T
    if abs(v - tgt) > band:
        print(f"FAIL: beat {v:.5f} off sqrt(1.25) = {tgt:.5f} beyond {band:.5f}")
        return 1

    # (2) bistability of the two-photon lock
    a_end = em(0.2, 0.4, 1.0, 0.0, 60.0, 2, 2)
    b_end = em(0.2 + math.pi, 0.4, 1.0, 0.0, 60.0, 2, 2)
    sep = (b_end - a_end) % (2 * math.pi)
    if MUTANT == "single-phase-lock":
        if min(sep, 2 * math.pi - sep) > 0.1:
            print(f"FAIL: the two starts stay {sep:.4f} apart - two locked "
                  "phases per period, not one")
            return 1
    elif abs(sep - math.pi) > 0.05:
        print(f"FAIL: locked-phase separation {sep:.4f} is not pi")
        return 1

    # tongue scaling mutant: eps^2 tongue would predict slipping here
    th_end = em(0.1, 0.3, 0.5, 0.0, 400.0, 1, 3)
    slipped = abs(th_end - 0.1) > 2 * math.pi
    if MUTANT == "tongue-squared":
        if not slipped:
            print("FAIL: (delta, eps) = (0.3, 0.5) locks - the tongue is eps, "
                  "not eps^2")
            return 1
    elif slipped:
        print("FAIL: slipping inside the Adler tongue")
        return 1

    # (3) mobility, one cell, own quadrature vs own EM ensemble
    delta, eps, D, Tm, M = 0.9, 1.0, 0.3, 700.0, 4
    vs = [(em(0.0, delta, eps, D, Tm, 1, 100 + m)) / Tm for m in range(M)]
    v_meas = sum(vs) / M
    v_pin = mobility_quad(delta, eps, D)
    band = max(0.10 * v_pin, 4 * math.sqrt(2 * D / (Tm * M)))
    if abs(v_meas - v_pin) > band:
        print(f"FAIL: mobility {v_meas:.4f} vs quadrature {v_pin:.4f} "
              f"beyond {band:.4f}")
        return 1

    # (4) protection: live ensemble vs own Bessel ratio
    cells = [(0.3, 5.0 / 3.0)] + ([(0.15, 10.0 / 3.0)] if MUTANT == "bessel-blind" else [])
    means = {}
    for D2, kappa in cells:
        c1s, c2s, hop_tot = [], [], 0
        for m in range(2):
            c1, c2, hops = em_avg(1.0, D2, 2500.0, 500 + m + int(D2 * 100))
            c1s.append(c1)
            c2s.append(c2)
            hop_tot += hops
        means[D2] = sum(c2s) / 2
        if D2 == 0.3:
            pin = bessel_ratio(kappa)
            if abs(means[D2] - pin) > 0.05 or abs(sum(c1s) / 2) > 0.35 or hop_tot < 10:
                print(f"FAIL: protection cell <cos2> = {means[D2]:.4f} vs "
                      f"I1/I0 = {pin:.4f}, <cos1> = {sum(c1s)/2:+.4f}, "
                      f"hops {hop_tot}")
                return 1
    if MUTANT == "bessel-blind":
        if abs(means[0.3] - means[0.15]) > 0.02:
            print(f"FAIL: mod-pi equilibrium moves with D "
                  f"({means[0.3]:.4f} at D=0.3 vs {means[0.15]:.4f} at D=0.15) "
                  "- it is the Bessel ratio of eps/2D, not a constant")
            return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: live beat, pi-separated bistable lock, mobility beside its "
          f"own quadrature, and <cos 2 theta> = {means[0.3]:.4f} beside "
          f"I1/I0 = {bessel_ratio(5.0/3.0):.4f} with the bare phase near zero "
          "- the reference wave, computed")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
