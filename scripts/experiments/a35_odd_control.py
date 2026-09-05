#!/usr/bin/env python3
"""a35_odd_control.py - A-35: what seeds the odd channel, and why its
decay does not depend on gamma.

A-34 read the slow part of (theta_{b+1} - theta_{b-1})/2 at a tenth of
the even channel at launch, decaying at 0.012 per unit at every gamma,
on the cells P-48 and P-49 registered: ground_state(N, True, 0), the
TWISTED pi ring in winding sector 0. That state carries a persistent
covariant strain of -pi/N on every bond, a circulation, and a
circulation is odd under the mirror through the rotor and the
antipode. So the mirror argument of A-34 ("sector zero drives the
even sector only") assumed an untwisted ring the cells are not.

The control that decides it: the same integrator and readout (the A-34
runner) on three rings at the same gamma -
  twisted sector 0  (the registered ring; circulation -pi/N per bond)
  twisted sector 1  (the opposite circulation, +pi/N per bond)
  untwisted         (no circulation; the P-46 ring)
If the odd seed is the twist's circulation meeting the rotor's sense
of rotation, it is absent on the untwisted ring and changes sign (or
size) between the two sectors. If it is the slip's own asymmetry or
the estimator's ripple residual, it is present on all three alike.
Also read: the odd channel with the running mean over one and over
three rotor periods (a ripple residual shrinks with the longer mean;
a displacement does not), and the SIGNED odd mean per window (the
sign test between sectors). Traces of the even and odd channels are
saved every 0.5 units for later reading. Derive layer, no registration.
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc, ground_state  # noqa: E402
from a34_odd_mode import running_mean, rms_about_mean, fit_rate, rate_over, om_open, WINDOWS, N, B, OFFS  # noqa: E402

RINGS = (("twisted_s0", True, 0), ("twisted_s1", True, 1), ("untwisted", False, 0))
GAMMAS = (0.5, 0.35)


def run(gamma, f, dt, t_end, twisted, sector):
    A, th = ground_state(N, twisted, sector)
    v = [0.0] * N
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    sinD = [math.sin(x) for x in D0]
    n_ramp = int(round(200.0 / dt)); per_unit = int(round(1.0 / dt))
    event = None; n_total = int(round(1500.0 / dt))
    TH = []
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
    return {"event_t": event * dt if event else None, "TH": TH}


def analyse(rec, gamma, dt, log):
    TH = rec["TH"]; n = len(TH)
    ref_r = [row[0] for row in TH]
    Om = (ref_r[-1] - ref_r[0]) / ((n - 1) * dt)
    per = max(1, int(round(2 * math.pi / Om / dt)))
    th1p = [row[1] for row in TH]; th1m = [row[2] for row in TH]
    out = {"gamma": gamma, "event_t": rec["event_t"], "Omega": Om, "windows": [], "trace": []}
    slow = {}
    for mult in (1, 3):
        half = (per * mult) // 2
        slow[mult] = (running_mean(th1p, half), running_mean(th1m, half))
    ev1 = [0.5 * (p + m) for p, m in zip(*slow[1])]
    od1 = [0.5 * (p - m) for p, m in zip(*slow[1])]
    step = int(round(0.5 / dt))
    out["trace"] = [[k * dt, ev1[k], od1[k]] for k in range(0, n, step)]
    for (a, b_) in WINDOWS:
        lo, hi = int(round(a / dt)), int(round(b_ / dt))
        if hi > n:
            continue
        w = {"window": [a, b_]}
        for mult in (1, 3):
            sp, sm = slow[mult][0][lo:hi], slow[mult][1][lo:hi]
            ev = [0.5 * (p + m) for p, m in zip(sp, sm)]
            od = [0.5 * (p - m) for p, m in zip(sp, sm)]
            w["even_per%d" % mult] = rms_about_mean(ev)
            w["odd_per%d" % mult] = rms_about_mean(od)
            if mult == 1:
                w["odd_mean_signed"] = sum(od) / len(od)
                w["odd_over_even"] = w["odd_per1"] / w["even_per1"] if w["even_per1"] else None
        out["windows"].append(w)
        log("  win [%3.0f,%3.0f] even %.4e odd %.4e (odd/even %.3f) | 3-period mean: even %.4e odd %.4e | odd signed mean %+.4e"
            % (a, b_, w["even_per1"], w["odd_per1"], w["odd_over_even"], w["even_per3"], w["odd_per3"], w["odd_mean_signed"]))
    ladder = [w for w in out["windows"] if w["window"][1] <= 280.0]
    out["fits"] = {ch: fit_rate([(0.5 * (w["window"][0] + w["window"][1]), w[ch]) for w in ladder if w[ch] > 0])
                   for ch in ("even_per1", "odd_per1", "odd_per3")}
    out["pred"] = {"odd_k1": rate_over(gamma, om_open(1)), "even_k2": rate_over(gamma, om_open(2))}
    fmt = lambda x: "%.4f" % x if x is not None else "none"
    log("  fits: even %s odd %s (3-period %s) | pred odd k1 %.4f even k2 %.4f"
        % (fmt(out["fits"]["even_per1"]), fmt(out["fits"]["odd_per1"]), fmt(out["fits"]["odd_per3"]), out["pred"]["odd_k1"], out["pred"]["even_k2"]))
    return out


def main():
    quick = "--quick" in sys.argv
    dt = 0.01 if quick else 0.001
    f = fold_fc(N, -math.pi) + 0.005
    t0 = time.time(); lines = []
    def log(s):
        print(s, flush=True); lines.append(s)
    res = {"N": N, "f": f, "dt": dt, "windows": WINDOWS, "cells": {}}
    for g in GAMMAS:
        for name, tw, sec in RINGS:
            t1 = time.time()
            rec = run(g, f, dt, 380.0, tw, sec)
            if rec["event_t"] is None:
                log("gamma %g %s: no slip" % (g, name)); continue
            log("gamma %g %-11s event %.1f (%.0f s)" % (g, name, rec["event_t"], time.time() - t1))
            res["cells"]["gamma_%g_%s" % (g, name)] = analyse(rec, g, dt, log)
    res["seconds_total"] = time.time() - t0
    log("total %.0f s" % res["seconds_total"])
    name = "a35_odd_control%s" % ("_quick" if quick else "")
    with open(os.path.join(HERE, name + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)
    with open(os.path.join(HERE, name + ".txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
