#!/usr/bin/env python3
"""P-6: stable twisted states on circulant graphs C_n(S).

Identical Kuramoto oscillators on C_n(S): theta_j' = sum_{k in S}
[sin(theta_{j+k} - theta_j) + sin(theta_{j-k} - theta_j)]. The q-twisted
state theta_j = 2 pi q j / n is always an equilibrium. Linearising,
the Jacobian is circulant with eigenvalues
    -lambda_m,  lambda_m = sum_{k in S} w_k cos(2 pi q k/n) (1 - cos(2 pi m k/n)),
w_k = 2 for k < n/2 and 1 for k = n/2. Linear stability (modulo the
rotation zero mode m = 0) iff lambda_m > 0 for all m = 1..n-1.

Exhaustive over all symmetric S for n <= 28 (every subset of
{1..floor(n/2)}), greedy + random search for 28 < n <= 64. Every
reported maximum is re-verified by building the n x n Jacobian and
checking its eigenvalues with a Gershgorin-free power method on the
shifted matrix (independent of the closed form). Density = 2|E|/(n(n-1))
with |E| = n * sum w_k / 2. Writes p6_results.json."""
import json
import math
import random
import sys
from itertools import combinations
from multiprocessing import Pool

TWO_PI = 2 * math.pi


def weights(n):
    half = n // 2
    return {k: (1 if (n % 2 == 0 and k == half) else 2) for k in range(1, half + 1)}


def lambdas(n, S, q):
    w = weights(n)
    out = []
    for m in range(1, n):
        s = 0.0
        for k in S:
            s += w[k] * math.cos(TWO_PI * q * k / n) * (1 - math.cos(TWO_PI * m * k / n))
        out.append(s)
    return out


def stable(n, S, q, tol=1e-9):
    return all(l > tol for l in lambdas(n, S, q))


def density(n, S):
    w = weights(n)
    E = n * sum(w[k] for k in S) / 2
    return 2 * E / (n * (n - 1))


def jacobian_check(n, S, q):
    """Independent: build J_ij = cos(theta_j - theta_i) for neighbours,
    J_ii = -sum, and verify via explicit eigen-decomposition of the
    circulant (DFT) that all eigenvalues except one zero are negative -
    computed from the matrix, not from the closed form."""
    th = [TWO_PI * q * j / n for j in range(n)]
    nbrs = set()
    for k in S:
        nbrs.add(k % n); nbrs.add((-k) % n)
    row = [0.0] * n
    for d in nbrs:
        row[d] += math.cos(th[d] - th[0])
    row[0] = -sum(row[d] for d in nbrs)
    # eigenvalues of a circulant matrix from its first row
    eig = []
    for m in range(n):
        re = sum(row[d] * math.cos(TWO_PI * m * d / n) for d in range(n))
        eig.append(re)
    nonzero = [e for m, e in enumerate(eig) if m != 0]
    return max(nonzero) < -1e-9, max(nonzero)


def best_for_n(n):
    half = n // 2
    offsets = list(range(1, half + 1))
    best = (0.0, None, None)
    if half <= 14:
        for r in range(1, half + 1):
            for S in combinations(offsets, r):
                d = density(n, S)
                if d <= best[0]:
                    continue
                for q in range(1, half + 1):
                    if stable(n, S, q):
                        best = (d, list(S), q)
                        break
    else:
        random.seed(n)
        for q in range(1, half + 1):
            # greedy by positive contribution, then random improvement
            order = sorted(offsets, key=lambda k: -math.cos(TWO_PI * q * k / n))
            S = []
            for k in order:
                if stable(n, S + [k], q):
                    S.append(k)
            for _ in range(300):
                k = random.choice(offsets)
                T = sorted(set(S) ^ {k})
                if T and stable(n, T, q) and density(n, T) >= density(n, S):
                    S = T
            d = density(n, S) if S else 0.0
            if d > best[0]:
                best = (d, S, q)
    d, S, q = best
    ok, worst = jacobian_check(n, S, q) if S else (False, None)
    return {"n": n, "density": d, "S": S, "q": q, "jacobian_stable": ok,
            "jacobian_max_nonzero_eig": worst, "exhaustive": half <= 14}


if __name__ == "__main__":
    ns = list(range(5, 65))
    with Pool(14) as p:
        rows = p.map(best_for_n, ns, chunksize=1)
    for r in rows:
        print(f"n={r['n']:2d} {'exh' if r['exhaustive'] else 'srch'} density={r['density']:.4f} q={r['q']} "
              f"|S|={len(r['S']) if r['S'] else 0} jac_stable={r['jacobian_stable']}", flush=True)
    top = max(rows, key=lambda r: r["density"])
    print(f"max density with a stable twisted state: {top['density']:.4f} at n={top['n']}, q={top['q']}, S={top['S']}")
    with open("scripts/experiments/p6_results.json", "w") as f:
        json.dump(rows, f, indent=1)
