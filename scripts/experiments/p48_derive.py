#!/usr/bin/env python3
"""P-48 derive layer: the bond stiffness kappa on the P-35/P-36 ring,
and what the band edge is a statement about.

THE QUESTION THAT STARTED IT. P-46 read the slip footprint as
evanescent because the rotor at Omega ~ f/gamma sits above the
lattice band top 2. That top is the grid's: a continuous ring has
none. The owner asked for a stiffness column kappa as the honest
refinement axis (the ring's spacing is fixed at 1, so N is length,
not resolution). The model with stiffness kappa is
    theta_dd_j = -gamma v_j + kappa (sin D_j - sin D_{j-1}) + f delta_jb.

THE IDENTITY (measured here first). With u = v / sqrt(kappa) and
tau = sqrt(kappa) t the equation reads
    d^2 theta / d tau^2 = -(gamma/sqrt kappa) u + (sin D_j - sin D_{j-1})
                          + (f/kappa) delta_jb,
i.e. (kappa, gamma, f) at time t is (1, gamma/sqrt kappa, f/kappa) at
time sqrt(kappa) t, EXACTLY - and exactly for the Euler-Cromer map too
when dt scales to sqrt(kappa) dt (the ramp keeps its step count).
kappa is a clock, not a parameter. The band top 2 sqrt(kappa) and the
rotor speed f/gamma scale together: the rotor sits above the band iff
    (f/kappa) / (gamma/sqrt kappa) > 2,  i.e.  Omega' = f/(gamma sqrt kappa) > 2,
which at kappa = 1 is the DAMPING statement f/gamma > 2. What the grid
put in is not the band edge (a fixed unit) but the freedom to place
gamma; P-46's cells sat at f/gamma = 98 / 49 / 20 by choice.

SO THE LADDER kappa STOOD IN FOR is a gamma ladder at kappa = 1 and
fixed reduced load: gamma in {0.1, 0.2, 0.5, 1, 2}, terminal Omega =
f/gamma from 20 down through the band edge to 1, read with the P-46
instrument unchanged (bond-phase lock-in, the two floors, the exact
discrete response root). The prediction, from the root alone: the
per-site ratio |w| rises from ~c/Omega^2 ~ 2.6e-3 at gamma 0.1 toward
order one as Omega crosses 2, where w leaves the real axis and the tail
becomes a damped propagating wave.

NULLS (8a): the lock-in floors are P-46's, computed from each run; the
in-band cells have a nonlinearity term the layer measures (the
neighbour's strain amplitude A_1/Omega is no longer small); the rotor's
Omega is MEASURED (the bond-phase mean), not assumed f/gamma - in band
the rotor radiates and slows. Lessons: L-3, L-5, L-8, L-11, L-12, L-13.

Run: python3 scripts/experiments/p48_derive.py
"""
import cmath
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc, ground_state  # noqa: E402
from p46_derive import evanescent, integrate_aftermath  # noqa: E402

EPS = 2.0 ** -52
OPS = 32


def ec_step(th, v, A, N, b, gamma, f, kappa, dt):
    """One Euler-Cromer step of the kappa model, in the P-36 order."""
    sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
    v2 = [v[j] + dt * (kappa * (sinD[j] - sinD[j - 1]) - gamma * v[j]
                       + (f if j == b else 0.0)) for j in range(N)]
    th2 = [th[j] + dt * v2[j] for j in range(N)]
    return th2, v2


def one_step_identity(rng, N, M, gamma, f, kappa, dt, vmax=2.0, mutant=None):
    """The map identity at M random states: (kappa, gamma, f, dt) on
    (theta, v) against (1, gamma/sqrt kappa, f/kappa, sqrt kappa dt) on
    (theta, v/sqrt kappa). Residuals against 32 eps times the summands."""
    A = [math.pi if j == 0 else 0.0 for j in range(N)]
    b = N // 2
    s = math.sqrt(kappa)
    g2 = gamma / (kappa if mutant == "kappa-blind" else s)
    f2 = f / (s if mutant == "load-blind" else kappa)
    worst_th = worst_v = 0.0
    for _ in range(M):
        th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
        v = [rng.uniform(-vmax, vmax) for _ in range(N)]
        thA, vA = ec_step(th, v, A, N, b, gamma, f, kappa, dt)
        u = [x / s for x in v]
        thB, uB = ec_step(th, u, A, N, b, g2, f2, 1.0, s * dt)
        for j in range(N):
            bv = OPS * EPS * (abs(v[j]) / s + s * dt * (2.0 + g2 * abs(u[j]) + abs(f2)))
            worst_v = max(worst_v, abs(vA[j] / s - uB[j]) / bv)
            bt = OPS * EPS * (abs(th[j]) + s * dt * abs(uB[j]))
            worst_th = max(worst_th, abs(thA[j] - thB[j]) / bt)
    return {"M": M, "kappa": kappa, "worst_v_ratio": worst_v, "worst_theta_ratio": worst_th}


def integrate_kappa(N, gamma, f_target, kappa, dt, n_ramp, sample_every,
                    after_steps, cap_steps):
    """Own loop of the kappa model on the twisted sector-0 ring, dead
    loaded at N/2 with the P-36 soft ramp over n_ramp STEPS. Samples
    (theta, v) every sample_every steps; the P-36 event at a sample;
    runs to the event plus after_steps. Returns samples and event."""
    A, th = ground_state(N, True, 0)
    v = [0.0] * N
    b = N // 2
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    samples = []
    event = None
    s = 0
    n_total = cap_steps
    while s < n_total:
        f = f_target * min(1.0, (s + 1) / n_ramp)
        th, v = ec_step(th, v, A, N, b, gamma, f, kappa, dt)
        s += 1
        if s % sample_every:
            continue
        samples.append((s, list(th), list(v)))
        if event is None:
            D = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
            if max(abs(D[j] - D0[j]) for j in range(N)) > 1.5 * math.pi:
                event = s
                n_total = s + after_steps
    return {"event_step": event, "samples": samples}


def trajectory_scaling(N, gamma, f1, kappa, dt, t_ramp=200.0, after=100.0):
    """Run (kappa, gamma, kappa f1, dt) and (1, gamma/sqrt kappa, f1,
    sqrt kappa dt) with identical step counts; compare theta and
    v/sqrt kappa at every sample; report the event steps and the
    growth of the deviation (the map is identical, the rounding is
    not, so this measures the trajectory's own amplification)."""
    s = math.sqrt(kappa)
    n_ramp = int(round(t_ramp / dt))
    se = int(round(1.0 / dt))
    after_steps = int(round(after / dt))
    cap = int(round(900.0 / dt))
    t0 = time.time()
    ra = integrate_kappa(N, gamma, kappa * f1, kappa, dt, n_ramp, se, after_steps, cap)
    rb = integrate_kappa(N, gamma / s, f1, 1.0, s * dt, n_ramp, se, after_steps, cap)
    dev = []
    theta_max = 0.0
    for (sa, tha, va), (sb, thb, vb) in zip(ra["samples"], rb["samples"]):
        assert sa == sb
        dth = max(abs(tha[j] - thb[j]) for j in range(N))
        dv = max(abs(va[j] / s - vb[j]) for j in range(N))
        theta_max = max(theta_max, max(abs(x) for x in tha))
        dev.append((sa * dt, dth, dv))
    return {"kappa": kappa, "gamma": gamma, "f": kappa * f1, "dt": dt,
            "n_steps": ra["samples"][-1][0] if ra["samples"] else 0,
            "theta_max": theta_max,
            "event_step_A": ra["event_step"], "event_step_B": rb["event_step"],
            "max_dtheta": max(d[1] for d in dev), "max_dv": max(d[2] for d in dev),
            "dtheta_at_event": next((d[1] for d in dev if ra["event_step"] and d[0] >= ra["event_step"] * dt), None),
            "dtheta_end": dev[-1][1], "seconds": time.time() - t0,
            "profile": [(round(t, 1), d1, d2) for t, d1, d2 in dev[::25]]}


def slow_velocity(frames_v, dtf, Om, sites):
    """RMS of the velocity averaged over one rotor period at each
    offset: the in-band (slow) content of the site's motion that a
    reference carrying an Omega-component mixes into the lock-in."""
    N = len(frames_v[0])
    b = N // 2
    per = max(1, int(round(2 * math.pi / Om / dtf)))
    out = {}
    for d in sites:
        series = [fr[(b + d) % N] for fr in frames_v]
        means = [sum(series[k:k + per]) / per for k in range(0, len(series) - per + 1, per)]
        out[str(d)] = math.sqrt(sum(m * m for m in means) / len(means)) if means else 0.0
    return out


def lockin_frames(frames_v, dtf, Om, sites, harmonics=(0.5, 1.0, 2.0)):
    """Offline lock-in of the recorded velocity frames at multiples of
    the rotor's mean frequency (a fixed-frequency reference; the chirp
    over a late window is below the self floor), per site offset.
    Returns {harmonic: {offset: amplitude}} and the RMS of v at the far
    sites (offset >= 4), the ring's total wave content."""
    n = len(frames_v)
    N = len(frames_v[0])
    b = N // 2
    out = {}
    for hmul in harmonics:
        acc = {d: 0j for d in sites}
        for k, fr in enumerate(frames_v):
            e = cmath.exp(complex(0.0, -hmul * Om * k * dtf))
            for d in sites:
                acc[d] += fr[(b + d) % N] * e
        out[str(hmul)] = {str(d): 2.0 * abs(acc[d]) / n for d in sites}
    far = [j for j in range(N) if min(abs(j - b), N - abs(j - b)) >= 4]
    rms = math.sqrt(sum(fr[j] ** 2 for fr in frames_v for j in far) / (n * len(far)))
    out["far_rms"] = rms
    return out


AFTER = {0.1: 200.0, 0.2: 120.0, 0.35: 100.0, 0.45: 90.0, 0.5: 80.0,
         0.6: 80.0, 0.8: 70.0, 1.0: 60.0}
WIN = {0.1: (100.0, 200.0), 0.2: (60.0, 120.0), 0.35: (40.0, 100.0),
       0.45: (30.0, 90.0), 0.5: (30.0, 80.0), 0.6: (30.0, 80.0),
       0.8: (20.0, 70.0), 1.0: (20.0, 60.0)}


def gamma_ladder_cell(N, f, gamma, dt=0.001):
    """The P-46 instrument at kappa = 1 and damping gamma, plus the
    recorded velocity frames over the window for the offline
    harmonic lock-in (Omega/2, Omega, 2 Omega)."""
    after = AFTER[gamma]
    win = WIN[gamma]
    t0 = time.time()
    r = integrate_aftermath(N, True, 0, gamma, f, dt, windows=[win],
                            after_event=after, offsets=(1, 2, 3), t_cap=1500.0,
                            record={"from": win[0], "to": win[1], "dtf": 0.01})
    w = r["windows"][0]
    if w.get("empty"):
        return {"gamma": gamma, "empty": True, "event_t": r["event_t"],
                "seconds": time.time() - t0}
    # the same cell demodulated against the rotor's phase alone
    rr = integrate_aftermath(N, True, 0, gamma, f, dt, windows=[win],
                             after_event=after, offsets=(1, 2, 3), t_cap=1500.0,
                             reference="rotor")
    wr = rr["windows"][0]
    Om = w["omega_bar"]
    spec = lockin_frames(r["frames"]["v"], 0.01, Om, (1, 2, 3, 4, 6))
    slow = slow_velocity(r["frames"]["v"], 0.01, Om, (1, 2, 3))
    out = {"gamma": gamma, "Omega_terminal": f / gamma, "event_t": r["event_t"],
           "window": list(win), "Omega_measured": Om, "Omega_over_terminal": Om / (f / gamma),
           "A": w["A"], "cmin": w["cmin"], "cmax": w["cmax"], "wave_amp": w["wave_amp"],
           "lockin_floor": w["lockin_floor"], "self_floor": w["self_floor"],
           "cycle": {k: w["cycle"].get(k) for k in ("turns", "mean", "omega_start", "omega_end", "chirp_floor", "step_floor")},
           "seconds": time.time() - t0}
    preds = {}
    for c in (w["cmin"], w["cmax"]):
        wv, A1 = evanescent(Om, c, gamma, dt)
        preds[str(round(c, 6))] = {"w_abs": abs(wv), "w_arg": math.atan2(wv.imag, wv.real), "A1": A1}
    out["pred"] = preds
    wm = sum(p["w_abs"] for p in preds.values()) / len(preds)
    A1m = sum(p["A1"] for p in preds.values()) / len(preds)
    out["spectrum"] = spec
    out["slow_rms"] = slow
    out["A_rotor_ref"] = wr["A"]
    out["omega_bar_rotor_ref"] = wr["omega_bar"]
    # the derived mixing floor of a reference carrying the neighbour's
    # Omega-oscillation (index X = A_1/Omega): (X/2) v_slow at the site
    X = w["A"]["1"] / Om
    out["mixing_floor_bond_ref"] = {d: 0.5 * X * slow[d] for d in slow}
    out["subharmonic"] = {"half_over_one_at_2": spec["0.5"]["2"] / max(spec["1.0"]["2"], 1e-300),
                          "half_over_one_at_4": spec["0.5"]["4"] / max(spec["1.0"]["4"], 1e-300),
                          "half_at_4_over_floor": spec["0.5"]["4"] / max(w["lockin_floor"], 1e-300),
                          "Omega_half_in_band": Om / 2.0 < 2.0 * math.sqrt(w["cmax"])}
    wlo, whi = min(p["w_abs"] for p in preds.values()), max(p["w_abs"] for p in preds.values())
    A1lo, A1hi = min(p["A1"] for p in preds.values()), max(p["A1"] for p in preds.values())
    fl2 = w["lockin_floor"] + w["self_floor"]["2"]
    out["checks"] = {
        # A_1 under the bond reference against its band, floors + mixing
        "A1_bond_in_band": A1lo - (w["lockin_floor"] + w["self_floor"]["1"] + out["mixing_floor_bond_ref"]["1"])
                           <= w["A"]["1"] <= A1hi + (w["lockin_floor"] + w["self_floor"]["1"] + out["mixing_floor_bond_ref"]["1"]),
        "A1_bond_rel_to_band": (w["A"]["1"] - A1hi) / A1hi if w["A"]["1"] > A1hi else ((w["A"]["1"] - A1lo) / A1lo if w["A"]["1"] < A1lo else 0.0),
        "mixing_over_A1": out["mixing_floor_bond_ref"]["1"] / w["A"]["1"],
        # A_2/A_1 under the rotor reference (the smear is common-mode) against the |w| band, floors
        "ratio21_rotor": wr["A"]["2"] / wr["A"]["1"],
        "ratio21_rotor_in_band": (wlo * wr["A"]["1"] - fl2) / wr["A"]["1"] <= wr["A"]["2"] / wr["A"]["1"] <= (whi * wr["A"]["1"] + fl2) / wr["A"]["1"],
        "ratio21_bond": w["A"]["2"] / w["A"]["1"],
        "ratio21_bond_excess_over_top": w["A"]["2"] / w["A"]["1"] / whi - 1.0,
        "mixing_over_A2_bond": out["mixing_floor_bond_ref"]["2"] / w["A"]["2"],
        # is the bond-reference excess at offset 2 covered by the derived mixing term + floors?
        "bond_excess_covered": w["A"]["2"] <= whi * w["A"]["1"] + fl2 + out["mixing_floor_bond_ref"]["2"],
        "smear_rotor_ref_A1": wr["A"]["1"] / w["A"]["1"]}
    out["read"] = {"A1_rel": w["A"]["1"] / A1m - 1.0,
                   "ratio21": w["A"]["2"] / w["A"]["1"], "ratio21_over_w": (w["A"]["2"] / w["A"]["1"]) / wm,
                   "ratio32": w["A"]["3"] / w["A"]["2"], "ratio32_over_w": (w["A"]["3"] / w["A"]["2"]) / wm,
                   "floor_over_A2": (w["lockin_floor"] + w["self_floor"]["2"]) / (w["A"]["1"] * wm),
                   "floor_over_A3": (w["lockin_floor"] + w["self_floor"]["3"]) / (w["A"]["1"] * wm * wm),
                   "neighbour_strain_amp": w["A"]["1"] / Om,
                   "nonlinearity_est": (w["A"]["1"] / Om) ** 2 / 8.0}
    return out


def main():
    t0 = time.time()
    out = {"eps": EPS, "ops": OPS}
    N = 64
    fold = fold_fc(N, -math.pi)
    f1 = fold + 0.005
    out["fold_twist0_N64"] = fold
    out["f1"] = f1

    # (i) the one-step map identity at the floor, and the two mutants
    rng = random.Random(20260902)
    ids = {}
    for kappa in (0.25, 4.0, 0.5, 2.0):
        for vmax in (2.0, 100.0):
            r = one_step_identity(rng, N, 5000, 0.1, kappa * f1, kappa, 0.001, vmax)
            ids["kappa_%g_vmax_%g" % (kappa, vmax)] = r
            print("one-step kappa %g vmax %g: v ratio %.3f theta ratio %.3f"
                  % (kappa, vmax, r["worst_v_ratio"], r["worst_theta_ratio"]), flush=True)
    for m in ("kappa-blind", "load-blind"):
        r = one_step_identity(random.Random(7), N, 200, 0.1, 4.0 * f1, 4.0, 0.001, 2.0, mutant=m)
        ids["mutant_" + m] = r
        print("mutant", m, "v ratio %.3e theta ratio %.3e" % (r["worst_v_ratio"], r["worst_theta_ratio"]), flush=True)
    out["one_step"] = ids

    # (ii) the trajectories through the slip: kappa 0.25 and 4 against kappa 1
    traj = {}
    for kappa in (0.25, 4.0, 0.5, 2.0):
        r = trajectory_scaling(N, 0.1, f1, kappa, 0.001)
        traj["kappa_%g" % kappa] = r
        print("trajectory kappa %g: events %s / %s, max dtheta %.2e (at event %s, end %.2e) max dv %.2e (%.0f s)"
              % (kappa, r["event_step_A"], r["event_step_B"], r["max_dtheta"],
                 r["dtheta_at_event"], r["dtheta_end"], r["max_dv"], r["seconds"]), flush=True)
    out["trajectories"] = traj

    # (iii) the gamma ladder at kappa = 1
    ladder = {}
    for g in (0.1, 0.2, 0.35, 0.45, 0.5, 0.6, 0.8, 1.0):
        c = gamma_ladder_cell(N, f1, g)
        ladder["gamma_%g" % g] = c
        if c.get("empty"):
            print("gamma %g: EMPTY window (event %s) - creep regime beyond the cap" % (g, c["event_t"]), flush=True)
            continue
        rd = c["read"]
        sh = c["subharmonic"]
        ck = c["checks"]
        print("   CHECKS: A1(bond) in band %s (rel %+.2e, mixing/A1 %.1e) | ratio21(rotor) %.4e in band %s | ratio21(bond) excess over top %+.1f%%, mixing/A2 %.1f%%, covered %s | rotor-ref smear of A1 %.3f | slow rms %s"
              % (ck["A1_bond_in_band"], ck["A1_bond_rel_to_band"], ck["mixing_over_A1"], ck["ratio21_rotor"], ck["ratio21_rotor_in_band"],
                 100 * ck["ratio21_bond_excess_over_top"], 100 * ck["mixing_over_A2_bond"], ck["bond_excess_covered"], ck["smear_rotor_ref_A1"],
                 {d: "%.2e" % v for d, v in c["slow_rms"].items()}), flush=True)
        print("   Omega/2 in band: %s; v(Omega/2)/v(Omega) at offset 2: %.3f, at offset 4: %.3f; v(Omega/2) at 4 over the wave floor: %.1f; far RMS %.3e; spectrum %s"
              % (sh["Omega_half_in_band"], sh["half_over_one_at_2"], sh["half_over_one_at_4"],
                 sh["half_at_4_over_floor"], c["spectrum"]["far_rms"],
                 {h: {d: "%.2e" % a for d, a in v.items()} for h, v in c["spectrum"].items() if h != "far_rms"}), flush=True)
        print("gamma %g: event %.1f Omega %.3f (%.3f of f/gamma) A1 rel %.2e | ratio21 %.3e = %.3f x |w| | ratio32 %.3e = %.3f x |w| | floors/A2 %.2f /A3 %.2f | strain amp %.3f nonlin %.1e | K-cycle mean %s (%.0f s)"
              % (g, c["event_t"], c["Omega_measured"], c["Omega_over_terminal"], rd["A1_rel"],
                 rd["ratio21"], rd["ratio21_over_w"], rd["ratio32"], rd["ratio32_over_w"],
                 rd["floor_over_A2"], rd["floor_over_A3"], rd["neighbour_strain_amp"],
                 rd["nonlinearity_est"], c["cycle"]["mean"], c["seconds"]), flush=True)
    out["gamma_ladder"] = ladder
    out["seconds_total"] = time.time() - t0
    with open(os.path.join(HERE, "p48_derive.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote p48_derive.json in %.0f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
