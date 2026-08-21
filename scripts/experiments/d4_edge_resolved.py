#!/usr/bin/env python3
"""E1 step 3: edge-resolved plateau measurement on the twisted ring.

Decides shift vs shrink: for each target rational and each (K, J),
locate the plateau's Omega-interval by coarse scan + edge bisection,
in the twisted ring and the control. Report center, width, and the
plateau's actual locked rho (deviation from p/q would indicate a
shifted locking VALUE, not just a moved window). Writes
d4_edge_results.json. Exploration tier."""

import json
import math
from pathlib import Path

TWO_PI = 2 * math.pi
N = 4
ITERS, TRANS = 3200, 900
TOL = 4e-4


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


def plateau(target, K, J, twisted, lo, hi, n=160):
    inside = [lo + (hi - lo) * k / n for k in range(n + 1)
              if abs(rho(lo + (hi - lo) * k / n, K, J, twisted) - target) < TOL]
    if not inside:
        return None
    a, b = inside[0], inside[-1]
    step = (hi - lo) / n

    def bisect(out, inn):
        for _ in range(28):
            m = (out + inn) / 2
            if abs(rho(m, K, J, twisted) - target) < TOL:
                inn = m
            else:
                out = m
        return inn

    left = bisect(a - step, a)
    right = bisect(b + step, b)
    center = (left + right) / 2
    locked = rho(center, K, J, twisted)
    return {"left": left, "right": right, "width": right - left,
            "center": center, "locked_rho": locked,
            "rho_dev": locked - target}


def main():
    targets = [(1, 2, 0.35, 0.65), (1, 3, 0.18, 0.45), (2, 3, 0.55, 0.82)]
    out = []
    print(f"{'K':>4} {'J':>4} {'p/q':>4} {'side':>7} | {'center':>9} "
          f"{'width':>9} {'rho-p/q':>10}")
    for K, J in [(1.0, 0.6), (1.4, 0.6)]:
        for p, q, lo, hi in targets:
            row = {"K": K, "J": J, "target": f"{p}/{q}"}
            for tw, name in ((False, "control"), (True, "twisted")):
                r = plateau(p / q, K, J, tw, lo, hi)
                row[name] = r
                if r:
                    print(f"{K:>4} {J:>4} {p}/{q:<3}{name:>8} | "
                          f"{r['center']:>9.5f} {r['width']:>9.5f} "
                          f"{r['rho_dev']:>10.2e}")
                else:
                    print(f"{K:>4} {J:>4} {p}/{q:<3}{name:>8} | absent")
            out.append(row)
    Path(__file__).with_name("d4_edge_results.json").write_text(
        json.dumps(out))
    print("wrote d4_edge_results.json")


if __name__ == "__main__":
    main()
