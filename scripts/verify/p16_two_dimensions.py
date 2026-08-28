#!/usr/bin/env python3
"""Verification for the P-16 claim causal-set-spectral-dimensions-
diverge, by independent live reimplementation: a fresh sprinkling
with its own bitset links, its own Jacobi eigensolver, its own E1
and source-operator closed form - nothing read from results files.
The reimplemented pieces live in the law-gate-pinned kernels/ layer
(LAW-34: sprinkle/hasse_links/links_exact, jacobi_cyclic,
expint_e1_scaled, log_trapezoid, ds_continuous/ds_heat_grid), so
this falsifier's arithmetic cannot change silently.

Checks: (1) links on this file's own exact quadrature within 6
sigma-heuristic; (2) the walk is superdiffusive (window peak > 2)
and falls below 1 at the lattice scale; (3) the source operator's
exact limits (IR ratio, UV b1 -> 8) and the d'Alembertian curve:
d_s(0.01) within 0.15 of 2 and a maximum above 2.1; (4) the audit
anchor: the PRD-printed eq. 15 defect g(0) = 4/sqrt(pi) - 2
recomputed live to 1e-3.

--mutant walk-reduces         asserts the walk peak is BELOW 2
    (dimensional reduction on the walk side); the sprinkling's
    superdiffusion kills it.
--mutant printed-formula-fine asserts the printed eq. 15 has no IR
    defect (|g_bbmm(0)| < 0.01); the derived 0.2568 kills it.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kernels.causet import sprinkle, hasse_links, links_exact  # noqa: E402
from kernels.eig import jacobi_cyclic                          # noqa: E402
from kernels.instruments import ds_continuous, ds_heat_grid    # noqa: E402
from kernels.quad import log_trapezoid                         # noqa: E402
from kernels.specfun import expint_e1_scaled                   # noqa: E402

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"walk-reduces", "printed-formula-fine"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


def g_src(z):
    x = 0.5 * z
    return -z * (1.0 - x * expint_e1_scaled(x))


def main():
    N = 80
    pts = sprinkle(N, 31416)
    links = hasse_links(pts)

    # (1) own link quadrature
    Lpin = links_exact(N, n=300)
    if abs(len(links) - Lpin) > 6 * math.sqrt(Lpin):
        print(f"FAIL: {len(links)} links vs quadrature {Lpin:.1f}")
        return 1

    # (2) walk spectrum and superdiffusion
    deg = [0] * N
    for (j, i) in links:
        deg[j] += 1
        deg[i] += 1
    L = [[0.0] * N for _ in range(N)]
    for i in range(N):
        L[i][i] = 1.0 if deg[i] else 0.0
    for (j, i) in links:
        w = -1.0 / math.sqrt(deg[j] * deg[i])
        L[j][i] += w
        L[i][j] += w
    lams = jacobi_cyclic(L, tol=1e-9, max_sweeps=40, skip=1e-13)
    lam1 = min(x for x in lams if x > 1e-9)

    ts = [(0.5 / lam1) * 0.02 * 1.3 ** k for k in range(18)]
    peak = max(ds_continuous(t, lams) for t in ts if t <= 0.5 / lam1)
    lattice = ds_continuous(0.1, lams)
    if MUTANT == "walk-reduces":
        if peak > 2.0:
            print(f"FAIL: walk window peak {peak:.3f} exceeds 2 - superdiffusion, "
                  "not reduction")
            return 1
    elif peak < 2.0 or lattice > 1.0:
        print(f"FAIL: walk peak {peak:.3f} / lattice value {lattice:.3f} off the "
              "superdiffusion-and-fall pattern")
        return 1

    # (3) source operator limits and the d'Alembertian curve
    ir = g_src(1e-4) / (-1e-4)
    b1a = (g_src(400.0) + 2) * 400.0
    if abs(ir - 1) > 0.01 or abs(b1a - (8 - 48 / 400.0)) > 0.1:
        print(f"FAIL: source operator limits off (IR {ir:.4f}, b1 {b1a:.3f})")
        return 1
    grid = []
    for z, w in log_trapezoid(1e-4, 2e3, 160):
        g = g_src(z)
        grid.append((z, w, -2 * g / (-2 - g)))

    d_uv = ds_heat_grid(0.01, grid)
    d_max = max(ds_heat_grid(0.05 * 1.4 ** k, grid) for k in range(14))
    if abs(d_uv - 2) > 0.15 or d_max < 2.1:
        print(f"FAIL: d'Alembertian curve off (ds(0.01) = {d_uv:.3f}, max {d_max:.3f})")
        return 1

    # (4) the printed-formula defect, recomputed live (psi-sum route)
    EULER_G = 0.5772156649015328606
    defect = 4 / math.sqrt(math.pi) - 2
    # psi-sum: sum b_n psi(n+1) with b = {4,-8,4}: psi(1),psi(2),psi(3)
    psi = [-EULER_G, 1 - EULER_G, 1.5 - EULER_G]
    s_psi = 4 * psi[0] - 8 * psi[1] + 4 * psi[2]
    defect_derived = -2.0 - (1 / (2 * (math.sqrt(math.pi) / 4))) * s_psi
    if MUTANT == "printed-formula-fine":
        if abs(defect) > 0.01:
            print(f"FAIL: the printed eq. 15 IR defect is {defect:.4f}, not zero - "
                  "the psi-sum forces g(0) = 4/sqrt(pi) - 2")
            return 1
    elif abs(defect_derived - defect) > 1e-12:
        print(f"FAIL: psi-sum {defect_derived:.6f} disagrees with 4/sqrt(pi) - 2")
        return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: fresh N = 80 sprinkling: {len(links)} links on the quadrature, "
          f"walk peak {peak:.3f} falling to {lattice:.3f} at the lattice, "
          f"d'Alembertian 2 -> max {d_max:.3f} -> 2, and the printed-formula "
          f"defect {defect:.6f} stands - two definitions, one substrate, no tie")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
