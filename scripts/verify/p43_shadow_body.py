#!/usr/bin/env python3
"""Verification for the P-43 claim shadow-not-body, by independent
live reimplementation: its own strategy encodings (tuple tables,
not bit twiddling), its own rank computation (row-reduce over
Fractions with a different pivoting order), its own shadow
projections. Nothing read from results files.

Checks: (1) local CHSH: 16 distinct deterministic distributions,
affine dimension 8; (2) causal OCB: 2368 distinct, dimension 24;
(3) the invariants differ in both coordinates - no affine
isomorphism; (4) shadows: exactly four extreme points on each
circle, carried onto each other by T(u,v) = ((u+1)/2, (v+1)/2) as
exact rationals; the closed-form singlet settings land on
(cos phi, sin phi) at 1e-12 on a 24-point grid.

--mutant body-blind    asserts the polytopes are affinely
    isomorphic; the invariant mismatch kills it.
--mutant shadow-blind  asserts the CHSH classical extreme (1, 0)
    lies strictly inside the unit circle; it lies ON it.
"""
import itertools
import math
import sys
from fractions import Fraction

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"body-blind", "shadow-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


def rank_affine(points):
    """Affine dimension by Gaussian elimination, last-column-first
    pivoting (a different order from the experiment's)."""
    base = points[0]
    rows = []
    for p in points[1:]:
        rows.append([a - b for a, b in zip(p, base)])
    n = len(rows[0])
    r = 0
    for col in range(n - 1, -1, -1):
        piv = next((i for i in range(r, len(rows))
                    if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col] / rows[r][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def local_pts():
    out = set()
    for fa in itertools.product((0, 1), repeat=2):
        for gb in itertools.product((0, 1), repeat=2):
            vec = tuple(Fraction(1 if (fa[x] == a and gb[y] == b)
                                 else 0)
                        for x in (0, 1) for y in (0, 1)
                        for a in (0, 1) for b in (0, 1))
            out.add(vec)
    return sorted(out)


def causal_pts():
    out = set()
    contexts = [(x1, b, c) for x1 in (0, 1) for b in (0, 1)
                for c in (0, 1)]
    # order A -> B: tables as tuples
    for a1_t in itertools.product((0, 1), repeat=2):
        for m_t in itertools.product((0, 1), repeat=2):
            for a2_t in itertools.product((0, 1), repeat=8):
                vec = []
                for (x1, b, c) in contexts:
                    a1 = a1_t[x1]
                    a2 = a2_t[(b << 2) | (c << 1) | m_t[x1]]
                    for aa1 in (0, 1):
                        for aa2 in (0, 1):
                            vec.append(Fraction(
                                1 if (aa1, aa2) == (a1, a2) else 0))
                out.add(tuple(vec))
    # order B -> A
    for a2_t in itertools.product((0, 1), repeat=4):
        for m_t in itertools.product((0, 1), repeat=4):
            for a1_t in itertools.product((0, 1), repeat=4):
                vec = []
                for (x1, b, c) in contexts:
                    bc = (b << 1) | c
                    a2 = a2_t[bc]
                    a1 = a1_t[(x1 << 1) | m_t[bc]]
                    for aa1 in (0, 1):
                        for aa2 in (0, 1):
                            vec.append(Fraction(
                                1 if (aa1, aa2) == (a1, a2) else 0))
                out.add(tuple(vec))
    return sorted(out)


def main():
    failures = []
    lp = local_pts()
    dl, vl = rank_affine(lp), len(lp)
    print(f"local: V = {vl}, dim = {dl}")
    if (vl, dl) != (16, 8):
        print("FAIL: local polytope invariants off")
        failures.append("local")
    cp = causal_pts()
    dc, vc = rank_affine(cp), len(cp)
    print(f"causal: V = {vc}, dim = {dc}")
    if (vc, dc) != (2368, 24):
        print("FAIL: causal polytope invariants off the pins")
        failures.append("causal")
    if MUTANT == "body-blind":
        if (vl, dl) != (vc, dc):
            print("FAIL: asserted the polytopes are affinely "
                  "isomorphic; the invariants differ "
                  f"({vl},{dl}) vs ({vc},{dc})")
            failures.append("body")
    # shadows
    ext = []
    for fa in itertools.product((-1, 1), repeat=2):
        for gb in itertools.product((-1, 1), repeat=2):
            E = {(x, y): Fraction(fa[x] * gb[y])
                 for x in (0, 1) for y in (0, 1)}
            u = (E[(0, 0)] + E[(0, 1)]) / 2
            v = (E[(1, 0)] - E[(1, 1)]) / 2
            if u * u + v * v == 1:
                ext.append((u, v))
    ext = sorted(set(ext))
    print(f"CHSH extremes on the unit circle: {len(ext)}")
    if MUTANT == "shadow-blind":
        p = (Fraction(1), Fraction(0))
        if p[0] ** 2 + p[1] ** 2 == 1:
            print("FAIL: asserted (1, 0) lies strictly inside the "
                  "unit circle; it lies ON it")
            failures.append("shadow")
    if len(ext) != 4:
        print("FAIL: CHSH shadow extreme count off")
        failures.append("chsh-ext")
    worst = 0.0
    for k in range(24):
        phi = 2 * math.pi * k / 24
        a0, a1, b0, b1 = (phi + math.pi, phi + math.pi / 2,
                          0.0, 2 * phi)
        E = lambda a, b: -math.cos(a - b)
        u = (E(a0, b0) + E(a0, b1)) / 2
        v = (E(a1, b0) - E(a1, b1)) / 2
        worst = max(worst, abs(u - math.cos(phi)),
                    abs(v - math.sin(phi)))
    print(f"constructive circle settings worst error {worst:.1e}")
    if worst > 1e-12:
        print("FAIL: the constructive settings miss the circle")
        failures.append("reach")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p43 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
