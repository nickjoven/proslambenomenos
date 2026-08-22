#!/usr/bin/env python3
"""Verification for circulant-twisted-max-density-small: over ALL
symmetric connection sets S of the circulant graphs C_n(S), n <= 20,
the largest edge density admitting a linearly stable q-twisted state
(theta_j = 2 pi q j / n) is 12/19 = 0.6316, attained at n = 20 by
S = {1,...,6}, q = 1. Stability via the circulant eigenvalues
lambda_m = sum_{k in S} w_k cos(2 pi q k/n)(1 - cos(2 pi m k/n)) > 0,
m = 1..n-1, cross-checked by building the Jacobian's first row and
taking its DFT. Exhaustive: 2^(n//2) subsets per n, all q.
--mutant claims-two-thirds asserts the maximum is 2/3 within n <= 20
(it is first reached at n = 22) and must fail."""
import math
import sys
from itertools import combinations

TWO_PI = 2 * math.pi
MUTANT = sys.argv[sys.argv.index("--mutant") + 1] if "--mutant" in sys.argv and sys.argv.index("--mutant") + 1 < len(sys.argv) else ("--mutant" in sys.argv or None)
KNOWN_MUTANTS = {"claims-two-thirds"}
if MUTANT is not None and MUTANT not in KNOWN_MUTANTS:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN_MUTANTS)}")
    sys.exit(2)


def weights(n):
    half = n // 2
    return {k: (1 if (n % 2 == 0 and k == half) else 2) for k in range(1, half + 1)}


def stable(n, S, q):
    w = weights(n)
    for m in range(1, n):
        if sum(w[k] * math.cos(TWO_PI * q * k / n) * (1 - math.cos(TWO_PI * m * k / n)) for k in S) <= 1e-9:
            return False
    return True


def density(n, S):
    w = weights(n)
    return sum(w[k] for k in S) / (n - 1)


def jacobian_ok(n, S, q):
    th = [TWO_PI * q * j / n for j in range(n)]
    nb = set(); [nb.update({k % n, (-k) % n}) for k in S]
    row = [0.0] * n
    for d in nb:
        row[d] += math.cos(th[d] - th[0])
    row[0] = -sum(row[d] for d in nb)
    eig = [sum(row[d] * math.cos(TWO_PI * m * d / n) for d in range(n)) for m in range(n)]
    return max(e for m, e in enumerate(eig) if m) < -1e-9


def main() -> int:
    best = (0.0, None, None, None)
    for n in range(5, 21):
        half = n // 2
        for r in range(1, half + 1):
            for S in combinations(range(1, half + 1), r):
                d = density(n, S)
                if d <= best[0]:
                    continue
                for q in range(1, half + 1):
                    if stable(n, S, q):
                        best = (d, n, list(S), q)
                        break
    d, n, S, q = best
    claimed = 2 / 3 if MUTANT == "claims-two-thirds" else 12 / 19
    jac = jacobian_ok(n, S, q)
    print(f"max density n<=20: {d:.6f} at n={n}, S={S}, q={q}; Jacobian check {jac}")
    ok = abs(d - claimed) < 1e-9 and n == 20 and S == [1, 2, 3, 4, 5, 6] and q == 1 and jac
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
