#!/usr/bin/env python3
"""D4 probe E1, step 2: K/J sweep of the twisted-ring temporal
staircase. Question: is the E1 signature (crushed 1/2 plateau,
enhanced odd/2N plateaus) a robust property of the seam or a
coupling artifact? Writes d4_sweep_results.json next to itself.
Exploration script; interpretation in notes."""

import json
import math
import sys
from pathlib import Path

TWO_PI = 2 * math.pi
N = 4
OMEGA_PTS = 240
ITERS, TRANS = 2200, 600
TOL = 6e-4


def rho(Omega, K, J, twisted):
    th = [0.13 * i for i in range(N)]
    total = 0.0
    for t in range(ITERS + TRANS):
        adv = []
        for i in range(N):
            up = (i + 1) % N
            dn = (i - 1) % N
            s_up = 0.5 if (twisted and i == N - 1) else 0.0
            s_dn = 0.5 if (twisted and dn == N - 1) else 0.0
            c = (J / TWO_PI) * (
                math.sin(TWO_PI * (th[up] - th[i] + s_up)) +
                math.sin(TWO_PI * (th[dn] - th[i] - s_dn)))
            adv.append(Omega - (K / TWO_PI) * math.sin(TWO_PI * th[i]) + c)
        for i in range(N):
            th[i] += adv[i]
        if t >= TRANS:
            total += sum(adv) / N
    return total / ITERS


def sweep(K, J, twisted):
    hits = {}
    for k in range(OMEGA_PTS + 1):
        r = rho(k / OMEGA_PTS, K, J, twisted)
        for q in range(1, 9):
            p = round(r * q)
            if abs(r - p / q) < TOL and math.gcd(p, q) == 1 and 0 <= p <= q:
                hits[f"{p}/{q}"] = hits.get(f"{p}/{q}", 0) + 1
                break
    return hits


def stat(hits, keys):
    return sum(hits.get(k, 0) for k in keys)


def main():
    Ks = [0.6, 1.0, 1.4]
    Js = [0.3, 0.6, 1.2]
    out = {"N": N, "omega_pts": OMEGA_PTS, "runs": []}
    print(f"{'K':>4} {'J':>4} | {'half T/C':>9} | {'odd/8 T/C':>10} | "
          f"{'thirds T/C':>10}")
    for K in Ks:
        for J in Js:
            c = sweep(K, J, False)
            t = sweep(K, J, True)
            half = (stat(t, ["1/2"]), stat(c, ["1/2"]))
            odd8 = (stat(t, ["1/8", "3/8", "5/8", "7/8"]),
                    stat(c, ["1/8", "3/8", "5/8", "7/8"]))
            thirds = (stat(t, ["1/3", "2/3"]), stat(c, ["1/3", "2/3"]))
            out["runs"].append({"K": K, "J": J, "control": c, "twisted": t})
            print(f"{K:>4} {J:>4} | {half[0]:>4}/{half[1]:<4} | "
                  f"{odd8[0]:>4}/{odd8[1]:<5} | {thirds[0]:>4}/{thirds[1]:<5}")
    Path(__file__).with_name("d4_sweep_results.json").write_text(
        json.dumps(out))
    print("wrote d4_sweep_results.json")


if __name__ == "__main__":
    main()
