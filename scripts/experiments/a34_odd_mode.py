#!/usr/bin/env python3
"""a34_odd_mode.py - A-34: the odd slow mode of the post-slip operator.

After the slip the rotor's bonds average to zero on slow timescales, so
the other N - 1 sites are an open chain with free ends. Its modes are
omega_k = 2 sqrt(c) sin(pi k / (2 (N - 1))); k odd is odd about the
rotor (a node at the antipode, a free end at the rotor), k even is
even. The ring's k = 1 used in LC-38, L-16, R-47b and R-48a is the open
chain's even k = 2; the open chain's odd k = 1 sits at half that
frequency and, overdamped, decays about four times slower. In sector
zero the drive is even, so the odd channel is expected at its floor.

One run per P-49 cell (gamma 0.35 / 0.5 / 0.8 / 1.0; sector 0, N = 64,
f = fold + 0.005, ramp 200, dt = 0.001), the registered integrator of
p49_derive.record_window, recording theta and v at sites b, b+-1, b+-2
at every step from the event to Delta = 380. Per window (the P-49
decay ladder plus the registered late window) and per site pair:
  slow_j(t)  = running mean over one rotor period of theta_j(t)
               (removes the drive-locked ripple and its harmonics)
  even(t)    = (slow_{+j} + slow_{-j}) / 2,  odd(t) = (slow_{+j} - slow_{-j}) / 2
  rms about the window mean, as P-49's x_1 rms is defined.
Also reported: the P-49 convention x_1 rms (theta_{b+1} about its
window mean, ripple included) with the ripple estimate A_1/(Omega sqrt 2)
from the drive-locked fundamental of v_{b+1}, and log-linear fitted
rates of even and odd rms over the ladder windows against the
open-chain predictions at c = 1 and at the window's cmin.
Derive layer, not a registration. Output a34_odd_mode.json and .txt.
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc, ground_state  # noqa: E402
from p49_derive import decompose  # noqa: E402

N = 64
B = N // 2
OFFS = (0, 1, -1, 2, -2)
WINDOWS = [(30.0, 80.0), (80.0, 130.0), (130.0, 180.0), (180.0, 230.0), (230.0, 280.0), (300.0, 380.0)]
GAMMAS = (0.35, 0.5, 0.8, 1.0)


def rate_over(g, om):
    return g / 2 - math.sqrt(g * g / 4 - om * om) if g / 2 > om else g / 2


def om_open(k, c=1.0):
    return 2 * math.sqrt(c) * math.sin(math.pi * k / (2 * (N - 1)))


def run(gamma, f, dt, t_end):
    A, th = ground_state(N, True, 0)
    v = [0.0] * N
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    sinD = [math.sin(x) for x in D0]
    n_ramp = int(round(200.0 / dt)); per_unit = int(round(1.0 / dt))
    event = None; n_total = int(round(1500.0 / dt))
    TH, V, C = [], [], []
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
                    event = s; n_total = s + int(round(t_end / dt)) + 1
            continue
        TH.append([th[(B + d) % N] for d in OFFS])
        V.append([v[(B + d) % N] for d in OFFS])
        if s % per_unit == 0:
            cs = [math.cos(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)
                  if min(abs(j - B), N - abs(j - B)) >= 1 and j != B - 1]
            C.append((min(cs), max(cs)))
    return {"event_t": event * dt, "TH": TH, "V": V, "C": C}


def running_mean(x, half):
    n = len(x); out = [0.0] * n; acc = 0.0
    # O(n) sliding window
    lo = 0; hi = 0
    for k in range(n):
        while hi < min(n, k + half + 1):
            acc += x[hi]; hi += 1
        while lo < max(0, k - half):
            acc -= x[lo]; lo += 1
        out[k] = acc / (hi - lo)
    return out


def rms_about_mean(x):
    n = len(x); m = sum(x) / n
    return math.sqrt(sum((a - m) ** 2 for a in x) / n)


def fit_rate(pts):
    """log-linear fit of rms vs window midpoint; returns rate (positive = decay)."""
    if len(pts) < 2:
        return None
    xs = [p[0] for p in pts]; ys = [math.log(p[1]) for p in pts]
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    return -sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else None


def analyse(rec, gamma, dt, log):
    TH, V = rec["TH"], rec["V"]; n = len(TH)
    ref_r = [row[0] for row in TH]
    Om = (ref_r[-1] - ref_r[0]) / ((n - 1) * dt)
    per = max(1, int(round(2 * math.pi / Om / dt)))
    half = per // 2
    # slow displacement per site: running mean over one rotor period
    slow = {d: running_mean([row[i] for row in TH], half) for i, d in enumerate(OFFS)}
    out = {"gamma": gamma, "event_t": rec["event_t"], "Omega": Om, "windows": []}
    for (a, b_) in WINDOWS:
        lo, hi = int(round(a / dt)), int(round(b_ / dt))
        if hi > n:
            continue
        w = {"window": [a, b_]}
        ci = [rec["C"][k] for k in range(int(a), min(int(b_), len(rec["C"])))]
        w["cmin"] = min(c[0] for c in ci); w["cmax"] = max(c[1] for c in ci)
        for j in (1, 2):
            sp, sm = slow[j][lo:hi], slow[-j][lo:hi]
            ev = [0.5 * (p + m) for p, m in zip(sp, sm)]
            od = [0.5 * (p - m) for p, m in zip(sp, sm)]
            w["even_%d" % j] = rms_about_mean(ev)
            w["odd_%d" % j] = rms_about_mean(od)
            w["slow_plus_%d" % j] = rms_about_mean(sp)
            w["slow_minus_%d" % j] = rms_about_mean(sm)
        # P-49 convention and the ripple estimate
        x1 = [row[1] for row in TH[lo:hi]]
        w["x1_rms_p49"] = rms_about_mean(x1)
        ref_b = [row[0] - row[1] for row in TH[lo:hi]]
        dec = decompose([row[1] for row in V[lo:hi]], ref_b, per)
        w["A1_fund"] = dec["amp"]
        w["ripple_rms_pred"] = dec["amp"] / Om / math.sqrt(2.0)
        w["odd_over_even_1"] = w["odd_1"] / w["even_1"] if w["even_1"] else None
        out["windows"].append(w)
        log("  win [%3.0f,%3.0f]  x1 %.4f  ripple %.4f | even1 %.4e odd1 %.4e (odd/even %.3f) | even2 %.4e odd2 %.4e | c [%.3f, %.3f]"
            % (a, b_, w["x1_rms_p49"], w["ripple_rms_pred"], w["even_1"], w["odd_1"], w["odd_over_even_1"], w["even_2"], w["odd_2"], w["cmin"], w["cmax"]))
    # predictions and fits
    cmin_all = min(w["cmin"] for w in out["windows"])
    pred = {}
    for name, k in (("odd_k1", 1), ("even_k2", 2)):
        pred[name] = {"omega_c1": om_open(k), "rate_c1": rate_over(gamma, om_open(k)),
                      "omega_cmin": om_open(k, cmin_all), "rate_cmin": rate_over(gamma, om_open(k, cmin_all))}
    out["pred"] = pred
    ladder = [w for w in out["windows"] if w["window"][1] <= 280.0]
    fits = {}
    for ch in ("even_1", "odd_1", "even_2", "odd_2"):
        pts = [(0.5 * (w["window"][0] + w["window"][1]), w[ch]) for w in ladder if w[ch] > 0]
        fits[ch] = {"rate_all": fit_rate(pts), "rate_first3": fit_rate(pts[:3])}
    out["fits"] = fits
    log("  pred: odd k=1 rate %.4f (c=1) %.4f (cmin) | even k=2 rate %.4f (c=1) %.4f (cmin)"
        % (pred["odd_k1"]["rate_c1"], pred["odd_k1"]["rate_cmin"], pred["even_k2"]["rate_c1"], pred["even_k2"]["rate_cmin"]))
    log("  fits: even1 %s / first3 %s | odd1 %s / first3 %s"
        % tuple("%.4f" % x if x is not None else "-" for x in (fits["even_1"]["rate_all"], fits["even_1"]["rate_first3"], fits["odd_1"]["rate_all"], fits["odd_1"]["rate_first3"])))
    return out


def main():
    quick = "--quick" in sys.argv
    dt = 0.01 if quick else 0.001
    f = fold_fc(N, -math.pi) + 0.005
    t0 = time.time()
    lines = []
    def log(s):
        print(s, flush=True); lines.append(s)
    res = {"N": N, "f": f, "dt": dt, "windows": WINDOWS, "cells": {}}
    for g in GAMMAS:
        t1 = time.time()
        rec = run(g, f, dt, 380.0)
        log("gamma %g  event %.1f  (%.0f s)" % (g, rec["event_t"], time.time() - t1))
        res["cells"]["gamma_%g" % g] = analyse(rec, g, dt, log)
    res["seconds_total"] = time.time() - t0
    log("total %.0f s" % res["seconds_total"])
    name = "a34_odd_mode%s" % ("_quick" if quick else "")
    with open(os.path.join(HERE, name + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)
    with open(os.path.join(HERE, name + ".txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
