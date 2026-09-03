#!/usr/bin/env python3
"""P-49 derive layer (A-29): the near-band reference excess, taken
apart exactly. P-48 read the slip footprint's offset-2 ratio 4 to 27
percent above the evanescent-root band when demodulated against the
bond phase theta_b - theta_{b+1}, and inside the band against the
rotor phase theta_b, along gamma 0.2 to 0.8 (rotor at Omega 9.8 to
2.35). The first-order mixing estimate (X/2) v_slow covered a third.
Here the accounting is exact: the ring is run again at each gamma
with the full time series at sites b .. b+3 recorded over the P-48
window, each site's velocity is split into (i) its fundamental
locked to the DRIVE phase (the bond phase, since the force on b+1 is
-sin D_b), (ii) its slow part (running mean over one rotor period),
(iii) the remainder (harmonics, transients), and each reference
demodulates each component separately. The reading of a reference
is the sum of its readings of the components; the component that
carries the excess is the mechanism.

Run: python3 scripts/experiments/p49_derive.py
"""
import cmath
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc, ground_state  # noqa: E402
from p46_derive import evanescent  # noqa: E402
from p48_derive import WIN  # noqa: E402

N = 64
B = N // 2
SITES = (0, 1, 2, 3)


def record_window(gamma, f, dt, win, t_ramp=200.0, t_cap=1500.0):
    """Euler-Cromer in the P-36 order; the P-36 event; then theta and
    v at sites b..b+3 at every step over the window (Delta in win)."""
    A, th = ground_state(N, True, 0)
    v = [0.0] * N
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    sinD = [math.sin(x) for x in D0]
    n_ramp = int(round(t_ramp / dt))
    per_unit = int(round(1.0 / dt))
    event = None
    n_total = int(round(t_cap / dt))
    TH, V = [], []
    cmin, cmax = 1.0, -1.0
    s = 0
    while s < n_total:
        fnow = f * min(1.0, (s + 1) / n_ramp)
        for j in range(N):
            v[j] += dt * (sinD[j] - sinD[j - 1] - gamma * v[j] + (fnow if j == B else 0.0))
        for j in range(N):
            th[j] += dt * v[j]
        sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        s += 1
        if event is None:
            if s % per_unit == 0:
                D = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
                if max(abs(D[j] - D0[j]) for j in range(N)) > 1.5 * math.pi:
                    event = s
                    n_total = s + int(round(win[1] / dt)) + 1
            continue
        Delta = (s - event) * dt
        if win[0] <= Delta < win[1]:
            TH.append([th[(B + d) % N] for d in SITES])
            V.append([v[(B + d) % N] for d in SITES])
            if s % per_unit == 0:
                for j in range(N):
                    if min(abs(j - B), N - abs(j - B)) >= 1 and j != B - 1:
                        c = math.cos(th[(j + 1) % N] - th[j] - A[j])
                        cmin, cmax = min(cmin, c), max(cmax, c)
    return {"event_t": event * dt if event else None, "TH": TH, "V": V, "cmin": cmin, "cmax": cmax}


def lockin(series, ref):
    n = len(series)
    return 2.0 * abs(sum(x * cmath.exp(-1j * r) for x, r in zip(series, ref))) / n


def decompose(series, ref_b, per):
    """series = a cos(ref_b) + b sin(ref_b) [the drive-locked
    fundamental, least squares] + slow [running mean over one period
    of the remainder] + rest."""
    n = len(series)
    c = [math.cos(r) for r in ref_b]
    s_ = [math.sin(r) for r in ref_b]
    # least squares on the two carriers (they are nearly orthogonal over
    # many periods; solve the 2x2 normal equations exactly)
    cc = sum(x * x for x in c)
    ss = sum(x * x for x in s_)
    cs = sum(x * y for x, y in zip(c, s_))
    yc = sum(x * y for x, y in zip(series, c))
    ys = sum(x * y for x, y in zip(series, s_))
    det = cc * ss - cs * cs
    a = (yc * ss - ys * cs) / det
    b = (ys * cc - yc * cs) / det
    fund = [a * x + b * y for x, y in zip(c, s_)]
    rem = [x - y for x, y in zip(series, fund)]
    half = per // 2
    slow = []
    for k in range(n):
        lo, hi = max(0, k - half), min(n, k + half + 1)
        slow.append(sum(rem[lo:hi]) / (hi - lo))
    rest = [x - y for x, y in zip(rem, slow)]
    return {"amp": math.hypot(a, b), "fund": fund, "slow": slow, "rest": rest}


def analyse(rec, gamma, dt):
    TH, V = rec["TH"], rec["V"]
    n = len(V)
    ref_r = [row[0] for row in TH]                    # rotor phase
    ref_b = [row[0] - row[1] for row in TH]           # bond phase theta_b - theta_{b+1}
    Om = (ref_r[-1] - ref_r[0]) / ((n - 1) * dt)
    per = max(1, int(round(2 * math.pi / Om / dt)))
    out = {"gamma": gamma, "n": n, "Omega": Om, "cmin": rec["cmin"], "cmax": rec["cmax"]}
    ws = [abs(evanescent(Om, c, gamma, dt)[0]) for c in (rec["cmin"], rec["cmax"])]
    out["w_band"] = [min(ws), max(ws)]
    x1 = [row[1] for row in TH]
    x1_mean = sum(x1) / n
    x1_dev = [x - x1_mean for x in x1]
    out["x1_rms"] = math.sqrt(sum(x * x for x in x1_dev) / n)
    out["smear_pred_rotor"] = abs(sum(cmath.exp(1j * x) for x in x1_dev)) / n
    per_site = {}
    for d in (1, 2, 3):
        ser = [row[d] for row in V]
        dec = decompose(ser, ref_b, per)
        rec_d = {"fund_amp": dec["amp"],
                 "slow_rms": math.sqrt(sum(x * x for x in dec["slow"]) / n),
                 "rest_rms": math.sqrt(sum(x * x for x in dec["rest"]) / n)}
        for name, ref in (("bond", ref_b), ("rotor", ref_r)):
            rec_d[name] = {"total": lockin(ser, ref),
                           "fund": lockin(dec["fund"], ref),
                           "slow": lockin(dec["slow"], ref),
                           "rest": lockin(dec["rest"], ref)}
            # the complex pieces, so the sum can be checked
            z = {k: sum(x * cmath.exp(-1j * r) for x, r in zip(comp, ref)) / n
                 for k, comp in (("fund", dec["fund"]), ("slow", dec["slow"]), ("rest", dec["rest"]))}
            rec_d[name]["phasors"] = {k: [zz.real, zz.imag] for k, zz in z.items()}
            rec_d[name]["sum_check"] = 2.0 * abs(sum(z.values()))
        per_site[str(d)] = rec_d
    out["sites"] = per_site
    for name in ("bond", "rotor"):
        r21 = per_site["2"][name]["total"] / per_site["1"][name]["total"]
        out["ratio21_" + name] = r21
        out["ratio21_%s_over_top" % name] = r21 / max(ws) - 1.0
    out["ratio21_fund_only"] = per_site["2"]["fund_amp"] / per_site["1"]["fund_amp"]
    out["ratio21_fund_over_top"] = out["ratio21_fund_only"] / max(ws) - 1.0
    return out


def main():
    t0 = time.time()
    fold = fold_fc(N, -math.pi)
    f = fold + 0.005
    dt = 0.001
    out = {"N": N, "f": f, "dt": dt, "cells": {}}
    for gamma in (0.2, 0.35, 0.5, 0.8):
        t1 = time.time()
        rec = record_window(gamma, f, dt, WIN[gamma])
        res = analyse(rec, gamma, dt)
        res["event_t"] = rec["event_t"]
        res["seconds"] = time.time() - t1
        out["cells"]["gamma_%g" % gamma] = res
        s1, s2 = res["sites"]["1"], res["sites"]["2"]
        print("gamma %g: Omega %.3f |w| band [%.4e, %.4e]; x1 rms %.3f, predicted rotor smear %.3f" % (gamma, res["Omega"], *res["w_band"], res["x1_rms"], res["smear_pred_rotor"]))
        print("   ratio21: bond %.4e (%+.1f%% vs top) rotor %.4e (%+.1f%%) fundamental-only %.4e (%+.1f%%)"
              % (res["ratio21_bond"], 100 * res["ratio21_bond_over_top"], res["ratio21_rotor"], 100 * res["ratio21_rotor_over_top"],
                 res["ratio21_fund_only"], 100 * res["ratio21_fund_over_top"]))
        for d in ("1", "2"):
            sd = res["sites"][d]
            print("   site %s: fund amp %.4e slow rms %.2e rest rms %.2e | bond reads total %.4e = fund %.4e + slow %.4e + rest %.4e (sum %.4e) | rotor reads total %.4e = fund %.4e + slow %.4e + rest %.4e"
                  % (d, sd["fund_amp"], sd["slow_rms"], sd["rest_rms"],
                     sd["bond"]["total"], sd["bond"]["fund"], sd["bond"]["slow"], sd["bond"]["rest"], sd["bond"]["sum_check"],
                     sd["rotor"]["total"], sd["rotor"]["fund"], sd["rotor"]["slow"], sd["rotor"]["rest"]), flush=True)
    out["seconds"] = time.time() - t0
    with open(os.path.join(HERE, "p49_derive.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote p49_derive.json in %.0f s" % out["seconds"])


if __name__ == "__main__":
    main()
