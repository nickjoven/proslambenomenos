#!/usr/bin/env python3
"""P-8: finite-T bias of model-free plateau-width measurement on the
sine circle map theta -> theta + Omega - (K/2pi) sin(2 pi theta).
Width of the p/q plateau = bisected edges of {Omega : |rho_T(Omega) -
p/q| < tol}, rho_T the rotation number over T iterations after a
transient T/4. Sweep T; fit w(T) = w_inf + c T^-a by least squares on
log(w(T) - w(T_max)) against log T using the three smallest T (so
T_max stands in for w_inf). Centre shift for q >= 3 measured as the
midpoint minus p/q. Writes p8_results.json."""
import json
import math
import sys
from multiprocessing import Pool

TWO_PI = 2 * math.pi


def rho(Om, K, T):
    th = 0.0
    for _ in range(T // 4):
        th += Om - (K / TWO_PI) * math.sin(TWO_PI * th)
    s = th
    for _ in range(T):
        th += Om - (K / TWO_PI) * math.sin(TWO_PI * th)
    return (th - s) / T


def edges(p, q, K, T, lo, hi, tol=2e-5, N=400):
    target = p / q
    inside = [lo + (hi - lo) * i / N for i in range(N + 1) if abs(rho(lo + (hi - lo) * i / N, K, T) - target) < tol]
    if not inside:
        return None
    a, b = inside[0], inside[-1]
    step = (hi - lo) / N
    def bis(out, inn):
        for _ in range(30):
            m = (out + inn) / 2
            if abs(rho(m, K, T) - target) < tol: inn = m
            else: out = m
        return inn
    return bis(a - step, a), bis(b + step, b)


def job(args):
    p, q, K, T, lo, hi = args
    e = edges(p, q, K, T, lo, hi)
    return {"p": p, "q": q, "K": K, "T": T, "left": e[0] if e else None, "right": e[1] if e else None,
            "width": (e[1] - e[0]) if e else None, "centre_shift": ((e[0] + e[1]) / 2 - p / q) if e else None}


if __name__ == "__main__":
    Ts = [600, 1200, 2400, 4800, 9600]
    plateaus = [(1, 2, 0.5, 0.47, 0.53), (1, 3, 0.5, 0.31, 0.36), (1, 2, 1.0, 0.35, 0.65), (1, 3, 1.0, 0.25, 0.42)]
    grid = [(p, q, K, T, lo, hi) for (p, q, K, lo, hi) in plateaus for T in Ts]
    with Pool(14) as pool:
        rows = pool.map(job, grid, chunksize=1)
    out = {"rows": rows, "fits": []}
    for (p, q, K, lo, hi) in plateaus:
        ws = [(r["T"], r["width"]) for r in rows if r["p"] == p and r["q"] == q and r["K"] == K and r["width"]]
        ws.sort()
        winf = ws[-1][1]
        pts = [(math.log(T), math.log(w - winf)) for T, w in ws[:-1] if w - winf > 0]
        from_above = all(w >= winf - 1e-12 for _, w in ws)
        if len(pts) >= 2:
            n = len(pts); sx = sum(x for x, _ in pts); sy = sum(y for _, y in pts)
            sxx = sum(x * x for x, _ in pts); sxy = sum(x * y for x, y in pts)
            a = -(n * sxy - sx * sy) / (n * sxx - sx * sx)
        else:
            a = None
        cs = [r["centre_shift"] for r in rows if r["p"] == p and r["q"] == q and r["K"] == K and r["centre_shift"] is not None]
        out["fits"].append({"p": p, "q": q, "K": K, "widths": ws, "from_above": from_above,
                            "exponent_a": a, "centre_shift_mean": sum(cs) / len(cs) if cs else None})
        print(f"{p}/{q} K={K}: " + ", ".join(f"T={T}:{w:.6f}" for T, w in ws) +
              f" | from above: {from_above} | a = {a if a is None else round(a, 2)} | centre shift {sum(cs)/len(cs):+.5f}", flush=True)
    with open("scripts/experiments/p8_results.json", "w") as f:
        json.dump(out, f, indent=1)
