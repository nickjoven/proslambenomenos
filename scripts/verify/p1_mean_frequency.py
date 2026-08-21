#!/usr/bin/env python3
"""Verification for klein-twisted-mean-frequency-identity: in a
Kuramoto lattice with antisymmetric (sine) coupling and consistent
seam offsets (s_ab = -s_ba), the mean phase advance per step equals
the mean natural frequency EXACTLY, at every step - twist or no twist
- because each edge contributes sin(x) + sin(-x) = 0 to the total.

Proof: sum over sites of sum over neighbors of sin(2pi(theta_b -
theta_a + s_ab)); each undirected edge appears twice with arguments
x and -x (s_ba = -s_ab), cancelling. Hence (1/NM) sum_a dtheta_a =
Omega + mean(Delta*G) = Omega when G has zero mean. Checked here on a
4 x 4 Klein-twisted lattice and its untwisted control, 300 steps,
|mean advance - Omega| < 1e-12 at every step. Exit 0 iff so."""

import math
import sys

TWO_PI = 2 * math.pi
N, M = 4, 4


def neighbors(i, j, twisted):
    out = []
    if i + 1 < N:
        out.append((i + 1, j, 0.0))
    else:
        out.append((0, M - 1 - j, 0.5 if twisted else 0.0))
    if i - 1 >= 0:
        out.append((i - 1, j, 0.0))
    else:
        out.append((N - 1, M - 1 - j, -0.5 if twisted else 0.0))
    out.append((i, (j + 1) % M, 0.0))
    out.append((i, (j - 1) % M, 0.0))
    return out


def main() -> int:
    ok = True
    G = {(i, j): math.sin(1.7 * i + 2.9 * j) for i in range(N) for j in range(M)}
    gm = sum(G.values()) / (N * M)
    G = {k: v - gm for k, v in G.items()}
    for twisted in (False, True):
        NBR = {(i, j): neighbors(i, j, twisted) for i in range(N) for j in range(M)}
        th = {(i, j): (0.37 * i + 0.61 * j * j) % 1.0 for i in range(N) for j in range(M)}
        Omega, Delta, J = 0.3137, 0.2, 0.6
        worst = 0.0
        for _ in range(300):
            adv = {}
            for k, v in th.items():
                c = sum(math.sin(TWO_PI * (th[(a, b)] - v + s)) for (a, b, s) in NBR[k])
                adv[k] = Omega + Delta * G[k] + (J / TWO_PI) * c
            mean_adv = sum(adv.values()) / (N * M)
            worst = max(worst, abs(mean_adv - Omega))
            for k in adv:
                th[k] += adv[k]
        print(f"{'twisted' if twisted else 'control'}: max |mean advance - Omega| = {worst:.2e}")
        ok &= worst < 1e-12
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
