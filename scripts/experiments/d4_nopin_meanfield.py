#!/usr/bin/env python3
"""D4 hole (a): the corpus-canonical dynamics has NO per-site pinning -
it is a Kuramoto lattice with distributed natural frequencies and a
self-consistent mean field. Question: does ANY rational (temporal
mode-locking) structure exist at all without the pinning drive E1
added? Expected (recorded in notes before running): the locked state
has a single collective frequency, rho varies smoothly with the
control parameter, and rational snaps occur only at grid-coincidence
rate. Twisted vs control compared. Writes d4_nopin_results.json."""

import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from d4_2d_pairs import NBR, N, M, TWO_PI  # noqa: E402

ITERS, TRANS = 2400, 800
TOL = 5e-4
# quenched zero-mean frequency offsets, deterministic
G = {(i, j): math.sin(1.7 * i + 2.9 * j) for i in range(N) for j in range(M)}
gm = sum(G.values()) / (N * M)
G = {k: v - gm for k, v in G.items()}


def run(Omega, Delta, J, twisted):
    th = {(i, j): (0.37 * i + 0.61 * j * j) % 1.0
          for i in range(N) for j in range(M)}
    total = 0.0
    for t in range(ITERS + TRANS):
        adv = {}
        for k, v in th.items():
            c = 0.0
            for (a, b, s) in NBR[k]:
                c += math.sin(TWO_PI * (th[(a, b)] - v + (s if twisted else 0.0)))
            adv[k] = Omega + Delta * G[k] + (J / TWO_PI) * c
        for k in adv:
            th[k] += adv[k]
        if t >= TRANS:
            total += sum(adv.values()) / (N * M)
    return total / ITERS


def main():
    J = 0.6
    grid = 100
    out = []
    print(f"{'Delta':>6} {'side':>8} | {'snaps(q<=8)':>12} {'max|rho-Om|':>12}")
    for Delta in (0.05, 0.2):
        for twisted in (False, True):
            snaps = 0
            maxdev = 0.0
            for k in range(grid + 1):
                Om = k / grid
                r = run(Om, Delta, J, twisted)
                maxdev = max(maxdev, abs(r - Om))
                for q in range(2, 9):
                    p = round(r * q)
                    if abs(r - p / q) < TOL and math.gcd(p, q) == 1 and 0 < p < q:
                        snaps += 1
                        break
                out.append({"Delta": Delta, "twisted": twisted, "Omega": Om, "rho": r})
            # chance rate: window 2*TOL around each rational q<=8 in (0,1)
            rats = sum(1 for q in range(2, 9) for p in range(1, q) if math.gcd(p, q) == 1)
            chance = (grid + 1) * rats * 2 * TOL
            print(f"{Delta:>6} {'twisted' if twisted else 'control':>8} | "
                  f"{snaps:>5} (chance ~{chance:.1f}) {maxdev:>12.2e}")
    Path(__file__).with_name("d4_nopin_results.json").write_text(json.dumps(out))
    print("wrote d4_nopin_results.json")


if __name__ == "__main__":
    main()
