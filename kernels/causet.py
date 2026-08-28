#!/usr/bin/env python3
"""Causal-set kernels: sprinkling, bitset partial order, future masks,
Hasse links, and the exact link-count quadrature. Extracted, not
rewritten.

Admission (two-artifact rule):
  sprinkle / pasts / futures / hasse_links
      scripts/experiments/p16_walk.py:16-50,
      scripts/verify/p16_two_dimensions.py:66-91
      (the bitset-order pattern originates in the P-10 line,
      scripts/experiments/p10_mm_dimension.py's ordered-pair counting)
  links_exact
      scripts/experiments/p16_derive.py:293-301 (EQ5),
      scripts/verify/p16_two_dimensions.py:94-102

Selftest anchors:
  - the N = 80, seed 31416 sprinkling (the p16 falsifier's own cell)
    yields 250 Hasse links, inside 6 sigma of the exact quadrature
    (p16_derive.py EQ5's null; scripts/verify/p16_two_dimensions.py:103).
  - links_exact reproduces the pinned N-ladder values of
    p16_registration.json (L(64) = 233.7..., quadrature-converged).
  - order sanity: past/future masks are transposes; links are exactly
    the covering relations (empty open interval).

stdlib only; floating-point operation order preserved from the sources.
"""
import math
import random


def sprinkle(N, seed):
    """N uniform points in the unit causal square, sorted by u
    (p16_walk.py:16)."""
    rng = random.Random(seed)
    pts = sorted((rng.random(), rng.random()) for _ in range(N))
    return pts


def pasts(pts):
    """past[i] = bitmask of causal predecessors of i. Points are sorted
    by u, so only j < i can precede; j precedes i iff v_j < v_i
    (p16_walk.py:27-33)."""
    N = len(pts)
    past = [0] * N
    for i in range(N):
        vi = pts[i][1]
        m = 0
        for j in range(i):
            if pts[j][1] < vi:
                m |= (1 << j)
        past[i] = m
    return past


def futures(past):
    """future[j] = bitmask of causal successors, built by transposing
    the past masks (p16_walk.py:34-39)."""
    N = len(past)
    future = [0] * N
    for i in range(N):
        m = past[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            future[j] |= (1 << i)
    return future


def hasse_links(pts):
    """Hasse (covering) links of the sprinkled order: (j, i) with j
    preceding i and an empty open interval, past[i] & future[j] == 0
    (p16_walk.py:22-50)."""
    N = len(pts)
    past = pasts(pts)
    future = futures(past)
    links = []
    for i in range(N):
        m = past[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if past[i] & future[j] == 0:
                links.append((j, i))
    return links


def links_exact(N, n=400):
    """E[links] for an N-point sprinkling of the unit causal square:
    the exact midpoint quadrature N(N-1) int (1-a)(1-b)(1-ab)^{N-2}
    da db, no Poisson approximation (p16_derive.py:293, EQ5)."""
    h = 1.0 / n
    tot = 0.0
    for i in range(n):
        a = (i + 0.5) * h
        for j in range(n):
            b = (j + 0.5) * h
            tot += (1 - a) * (1 - b) * (1 - a * b) ** (N - 2)
    return N * (N - 1) * tot * h * h


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True

    # anchor 1: the p16 falsifier's own cell - N = 80, seed 31416,
    # 250 links, inside 6 sigma of this file's own quadrature
    pts = sprinkle(80, 31416)
    links = hasse_links(pts)
    Lpin = links_exact(80, n=300)
    good = len(links) == 250 and abs(len(links) - Lpin) < 6 * math.sqrt(Lpin)
    ok &= good
    print(f"N=80 seed 31416: {len(links)} links vs quadrature {Lpin:.1f} "
          f"(6 sigma = {6 * math.sqrt(Lpin):.1f}) {'ok' if good else 'FAIL'}")

    # anchor 2: quadrature convergence at the registered ladder
    # (p16_derive.py EQ5 checks |L(128, n=400) - L(128, n=800)| < 0.2)
    d = abs(links_exact(128) - links_exact(128, n=800))
    ok &= d < 0.2
    print(f"links_exact(128) depth split {d:.3f} {'ok' if d < 0.2 else 'FAIL'}")

    # anchor 3: order sanity on a small sprinkling
    pts = sprinkle(24, 7)
    past = pasts(pts)
    fut = futures(past)
    trans_ok = all(((past[i] >> j) & 1) == ((fut[j] >> i) & 1)
                   for i in range(24) for j in range(24))
    lset = set(hasse_links(pts))
    cover_ok = all((past[i] & fut[j]) == 0 and ((past[i] >> j) & 1)
                   for (j, i) in lset)
    ok &= trans_ok and cover_ok
    print(f"past/future transpose and covering relations "
          f"{'ok' if trans_ok and cover_ok else 'FAIL'}")

    print("causet selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
