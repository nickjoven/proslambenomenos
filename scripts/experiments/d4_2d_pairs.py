#!/usr/bin/env python3
"""D4 proper: 2D Klein-twisted lattice - joint admissibility of
(spatial parity pair, temporal rational).

Lattice N x M, phases in turns. Neighbors: y periodic; x crosses the
Klein seam: (N-1, j) <-> (0, M-1-j) with +1/2 turn offset (and the
reverse edge with -1/2), per v1 klein_bottle.md. Per-site pinning
supplies the drive (as in E1). For each Omega and seed branch, after
transient we record:
  rho   - collective rotation number, snapped to p/q (q <= 8)
  b_x   - parity of the x-winding around the orientation DOUBLE loop
          (the x-cycle closes only after two traversals; odd double
          winding == half-integer single-loop winding)
  b_y   - y bond order: mean cos(2pi * dy-theta); >0.5 uniform (0),
          <-0.5 staggered (1), else defect (-)
Cross-tabulates q-parity and p-parity of rho against (b_x, b_y).
Writes d4_2d_results.json. Exploration tier."""

import json
import math
from pathlib import Path

TWO_PI = 2 * math.pi
N, M = 4, 4
ITERS, TRANS = 2600, 900
TOL = 5e-4


def neighbors(i, j):
    out = []
    if i + 1 < N:
        out.append((i + 1, j, 0.0))
    else:
        out.append((0, M - 1 - j, 0.5))
    if i - 1 >= 0:
        out.append((i - 1, j, 0.0))
    else:
        out.append((N - 1, M - 1 - j, -0.5))
    out.append((i, (j + 1) % M, 0.0))
    out.append((i, (j - 1) % M, 0.0))
    return out


NBR = {(i, j): neighbors(i, j) for i in range(N) for j in range(M)}


def seed(branch):
    th = {}
    for i in range(N):
        for j in range(M):
            if branch == "uniform":      # W1 = 1/2 gradient, y-uniform
                th[(i, j)] = 0.5 * i / N
            elif branch == "staggered":  # W1 = 0, y pi-staggered
                th[(i, j)] = 0.5 * (j % 2)
            else:                        # pseudo-random, deterministic
                th[(i, j)] = (0.37 * i + 0.61 * j * j) % 1.0
    return th


def run(Omega, K, J, branch):
    th = seed(branch)
    total = 0.0
    for t in range(ITERS + TRANS):
        adv = {}
        for (i, j), v in th.items():
            c = 0.0
            for (a, b, s) in NBR[(i, j)]:
                c += math.sin(TWO_PI * (th[(a, b)] - v + s))
            adv[(i, j)] = Omega - (K / TWO_PI) * math.sin(TWO_PI * v) \
                + (J / TWO_PI) * c
        for k in adv:
            th[k] += adv[k]
        if t >= TRANS:
            total += sum(adv.values()) / (N * M)
    rho = total / ITERS

    def pv(d):
        return d - round(d)

    # x double-loop winding from row j = 0
    w, i, j = 0.0, 0, 0
    for _ in range(2):
        for step in range(N - 1):
            w += pv(th[(i + 1, j)] - th[(i, j)])
            i += 1
        w += pv(th[(0, M - 1 - j)] - th[(i, j)] + 0.5) - 0.5
        i, j = 0, M - 1 - j
    b_x = int(round(w)) % 2

    sy = sum(math.cos(TWO_PI * (th[(i, (j + 1) % M)] - th[(i, j)]))
             for i in range(N) for j in range(M)) / (N * M)
    b_y = 0 if sy > 0.5 else (1 if sy < -0.5 else -1)
    return rho, b_x, b_y


def main():
    grid = 160
    results = []
    for K, J in [(1.0, 0.6), (1.4, 0.6)]:
        for branch in ("uniform", "staggered", "random"):
            for k in range(grid + 1):
                Om = k / grid
                rho, bx, by = run(Om, K, J, branch)
                snapped = None
                for q in range(1, 9):
                    p = round(rho * q)
                    if abs(rho - p / q) < TOL and math.gcd(p, q) == 1 \
                            and 0 <= p <= q:
                        snapped = (p, q)
                        break
                results.append({"K": K, "J": J, "branch": branch,
                                "Omega": Om, "rho": rho,
                                "pq": snapped, "bx": bx, "by": by})
    Path(__file__).with_name("d4_2d_results.json").write_text(
        json.dumps(results))
    # cross-tab: locked states only, by (bx, by) vs q-parity and p-parity
    tab = {}
    for r in results:
        if r["pq"] is None or r["by"] == -1:
            continue
        p, q = r["pq"]
        key = (r["bx"], r["by"])
        cell = tab.setdefault(key, {"q_odd": 0, "q_even": 0,
                                    "p_odd": 0, "p_even": 0, "n": 0})
        cell["n"] += 1
        cell["q_odd" if q % 2 else "q_even"] += 1
        cell["p_odd" if p % 2 else "p_even"] += 1
    print(f"{'(bx,by)':>8} {'n':>5} {'q_odd':>6} {'q_even':>7} "
          f"{'p_odd':>6} {'p_even':>7}")
    for key in sorted(tab):
        c = tab[key]
        print(f"{str(key):>8} {c['n']:>5} {c['q_odd']:>6} {c['q_even']:>7} "
              f"{c['p_odd']:>6} {c['p_even']:>7}")
    defects = sum(1 for r in results if r["by"] == -1 and r["pq"])
    print(f"locked-but-defect (by undefined): {defects}")
    print("wrote d4_2d_results.json")


if __name__ == "__main__":
    main()
