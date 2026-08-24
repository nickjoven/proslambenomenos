#!/usr/bin/env python3
"""P-10 step 3: Myrheim-Meyer dimension recovery from sprinkled orders.

Registered BEFORE this file was written: PREDICTIONS.md P-10 (commit
3ce3997), with the null, the variance, the bands, and the mutant
expectations all derived in scripts/experiments/p10_symbolic.py
(27 EQ lines, committed output p10_symbolic_out.txt). Constants below
are copied from that output; nothing here re-tunes them.

What runs: for d in {2,3,4} and N in {2^7..2^13}, M(N) independent
fixed-N sprinkles into the unit causal interval of d-Minkowski
(accept-reject from the unit box; the acceptance rate is checked
against the derived volume fraction, EQ 1-3). R = number of causally
related unordered pairs (t-sorted brute force, dt^2 > |dx|^2);
d_hat = F^-1(R / C(N,2)) by bisection on the Gamma form anchored at
the direct integrals (EQ 11-18).

Variants (paired: mutants reuse the identical sampled points):
  none               - the real order
  shuffled-order     - random permutation of the time coordinate
                       across points, spatial parts kept (all d)
  shuffled-lightcone - d=2 only: random permutation of the lightcone
                       coordinate v = t + x across points (derived to
                       be a distributional symmetry, EQ 22)

Usage:
  p10_mm_dimension.py                     full registered grid ->
                                          scripts/experiments/p10_results.json
  p10_mm_dimension.py --mutant shuffled-order   restrict variants
  p10_mm_dimension.py --quick             small smoke grid (no JSON)

stdlib only; fixed seed 20260824; deterministic given the seed.
"""
import json
import math
import random
import statistics
import sys
import time
from math import lgamma, sqrt

SEED = 20260824
DATE = "2026-08-24"
N_GRID = [128, 256, 512, 1024, 2048, 4096, 8192]
M_SCHED = {128: 40, 256: 40, 512: 40, 1024: 40, 2048: 24, 4096: 16, 8192: 12}

# Constants from p10_symbolic.py (registered; EQ ids in parentheses).
F_EXACT = {2: 0.5, 3: 8.0 / 35.0, 4: 0.1}          # EQ 6-14
EG2 = {2: 5.0 / 18.0, 3: 0.0742857144, 4: 0.02}    # EQ 19-21
DSTAR = {3: 3.0804, 4: 4.2296}                     # EQ 26-27
CD = {2: 0.5, 3: math.pi / 12.0, 4: math.pi / 24.0}  # EQ 1-3
SD_WINDOW = (0.4, 2.2)                             # registered expects (2)
MUTANT_TOL = 0.3                                   # registered expects (4)


def F(d):
    return 0.5 * math.exp(lgamma(d + 1) + lgamma(d / 2) - lgamma(1.5 * d))


def dF(d, h=1e-6):
    return (F(d + h) - F(d - h)) / (2 * h)


def d2F(d, h=1e-4):
    return (F(d + h) - 2 * F(d) + F(d - h)) / (h * h)


def invert(fv, lo=1.0, hi=24.0):
    if fv >= F(lo):
        return lo
    if fv <= F(hi):
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if F(mid) > fv:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def band_params(d, N, M):
    """Registered band: |mean_M d_hat - d| <= |bias| + 4 sigma_d/sqrt(M)."""
    f = F_EXACT[d]
    k2 = EG2[d] - f * f
    C2 = N * (N - 1) // 2
    C3 = N * (N - 1) * (N - 2) // 6
    var_f = (C2 * f * (1 - f) + 6 * C3 * k2) / C2 ** 2
    fp = dF(d)
    sigma_d = sqrt(var_f) / abs(fp)
    bias = -d2F(d) * var_f / (2 * fp ** 3)
    return sigma_d, bias, abs(bias) + 4 * sigma_d / sqrt(M)


def sprinkle(d, N, rng):
    """Fixed-N uniform sample of the interval; accept-reject from the
    unit box. Returns (T, spatial coordinate lists, trials)."""
    D = d - 1
    u = rng.random
    T = []
    XS = [[] for _ in range(D)]
    trials = 0
    while len(T) < N:
        trials += 1
        t = u()
        xs = [u() - 0.5 for _ in range(D)]
        r2 = 0.0
        for x in xs:
            r2 += x * x
        m = t if t < 0.5 else 1.0 - t
        if r2 < m * m:
            T.append(t)
            for k in range(D):
                XS[k].append(xs[k])
    return T, XS, trials


def count_related(T, XS):
    """Causally related unordered pairs: dt > |dx|, brute force over
    the t-sorted points."""
    n = len(T)
    order = sorted(range(n), key=T.__getitem__)
    t = [T[i] for i in order]
    cols = [[c[i] for i in order] for c in XS]
    cnt = 0
    if len(cols) == 1:
        x = cols[0]
        for i in range(n - 1):
            ti = t[i]
            xi = x[i]
            for j in range(i + 1, n):
                dt = t[j] - ti
                dx = x[j] - xi
                if dt * dt > dx * dx:
                    cnt += 1
    elif len(cols) == 2:
        x, y = cols
        for i in range(n - 1):
            ti = t[i]
            xi = x[i]
            yi = y[i]
            for j in range(i + 1, n):
                dt = t[j] - ti
                dx = x[j] - xi
                dy = y[j] - yi
                if dt * dt > dx * dx + dy * dy:
                    cnt += 1
    else:
        x, y, z = cols
        for i in range(n - 1):
            ti = t[i]
            xi = x[i]
            yi = y[i]
            zi = z[i]
            for j in range(i + 1, n):
                dt = t[j] - ti
                dx = x[j] - xi
                dy = y[j] - yi
                dz = z[j] - zi
                if dt * dt > dx * dx + dy * dy + dz * dz:
                    cnt += 1
    return cnt


def apply_mutant(d, T, XS, mutant, rng):
    if mutant == "none":
        return T, XS
    if mutant == "shuffled-order":
        T2 = T[:]
        rng.shuffle(T2)
        return T2, XS
    if mutant == "shuffled-lightcone":
        if d != 2:
            raise ValueError("shuffled-lightcone is a d=2 variant")
        x = XS[0]
        u = [T[i] - x[i] for i in range(len(T))]
        v = [T[i] + x[i] for i in range(len(T))]
        rng.shuffle(v)
        T2 = [0.5 * (u[i] + v[i]) for i in range(len(T))]
        X2 = [0.5 * (v[i] - u[i]) for i in range(len(T))]
        return T2, [X2]
    raise ValueError(f"unknown mutant {mutant!r}")


def variants_for(d, restrict):
    vs = ["none", "shuffled-order"]
    if d == 2:
        vs.append("shuffled-lightcone")
    if restrict != "all":
        vs = [v for v in vs if v == restrict]
    return vs


def main() -> int:
    restrict = "all"
    quick = False
    args = sys.argv[1:]
    if "--mutant" in args:
        restrict = args[args.index("--mutant") + 1]
        known = {"none", "shuffled-order", "shuffled-lightcone"}
        if restrict not in known:
            print(f"usage error: unknown mutant {restrict!r}; known: {sorted(known)}")
            return 2
    if "--quick" in args:
        quick = True
    n_grid = [128, 256] if quick else N_GRID
    m_sched = {n: 6 for n in n_grid} if quick else M_SCHED

    t0 = time.time()
    cells = []
    for d in (2, 3, 4):
        for N in n_grid:
            M = m_sched[N]
            variants = variants_for(d, restrict)
            if not variants:
                continue
            per = {v: {"dhats": [], "fobs": []} for v in variants}
            acc_n = acc_tr = 0
            C2 = N * (N - 1) / 2.0
            for run in range(M):
                srng = random.Random(f"{SEED}:{d}:{N}:sample:{run}")
                T, XS, trials = sprinkle(d, N, srng)
                acc_n += N
                acc_tr += trials
                for v in variants:
                    mrng = random.Random(f"{SEED}:{d}:{N}:{v}:{run}")
                    T2, XS2 = apply_mutant(d, T, XS, v, mrng)
                    R = count_related(T2, XS2)
                    fo = R / C2
                    per[v]["fobs"].append(fo)
                    per[v]["dhats"].append(invert(fo))
            rate = acc_n / acc_tr
            p = CD[d]
            acc_tol = 4 * sqrt(p * (1 - p) / acc_tr)
            acc_ok = abs(rate - p) <= acc_tol
            sigma_d, bias, band = band_params(d, N, M)
            for v in variants:
                dh = per[v]["dhats"]
                mean = statistics.fmean(dh)
                sd = statistics.stdev(dh) if len(dh) > 1 else 0.0
                cells.append({
                    "d": d, "N": N, "M": M, "mutant": v,
                    "f_mean": statistics.fmean(per[v]["fobs"]),
                    "dhat_mean": mean, "dhat_sd": sd, "dhats": dh,
                    "sigma_d_pred": sigma_d, "bias_pred": bias,
                    "band": band, "err": mean - d,
                    "in_band": abs(mean - d) <= band,
                    "sd_ratio": (sd / sigma_d) if sigma_d else None,
                    "acceptance_rate": rate,
                    "acceptance_expected": p,
                    "acceptance_ok": acc_ok,
                })
                print(f"d={d} N={N:5d} M={M:2d} {v:18s} "
                      f"mean={mean:.4f} sd={sd:.4f} err={mean - d:+.4f} "
                      f"band={band:.4f} in_band={abs(mean - d) <= band} "
                      f"sd_ratio={sd / sigma_d:.2f} acc_ok={acc_ok} "
                      f"[{time.time() - t0:.0f}s]", flush=True)

    # ---- registered expectations, evaluated mechanically ----
    def cell(d, N, v):
        for c in cells:
            if c["d"] == d and c["N"] == N and c["mutant"] == v:
                return c
        return None

    summary = {}
    if restrict == "all" and not quick:
        nulls = [c for c in cells if c["mutant"] == "none"]
        e1_fail = [(c["d"], c["N"]) for c in nulls if not c["in_band"]]
        e2_fail = [(c["d"], c["N"]) for c in nulls
                   if not (SD_WINDOW[0] <= c["sd_ratio"] <= SD_WINDOW[1])]
        e3_sd = all(cell(d, 8192, "none")["dhat_sd"]
                    < cell(d, 128, "none")["dhat_sd"] for d in (2, 3, 4))
        rms = {N: sqrt(statistics.fmean(
            [cell(d, N, "none")["err"] ** 2 for d in (2, 3, 4)]))
            for N in (128, 8192)}
        e3_rms = rms[8192] < rms[128]
        # (4) mutant: outside band for d=4 all N, d=3 N>=256; near d*.
        mut34 = [c for c in cells if c["mutant"] == "shuffled-order"
                 and c["d"] in (3, 4)]
        e4_outside_fail = [(c["d"], c["N"]) for c in mut34
                           if (c["d"] == 4 or c["N"] >= 256) and c["in_band"]]
        e4_dstar_fail = [(c["d"], c["N"]) for c in mut34
                         if abs(c["dhat_mean"] - DSTAR[c["d"]]) > MUTANT_TOL]
        mut2 = [c for c in cells if c["d"] == 2 and c["mutant"] != "none"]
        e4_d2_fail = [(c["mutant"], c["N"]) for c in mut2 if not c["in_band"]]
        acc_fail = [(c["d"], c["N"]) for c in cells if not c["acceptance_ok"]]
        summary = {
            "e1_all_null_cells_in_band": not e1_fail,
            "e1_failures": e1_fail,
            "e2_sd_ratio_in_window": not e2_fail,
            "e2_failures": e2_fail,
            "e3_sd_shrinks_per_d": e3_sd,
            "e3_rms_err": {str(k): v for k, v in rms.items()},
            "e3_rms_shrinks": e3_rms,
            "e4_mutant_outside_bands_d3ge256_d4": not e4_outside_fail,
            "e4_outside_failures": e4_outside_fail,
            "e4_mutant_near_dstar": not e4_dstar_fail,
            "e4_dstar_failures": e4_dstar_fail,
            "e4_d2_mutants_stay_in_band": not e4_d2_fail,
            "e4_d2_failures": e4_d2_fail,
            "acceptance_all_ok": not acc_fail,
            "acceptance_failures": acc_fail,
        }
        print("expects summary:", json.dumps(summary, indent=1), flush=True)
        out = {
            "prediction": "P-10", "seed": SEED, "date": DATE,
            "n_grid": N_GRID, "m_sched": {str(k): v for k, v in M_SCHED.items()},
            "constants": {
                "f_exact": {str(k): v for k, v in F_EXACT.items()},
                "Eg2": {str(k): v for k, v in EG2.items()},
                "dstar": {str(k): v for k, v in DSTAR.items()},
                "volume_fraction": {str(k): v for k, v in CD.items()},
                "sd_window": SD_WINDOW, "mutant_tol": MUTANT_TOL,
            },
            "expects_summary": summary,
            "cells": cells,
            "elapsed_s": round(time.time() - t0, 1),
        }
        path = "scripts/experiments/p10_results.json"
        with open(path, "w") as fh:
            json.dump(out, fh, indent=1)
        print(f"wrote {path} ({time.time() - t0:.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
