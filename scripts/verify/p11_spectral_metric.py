#!/usr/bin/env python3
"""Verification for the P-11 claim connes-distance-representation-
dichotomy, by independent reimplementation (no access to
p11_results.json; the Gram matrix, witnesses, and bounds are rebuilt
here from scratch):

Construction A (algebra on vertices only) on cycles C_n, n >= 4:
  d(0,1) = 2/sqrt(3):  the witness (-1/sqrt(3), +1/sqrt(3), 0, ...)
      has Gram norm exactly 1 (its diag(f) L diag(f) decouples into a
      2x2 block of norm 1), and the same 2x2 principal-minor bound
      caps every feasible f at 2/sqrt(3).
  d(0,j) = sqrt(2) for j >= 2:  witness (-1/sqrt(2), 0, ...,
      +1/sqrt(2)_j, ...) has Gram norm 1; the diagonal Rayleigh bound
      2 g_i^2 <= 1 caps every pair at sqrt(2). The metric saturates.
Construction B (algebra also on edges by source pullback):
  on the cycle, the commutator norm is max|df| and d = hop exactly;
  on a dense circulant the norm aggregates over incoming edges in l2,
  the hop tent is infeasible, and no feasible f exceeds hop distance.

--mutant hop-metric        asserts construction A's far distance grows
    with hop (d(0, n/2) >= n/2 - 0.5) and must FAIL: it saturates.
--mutant tent-everywhere   asserts the hop tent stays norm-1 feasible
    on the dense circulant C_20({1..6}) and must FAIL: in-degree 6
    aggregation pushes its norm above 1.
"""
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"hop-metric", "tent-everywhere"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


def gram_norm(f, iters=250):
    """sqrt(lam_max(diag(f) L diag(f))) on the cycle, power iteration."""
    n = len(f)
    G = [[0.0] * n for _ in range(n)]
    for i in range(n):
        G[i][i] = 2.0 * f[i] * f[i]
        j = (i + 1) % n
        G[i][j] = -f[i] * f[j]
        G[j][i] = -f[j] * f[i]
    v = [1.0 / math.sqrt(n)] * n
    v[0] += 0.01
    lam = 0.0
    for _ in range(iters):
        w = [sum(G[i][j] * v[j] for j in range(n)) for i in range(n)]
        lam = math.sqrt(sum(x * x for x in w))
        if lam == 0:
            return 0.0
        v = [x / lam for x in w]
    return math.sqrt(lam)


def main():
    rng = random.Random(17)

    # A. neighbour witness and its exactness, n = 6, 11, 20
    for n in (6, 11, 20):
        w1 = [0.0] * n
        w1[0], w1[1] = -1 / math.sqrt(3), 1 / math.sqrt(3)
        nm = gram_norm(w1)
        if abs(nm - 1.0) > 1e-9:
            print(f"FAIL: neighbour witness norm {nm:.12f} != 1 on C_{n}")
            return 1
        j = n // 2
        wj = [0.0] * n
        wj[0], wj[j] = -1 / math.sqrt(2), 1 / math.sqrt(2)
        nmj = gram_norm(wj)
        if abs(nmj - 1.0) > 1e-9:
            print(f"FAIL: far witness norm {nmj:.12f} != 1 on C_{n}")
            return 1
        far = wj[j] - wj[0]
        target = (j - 0.5) if MUTANT == "hop-metric" else 1.40
        if far < target:
            print(f"FAIL: construction A d(0,{j}) witness {far:.4f} < "
                  f"{'hop-growth target' if MUTANT else 'registered floor'} {target}")
            return 1
        # bounds on random feasible (gauge by scan over shifts)
        for _ in range(15):
            g = [rng.gauss(0, 1) for _ in range(n)]
            shifts = [min(g) + i / 20 * (max(g) - min(g)) for i in range(21)]
            c = min(shifts, key=lambda cc: gram_norm([x - cc for x in g]))
            gg = [(x - c) for x in g]
            sc = max(gram_norm(gg), 1e-9)
            gg = [x / sc for x in gg]
            if max(abs(x) for x in gg) > 1 / math.sqrt(2) + 1e-6:
                print("FAIL: diagonal bound |g| <= 1/sqrt(2) violated by a feasible f")
                return 1
            if gg[1] - gg[0] > 2 / math.sqrt(3) + 1e-6:
                print("FAIL: minor bound d(0,1) <= 2/sqrt(3) violated by a feasible f")
                return 1

    # B. cycle: tent = hop exactly; dense circulant: tent infeasible,
    #    feasible f never exceed hop
    n, S = 20, list(range(1, 7))
    edges = [(u, (u + k) % n) for u in range(n) for k in S]
    nbrs = sorted({k % n for k in S} | {(-k) % n for k in S})
    dist = [None] * n
    dist[0] = 0
    frontier = [0]
    while frontier:
        nxt = []
        for u in frontier:
            for k in nbrs:
                v = (u + k) % n
                if dist[v] is None:
                    dist[v] = dist[u] + 1
                    nxt.append(v)
        frontier = nxt

    def b_norm(f, edges, n):
        acc = [0.0] * n
        for (u, v) in edges:
            d = f[v] - f[u]
            acc[v] += d * d
        return math.sqrt(max(acc))

    cyc_edges = [(u, (u + 1) % n) for u in range(n)]
    tent_cycle = [float(min(i, n - i)) for i in range(n)]
    if abs(b_norm(tent_cycle, cyc_edges, n) - 1.0) > 1e-9:
        print("FAIL: cycle tent norm != 1 under construction B")
        return 1
    tent = [float(h) for h in dist]
    tn = b_norm(tent, edges, n)
    if MUTANT == "tent-everywhere":
        if abs(tn - 1.0) > 1e-9:
            print(f"FAIL: dense-circulant tent norm {tn:.4f} != 1 "
                  "(in-degree aggregation; the tent is infeasible off the cycle)")
            return 1
    elif tn <= 1.0 + 1e-9:
        print(f"FAIL: dense-circulant tent norm {tn:.4f} unexpectedly <= 1")
        return 1
    worst = 0.0
    for _ in range(200):
        g = [rng.gauss(0, 1) for _ in range(n)]
        nb = b_norm(g, edges, n)
        if nb < 1e-9:
            continue
        g = [x / nb for x in g]
        for j in range(1, n):
            worst = max(worst, (g[j] - g[0]) - dist[j])
    if worst > 1e-9:
        print(f"FAIL: a feasible construction-B f exceeds hop distance by {worst:.2e}")
        return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print("PASS: construction A witnesses exact (d(0,1) = 2/sqrt(3), far = sqrt(2), "
          "norms 1 to 1e-9) with diagonal/minor caps holding on random feasible f; "
          "construction B: tent = hop on the cycle, infeasible on the dense "
          f"circulant (norm {tn:.3f}), and no feasible f exceeds hop")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
