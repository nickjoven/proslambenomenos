#!/usr/bin/env python3
"""P-11 derivation layer (pre-registration): the Connes spectral
distance d(p,q) = sup{ f(q)-f(p) : ||[D, f]||_op <= 1 } on cycle
graphs C_n, for two representations of the SAME algebra (functions
on vertices) with the SAME incidence Dirac D = [[0, B^T], [B, 0]]
on H = l2(V) + l2(E):

  A. vertex-only rep: f acts as diag(f) on l2(V), 0 on l2(E).
     Computed here: [D, f] = [[0, -f B^T], [B f, 0]], whose norm
     reduces to ||(S - I) diag f||, Gram matrix diag(f) L diag(f)
     with L the cycle Laplacian - the constraint feels the VALUES
     of f, so the seminorm is not shift-invariant and the distance
     uses the gauge inf over constants.
  B. source-pullback rep: f acts as diag(f) on l2(V) AND as
     diag(f(source(e))) on l2(E). The commutator's rows then carry
     only DIFFERENCES f(v) - f(u), the norm collapses to
     max_e |f(v)-f(u)|, and the spectral distance equals hop
     distance exactly (tent function feasible and extremal).

Every reduction is checked against the explicitly built full
commutator - nothing is trusted from memory. DERIVE 1-2 are
identity checks; DERIVE 3 tabulates primal lower bounds for
construction A at small n. Stdlib only.
"""
import math
import random
import sys


def full_commutator_A(f):
    """[D, f] for construction A, built from D and diag(f) explicitly."""
    n = len(f)
    M = [[0.0] * (2 * n) for _ in range(2 * n)]
    for e in range(n):
        u, v = e, (e + 1) % n
        # E<-V block rows: B diag(f): -f(u) at u, +f(v) at v
        M[n + e][u] = -f[u]
        M[n + e][v] = f[v]
        # V<-E block: -f B^T
        M[u][n + e] = f[u]      # -f(u) * B[e][u] = -f(u) * (-1)
        M[v][n + e] = -f[v]     # -f(v) * B[e][v] = -f(v) * (+1)
    return M


def full_commutator_B(f):
    """[D, f] for construction B: f also acts on edges by source value."""
    n = len(f)
    M = [[0.0] * (2 * n) for _ in range(2 * n)]
    for e in range(n):
        u, v = e, (e + 1) % n
        d = f[v] - f[u]
        # B diag(f_V) - diag(f_src) B : row e has 0 at u, (f(v)-f(u)) at v
        M[n + e][v] = d
        # top-right block: diag(f_V) B^T - B^T diag(f_src) (adjoint pattern)
        M[v][n + e] = -d
    return M


def opnorm_full(M, iters=400, seed=3):
    size = len(M)
    rng = random.Random(seed)
    v = [rng.gauss(0, 1) for _ in range(size)]
    lam = 0.0
    for _ in range(iters):
        w = [sum(M[i][j] * v[j] for j in range(size)) for i in range(size)]
        u = [sum(M[i][j] * w[i] for i in range(size)) for j in range(size)]
        lam = math.sqrt(sum(x * x for x in u))
        if lam == 0:
            return 0.0
        v = [x / lam for x in u]
    return lam ** 0.5


def norm_A(f, iters=120):
    """||[D,f]|| for construction A via the n x n Gram matrix
    G = diag(f) L diag(f), L the cycle Laplacian."""
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


def norm_A_gauged(f, golden=28):
    lo, hi = min(f) - 1.5, max(f) + 1.5
    for _ in range(golden):
        a = lo + 0.382 * (hi - lo)
        b = lo + 0.618 * (hi - lo)
        if norm_A([x - a for x in f]) < norm_A([x - b for x in f]):
            hi = b
        else:
            lo = a
    c = 0.5 * (lo + hi)
    return norm_A([x - c for x in f])


def main():
    rng = random.Random(42)

    # DERIVE 1: reductions match the explicitly built commutators
    ok1 = True
    worst = 0.0
    for n in (4, 5, 7):
        for _ in range(6):
            f = [rng.gauss(0, 1) for _ in range(n)]
            nf = opnorm_full(full_commutator_A(f))
            na = norm_A(f, iters=400)
            worst = max(worst, abs(nf - na) / max(nf, 1e-12))
            if abs(nf - na) > 1e-6 * max(1, nf):
                ok1 = False
            nb = opnorm_full(full_commutator_B(f))
            dmax = max(abs(f[(i + 1) % n] - f[i]) for i in range(n))
            worst = max(worst, abs(nb - dmax) / max(dmax, 1e-12))
            if abs(nb - dmax) > 1e-6 * max(1, dmax):
                ok1 = False
    print(f"DERIVE 1 {'PASS' if ok1 else 'FAIL'}: construction A norm = "
          f"sqrt(lam_max(diag(f) L diag(f))); construction B norm = max|df| "
          f"(worst rel dev {worst:.2e} vs the explicit 2n x 2n commutators)")

    # DERIVE 2: construction B recovers hop distance exactly -
    # tent function feasible (norm = 1) and extremal; telescoping
    # bounds any feasible f. Checked for n = 3..10, all j.
    ok2 = True
    for n in range(3, 11):
        for j in range(1, n // 2 + 1):
            tent = [float(min(i, n - i)) for i in range(n)]  # hop distance to 0
            nb = opnorm_full(full_commutator_B(tent))
            hop = float(min(j, n - j))
            if abs(nb - 1.0) > 1e-6 or abs(tent[j] - hop) > 1e-12:
                ok2 = False
    print(f"DERIVE 2 {'PASS' if ok2 else 'FAIL'}: construction B - the hop-"
          "distance tent has commutator norm 1 and attains f(j)-f(0) = "
          "d_hop; any feasible f telescopes to <= d_hop along the short "
          "arc, so d_spec = d_hop exactly")

    # DERIVE 3: construction A - gauged primal lower bounds
    print("DERIVE 3: construction A gauged d_spec(0,j) lower bounds vs hop")
    for n in (3, 4, 5, 6, 8, 10):
        row = []
        for j in range(1, n // 2 + 1):
            best = 0.0
            for _ in range(10):
                f = [rng.gauss(0, 1) for _ in range(n)]
                val = (f[j] - f[0]) / max(norm_A_gauged(f), 1e-9)
                step = 0.5
                for _ in range(80):
                    i = rng.randrange(n)
                    g = list(f)
                    g[i] += rng.gauss(0, step)
                    nv = (g[j] - g[0]) / max(norm_A_gauged(g), 1e-9)
                    if nv > val:
                        f, val = g, nv
                    else:
                        step *= 0.99
                best = max(best, val)
            row.append(f"j={j}: {best:.4f} (hop {min(j, n - j)})")
        print(f"  n={n}: " + "; ".join(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
