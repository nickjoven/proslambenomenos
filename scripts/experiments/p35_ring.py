#!/usr/bin/env python3
"""P-35 registered cells: sector-slip onset on the free pi ring
under a soft-ramped dead load. Protocol and clause bands fixed in
notes/p35_free_ring.md and PREDICTIONS.md P-35 BEFORE this ran.

Per configuration {control, twist n=0, twist n=1} x N (and gamma
variants at N = 64): scan the derived f grid upward from
fold - 0.10 in steps of 0.005; each level is an independent run
(ground-state init, linear ramp over T_ramp = 200, hold
T_meas = 500); onset f* = first level whose held segment changes
the covariant winding. Observables: f*, W at every sample (sector
arithmetic), the 1/8-grid spectral address pre-onset, slip-gap
min/median/max at the onset level. Integrator: Euler-Cromer,
dt = 0.02; declared validation cell = N 64 control at dt/2.

Run: python3 scripts/experiments/p35_ring.py [--quick]
"""
import json
import math
import os
import sys

TAU = 2 * math.pi


def wrap(x):
    return (x + math.pi) % TAU - math.pi


def fold_fc(N, total):
    def sum_s(c, f):
        s = 0.0
        for m in range(N):
            x = c + m * f / N
            if x <= -1.0 or x >= 1.0:
                return None
            s += math.asin(x)
        return s

    def has_root(f):
        lo, hi = -0.999999, 1.0 - (N - 1) * f / N - 1e-12
        if hi <= lo:
            return False
        slo, shi = sum_s(lo, f), sum_s(hi, f)
        if slo is None or shi is None:
            return False
        return (slo - total) * (shi - total) <= 0

    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if has_root(mid):
            lo = mid
        else:
            hi = mid
    return lo


def ground_state(N, twisted, sector):
    A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
    delta = ((2 * sector - 1) * math.pi / N) if twisted else 0.0
    th, acc = [], 0.0
    for j in range(N):
        th.append(acc)
        acc += delta + A[j]
    return A, th


def winding(th, A, N):
    return sum(wrap(th[(j + 1) % N] - th[j] - A[j])
               for j in range(N)) / TAU


def address(th, N):
    """1/8-grid fractional DFT peak index of e^{i theta}."""
    best, bidx = -1.0, None
    for kk in [x / 8.0 for x in range(-16, 17)]:
        re = sum(math.cos(th[j] - TAU * kk * j / N) for j in range(N))
        im = sum(math.sin(th[j] - TAU * kk * j / N) for j in range(N))
        a = math.hypot(re, im)
        if a > best:
            best, bidx = a, kk
    return bidx


def run_level(N, twisted, sector, gamma, f_target, dt,
              t_ramp=200.0, t_meas=500.0):
    """One independent run. Returns dict with slip flag, first
    slip time, W samples (as sector-arithmetic checks), address
    samples pre-onset, slip times in the held window."""
    A, th = ground_state(N, twisted, sector)
    w = [0.0] * N
    b = N // 2
    W0 = winding(th, A, N)
    n_ramp = int(t_ramp / dt)
    n_meas = int(t_meas / dt)
    sample_every = max(1, int(1.0 / dt))
    addr_every = 25 * sample_every
    worst_sector = 0.0
    addr_bad = 0
    addr_n = 0
    slips = []
    Wlast = W0
    target_addr = (sector - 0.5) if twisted else 0.0
    for s in range(n_ramp + n_meas):
        f = f_target * min(1.0, (s + 1) / n_ramp)
        for j in range(N):
            Dr = th[(j + 1) % N] - th[j] - A[j]
            Dl = th[j] - th[j - 1] - A[j - 1]
            acc = (math.sin(Dr) - math.sin(Dl) - gamma * w[j]
                   + (f if j == b else 0.0))
            w[j] += dt * acc
        for j in range(N):
            th[j] += dt * w[j]
        if (s + 1) % sample_every == 0:
            W = winding(th, A, N)
            if not slips:
                # sector arithmetic between events: W sits on the
                # half-integer (twisted) / integer (control) lattice
                off = (abs(W - (round(W - 0.5) + 0.5)) if twisted
                       else abs(W - round(W)))
                worst_sector = max(worst_sector, off)
            if abs(W - Wlast) > 0.6:
                slips.append((s + 1) * dt)
                Wlast = W
            if (s + 1) % addr_every == 0 and not slips:
                addr_n += 1
                if abs(address(th, N) - target_addr) > 1e-9:
                    addr_bad += 1
        if slips and (s + 1) * dt > slips[0] + 120.0:
            break  # enough gap statistics collected
    gaps = [t2 - t1 for t1, t2 in zip(slips, slips[1:])]
    # settled post-slip sector arithmetic: integer slips preserve
    # the half-integer offset
    post_off = None
    if slips:
        W = winding(th, A, N)
        post_off = (abs(W - (round(W - 0.5) + 0.5)) if twisted
                    else abs(W - round(W)))
    return {"slip": bool(slips), "first_slip_t": slips[0] if slips
            else None, "worst_sector_off": worst_sector,
            "post_slip_off": post_off,
            "addr_samples": addr_n, "addr_bad": addr_bad,
            "gaps_min_med_max": [min(gaps), sorted(gaps)[len(gaps)//2],
                                 max(gaps)] if gaps else None,
            "n_slips": len(slips)}


def onset_scan(N, twisted, sector, gamma, dt=0.02):
    total = ((2 * sector - 1) * math.pi) if twisted else 0.0
    fold = fold_fc(N, total)
    grid0 = fold - 0.10
    onset, detail = None, None
    lev = 0
    while grid0 + 0.005 * lev <= fold + 0.06 + 1e-9:
        f = grid0 + 0.005 * lev
        r = run_level(N, twisted, sector, gamma, f, dt)
        if r["slip"]:
            onset, detail = f, r
            break
        detail = r
        lev += 1
    return {"fold": fold, "onset": onset, "detail": detail}


def main():
    quick = "--quick" in sys.argv
    dt = 0.02
    cells = []
    Ns = [64] if quick else [64, 96, 128]
    for N in Ns:
        for tag, tw, sec in (("control", False, 0),
                             ("twist0", True, 0), ("twist1", True, 1)):
            cells.append((tag, N, tw, sec, 0.02))
    if not quick:
        for g in (0.01, 0.04):
            for tag, tw, sec in (("control", False, 0),
                                 ("twist0", True, 0),
                                 ("twist1", True, 1)):
                cells.append((tag, 64, tw, sec, g))
    out = {"cells": {}}
    for tag, N, tw, sec, g in cells:
        key = "%s_N%d_g%g" % (tag, N, g)
        r = onset_scan(N, tw, sec, g, dt)
        out["cells"][key] = r
        print(key, "fold %.4f onset %s" % (r["fold"], r["onset"]),
              "sector_off %.2e" % r["detail"]["worst_sector_off"],
              "addr %d/%d bad" % (r["detail"]["addr_bad"],
                                  r["detail"]["addr_samples"]),
              flush=True)
    # validation cell: dt/2 at N=64 control
    v = onset_scan(64, False, 0, 0.02, dt / 2)
    out["validation_dt_half"] = {"onset": v["onset"], "fold": v["fold"]}
    print("validation dt/2: onset", v["onset"])

    # clause evaluation (gamma = 0.02 cells)
    ev = {}
    for N in Ns:
        c = out["cells"]["control_N%d_g0.02" % N]["onset"]
        t0 = out["cells"]["twist0_N%d_g0.02" % N]["onset"]
        t1 = out["cells"]["twist1_N%d_g0.02" % N]["onset"]
        if None in (c, t0, t1):
            ev[str(N)] = {"incomplete": True}
            continue
        split = abs(t1 - t0)
        fold_c = out["cells"]["control_N%d_g0.02" % N]["fold"]
        fold_t = out["cells"]["twist1_N%d_g0.02" % N]["fold"]
        fr = fold_t / fold_c
        band = 2 * 0.005 / fold_c + max(split, 0.005) / fold_c + 1e-4
        ratio = 0.5 * (t0 + t1) / c
        ev[str(N)] = {"ratio": ratio, "fold_ratio": fr, "band": band,
                      "b_holds": abs(ratio - fr) <= band,
                      "split": split, "c_holds": split <= 0.005 + 1e-9}
    out["clauses"] = ev
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p35_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(ev, indent=1))


if __name__ == "__main__":
    main()
