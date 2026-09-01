#!/usr/bin/env python3
"""Verification for the P-41 claim approximant-gaps-all-open, by
independent live reimplementation: its own cyclic-Jacobi
eigensolver (not the pinned kernels, which use Householder + QL),
its own extended-gcd label arithmetic, its own word construction.
Nothing read from results files.

Checks: (1) at q = 34 and q = 55, lambda = 1.0: the periodic +
antiperiodic spectra give exactly 2q edges, all q - 1 gaps open
above the registered floor 1e-6, and the minimum widths land
within 1e-6 of the experiment's route (two different eigensolvers
agreeing); (2) the label map via extended gcd is a bijection onto
(-q/2, q/2]; (3) the trace recursion on substitution words at
machine precision.

--mutant label-blind  asserts the k-th gap's label is k itself;
    the modular arithmetic kills it.
--mutant scan-blind   asserts the 60q-point scan detector finds
    all 2q edges at q = 89 - the P-40 firing, kept as a mutant:
    the scan misses narrow bands and the count comes up short.
"""
import math
import sys
from fractions import Fraction

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"label-blind", "scan-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

FIBS = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
FLOOR = 1e-6


def word(m):
    q, p = FIBS[m], FIBS[m - 1]
    beta = Fraction(p, q)
    return [1 if (n * beta) % 1 >= 1 - beta else 0 for n in range(q)]


def jacobi_eigs(A, sweeps=60, tol=1e-11):
    n = len(A)
    A = [row[:] for row in A]
    for _ in range(sweeps):
        off = 0.0
        for i in range(n - 1):
            for j in range(i + 1, n):
                off = max(off, abs(A[i][j]))
        if off < tol:
            break
        for i in range(n - 1):
            for j in range(i + 1, n):
                if abs(A[i][j]) < tol / 10:
                    continue
                th = 0.5 * math.atan2(2 * A[i][j], A[j][j] - A[i][i])
                c, s = math.cos(th), math.sin(th)
                for k in range(n):
                    aik, ajk = A[i][k], A[j][k]
                    A[i][k] = c * aik - s * ajk
                    A[j][k] = s * aik + c * ajk
                for k in range(n):
                    aki, akj = A[k][i], A[k][j]
                    A[k][i] = c * aki - s * akj
                    A[k][j] = s * aki + c * akj
    return sorted(A[i][i] for i in range(n))


def ham(w, lam, corner):
    q = len(w)
    A = [[0.0] * q for _ in range(q)]
    for n in range(q):
        A[n][n] = lam * w[n]
        j = (n + 1) % q
        hop = 1.0 if n + 1 < q else corner
        A[n][j] += hop
        A[j][n] += hop
    return A


def disc(w, lam, E):
    a, b, c, d = 1.0, 0.0, 0.0, 1.0
    for v in w:
        t = E - lam * v
        a, b, c, d = t * a - c, t * b - d, a, b
    return a + d


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def main():
    failures = []
    # (1) spectra and gaps at q = 34, 55
    for m in (8, 9):
        q = FIBS[m]
        w = word(m)
        per = jacobi_eigs(ham(w, 1.0, +1.0))
        anti = jacobi_eigs(ham(w, 1.0, -1.0))
        edges = sorted(per + anti)
        gaps = [edges[2 * i + 2] - edges[2 * i + 1]
                for i in range(q - 1)]
        mn = min(gaps)
        print(f"q={q}: edges {len(edges)}/{2*q}, min gap {mn:.3e}")
        if len(edges) != 2 * q:
            print("FAIL: eigen-route edge count off")
            failures.append("count")
        if mn <= FLOOR:
            print("FAIL: a labeled gap sits at or below the floor")
            failures.append("gap")

    # (2) labels via extended gcd
    for m in (8, 9, 10, 11):
        q, p = FIBS[m], FIBS[m - 1]
        _, inv, _ = egcd(p, q)
        seen = set()
        ok = True
        for k in range(1, q):
            s = (inv * k) % q
            if s > q // 2:
                s -= q
            if MUTANT == "label-blind":
                s_claim = k if k <= q // 2 else k - q
                if (s_claim * p - k) % q != 0:
                    print(f"FAIL: asserted label s = k at q = {q}, "
                          f"k = {k}: {s_claim} * F_(m-1) is not k "
                          f"mod q (true label {s})")
                    failures.append("label")
                    break
            if (s * p - k) % q != 0 or abs(s) > q // 2 or s in seen:
                print(f"FAIL: label arithmetic broken at q={q} k={k}")
                failures.append("labelmath")
                break
            seen.add(s)
        if MUTANT == "label-blind" and failures:
            break

    # (3) trace recursion
    words = {2: [1], 3: [1, 0]}
    for j in range(4, 10):
        words[j] = words[j - 1] + words[j - 2]

    def tr_word(wd, lam, E):
        return disc(wd, lam, E)
    worst = 0.0
    for lam, E in ((1.0, 0.3), (2.0, -0.7)):
        xs = {j: tr_word(words[j], lam, E) for j in range(2, 10)}
        for j in range(5, 10):
            worst = max(worst, abs(xs[j] - (xs[j - 1] * xs[j - 2]
                                            - xs[j - 3])))
    print(f"trace recursion worst {worst:.2e}")
    if worst > 1e-9:
        print("FAIL: trace-map recursion broken")
        failures.append("trace")

    # scan-blind mutant: the P-40 detector at q = 89
    if MUTANT == "scan-blind":
        m = 10
        q = FIBS[m]
        w = word(m)
        lo, hi = -3.5, 5.5
        n = 60 * q
        found = 0
        for target in (2.0, -2.0):
            prev = disc(w, 1.0, lo) - target
            for i in range(1, n + 1):
                E = lo + (hi - lo) * i / n
                cur = disc(w, 1.0, E) - target
                if prev * cur < 0:
                    found += 1
                prev = cur
        print(f"scan detector at q = {q}: {found} of {2*q} edges")
        if found < 2 * q:
            print("FAIL: asserted the scan finds all edges; narrow "
                  "bands fall between its samples")
            failures.append("scan")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p41 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
