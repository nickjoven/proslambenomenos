#!/usr/bin/env python3
"""P-11 registered computation. Scores every clause of the P-11 entry
(PREDICTIONS.md) and writes p11_results.json. Stdlib only.

Clause (a): construction B on the three P-6 maximiser circulants -
  tent (hop-distance) function's commutator norm vs 1, and 200 random
  feasible f per graph vs hop distance. NOTE: the norm of the B-rep
  commutator on a general graph is max_v sqrt(sum over incoming edges
  of (df)^2) - computed here explicitly, not assumed; on the cycle
  the sum has one term (in-degree 1 under the i -> i+k orientation
  only when |S| = 1), which is where the registered "tent norm = 1"
  came from. The script measures what actually happens.
Clause (b): construction A on cycles - the closed-form witnesses
  w1 = (-1/sqrt(3), +1/sqrt(3), 0, ...)        -> d(0,1) >= 2/sqrt(3)
  wj = (-1/sqrt(2), 0, ..., +1/sqrt(2)_j, ...) -> d(0,j) >= sqrt(2)
  each checked to have Gram norm exactly 1; the diagonal Rayleigh
  bound |g_i| <= 1/sqrt(2) and the 2x2-minor bound f_1 - f_0 <=
  2/sqrt(3) checked on random feasible f.
"""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from p11_derive import norm_A, norm_A_gauged  # noqa: E402

OUT = {"clauses": {}, "detail": {}}


def circulant_edges(n, S):
    """Directed edge list (u, v) for the orientation u -> u+k, k in S."""
    edges = []
    for u in range(n):
        for k in sorted(S):
            edges.append((u, (u + k) % n))
    return edges


def hop_distances(n, S, src=0):
    nbrs = sorted({k % n for k in S} | {(-k) % n for k in S})
    dist = [None] * n
    dist[src] = 0
    frontier = [src]
    while frontier:
        nxt = []
        for u in frontier:
            for k in nbrs:
                v = (u + k) % n
                if dist[v] is None:
                    dist[v] = dist[u] + 1
                    nxt.append(v)
        frontier = nxt
    return dist


def b_norm(f, edges, n):
    """||[D, f]|| for construction B: max over vertices v of
    sqrt(sum over edges INTO v of (f(v) - f(u))^2). Derived in
    p11_derive.py for the cycle and by the same single-nonzero-row
    structure here (each directed edge row carries f(v) - f(u) at
    column v); cross-checked against an explicit dense commutator
    for one small graph below."""
    acc = [0.0] * n
    for (u, v) in edges:
        d = f[v] - f[u]
        acc[v] += d * d
    return math.sqrt(max(acc))


def b_norm_dense(f, edges, n):
    """Explicit dense commutator norm (power iteration) - the
    cross-check for b_norm's reduction."""
    m = len(edges)
    size = n + m
    M = [[0.0] * size for _ in range(size)]
    for e, (u, v) in enumerate(edges):
        d = f[v] - f[u]
        M[n + e][v] = d
        M[v][n + e] = -d
    rng = random.Random(5)
    vec = [rng.gauss(0, 1) for _ in range(size)]
    lam = 0.0
    for _ in range(300):
        w = [sum(M[i][j] * vec[j] for j in range(size)) for i in range(size)]
        u2 = [sum(M[i][j] * w[i] for i in range(size)) for j in range(size)]
        lam = math.sqrt(sum(x * x for x in u2))
        if lam == 0:
            return 0.0
        vec = [x / lam for x in u2]
    return lam ** 0.5


def main():
    rng = random.Random(99)

    # the three P-6 maximiser circulants (S for n = 44 read from the
    # committed p6 results, pinned by content not memory)
    p6 = json.loads((HERE / "p6_results.json").read_text())
    rows44 = [r for r in (p6 if isinstance(p6, list) else [])
              if isinstance(r, dict) and r.get("n") == 44]
    s44 = sorted(max(rows44, key=lambda r: r["density"])["S"]) if rows44 else None
    graphs = {"C20": (20, list(range(1, 7))), "C22": (22, list(range(1, 8)))}
    if s44:
        graphs["C44"] = (44, s44)
    OUT["detail"]["c44_S"] = s44

    # cross-check the b_norm reduction once, on C20
    n, S = graphs["C20"]
    edges = circulant_edges(n, S)
    f = [rng.gauss(0, 1) for _ in range(n)]
    dv = abs(b_norm(f, edges, n) - b_norm_dense(f, edges, n))
    OUT["detail"]["b_norm_crosscheck_dev"] = dv
    ok_cross = dv < 1e-6

    # clause (a)
    a_rows = {}
    tent_norm_ok = True
    no_exceed = True
    for tag, (n, S) in graphs.items():
        edges = circulant_edges(n, S)
        hop = hop_distances(n, S)
        tent = [float(h) for h in hop]
        tn = b_norm(tent, edges, n)
        tent_norm_ok = tent_norm_ok and abs(tn - 1.0) < 1e-9
        worst_excess = 0.0
        for _ in range(200):
            g = [rng.gauss(0, 1) for _ in range(n)]
            nb = b_norm(g, edges, n)
            if nb < 1e-9:
                continue
            g = [x / nb for x in g]
            for j in range(1, n):
                worst_excess = max(worst_excess, (g[j] - g[0]) - hop[j])
        no_exceed = no_exceed and worst_excess <= 1e-9
        # scaled-tent lower bound on d_spec, and in-degree structure
        indeg = len(S)
        a_rows[tag] = {"n": n, "S": S, "tent_norm": tn, "in_degree": indeg,
                       "scaled_tent_lower_bound_d(0,antipode)":
                           max(hop) / tn if tn > 0 else None,
                       "hop_antipode": max(hop),
                       "worst_feasible_excess_over_hop": worst_excess}
    OUT["detail"]["construction_B"] = a_rows
    OUT["clauses"]["a_tent_norm_1"] = bool(tent_norm_ok)
    OUT["clauses"]["a_no_feasible_exceeds_hop"] = bool(no_exceed and ok_cross)

    # clause (b): construction A on cycles
    b_ok = {"witness_neighbor": True, "witness_far": True,
            "diag_bound": True, "minor_bound": True}
    wn_vals, wf_vals = {}, {}
    for n in (8, 12, 16, 20):
        w1 = [0.0] * n
        w1[0], w1[1] = -1 / math.sqrt(3), 1 / math.sqrt(3)
        nm = norm_A(w1, iters=400)
        wn_vals[n] = {"norm": nm, "value": w1[1] - w1[0]}
        if abs(nm - 1.0) > 1e-9 or abs((w1[1] - w1[0]) - 2 / math.sqrt(3)) > 1e-12:
            b_ok["witness_neighbor"] = False
        j = n // 2
        wj = [0.0] * n
        wj[0], wj[j] = -1 / math.sqrt(2), 1 / math.sqrt(2)
        nmj = norm_A(wj, iters=400)
        wf_vals[n] = {"norm": nmj, "value": wj[j] - wj[0]}
        if abs(nmj - 1.0) > 1e-9 or (wj[j] - wj[0]) < 1.40:
            b_ok["witness_far"] = False
        # random feasible f: diagonal and minor bounds
        for _ in range(150):
            g = [rng.gauss(0, 1) for _ in range(n)]
            ng = norm_A_gauged(g)
            if ng < 1e-9:
                continue
            g = [x / ng for x in g]
            # re-gauge: golden was inside norm; use the shift that
            # attained it approximately - re-evaluate directly
            ng2 = norm_A_gauged(g)
            g = [x / max(ng2, 1e-9) for x in g]
            # find the gauge witness shift by scan
            best_c, best_v = 0.0, float("inf")
            for cc in [i / 50 * (max(g) - min(g)) + min(g) for i in range(51)]:
                v = norm_A([x - cc for x in g])
                if v < best_v:
                    best_c, best_v = cc, v
            gg = [x - best_c for x in g]
            sc = max(best_v, 1e-9)
            gg = [x / sc for x in gg]
            if max(abs(x) for x in gg) > 1 / math.sqrt(2) + 1e-6:
                b_ok["diag_bound"] = False
            if (gg[1] - gg[0]) > 2 / math.sqrt(3) + 1e-6:
                b_ok["minor_bound"] = False
    OUT["detail"]["witness_neighbor"] = wn_vals
    OUT["detail"]["witness_far"] = wf_vals
    for k, v in b_ok.items():
        OUT["clauses"][f"b_{k}"] = bool(v)

    (HERE / "p11_results.json").write_text(json.dumps(OUT, indent=1) + "\n")
    for k, v in OUT["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    for tag, row in a_rows.items():
        print(f"  {tag}: tent_norm {row['tent_norm']:.4f} (in-degree {row['in_degree']}), "
              f"hop antipode {row['hop_antipode']}, scaled-tent lower bound "
              f"{row['scaled_tent_lower_bound_d(0,antipode)']:.4f}, "
              f"worst feasible excess {row['worst_feasible_excess_over_hop']:.2e}")
    print(f"  witness d(0,1): value {2/math.sqrt(3):.6f}, norms "
          f"{[round(v['norm'], 9) for v in wn_vals.values()]}")
    print(f"  witness d(0,n/2): value {math.sqrt(2):.6f}, norms "
          f"{[round(v['norm'], 9) for v in wf_vals.values()]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
