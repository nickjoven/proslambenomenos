#!/usr/bin/env python3
"""Verification for the P-18 ALF-lattice claim, by independent
miniature reimplementation - nothing here reads the experiment's
stored results; every number is recomputed live at HALF the
experiment's sample rate (44100 vs 88200) with a DIFFERENT observable
(the period of the bridge waveform by windowed autocorrelation with
parabolic interpolation, where the experiment clusters slip-onset
intervals), shorter runs, and per-beta force selected only by lock
quality over the broad period band [1.5, 2.5] T0 - a band that
contains exact doubling (2.0), so the selection cannot bias the test.

Checks (plain run, all must hold):
  T1 lattice slope: the m=1 locked period P(beta) over beta in
     {0.10, 0.13, 0.16} has least-squares slope dP/dbeta in
     [-1.35, -0.65] T0 (lattice term: -1; the additive slip-episode
     offset cancels in the slope).
  T2 not an integer subharmonic: every measured P differs from
     2.000 T0 by at least 0.04 T0.
  T3 offset sanity: residuals P - (1 + (1-beta_eff)) all lie in
     [0.00, 0.10] T0, using the delay-quantized effective beta.

--mutant exact-doubling     asserts each P within 0.03 T0 of 2.000
    (the "subharmonic = f0/2 exactly, beta-independent" reading of
    arXiv:2502.11902) and must FAIL.
--mutant beta-independent   asserts slope dP/dbeta in [-0.3, 0.3]
    and must FAIL.
Stdlib only.  Deterministic.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"exact-doubling", "beta-independent"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

FS = 44100.0
FS_REF = 88200.0            # the experiment's rate; one-pole filter
RATE = FS_REF / FS          # coefficients are per-sample, so holding
                            # the PHYSICAL time constants fixed at a
                            # different rate means a -> a**RATE
F0 = 196.9
LENGTH, DIAMETER, DENSITY = 0.325, 0.8e-3, 7700.0
MU_S, MU_D, V0 = 0.8, 0.25, 0.01
G_NUT, A_NUT = 0.999, 0.40 ** RATE
G_BR, A_BR = 0.998, 0.70 ** RATE
Z_TORS_RATIO, C_TORS = 2.0, 3200.0
G_T, A_T = 0.98, 0.60 ** RATE
A_CONTACT = 0.70 ** RATE
V_BOW = 0.05
DUR, WIN = 1.5, 0.35

BETAS = (0.10, 0.13, 0.16)
FORCE_LADDERS = {0.10: (1.3, 1.5, 1.7), 0.13: (1.0, 1.1, 1.25),
                 0.16: (0.85, 0.95, 1.05)}


def run_bridge(beta, force):
    """Integrate one string; return (bridge samples in the final WIN
    seconds, effective beta after delay quantization)."""
    rho_l = DENSITY * math.pi * (DIAMETER / 2) ** 2
    c = 2.0 * LENGTH * F0
    Z = rho_l * c
    gamma = (1.0 + 1.0 / Z_TORS_RATIO) / (2 * Z)
    half_z = 1.0 / (2 * Z)
    half_zt = 1.0 / (2 * Z_TORS_RATIO * Z)

    loop = FS / F0
    d_b = max(2, round(beta * loop))
    d_n = max(2, round((1 - beta) * loop))
    beta_eff = d_b / (d_b + d_n)
    loop_t = FS * 2.0 * LENGTH / C_TORS
    dt_b = max(2, round(beta * loop_t))
    dt_n = max(2, round((1 - beta) * loop_t))

    st = {"bb": [0.0] * d_b, "bn": [0.0] * d_n,
          "tb": [0.0] * dt_b, "tn": [0.0] * dt_n}
    pb = pn = ptb = ptn = 0
    lb = ln_ = ltb = ltn = fsm = 0.0
    slipping = False
    k = force * gamma
    thr = MU_S * k
    ramp = int(0.01 * FS)
    n_steps = int(DUR * FS)
    rec = n_steps - int(WIN * FS)
    bridge = []

    for n in range(n_steps):
        xb = st["bb"][pb]
        lb = (1 - A_BR) * xb + A_BR * lb
        vib = -G_BR * lb
        ln_ = (1 - A_NUT) * st["bn"][pn] + A_NUT * ln_
        vin = -G_NUT * ln_
        ltb = (1 - A_T) * st["tb"][ptb] + A_T * ltb
        ltn = (1 - A_T) * st["tn"][ptn] + A_T * ltn
        vh = vib + vin - G_T * ltb - G_T * ltn

        vb = V_BOW * min(1.0, (n + 1) / ramp)
        cd = vb - vh
        ca = abs(cd)
        stick = ca <= thr
        B = V0 - ca + k * MU_D
        C = V0 * (k * MU_S - ca)
        disc = B * B - 4 * C
        if (not stick) or (slipping and B < 0 and disc >= 0):
            x = 0.5 * (-B + math.sqrt(max(disc, 0.0)))
            vc = vb - (1.0 if cd >= 0 else -1.0) * max(x, 0.0)
            slipping = abs(vc - vb) > 1e-9
        else:
            vc = vb
            slipping = False
        F = (vc - vh) / gamma
        fsm = (1 - A_CONTACT) * F + A_CONTACT * fsm

        st["bb"][pb] = vin + fsm * half_z
        st["bn"][pn] = vib + fsm * half_z
        st["tb"][ptb] = -G_T * ltn + fsm * half_zt
        st["tn"][ptn] = -G_T * ltb + fsm * half_zt
        pb = (pb + 1) % d_b
        pn = (pn + 1) % d_n
        ptb = (ptb + 1) % dt_b
        ptn = (ptn + 1) % dt_n
        if n >= rec:
            bridge.append(xb)
    return bridge, beta_eff


def autocorr_period(sig):
    """Period (in T0) and quality of the dominant autocorrelation peak
    in the band [1.5, 2.5] T0, parabolic-interpolated."""
    T0 = FS / F0
    mean = sum(sig) / len(sig)
    x = [v - mean for v in sig]
    r0 = sum(v * v for v in x)
    lo, hi = int(1.5 * T0), int(2.5 * T0)
    n = len(x)
    best_lag, best_r = None, -1.0
    rs = {}
    for lag in range(lo, hi + 1):
        r = sum(x[i] * x[i + lag] for i in range(n - lag)) / r0
        rs[lag] = r
        if r > best_r:
            best_lag, best_r = lag, r
    if best_lag in (lo, hi):
        return best_lag / T0, best_r
    ra, rb, rc = rs[best_lag - 1], rs[best_lag], rs[best_lag + 1]
    denom = ra - 2 * rb + rc
    frac = 0.5 * (ra - rc) / denom if denom != 0 else 0.0
    return (best_lag + frac) / T0, best_r


def main():
    pts = []
    for beta in BETAS:
        best = None
        for force in FORCE_LADDERS[beta]:
            bridge, beta_eff = run_bridge(beta, force)
            period, quality = autocorr_period(bridge)
            if best is None or quality > best[3]:
                best = (beta_eff, force, period, quality)
        beta_eff, force, period, quality = best
        print(f"beta={beta:.2f} (eff {beta_eff:.4f}) F={force:.2f}: "
              f"P = {period:.4f} T0, quality {quality:.3f}")
        if quality < 0.80:
            print(f"FAIL: lock quality {quality:.3f} < 0.80")
            sys.exit(1)
        pts.append((beta_eff, period))

    xs = [b for b, _ in pts]
    ys = [p for _, p in pts]
    xbar, ybar = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((a - xbar) * (b - ybar) for a, b in zip(xs, ys)) / \
        sum((a - xbar) ** 2 for a in xs)
    resid = [p - (1 + (1 - b)) for b, p in pts]
    print(f"slope dP/dbeta = {slope:.3f} T0; "
          f"residuals vs lattice: {[round(r, 3) for r in resid]}")

    if MUTANT == "exact-doubling":
        bad = [p for _, p in pts if abs(p - 2.0) > 0.03]
        if bad:
            print(f"MUTANT FAIL: {len(bad)}/3 periods not within "
                  f"0.03 of 2.000: {[round(p, 4) for p in bad]}")
            sys.exit(1)
        print("mutant unexpectedly passed")
        sys.exit(0)
    if MUTANT == "beta-independent":
        if not (-0.3 <= slope <= 0.3):
            print(f"MUTANT FAIL: slope {slope:.3f} outside [-0.3, 0.3]")
            sys.exit(1)
        print("mutant unexpectedly passed")
        sys.exit(0)

    ok = True
    if not (-1.35 <= slope <= -0.65):
        print(f"FAIL T1: slope {slope:.3f} outside [-1.35, -0.65]")
        ok = False
    for (b, p) in pts:
        if abs(p - 2.0) < 0.04:
            print(f"FAIL T2: P = {p:.4f} within 0.04 of exact doubling")
            ok = False
    for r in resid:
        if not (0.0 <= r <= 0.10):
            print(f"FAIL T3: residual {r:.3f} outside [0.00, 0.10]")
            ok = False
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
