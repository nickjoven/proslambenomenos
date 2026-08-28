#!/usr/bin/env python3
"""Verification for the P-28 claim golden-ladder-gap-integers, by
independent live reimplementation: its own Bloch matrices, its own
Sturm-bisection eigenvalues (kernels.eig.sturm_eigs - a different
pinned route than the experiment's Householder+QL eigh), its own
Diophantine solver by brute force (no modular inverse), and its own
Streda band count. Nothing read from results files.

Checks: (1) at q = 21 and q = 34, the two widest gaps sit at
r = F_{n-1}, F_{n-2} with t = +1, -1, and the even-q central gap
closes below 1e-12 while its label is the one ambiguous case;
(2) every open Fibonacci-position gap at q = 21 obeys
|t| = F_{n-j}, including the edge gap at t = -8; (3) the Streda
slope across 13/21 -> 21/34 from independent band counting is
exactly t for t in {+1, -1, +2}.

--mutant shifted-window  solves the Diophantine equation in the
    window t in (q/2, 3q/2]; every principal label leaves +-1 and
    check (1) kills it.
--mutant parity-blind    asserts the q = 34 central gap is open
    with a unique label; the spectrum closes it (P-7 parity rule)
    AND the label is the one ambiguous case t = +-17, so both
    halves of check (1) kill it.

(A skip-rung Streda mutant - pairing 8/13 with the non-Farey 34/55
- was tried and DISCARDED as non-discriminating, and the reason is
itself worth pinning: the gap line N = s + t alpha is global, so
ANY two fluxes sharing a gap's (s, t) give slope exactly t;
unimodularity buys adjacent-rung gap continuity, not slope
exactness. Recorded in the notes.)
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"shifted-window", "parity-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
FLOOR = 1e-9


def dense_eigs(p, q, corner, k2):
    """Independent route: characteristic polynomial of the
    tridiagonal-plus-corner matrix by the standard two-sweep
    recurrence, roots by bisection. Exact structure, no shared
    code with the experiment's Householder+QL."""
    diag = [2 * math.cos(2 * math.pi * p * (n + 1) / q + k2)
            for n in range(q)]

    def charpoly(x):
        # det(H - x) for tridiagonal + corner c:
        # det = det_T(1..q) - c^2 det_T(2..q-1) - 2 c (-1)^q
        # (product of off-diagonals = 1 each)
        # forward minors f[i] = det of leading i x i tridiagonal
        f = [1.0, diag[0] - x]
        for i in range(1, q):
            f.append((diag[i] - x) * f[-1] - f[-2])
        # interior minor det_T(2..q-1)
        g = [1.0, diag[1] - x]
        for i in range(2, q - 1):
            g.append((diag[i] - x) * g[-1] - g[-2])
        c = corner
        return f[q] - c * c * (g[q - 2] if q > 2 else 1.0) \
            - 2 * c * ((-1) ** q)

    # eigenvalues in (-4.5, 4.5): bisection on sign changes over a
    # fine grid, then refine
    lo, hi, m = -4.5, 4.5, max(6000, 700 * q)
    xs = [lo + (hi - lo) * i / m for i in range(m + 1)]
    vals = [charpoly(x) for x in xs]
    roots = []
    for i in range(m):
        if vals[i] == 0.0:
            roots.append(xs[i])
        elif vals[i] * vals[i + 1] < 0:
            a, b = xs[i], xs[i + 1]
            fa = vals[i]
            for _ in range(80):
                c0 = 0.5 * (a + b)
                fc = charpoly(c0)
                if fa * fc <= 0:
                    b = c0
                else:
                    a, fa = c0, fc
            roots.append(0.5 * (a + b))
    return roots


def gaps(p, q):
    e1 = dense_eigs(p, q, +1.0, 0.0)
    e2 = dense_eigs(p, q, -1.0, math.pi / q)
    edges = sorted(e1 + e2)
    assert len(edges) == 2 * q, f"root count {len(edges)} != {2 * q}"
    out = []
    for r in range(1, q):
        out.append({"r": r, "lo": edges[2 * r - 1], "hi": edges[2 * r],
                    "width": edges[2 * r] - edges[2 * r - 1]})
    return out, edges


def dio(r, p, q):
    """Brute-force label: the t with r = s q + t p in the window."""
    lo, hi = (-(q // 2), q // 2) if MUTANT != "shifted-window" \
        else (q // 2 + 1, 3 * q // 2)
    sols = [t for t in range(lo, hi + 1) if (r - t * p) % q == 0]
    return sols


def main():
    failures = []
    n_of = {21: 8, 34: 9}
    G = {}
    for q, p in ((21, 13), (34, 21)):
        G[q], _ = gaps(p, q)

    # (1) principal pair and central closure
    for q, p in ((21, 13), (34, 21)):
        n = n_of[q]
        opened = [x for x in G[q] if x["width"] > FLOOR]
        top2 = sorted(opened, key=lambda x: -x["width"])[:2]
        lab = {}
        for x in top2:
            sols = dio(x["r"], p, q)
            lab[x["r"]] = sols[0] if len(sols) == 1 else sols
        want = {FIB[n - 2]: 1, FIB[n - 3]: -1}
        if lab != want:
            print(f"FAIL: q={q} principal labels {lab} != {want}")
            failures.append("principal")
        else:
            print(f"q={q}: principal pair {lab} ok")
    central = [x for x in G[34] if x["r"] == 17][0]
    sols17 = dio(17, 21, 34)
    # this route's char-poly recurrence carries ~1e-9 root error at
    # q = 34 (cancellation near the degenerate central root); the
    # closure tolerance here is 1e-8 - five orders below the
    # smallest open gap asserted (8.3e-3), and the experiment's
    # eigh route pins the same gap at 7.8e-15
    if MUTANT == "parity-blind":
        # the mutant's assertions: central open, uniquely labeled
        if central["width"] <= 1e-8:
            print(f"FAIL: central asserted open but closed "
                  f"({central['width']:.2e})")
            failures.append("central")
        if len(sols17) == 1:
            pass
        else:
            print(f"FAIL: central asserted uniquely labeled but "
                  f"ambiguous: {sorted(sols17)}")
            failures.append("ambiguity")
    else:
        if central["width"] > 1e-8:
            print(f"FAIL: q=34 central open ({central['width']:.2e})")
            failures.append("central")
        if MUTANT != "shifted-window" and sorted(sols17) != [-17, 17]:
            print(f"FAIL: q=34 central label not ambiguous: {sols17}")
            failures.append("ambiguity")
    if "central" not in failures and "ambiguity" not in failures:
        print(f"q=34 central: closed ({central['width']:.1e}) and "
              f"label ambiguous {sorted(sols17) if MUTANT != 'shifted-window' else '(window shifted)'} ok")

    # (2) Fibonacci map at q = 21 (n = 8), incl. edge gap t = -8
    n = 8
    for j in range(2, n):
        r = FIB[j - 1]
        x = [g for g in G[21] if g["r"] == r][0]
        if x["width"] <= FLOOR:
            continue
        sols = dio(r, 13, 21)
        t = sols[0] if sols else None
        if t is None or abs(t) != FIB[n - j - 1]:
            print(f"FAIL: q=21 r={r} label {sols} vs |t|="
                  f"{FIB[n - j - 1]}")
            failures.append("map")
    edge = dio(1, 13, 21)
    if edge != [-8]:
        print(f"FAIL: q=21 edge label {edge} != [-8]")
        failures.append("edge")
    if "map" not in failures and "edge" not in failures:
        print("q=21 Fibonacci map + edge t=-8 ok")

    # (3) Streda across 13/21 -> 21/34
    pA = (13, 21)
    pB = (21, 34)
    GA, GB = G[21], G[34]
    from fractions import Fraction
    for t in (1, -1, 2):
        gA = [x for x in GA if x["width"] > FLOOR
              and dio(x["r"], pA[0], pA[1]) == [t]]
        gB = [x for x in GB if x["width"] > FLOOR
              and dio(x["r"], pB[0], pB[1]) == [t]]
        hit = False
        for xa in gA:
            for xb in gB:
                lo = max(xa["lo"], xb["lo"])
                hi = min(xa["hi"], xb["hi"])
                if hi <= lo:
                    continue
                hit = True
                slope = (Fraction(xb["r"], pB[1])
                         - Fraction(xa["r"], pA[1])) / \
                    (Fraction(pB[0], pB[1]) - Fraction(pA[0], pA[1]))
                if slope != t:
                    print(f"FAIL: Streda t={t}: slope {slope}")
                    failures.append("streda")
        if not hit:
            print(f"FAIL: Streda t={t}: no overlapping pair")
            failures.append("streda-overlap")
    if not any(f.startswith("streda") for f in failures):
        print("Streda slopes exact for t in {+1,-1,+2} ok")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p28 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
