#!/usr/bin/env python3
"""P-43 derivation layer (pre-registration): the shadow is the
same square; the bodies are different polytopes.

Item 2 of the 2026-09-01 theoretical press (lessons L-8 consulted
per AGENTS 8d). Liu-Chiribella remark that their causal-vs-ICO
picture 'coincides' with the CHSH picture - a circle of quantum
correlations with the classical square inscribed. Is that
coincidence a 2-dimensional SHADOW of a real isomorphism between
the local polytope and the causal polytope, or only a shadow?

Derived facts (all exact rational arithmetic unless stated):
  EQ1  the local CHSH polytope: 16 deterministic strategies
       a = f(x), b = g(y) as distributions p(ab|xy) in R^16; all
       16 distinct (each is 0/1-valued, hence a vertex); affine
       dimension by incremental Fraction elimination = 8.
  EQ2  the causal OCB polytope: the 8192 deterministic one-way
       strategies of P-39 as distributions p(a1 a2 | x1, b, c) in
       R^32; deduped vertex count V and affine dimension D
       computed the same way - the PINS this registration carries.
  EQ3  the refusal: affine isomorphism preserves (dimension,
       vertex count); the pairs differ, so the bodies are NOT
       affinely isomorphic - the coincidence is only a shadow.
  EQ4  the shadows really are the same picture: causal side
       projected onto (P_A, P_B) has extreme points (1,1/2),
       (1/2,1), (0,1/2), (1/2,0) ON the circle of radius 1/2
       around (1/2,1/2) (P-39, recomputed); CHSH side projected
       onto (u, v) = ((E00+E01)/2, (E10-E11)/2) has extreme
       points (+-1, 0), (0, +-1) ON the unit circle (exact: E's
       of deterministic strategies are +-1); the affine map
       T(u,v) = ((u+1)/2, (v+1)/2) carries square+circle onto
       square+circle, verified on every extreme point exactly.
       The CHSH quantum circle is ACHIEVED constructively:
       singlet correlators at the closed-form settings
       (phi+pi, phi+pi/2, 0, 2 phi) land on (cos phi, sin phi)
       at machine epsilon on the whole phi grid; its
       completeness (nothing outside the disc) is IMPORTED
       (Tsirelson / Landau / Masanes, LC-32), mirroring P-39's
       earned-achievability / imported-bound split.

Run: python3 scripts/experiments/p43_derive.py
"""
import itertools
import json
import math
import os
from fractions import Fraction


# ---------------------------------------------------------------
# exact affine dimension: incremental elimination over Fractions
# ---------------------------------------------------------------
def affine_dim(points):
    base = points[0]
    basis = []
    for p in points[1:]:
        v = [a - b for a, b in zip(p, base)]
        for bvec in basis:
            piv = next((i for i, x in enumerate(bvec) if x != 0), None)
            if piv is not None and v[piv] != 0:
                f = v[piv] / bvec[piv]
                v = [a - f * b for a, b in zip(v, bvec)]
        if any(x != 0 for x in v):
            basis.append(v)
    return len(basis)


# ---------------------------------------------------------------
# EQ1: local CHSH polytope
# ---------------------------------------------------------------
def local_points():
    pts = []
    for fa in itertools.product((0, 1), repeat=2):
        for gb in itertools.product((0, 1), repeat=2):
            vec = []
            for x in (0, 1):
                for y in (0, 1):
                    for a in (0, 1):
                        for b in (0, 1):
                            vec.append(Fraction(
                                1 if (fa[x] == a and gb[y] == b)
                                else 0))
            pts.append(tuple(vec))
    return pts


# ---------------------------------------------------------------
# EQ2: causal OCB polytope (P-39's strategy spaces)
# ---------------------------------------------------------------
def causal_points():
    pts = set()
    # order A -> B
    for f_bits in range(4):
        for g_bits in range(4):
            for h_bits in range(256):
                vec = []
                for x1 in (0, 1):
                    for b in (0, 1):
                        for c in (0, 1):
                            a1 = (f_bits >> x1) & 1
                            m = (g_bits >> x1) & 1
                            a2 = (h_bits >> ((b << 2) | (c << 1) | m)) & 1
                            for aa1 in (0, 1):
                                for aa2 in (0, 1):
                                    vec.append(Fraction(
                                        1 if (aa1 == a1 and aa2 == a2)
                                        else 0))
                pts.add(tuple(vec))
    # order B -> A
    for f_bits in range(16):
        for g_bits in range(16):
            for h_bits in range(16):
                vec = []
                for x1 in (0, 1):
                    for b in (0, 1):
                        for c in (0, 1):
                            a2 = (f_bits >> ((b << 1) | c)) & 1
                            m = (g_bits >> ((b << 1) | c)) & 1
                            a1 = (h_bits >> ((x1 << 1) | m)) & 1
                            for aa1 in (0, 1):
                                for aa2 in (0, 1):
                                    vec.append(Fraction(
                                        1 if (aa1 == a1 and aa2 == a2)
                                        else 0))
                pts.add(tuple(vec))
    return sorted(pts)


# ---------------------------------------------------------------
# EQ4: shadows
# ---------------------------------------------------------------
def causal_shadow(pts):
    shadow = set()
    for p in pts:
        # p indexed by (x1, b, c, a1, a2): stride 4 per context
        # P_A = P(a1 = b | c = 0), P_B = P(a2 = x1 | c = 1)
        pa = Fraction(0)
        pb = Fraction(0)
        idx = 0
        for x1 in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    for a1 in (0, 1):
                        for a2 in (0, 1):
                            v = p[idx]
                            idx += 1
                            if c == 0 and a1 == b:
                                pa += v
                            if c == 1 and a2 == x1:
                                pb += v
        shadow.add((pa / 4, pb / 4))
    return sorted(shadow)


def chsh_shadow():
    pts = set()
    for fa in itertools.product((-1, 1), repeat=2):
        for gb in itertools.product((-1, 1), repeat=2):
            E = {(x, y): Fraction(fa[x] * gb[y])
                 for x in (0, 1) for y in (0, 1)}
            u = (E[(0, 0)] + E[(0, 1)]) / 2
            v = (E[(1, 0)] - E[(1, 1)]) / 2
            pts.add((u, v))
    return sorted(pts)


def chsh_quantum_reach(nphi=24):
    """Achievability of the unit circle, CONSTRUCTIVE: singlet
    correlators E(a, b) = -cos(a - b) with the closed-form
    settings (a0, a1, b0, b1) = (phi + pi, phi + pi/2, 0, 2 phi)
    give (u, v) = (cos phi, sin phi) exactly; verified on the phi
    grid at 1e-12. (An earlier grid-and-climb optimizer stalled at
    cos(pi/12) on some directions - flat 4-angle landscape; the
    construction replaces the search.)"""
    worst = 0.0
    for k in range(nphi):
        phi = 2 * math.pi * k / nphi
        a0, a1, b0, b1 = phi + math.pi, phi + math.pi / 2, 0.0, 2 * phi
        E = lambda a, b: -math.cos(a - b)
        u = (E(a0, b0) + E(a0, b1)) / 2
        v = (E(a1, b0) - E(a1, b1)) / 2
        worst = max(worst, abs(u - math.cos(phi)),
                    abs(v - math.sin(phi)))
    return {"worst_settings_error": worst, "reach": 1.0}


def main():
    lp = local_points()
    lset = set(lp)
    cp = causal_points()
    res = {"EQ1": {"vertices": len(lset), "dim": affine_dim(lp)},
           "EQ2": {"vertices": len(cp), "dim": affine_dim(cp)}}
    res["EQ3"] = {"same_dim": res["EQ1"]["dim"] == res["EQ2"]["dim"],
                  "same_vertices":
                  res["EQ1"]["vertices"] == res["EQ2"]["vertices"],
                  "affinely_isomorphic_possible":
                  res["EQ1"] == res["EQ2"]}
    cs = causal_shadow(cp)
    xs = chsh_shadow()
    half = Fraction(1, 2)

    def on_circle_causal(p):
        return (p[0] - half) ** 2 + (p[1] - half) ** 2 == \
            Fraction(1, 4)

    def on_circle_chsh(p):
        return p[0] ** 2 + p[1] ** 2 == 1
    causal_ext = [p for p in cs if on_circle_causal(p)]
    chsh_ext = [p for p in xs if on_circle_chsh(p)]
    T = lambda p: ((p[0] + 1) / 2, (p[1] + 1) / 2)
    mapped = sorted(T(p) for p in chsh_ext)
    res["EQ4"] = {
        "causal_shadow_points": len(cs),
        "causal_extremes_on_circle": [tuple(map(str, p))
                                      for p in sorted(causal_ext)],
        "chsh_shadow_points": len(xs),
        "chsh_extremes_on_circle": [tuple(map(str, p))
                                    for p in sorted(chsh_ext)],
        "map_matches": mapped == sorted(causal_ext),
        "chsh_quantum_reach_min_over_phi": chsh_quantum_reach()}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p43_registration.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
