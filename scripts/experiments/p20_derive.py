#!/usr/bin/env python3
"""P-20 derivation layer (pre-registration): the eps budget and the
frame-separability map.

Runs BEFORE the registered computation and pins every number the
P-20 clauses compare against (p20_registration.json, committed in the
registration commit). Nothing here measures slip durations or frame
histograms - those are the registered computation's job
(p20_eps_budget.py). What is derived here:

1. ONE-POLE PHASE DELAY. The reflection and contact filters in
   p19_alf_waveguide.py are all y_n = (1-a) x_n + a y_{n-1}, i.e.
   H(z) = (1-a)/(1 - a z^-1). Its phase is
   arg H(e^{-jw}) = -atan(a sin w / (1 - a cos w)), so the phase
   delay in samples is atan(a sin w/(1-a cos w))/w -> a/(1-a) as
   w -> 0. The CAS (symb.py) checks the derivative identity behind
   the limit (EQ1, EQ2 below) and a live run of the actual recursion
   on a slow sinusoid confirms the a/(1-a) number (EQ4).

2. FILTER PASSES PER PATH, read from the p19 update loop:
   - The main loop (one full period T0's worth of travel) passes the
     bridge one-pole (A_BR = 0.70) and the nut one-pole
     (A_NUT = 0.40) once each: 0.7/0.3 + 0.4/0.6 = 3.000 samples.
   - ONE extra nut-side round trip (the ALF mechanism's extra turn)
     passes the nut one-pole once, and its reflection off the STUCK
     bow is carried entirely by the contact-smoothed injection term:
     in the loop, buf_n[pn] = vi_b + dv_tr, so a wave returning from
     the nut re-enters the nut-bound line only through
     dv_tr = f_sm * half_z, which has passed the A_CONTACT = 0.70
     one-pole. EQ3 checks the junction algebra: with the bow stuck
     (vc pinned), the nut-side reflection coefficient is
     -(1/(2Z))/gamma = -Zt/(Z+Zt) (= -2/3 at Zt = 2Z), i.e. the
     whole reflected amplitude is the filtered term - the direct
     (unfiltered) pass-through vi_b goes to the OTHER line.
     Per extra trip: 0.4/0.6 + 0.7/0.3 = 3.000 samples.
   - The torsional branch has its own delay pair and does not sit on
     the transverse trigger path; its filters are not counted.
     (Scope: if the trigger is torsional - Guettler's second family -
     this count is wrong by construction; that family is excluded by
     P-19 and stays excluded here.)

3. DELAY-LINE ROUNDING. d_b = round(beta*loop), d_n =
   round((1-beta)*loop) with loop = FS/F0 = 447.9431 samples, so the
   realized loop is d_b + d_n = 448 (offset +0.0569 samples at every
   grid beta) and each extra nut trip is off by
   d_n - (1-beta)*loop.

4. THE BUDGET. eps_pred = filter passes + rounding + S, with S the
   mean slipping samples per lock cycle, TO BE MEASURED (an
   observable independent of the period offsets). Given the
   committed P-19 eps values (known anchors, listed below), the
   budget therefore PREDICTS S per cell (s_required_samples): the
   registered test is whether the measured S lands there, i.e.
   |eps_meas - eps_pred| <= 0.015 T0 per cell with no tuned
   quantity anywhere.

5. THE SEPARABILITY MAP. At frame rate fps, the single-interval
   frame separation between an m=1 lattice lock and exact doubling
   is D = (2 - P/T0) * T0 * fps = (beta - eps/T0) * fps/f0 frames.
   Single-interval separability needs D >= 1:
   beta >= f0/fps + eps/T0. At f0 = 196.9, fps = 3000 the eps-free
   floor is f0/fps = 0.06563; with the P-19 grid's median measured
   eps (0.0411 T0) the threshold is beta* = 0.10676. Cells are
   partitioned before any histogram is simulated, using the KNOWN
   committed/session eps of each cell and a registered margin of
   0.02 in beta.

KNOWN ANCHORS (not predictions): the four P-19 RUNS locks from
committed p19_results.json, and the Kawano-point session numbers of
2026-08-25 (beta = 50/325, force plateau [0.90, 1.15], operating
F = 1.05, lock 1.8886977 T0 = 104.25 Hz, frame histograms 29 vs
30-31) - those were computed before this registration and are inputs
here, never outcomes.

Deterministic, stdlib only. Writes p20_registration.json.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from symb import N, V, add, mul, sub, div, powe, sin, cos, d, equal, ev  # noqa: E402

FS = 88200.0
F0 = 196.9
FPS = 3000.0
A_NUT, A_BR, A_CONTACT = 0.40, 0.70, 0.70
LOOP = FS / F0
T0_MS = 1000.0 / F0

OUT = []


def say(line):
    OUT.append(line)
    print(line)


# ---------------------------------------------------------------- EQ1-EQ2
# g(w) = a sin w / (1 - a cos w) is tan(-arg H); its derivative is
# (a cos w - a^2)/(1 - a cos w)^2, whose w->0 value is a/(1-a).
a, w = V("a"), V("w")
g = mul(mul(N(1), a), sin(w), powe(sub(N(1), mul(a, cos(w))), N(-1)))
dg = d(g, "w")
rhs = mul(sub(mul(a, cos(w)), mul(a, a)),
          powe(sub(N(1), mul(a, cos(w))), N(-2)))
ok, worst, nval = equal(dg, rhs, {"a": (0.05, 0.9), "w": (0.05, 1.2)})
say(f"EQ1 d/dw [a sin w/(1-a cos w)] == (a cos w - a^2)/(1-a cos w)^2: "
    f"{ok} (worst {worst:.2e}, {nval} samples)")
assert ok

lim_ok = True
for av in (0.40, 0.60, 0.70):
    v0 = ev(rhs, {"a": av, "w": 1e-6})
    lim_ok &= abs(v0 - av / (1 - av)) < 1e-5
say(f"EQ2 w->0 limit equals a/(1-a) at a in (0.40, 0.60, 0.70): {lim_ok}")
assert lim_ok

# ---------------------------------------------------------------- EQ3
# Stuck-bow junction: reflection into the nut-bound line is entirely
# the filtered injection term, amplitude -(1/(2Z))/gamma = -Zt/(Z+Zt).
Z, Zt = V("Z"), V("Zt")
gamma = add(powe(mul(N(2), Z), N(-1)), powe(mul(N(2), Zt), N(-1)))
lhs3 = mul(N(-1), powe(mul(N(2), Z), N(-1)), powe(gamma, N(-1)))
rhs3 = mul(N(-1), Zt, powe(add(Z, Zt), N(-1)))
ok3, worst3, n3 = equal(lhs3, rhs3, {"Z": (0.1, 10.0), "Zt": (0.1, 10.0)})
say(f"EQ3 stuck-bow nut-side reflection -(1/2Z)/gamma == -Zt/(Z+Zt): "
    f"{ok3} (worst {worst3:.2e}); at Zt=2Z this is -2/3, all of it "
    f"through the contact one-pole")
assert ok3

# ---------------------------------------------------------------- EQ4
# The actual recursion, run live on a slow sinusoid, shows the
# a/(1-a)-sample delay directly (phase of the filtered output by
# projection onto sin/cos, exact for a pure tone in steady state).
eq4_ok = True
for av in (A_NUT, A_BR):
    wv = 2 * math.pi * 0.0005          # 0.05% of the sample rate
    y = 0.0
    ns = 200000
    sy_s = sy_c = 0.0
    for n in range(ns):
        y = (1 - av) * math.sin(wv * n) + av * y
        if n >= ns // 2:
            sy_s += y * math.sin(wv * n)
            sy_c += y * math.cos(wv * n)
    delay = -math.atan2(sy_c, sy_s) / wv
    pred = av / (1 - av)
    say(f"EQ4 live one-pole a={av:.2f}: measured delay {delay:.4f} "
        f"samples vs a/(1-a) = {pred:.4f}")
    eq4_ok &= abs(delay - pred) < 0.01
assert eq4_ok

D_NUT = A_NUT / (1 - A_NUT)
D_BR = A_BR / (1 - A_BR)
D_CON = A_CONTACT / (1 - A_CONTACT)
say(f"filter delays (samples): nut {D_NUT:.4f}, bridge {D_BR:.4f}, "
    f"contact {D_CON:.4f}; base loop {D_BR + D_NUT:.4f}, per extra "
    f"nut trip {D_NUT + D_CON:.4f}")

# ---------------------------------------------------------------- cells
# Known anchors: committed P-19 results + the Kawano session point.
p19 = json.loads((HERE / "p19_results.json").read_text())
KAWANO_BETA = 50.0 / 325.0
KAWANO_P_T0 = 1.8886976751865794     # session 2026-08-25, known anchor
KAWANO_F = 1.05                      # mid of session plateau [0.90, 1.15]

cells = []
for r in p19["runs"]:
    cells.append({"beta": r["beta"], "force": r["force"], "m": r["m"],
                  "P_known_T0": r["lock_mean_T0"], "source": "p19_results"})
cells.append({"beta": KAWANO_BETA, "force": KAWANO_F, "m": 1,
              "P_known_T0": round(KAWANO_P_T0, 5),
              "source": "session-2026-08-25 (known anchor)"})

for c in cells:
    beta, m = c["beta"], c["m"]
    d_b = max(2, round(beta * LOOP))
    d_n = max(2, round((1 - beta) * LOOP))
    r_full = (d_b + d_n) - LOOP
    r_nut = d_n - (1 - beta) * LOOP
    filt = (D_BR + D_NUT) + m * (D_NUT + D_CON)
    rounding = r_full + m * r_nut
    fixed = filt + rounding
    eps_known = (c["P_known_T0"] - (1 + m * (1 - beta))) * LOOP
    c.update({
        "d_b": d_b, "d_n": d_n,
        "filter_samples": round(filt, 4),
        "rounding_samples": round(rounding, 4),
        "fixed_samples": round(fixed, 4),
        "fixed_T0": round(fixed / LOOP, 5),
        "eps_known_samples": round(eps_known, 3),
        "eps_known_T0": round(eps_known / LOOP, 5),
        "s_required_samples": round(eps_known - fixed, 3),
    })
    say(f"cell beta={beta:.6f} m={m} F={c['force']}: fixed part "
        f"{fixed:.3f} samples (filters {filt:.3f} + rounding "
        f"{rounding:+.3f}); known eps {eps_known:.2f} samples -> "
        f"the budget requires S = {eps_known - fixed:.2f} samples "
        f"of slip per cycle")

# ---------------------------------------------------------------- map
f_floor = F0 / FPS
eps_m1 = sorted(c["eps_known_T0"] for c in cells if c["m"] == 1
                and c["source"] == "p19_results")
eps_med = eps_m1[len(eps_m1) // 2]
beta_star = f_floor + eps_med
MARGIN = 0.02
say(f"separability: D = (beta - eps/T0)*fps/f0 frames; floor f0/fps "
    f"= {f_floor:.5f}; threshold beta* = {beta_star:.5f} at the grid "
    f"median eps {eps_med:.4f} T0 (fps = {FPS:.0f}, f0 = {F0})")

no_overlap, overlap = [], []
for c in cells:
    if c["m"] != 1:
        c["D_frames"] = None
        continue
    Dfr = (c["beta"] - c["eps_known_T0"]) * FPS / F0
    c["D_frames"] = round(Dfr, 3)
    side = c["beta"] - c["eps_known_T0"] - f_floor
    if side >= MARGIN:
        no_overlap.append(c["beta"])
    elif side < 0:
        overlap.append(c["beta"])
    say(f"  beta={c['beta']:.6f}: D = {Dfr:.3f} frames, "
        f"margin {side:+.5f} -> "
        f"{'no-overlap side' if side >= MARGIN else ('overlap side' if side < 0 else 'inside margin band (untested)')}")

reg = {
    "registered": "2026-08-26",
    "before_measuring": ["slip-episode durations", "frame histograms",
                         "per-force eps values"],
    "known_anchors": {
        "p19_results": "committed on this branch before this file",
        "kawano_point": {
            "beta": KAWANO_BETA, "force": KAWANO_F,
            "P_T0": KAWANO_P_T0, "plateau_F": [0.90, 1.15],
            "provenance": "interactive session 2026-08-25; lock, "
            "plateau, and 29-vs-30/31 frame histograms were computed "
            "there BEFORE this registration and are anchors, not "
            "predictions"},
    },
    "filter_delay_samples": {"nut": D_NUT, "bridge": D_BR,
                             "contact": D_CON,
                             "base_loop": D_BR + D_NUT,
                             "per_extra_nut_trip": D_NUT + D_CON},
    "s_definition": "S = (samples with the slip branch taken and "
    "nonzero slip velocity in the measurement window) / (number of "
    "dominant-cluster inter-onset intervals in the window), measured "
    "on the same deterministic runs that yield the periods",
    "cells": cells,
    "clause_a": {
        "band_T0": 0.015,
        "text": "per cell, |eps_meas - eps_pred| <= 0.015 T0 with "
        "eps_pred = filter + rounding + S and nothing tuned; AND the "
        "sign of eps_meas differences between adjacent m=1 grid betas "
        "(0.10->0.13, 0.13->0.16) is reproduced by eps_pred",
    },
    "clause_b": {
        "drift_band_T0": 0.016,
        "sign_floor_T0": 0.002,
        "force_ladders": {"0.10": [1.20, 1.50, 1.60],
                          "0.13": [0.95, 1.10, 1.20],
                          "0.16": [0.90, 0.95, 1.05]},
        "text": "within each committed m=1 plateau, eps_meas range "
        "across the ladder < 0.016 T0 (the committed force-scan "
        "drift bound), and between the ladder endpoints the slip "
        "term S moves in the same direction as eps_meas whenever "
        "|delta eps_meas| > 0.002 T0 (else the direction sub-clause "
        "is vacuous for that beta)",
    },
    "clause_c": {
        "fps": FPS, "floor_beta": round(f_floor, 5),
        "beta_star_at_median_eps": round(beta_star, 5),
        "margin_beta": MARGIN,
        "no_overlap_betas": no_overlap,
        "overlap_betas": overlap,
        "protocol": "onset frame = floor(t*fps); interval = frame "
        "difference of consecutive dominant-cluster onsets; doubling "
        "comparator = synthetic train at spacing 2 T0 from the same "
        "first onset, same quantization; overlap = nonempty "
        "intersection of the two supports",
        "text": "cells on the no-overlap side show zero histogram "
        "overlap with the doubling comparator; cells on the overlap "
        "side show overlap",
    },
    "changes_my_mind": [
        "any cell with |eps_meas - eps_pred| > 0.030 T0 (double the "
        "band) kills the claimed eps decomposition; the "
        "alf-period-lattice scope sentence then needs a correction "
        "recorded in the R entry, not a rescue",
        "histogram overlap in any cell whose derived D >= 1.5 frames "
        "(here beta = 0.16 and the Kawano cell) kills the "
        "separability arithmetic",
    ],
    "not_claimed_in_advance": [
        "real strings", "the torsional trigger family",
        "frame rates other than 3000 fps",
        "force dependence beyond the committed plateaus",
        "other strings, tunings, or bow models",
    ],
}

path = HERE / "p20_registration.json"
path.write_text(json.dumps(reg, indent=1) + "\n")
say(f"wrote {path.name}")
(HERE / "p20_derive_out.txt").write_text("\n".join(OUT) + "\n")
