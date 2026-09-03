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


if __name__ == "__main__" and "--second" not in sys.argv:
    main()


# ---------------------------------------------------------------------
# The layer's second pass (after the accounting above): the late-window
# instrument, the decay ladder, the smear identity, the derived floors,
# and the mutants. Everything the P-49 clauses depend on is measured
# here and written to p49_derive.json.
#
# FLOORS (8a), all from the run: (i) the 2-Omega self floor of the
# lock-in, A_d/(Omega T); (ii) the describing-function stiffness
# correction of a sine bond driven at strain amplitude delta: the
# fundamental of sin(D_0 + delta cos) is cos(D_0) (2 J_1(delta)/delta)
# delta = c (1 - delta^2/8 + ...) delta, so the linear root's band is
# widened to [w(c (1 - delta^2/8)), w(c)] with delta = |x_1 - x_2| at
# the drive frequency, A_1 |1 - w|/Omega; (iii) the slow content that
# survives (period-mean rms) enters only through the smear.
# THE SMEAR IDENTITY: the rotor-phase lock-in of a site's drive-locked
# fundamental is that fundamental times <e^{-i x_1}> (x_1 the
# neighbour's displacement about its window mean), so
# |A_1(rotor)/A_1(bond) - |<e^{-i x_1}>|| <= (|slow| + |rest| phasors of
# the rotor reading)/A_1(bond) + the self floor - a triangle inequality,
# exact.
# ---------------------------------------------------------------------

def bessel_j1_over_x(x):
    """2 J_1(x)/x by series (x < 2 here)."""
    s, term, k = 1.0, 1.0, 0
    x2 = (x / 2.0) ** 2
    while k < 30:
        k += 1
        term *= -x2 / (k * (k + 1))
        s += term
        if abs(term) < 1e-17:
            break
    return s


def cell_readout(gamma, f, dt, win, mutant=None):
    rec = record_window(gamma, f, dt, win)
    r = analyse(rec, gamma, dt)
    n = r["n"]
    T = n * dt
    Om = r["Omega"]
    s1, s2, s3 = r["sites"]["1"], r["sites"]["2"], r["sites"]["3"]
    A1, A2, A3 = s1["fund_amp"], s2["fund_amp"], s3["fund_amp"]
    # the strain amplitude at the drive frequency across bond b+1
    w_mid = evanescent(Om, 0.5 * (r["cmin"] + r["cmax"]), gamma, dt)[0]
    delta = A1 * abs(1.0 - w_mid) / Om
    df = bessel_j1_over_x(delta)              # 1 - delta^2/8 + ...
    cs = (r["cmin"] * df, r["cmax"])
    if mutant == "band-blind":
        ws = [1.0 / Om, 1.0 / Om]
        A1s = [evanescent(Om, c, gamma, dt)[1] for c in cs]
    else:
        ws = [abs(evanescent(Om, c, gamma, dt)[0]) for c in cs]
        A1s = [evanescent(Om, c, gamma, dt)[1] for c in cs]
    self2 = A2 / (Om * T)
    self1 = A1 / (Om * T)
    ratio = A2 / A1
    fl_ratio = (self2 + ratio * self1) / A1
    out = {"gamma": gamma, "window": list(win), "event_t": rec["event_t"], "Omega": Om, "T": T,
           "cmin": r["cmin"], "cmax": r["cmax"], "delta": delta, "describing_factor": df,
           "x1_rms": r["x1_rms"], "slow2_rms": s2["slow_rms"],
           "A1": A1, "A2": A2, "A3": A3, "ratio21": ratio, "ratio32": A3 / A2,
           "w_band": [min(ws), max(ws)], "A1_band": [min(A1s), max(A1s)],
           "self_floor_ratio": fl_ratio, "self_floor_A1": self1,
           "ratio21_in_band": min(ws) - fl_ratio <= ratio <= max(ws) + fl_ratio,
           "ratio21_over_top": ratio / max(ws) - 1.0,
           "A1_in_band": min(A1s) - self1 <= A1 <= max(A1s) + self1,
           "A1_rel_to_top": A1 / max(A1s) - 1.0}
    # the smear identity at site 1
    rot = s1["rotor"]
    pred = r["smear_pred_rotor"]
    if mutant == "smear-blind":
        pred = 1.0
    meas = rot["total"] / s1["bond"]["total"]
    leak = (2.0 * abs(complex(*rot["phasors"]["slow"])) + 2.0 * abs(complex(*rot["phasors"]["rest"]))) / s1["bond"]["total"]
    out["smear"] = {"measured": meas, "predicted": pred, "tolerance": leak + self1 / A1,
                    "holds": abs(meas - pred) <= leak + self1 / A1}
    return out


def second_pass():
    fold = fold_fc(N, -math.pi)
    f = fold + 0.005
    dt = 0.001
    out = {"f": f, "dt": dt}
    t0 = time.time()
    # late-window cells above and in the band
    late = {}
    for gamma in (0.35, 0.5, 0.8, 1.0):
        c = cell_readout(gamma, f, dt, (300.0, 380.0))
        late["gamma_%g" % gamma] = c
        print("late gamma %g: Om %.3f delta %.3f (df %.4f) | ratio21 %.4e band [%.4e, %.4e] floor %.1e in %s (%+.2f%% vs top) | A1 %.4e band [%.4e, %.4e] in %s (%+.2f%%) | smear meas %.4f pred %.4f tol %.4f holds %s | ratio32 %.4e (%.0f s)"
              % (gamma, c["Omega"], c["delta"], c["describing_factor"], c["ratio21"], *c["w_band"], c["self_floor_ratio"], c["ratio21_in_band"], 100 * c["ratio21_over_top"],
                 c["A1"], *c["A1_band"], c["A1_in_band"], 100 * c["A1_rel_to_top"], c["smear"]["measured"], c["smear"]["predicted"], c["smear"]["tolerance"], c["smear"]["holds"], c["ratio32"], time.time() - t0), flush=True)
    out["late"] = late
    # the decay ladder at gamma 0.5
    dec = []
    for w0 in (30.0, 80.0, 130.0, 180.0, 230.0, 300.0):
        c = cell_readout(0.5, f, dt, (w0, w0 + 50.0))
        dec.append(c)
        print("decay gamma 0.5 window [%g, %g]: x1 rms %.3f slow2 %.2e | excess %+.2f%% (floor %.2f%%) | A1 %+.2f%% | smear meas %.4f pred %.4f tol %.4f holds %s"
              % (w0, w0 + 50, c["x1_rms"], c["slow2_rms"], 100 * c["ratio21_over_top"], 100 * c["self_floor_ratio"] / max(c["w_band"]), 100 * c["A1_rel_to_top"],
                 c["smear"]["measured"], c["smear"]["predicted"], c["smear"]["tolerance"], c["smear"]["holds"]), flush=True)
    out["decay"] = dec
    # mutants on one cell each (L-8)
    muts = {}
    c = cell_readout(0.5, f, dt, (30.0, 80.0), mutant="smear-blind")
    muts["smear-blind"] = {"holds": c["smear"]["holds"], "measured": c["smear"]["measured"], "predicted": c["smear"]["predicted"], "tolerance": c["smear"]["tolerance"]}
    c = cell_readout(1.0, f, dt, (300.0, 380.0), mutant="band-blind")
    muts["band-blind"] = {"ratio21_in_band": c["ratio21_in_band"], "ratio21": c["ratio21"], "band": c["w_band"]}
    print("mutants:", json.dumps(muts), flush=True)
    out["mutants"] = muts
    out["seconds"] = time.time() - t0
    with open(os.path.join(HERE, "p49_derive.json"), "r") as fh:
        prev = json.load(fh)
    prev["second_pass"] = out
    with open(os.path.join(HERE, "p49_derive.json"), "w") as fh:
        json.dump(prev, fh, indent=1)
    print("second pass written in %.0f s" % out["seconds"])


if __name__ == "__main__" and "--second" in sys.argv:
    second_pass()
