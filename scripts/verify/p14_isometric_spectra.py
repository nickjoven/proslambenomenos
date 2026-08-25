#!/usr/bin/env python3
"""Verification for the P-14 claim isometric-not-isospectral-chain,
by independent reimplementation: both chains are rebuilt here at a
grid size the experiment never used (n = 749), the weighted-seminorm
distances and the lowest 40 Dirichlet eigenvalues are recomputed
live (Sturm bisection, validated inline against the uniform chain's
closed form), and nothing is read from the results file.

Checks: (1) inline eigensolver validation to 1e-11; (2) isometry -
the end-to-end seminorm distances of ramp and zramp agree within
5e-3 relative and sit within 5e-3 of the continuum travel time
T = 2113.553233; (3) spectral split - max_k |Delta omega_k^2| >
1e-9 over the lowest 40 modes; (4) subleading - both spectra obey
|omega_k T/(k pi) - 1| < 4e-3 for 5 <= k <= 30 at this coarser grid.

--mutant isospectral      asserts max_k |Delta omega_k^2| < 1e-12
    (the spectra would have to coincide) and must FAIL.
--mutant z-blind-seminorm asserts the seminorm distances differ by
    more than 1e-3 relative (the commutator would have to see the
    impedance) and must FAIL: the split is O(1/n) bookkeeping.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"isospectral", "z-blind-seminorm"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

L, X0, X1, C_MIN = 1500.0, 150.0, 1350.0, 0.5
B = (C_MIN - 1.0) / (X1 - X0)
T_TOT = X0 + math.log(1.0 + B * (X1 - X0)) / B + (L - X1) / C_MIN
N_GRID = 749


def c_of(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    return 1.0 + B * (x - X0)


def chain(profile, n):
    a = L / (n + 1)
    rho = (lambda xx: 1.0 / c_of(xx) ** 2) if profile == "ramp" else (lambda xx: 1.0 / c_of(xx))
    Tt = (lambda xx: 1.0) if profile == "ramp" else (lambda xx: c_of(xx))
    m = [a * rho(i * a) for i in range(1, n + 1)]
    J = [Tt((i + 0.5) * a) / a for i in range(0, n + 1)]
    return a, m, J


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


def spectrum(profile, n, kmax):
    _, m, J = chain(profile, n)
    diag = [(J[i] + J[i + 1]) / m[i] for i in range(n)]
    off = [-J[i + 1] / math.sqrt(m[i] * m[i + 1]) for i in range(n - 1)]
    return lowest_eigs(diag, off, kmax)


def seminorm_T(profile, n):
    a, m, J = chain(profile, n)
    tot = 0.0
    for i in range(n - 1):
        c_e = math.sqrt(J[i + 1] * a * a / (0.5 * (m[i] + m[i + 1])))
        tot += a / c_e
    return tot


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

    # 2. isometry of the seminorm distances
    tr, tz = seminorm_T("ramp", N_GRID), seminorm_T("zramp", N_GRID)
    split = abs(tr - tz) / T_TOT
    dev = max(abs(tr - T_TOT), abs(tz - T_TOT)) / T_TOT
    if MUTANT == "z-blind-seminorm":
        if split <= 1e-3:
            print(f"FAIL: seminorm split {split:.2e} <= 1e-3 - the commutator "
                  "distance does not see the impedance")
            return 1
    elif split > 5e-3 or dev > 5e-3:
        print(f"FAIL: seminorm distances not isometric (split {split:.2e}, dev {dev:.2e})")
        return 1

    # 3+4. spectra: split present, Weyl subleading
    er = spectrum("ramp", N_GRID, 40)
    ez = spectrum("zramp", N_GRID, 40)
    dmax = max(abs(a_ - b_) for a_, b_ in zip(er, ez))
    if MUTANT == "isospectral":
        if dmax >= 1e-12:
            print(f"FAIL: max |Delta omega^2| = {dmax:.3e} >= 1e-12 - the two "
                  "chains are not isospectral")
            return 1
    elif dmax <= 1e-9:
        print(f"FAIL: spectral split {dmax:.3e} <= 1e-9 not resolved")
        return 1
    for tag, ee in (("ramp", er), ("zramp", ez)):
        w = max(abs(math.sqrt(ee[k - 1]) * T_TOT / (k * math.pi) - 1.0)
                for k in range(5, 31))
        if w > 4e-3:
            print(f"FAIL: {tag} Weyl deviation {w:.2e} > 4e-3 over k = 5..30")
            return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: live n = {N_GRID}: seminorm distances isometric (split {split:.2e}, "
          f"both within {dev:.2e} of T = {T_TOT:.3f}); spectra split by "
          f"{dmax:.3e} in omega^2; Weyl holds on both - same metric, "
          "different sound")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
