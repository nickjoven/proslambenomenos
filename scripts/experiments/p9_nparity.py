#!/usr/bin/env python3
"""P-9: N-parity of 1/2-plateau shrinkage on E1's pinned twisted ring.
Same model and edge-resolution method as d4_edge_resolved.py, with N
as a variable. For each N in 4..9 and (K, J) in {(1.0, 0.6),
(1.4, 0.6)}: twisted and control 1/2-plateau widths and their ratio.
Writes p9_results.json."""
import json
import math
from multiprocessing import Pool

TWO_PI = 2 * math.pi
ITERS, TRANS = 3200, 900
TOL = 4e-4


IC = "e1"   # "e1": theta_i = 0.13 i (E1's); "attractor": control in-phase, twisted half-winding


def rho(Omega, K, J, twisted, N):
    if IC == "e1":
        th = [0.13 * i for i in range(N)]
    else:
        th = [(0.5 * i / N) if twisted else 0.0 for i in range(N)]
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


def plateau(target, K, J, twisted, N, lo, hi, n=160):
    inside = [lo + (hi - lo) * k / n for k in range(n + 1)
              if abs(rho(lo + (hi - lo) * k / n, K, J, twisted, N) - target) < TOL]
    if not inside:
        return None
    a, b = inside[0], inside[-1]
    step = (hi - lo) / n

    def bisect(out, inn):
        for _ in range(28):
            m = (out + inn) / 2
            if abs(rho(m, K, J, twisted, N) - target) < TOL:
                inn = m
            else:
                out = m
        return inn
    left = bisect(a - step, a); right = bisect(b + step, b)
    return right - left


def job(args):
    N, K, J, twisted = args
    w = plateau(0.5, K, J, twisted, N, 0.40, 0.60)
    return {"N": N, "K": K, "J": J, "twisted": twisted, "width": w}


if __name__ == "__main__":
    import sys
    if "--attractor-ic" in sys.argv:
        IC = "attractor"
    grid = [(N, K, J, tw) for N in range(4, 10) for (K, J) in ((1.0, 0.6), (1.4, 0.6)) for tw in (False, True)]
    with Pool(14) as p:
        rows = p.map(job, grid, chunksize=1)
    out = {"rows": rows, "ratios": []}
    for (K, J) in ((1.0, 0.6), (1.4, 0.6)):
        for N in range(4, 10):
            wc = next(r["width"] for r in rows if r["N"] == N and r["K"] == K and not r["twisted"])
            wt = next(r["width"] for r in rows if r["N"] == N and r["K"] == K and r["twisted"])
            ratio = (wt / wc) if (wc and wt is not None) else None
            out["ratios"].append({"N": N, "K": K, "J": J, "w_control": wc, "w_twisted": wt, "ratio": ratio})
            print(f"K={K} J={J} N={N} {'even' if N % 2 == 0 else 'odd '}: control {wc if wc is None else round(wc, 5)}  "
                  f"twisted {wt if wt is None else round(wt, 5)}  ratio {ratio if ratio is None else round(ratio, 3)}", flush=True)
    with open(f"scripts/experiments/p9_results{'_attractor' if IC == 'attractor' else ''}.json", "w") as f:
        json.dump(out, f, indent=1)
