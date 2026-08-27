#!/usr/bin/env python3
"""Verification for the P-7 claim harper-golden-ladder, by independent
live reimplementation: its own Bloch matrices, its own Jacobi
eigensolver, its own Catalan series, run on the SHORT ladder
(1,2)..(13,21) - fast enough for CI - reading nothing from results
files.

Checks: (1) the q = 2 anchor lands on +-[0, 2 sqrt 2] with the
Dirac touch (the c25 interop); (2) the q = 3 edges land on the
factored exact values; (3) parity rule holds through q = 21;
(4) q S(q) at q = 13 and 21 sits within 0.55 of 32 G / pi computed
from this file's own series; (5) the two-step clock
ln(S(8)/S(21))/2 sits within 0.12 of ln phi.

--mutant bandwidth-constant  asserts S does not contract:
    S(21) > 0.8 S(5); the ladder contracts by ~4x, so FAIL.
--mutant silver-clock        asserts the clock is the silver mean,
    |ln(S(8)/S(21))/2 - ln(1+sqrt 2)| < 0.12; the measured clock is
    golden (0.48, not 0.88), so FAIL.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"bandwidth-constant", "silver-clock"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


def jacobi_eigs(A, tol=1e-11, max_sweeps=40):
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < tol:
            break
        skip = tol / (n * n)
        for p in range(n - 1):
            for q_ in range(p + 1, n):
                if abs(a[p][q_]) < skip:
                    continue
                t = 0.5 * math.atan2(2 * a[p][q_], a[q_][q_] - a[p][p]) \
                    if a[p][p] != a[q_][q_] else math.pi / 4
                c, s_ = math.cos(t), math.sin(t)
                for k in range(n):
                    x, y = a[p][k], a[q_][k]
                    a[p][k], a[q_][k] = c * x - s_ * y, s_ * x + c * y
                for k in range(n):
                    x, y = a[k][p], a[k][q_]
                    a[k][p], a[k][q_] = c * x - s_ * y, s_ * x + c * y
    return sorted(a[i][i] for i in range(n))


def bands(p, q):
    def H(corner, k2):
        if q == 2:
            d = [2 * math.cos(2 * math.pi * p * n / q + k2) for n in (1, 2)]
            o = 1 + corner
            return [[d[0], o], [o, d[1]]]
        M = [[0.0] * q for _ in range(q)]
        for n in range(q):
            M[n][n] = 2 * math.cos(2 * math.pi * p * (n + 1) / q + k2)
        for n in range(q - 1):
            M[n][n + 1] = M[n + 1][n] = 1.0
        M[0][q - 1] = M[q - 1][0] = corner
        return M
    edges = sorted(jacobi_eigs(H(+1.0, 0.0)) + jacobi_eigs(H(-1.0, math.pi / q)))
    bs = [(edges[2 * i], edges[2 * i + 1]) for i in range(len(edges) // 2)]
    S = sum(b - a for a, b in bs)
    gaps = [bs[i + 1][0] - bs[i][1] for i in range(len(bs) - 1)]
    return S, gaps


def main():
    # (1) q = 2 anchor
    S2, g2 = bands(1, 2)
    if abs(S2 - 4 * math.sqrt(2)) > 1e-9 or abs(g2[0]) > 1e-9:
        print(f"FAIL: q = 2 bandwidth {S2:.6f} or central gap {g2[0]:.1e} off the "
              "closed form 4 sqrt 2 with Dirac touch")
        return 1

    # (2) q = 3 exact edges via the bandwidth
    S3, g3 = bands(1, 3)
    S3_exact = 4 * math.sqrt(3) - 4
    if abs(S3 - S3_exact) > 1e-9 or min(g3) < 0.2:
        print(f"FAIL: q = 3 bandwidth {S3:.6f} off 4 sqrt 3 - 4 = {S3_exact:.6f}")
        return 1

    # ladder to q = 21
    ladder = [(2, 3), (3, 5), (5, 8), (8, 13), (13, 21)]
    S = {2: S2, 3: S3}
    for (p, q) in ladder[1:]:
        Sq, gaps = bands(p, q)
        S[q] = Sq
        if q % 2 == 1:
            if min(gaps) < 1e-8:
                print(f"FAIL: closed gap {min(gaps):.1e} at odd q = {q}")
                return 1
        else:
            mid = (q - 1) // 2
            if gaps[mid] > 1e-8 or min(g for i, g in enumerate(gaps) if i != mid) < 1e-8:
                print(f"FAIL: parity rule broken at even q = {q}")
                return 1

    if MUTANT == "bandwidth-constant":
        if S[21] < 0.8 * S[5]:
            print(f"FAIL: S(21) = {S[21]:.4f} contracted well below 0.8 S(5) = "
                  f"{0.8 * S[5]:.4f} - the bandwidth is not constant")
            return 1

    # (4) plateau against own Catalan
    s_, ps = 0.0, []
    for n in range(4000):
        s_ += (-1) ** n / (2 * n + 1) ** 2
        ps.append(s_)
    tail = ps[-61:]
    while len(tail) > 1:
        tail = [0.5 * (a + b) for a, b in zip(tail, tail[1:])]
    thouless = 32 * tail[0] / math.pi
    for q in (13, 21):
        if abs(q * S[q] - thouless) > 0.55:
            print(f"FAIL: q S at q = {q} is {q * S[q]:.4f}, beyond 0.55 of "
                  f"{thouless:.4f}")
            return 1

    # (5) the two-step clock
    slope = math.log(S[8] / S[21]) / 2
    lnphi = math.log((1 + math.sqrt(5)) / 2)
    if MUTANT == "silver-clock":
        if abs(slope - math.log(1 + math.sqrt(2))) > 0.12:
            print(f"FAIL: clock {slope:.4f} is nowhere near the silver mean "
                  f"{math.log(1 + math.sqrt(2)):.4f} - it is golden")
            return 1
    elif abs(slope - lnphi) > 0.12:
        print(f"FAIL: two-step clock {slope:.4f} off ln phi = {lnphi:.4f}")
        return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: live short ladder: anchors exact, parity holds to q = 21, "
          f"q S = {13 * S[13]:.3f}/{21 * S[21]:.3f} beside 32G/pi = {thouless:.4f}, "
          f"clock {slope:.4f} beside ln phi = {lnphi:.4f} - the address is "
          "golden, the plateau is Catalan's")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
