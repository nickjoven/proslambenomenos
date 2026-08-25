#!/usr/bin/env python3
"""Verification for the P-18 claim c2-profile-recovers-first-order-shifts,
by independent reimplementation: the C2 (quintic smoothstep) pair and
the linear control pair are rebuilt here at grid sizes the experiment
never used (n = 599 and 1199, Richardson in a^2), the first-order
shift predictions are re-derived live from V = c'^2/4 - c c''/2 by
this file's own quadrature, and nothing is read from the results
file.

Checks: (1) inline eigensolver validation to 1e-11; (2) the C2 pair's
Richardson Delta omega_k^2 tracks the live-derived shift_k with RMS
below 0.1 x Vbar_s over k = 5..30; (3) the derived sign flip at
k = 1: Delta omega_1^2 < -4e-8 and within 6e-8 of the live shift_1;
(4) the linear control pair fails the same first-order prediction
with RMS above 1.0 x Vbar_lin - the corners are the difference.

--mutant c1-corners-benign    asserts the linear pair ALSO passes the
    0.1 x Vbar bar (the C1 corners would have to be harmless) and
    must FAIL.
--mutant wrong-sign-potential predicts with V = c'^2/4 + c c''/2
    (sign error on the curvature term) and must FAIL both the RMS bar
    and the k = 1 residual.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"c1-corners-benign", "wrong-sign-potential"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

L, X0, X1, C_MIN = 1500.0, 150.0, 1350.0, 0.5
DX = X1 - X0
B_LIN = (C_MIN - 1.0) / DX
GRIDS = (599, 1199)
KMAX = 30
K_LO = 5


def c_smooth(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    u = (x - X0) / DX
    return 1.0 - 0.5 * (u * u * u * (10.0 + u * (-15.0 + 6.0 * u)))


def cp_smooth(x):
    if x <= X0 or x >= X1:
        return 0.0
    u = (x - X0) / DX
    return -0.5 * (30.0 * u * u * (1.0 - u) * (1.0 - u)) / DX


def cpp_smooth(x):
    if x <= X0 or x >= X1:
        return 0.0
    u = (x - X0) / DX
    return -0.5 * (60.0 * u * (1.0 - u) * (1.0 - 2.0 * u)) / (DX * DX)


def c_linear(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    return 1.0 + B_LIN * (x - X0)


def derive_shifts(c_of, cp_of, cpp_of, sign, kmax, msteps=6000):
    """Live quadrature: T, Vbar and shift_k from V = c'^2/4 sign c c''/2."""
    h = DX / msteps
    xs = [X0 + i * h for i in range(msteps + 1)]
    tau = [X0]
    for i in range(msteps):
        xm = xs[i] + 0.5 * h
        tau.append(tau[-1] + (h / 6.0) * (1.0 / c_of(xs[i]) + 4.0 / c_of(xm)
                                          + 1.0 / c_of(xs[i + 1])))
    T = tau[-1] + (L - X1) / C_MIN
    Vs = [0.25 * cp_of(x) ** 2 + sign * 0.5 * c_of(x) * cpp_of(x) for x in xs]
    invc = [1.0 / c_of(x) for x in xs]

    def integ(g):
        return (h / 3.0) * (g[0] + g[-1] + 4.0 * sum(g[1:-1:2]) + 2.0 * sum(g[2:-2:2]))

    vbar = integ([Vs[i] * invc[i] for i in range(msteps + 1)]) / T
    shifts = []
    for kk in range(1, kmax + 1):
        g = [Vs[i] * math.sin(kk * math.pi * tau[i] / T) ** 2 * invc[i]
             for i in range(msteps + 1)]
        shifts.append((2.0 / T) * integ(g))
    return T, vbar, shifts


def chain(c_of, kind, n):
    a = L / (n + 1)
    rho = (lambda xx: 1.0 / c_of(xx) ** 2) if kind == "ramp" else (lambda xx: 1.0 / c_of(xx))
    Tt = (lambda xx: 1.0) if kind == "ramp" else (lambda xx: c_of(xx))
    m = [a * rho(i * a) for i in range(1, n + 1)]
    J = [Tt((i + 0.5) * a) / a for i in range(0, n + 1)]
    return m, J


def sturm_count(diag, off, lam):
    cnt = 0
    q = diag[0] - lam
    if q < 0:
        cnt += 1
    for i in range(1, len(diag)):
        e2 = off[i - 1] * off[i - 1]
        q = diag[i] - lam - (e2 / q if q != 0 else e2 / 1e-300)
        if q < 0:
            cnt += 1
    return cnt


def lowest_eigs(diag, off, kmax):
    n = len(diag)
    hi = max(dd + (abs(off[i - 1]) if i else 0) + (abs(off[i]) if i < n - 1 else 0)
             for i, dd in enumerate(diag))
    out = []
    for kk in range(1, kmax + 1):
        a_, b_ = 0.0, hi
        for _ in range(80):
            mid = 0.5 * (a_ + b_)
            if sturm_count(diag, off, mid) >= kk:
                b_ = mid
            else:
                a_ = mid
        out.append(0.5 * (a_ + b_))
    return out


def spectrum(c_of, kind, n, kmax):
    m, J = chain(c_of, kind, n)
    diag = [(J[i] + J[i + 1]) / m[i] for i in range(n)]
    off = [-J[i + 1] / math.sqrt(m[i] * m[i + 1]) for i in range(n - 1)]
    return lowest_eigs(diag, off, kmax)


def richardson_delta(c_of, kmax):
    delta = {}
    for n in GRIDS:
        er = spectrum(c_of, "ramp", n, kmax)
        ez = spectrum(c_of, "zramp", n, kmax)
        delta[n] = [a_ - b_ for a_, b_ in zip(er, ez)]
    return [(4 * delta[GRIDS[1]][k] - delta[GRIDS[0]][k]) / 3.0 for k in range(kmax)]


def rms_resid(dext, shifts):
    resid = [dext[k - 1] - shifts[k - 1] for k in range(K_LO, KMAX + 1)]
    return math.sqrt(sum(r * r for r in resid) / len(resid))


def main():
    # 1. inline eigensolver validation on the uniform chain
    n0 = 150
    eig0 = lowest_eigs([2.0] * n0, [-1.0] * (n0 - 1), 10)
    worst = max(abs(e - 4 * math.sin(k * math.pi / (2 * (n0 + 1))) ** 2)
                / (4 * math.sin(k * math.pi / (2 * (n0 + 1))) ** 2)
                for k, e in enumerate(eig0, 1))
    if worst > 1e-11:
        print(f"FAIL: eigensolver validation {worst:.2e} > 1e-11 on the uniform chain")
        return 1

    sign = +1.0 if MUTANT == "wrong-sign-potential" else -1.0
    T_s, vbar_s, shifts_s = derive_shifts(c_smooth, cp_smooth, cpp_smooth, sign, KMAX)
    dext_s = richardson_delta(c_smooth, KMAX)
    rms_s = rms_resid(dext_s, shifts_s)

    # 2. C2 pair tracks the live first-order shifts
    if rms_s > 0.1 * vbar_s:
        print(f"FAIL: C2 RMS residual {rms_s / vbar_s:.3f} x Vbar_s > 0.1 over "
              f"k = {K_LO}..{KMAX} (live shifts, Richardson over n = {GRIDS})")
        return 1

    # 3. the sign flip at k = 1
    if not (dext_s[0] < -4e-8 and abs(dext_s[0] - shifts_s[0]) < 6e-8):
        print(f"FAIL: k = 1 sign flip not recovered (Delta_1 = {dext_s[0]:.3e}, "
              f"live shift_1 = {shifts_s[0]:.3e})")
        return 1

    # 4. the linear control fails the same prediction (flat V0 = b^2/4)
    T_l = X0 + math.log(1.0 + B_LIN * DX) / B_LIN + (L - X1) / C_MIN
    V0 = B_LIN * B_LIN / 4.0
    tau1, tau2 = X0, X0 + math.log(1.0 + B_LIN * DX) / B_LIN

    def prim(tt, kk):
        return 0.5 * tt - (T_l / (4 * math.pi * kk)) * math.sin(2 * math.pi * kk * tt / T_l)

    shifts_l = [(2.0 * V0 / T_l) * (prim(tau2, kk) - prim(tau1, kk))
                for kk in range(1, KMAX + 1)]
    vbar_l = V0 * (tau2 - tau1) / T_l
    dext_l = richardson_delta(c_linear, KMAX)
    rms_l = rms_resid(dext_l, shifts_l)
    if MUTANT == "c1-corners-benign":
        if rms_l > 0.1 * vbar_l:
            print(f"FAIL: linear pair RMS {rms_l / vbar_l:.3f} x Vbar_lin > 0.1 - "
                  "the C1 corners are not benign")
            return 1
    elif rms_l < 1.0 * vbar_l:
        print(f"FAIL: linear control RMS {rms_l / vbar_l:.3f} x Vbar_lin < 1.0 - "
              "R-10's failure did not reproduce at this scale")
        return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: live n = {GRIDS}: C2 pair RMS {rms_s / vbar_s:.3f} x Vbar_s "
          f"(bar 0.1), sign flip Delta_1 = {dext_s[0]:.3e} beside live "
          f"shift_1 = {shifts_s[0]:.3e}; linear control RMS "
          f"{rms_l / vbar_l:.3f} x Vbar_lin - corners were the failure, "
          "first-order theory was not")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
