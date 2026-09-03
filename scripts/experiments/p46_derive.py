#!/usr/bin/env python3
"""P-46 derive layer: the slip aftermath on the dead-loaded free
pi ring, in the P-45 current. Three derived pieces, each measured
here before registration and written to p46_derive.json:

MOMENTUM (exact, slip-blind). Summing the P-36 equation of motion
over the ring telescopes the bond forces away:
    dP/dt = f - gamma P,   P = sum_j v_j,
at every instant, slip or no slip. Under Euler-Cromer the discrete
version is exact too: P_{n+1} = P_n + dt (f_n - gamma P_n), and in
the hold phase P_n = f/gamma + (P_0 - f/gamma)(1 - gamma dt)^n.
The ring's share P_ring = sum_{j != b} v_j obeys, exactly,
    dP_ring/dt = -gamma P_ring - (sin D_b - sin D_{b-1}),
the last term being the rotor's torque on the ring through its two
bonds. So the pre-event rigid drift f/(N gamma) of the free ring
is handed to the rotor: the ring's drift decays at rate gamma up
to the integrated rotor torque, and the rotor spins up toward
f/gamma on the same timescale (R-44's unregistered reading called
the rotor at ~56 "held by a mean drag"; it was 0.55 of terminal at
event + 40 because 1 - e^{-0.8} = 0.55 - a spin-up, not a drag.
The 182 R-44 called out-flow after the slip was accumulated over
the whole run, mostly pre-event, when the loaded site fed the
ring's drift. Both corrected here.)

EVANESCENCE (linear response, derived). Once the rotor's frequency
Omega ~ f/gamma sits above the lattice band edge 2, the bond force
sin D_b (amplitude exactly 1 at the rotor's own phase) drives the
neighbour site b+1, the end of a semi-infinite chain of stiffness
c = cos D ~ 1 with damping gamma. With z = Omega^2 - i gamma Omega
the evanescent root w (|w| < 1) solves w + 1/w = 2 - z/c, i.e.
|w| ~ c/Omega^2, staggered; the end site's velocity amplitude is
A_1 = |Omega / (c (1 - w) - z)| ~ 1/Omega, and A_{d+1}/A_d = |w|.
The footprint above the band is therefore a geometric tail with
ratio c/Omega^2 per site: ~1e-4 at gamma = 0.02. Read by lock-in
against the rotor's own phase, A_d = |(1/T) int v_{b+d} e^{-i
theta_b} dt|, exact for the fundamental whatever the chirp.

THE NULLS (8a). The lock-in's response to the in-band wave the
slip launches (amplitude a, frequency <= 2) is bounded by
2a / (T (Omega - 2)); the windowed mean torque's leakage from an
oscillation of amplitude A_T at Omega is 2 A_T / (T (Omega - 2)).
Both floors are computed from the run's own measured a, A_T,
Omega, never from a guess. They decide which offsets are
measurable at which gamma (8c): A_2 at gamma = 0.02 sits below
the wave floor for any window inside the run; offsets 1 and 2 at
gamma in {0.04, 0.1}; offset 1 only at 0.02.

THE ANCHOR (L-9). Before any nonlinear run, the lock-in pipeline
is pointed at a linear semi-infinite chain driven by a unit
sinusoid at its end, integrated with the same Euler-Cromer; A_1
and A_2/A_1 must land on the closed forms above.

Run: python3 scripts/experiments/p46_derive.py
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
from p45_derive import site_energy  # noqa: E402

EPS = 2.0 ** -52
OPS = 32


def evanescent(Omega, c, gamma, dt=None):
    """(w, A_1) for the damped chain: w the root of w + 1/w = 2 - z/c
    with |w| < 1, A_1 the end-site velocity amplitude per unit force.
    With dt given, z and the velocity factor are the EXACT ones of the
    Euler-Cromer map (v' = v + dt a, x' = x + dt v'): for a mode
    x q^n with q = e^{i Omega dt}, v' = x (q - 1)/dt and the map
    gives -z_d x = c (w + 1/w - 2) x + F with
    z_d = -[(q - 1)^2 / (q dt^2) + gamma (q - 1)/(q dt)], which tends
    to Omega^2 - i gamma Omega as dt -> 0. The continuous form was
    off by ~(dt Omega)^2, the size of the registered band at
    gamma = 0.02; the discrete form removes that error entirely."""
    if dt is None:
        z = complex(Omega * Omega, -gamma * Omega)
        vfac = Omega
    else:
        q = cmath.exp(complex(0.0, Omega * dt))
        z = -((q - 1.0) ** 2 / (q * dt * dt) + gamma * (q - 1.0) / (q * dt))
        vfac = abs(q - 1.0) / dt
    s = 2.0 - z / c
    disc = cmath.sqrt(s * s - 4.0)
    w1 = (s + disc) / 2.0
    w2 = (s - disc) / 2.0
    w = w1 if abs(w1) < abs(w2) else w2
    A1 = abs(vfac / (c * (1.0 - w) - z))
    return w, A1


def integrate_aftermath(N, twisted, sector, gamma, f_target, dt,
                        t_ramp=200.0, after_event=400.0, t_cap=900.0,
                        windows=None, offsets=(1, 2, 3), record=None,
                        mutant=None, reference="bond"):
    """Euler-Cromer in the P-36 order with the momentum bookkeeping,
    the P-36 event detector, post-event unit samples of P_ring and
    v_b, lock-in accumulators over the given post-event windows
    [(d0, d1), ...] for the given offsets, the windowed mean torque,
    and optional wavebench frame recording {'from': d, 'to': d,
    'dtf': x}. Everything indexed by Delta = t - t_event."""
    A, th = ground_state(N, twisted, sector)
    v = [0.0] * N
    b = N // 2
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    sinD = [math.sin(x) for x in D0]
    n_ramp = int(round(t_ramp / dt))
    per_unit = int(round(1.0 / dt))
    P = 0.0
    worst_rec = 0.0      # discrete P recursion residual / bound
    worst_ring = 0.0     # ring-share identity residual / bound
    event_step = None
    samples = []         # (Delta, P, P_ring, v_b)
    windows = windows or []
    acc = [{"n": 0, "lock": {d: 0j for d in offsets}, "torque": 0.0,
            "Tmax": 0.0, "omega": 0.0, "wave": 0.0,
            "cmin": 1.0, "cmax": -1.0,
            # cycle-windowed torque: from the first rotor-turn
            # crossing after d0 to the last before d1
            "cyc_on": False, "cyc_sum": 0.0, "cyc_n": 0, "cyc_turns": 0,
            "cyc_omega_start": None, "cyc_omega_end": None,
            "cyc_sum_at_last_turn": 0.0, "cyc_n_at_last_turn": 0,
            "cyc_turns_at_last": 0, "cyc_omega_at_last": None}
           for _ in windows]
    turn_prev = math.floor(th[b] / (2 * math.pi))
    frames = {"h": [], "J": [], "v": []}
    h_pre = None
    E_b_split = {"pre": {"inflow": 0.0, "diss": 0.0, "inj": 0.0},
                 "post": {"inflow": 0.0, "diss": 0.0, "inj": 0.0}}
    s = 0
    n_total = int(round(t_cap / dt))
    while s < n_total:
        f = f_target * min(1.0, (s + 1) / n_ramp)
        P_old = P
        if s == 0:
            Pr_old = P - v[b]
        for j in range(N):
            a = sinD[j] - sinD[j - 1] - gamma * v[j] + (f if j == b else 0.0)
            v[j] += dt * a
        for j in range(N):
            th[j] += dt * v[j]
        P = sum(v)
        # (a) exact discrete recursion, per step, at the floor
        pred = P_old + dt * (f - gamma * P_old)
        bound = OPS * EPS * (abs(P_old) + sum(abs(x) for x in v)
                             + dt * (abs(f) + gamma * abs(P_old))
                             + dt * sum(abs(x) for x in sinD) * 2)
        worst_rec = max(worst_rec, abs(P - pred) / bound)
        # ring-share identity, per step, exact: the rotor's torque on
        # the ring is the two-bond force, P_ring' = P_ring + dt(-gamma P_ring - T)
        T_old = sinD[b] - sinD[b - 1]
        Pr_new = P - v[b]
        pred_r = Pr_old + dt * (-gamma * Pr_old - T_old)
        bound_r = OPS * EPS * (abs(P) + abs(v[b]) + sum(abs(x) for x in v)
                               + abs(Pr_old) + dt * (gamma * abs(Pr_old) + 2.0)
                               + dt * sum(abs(x) for x in sinD) * 2)
        worst_ring = max(worst_ring, abs(Pr_new - pred_r) / bound_r)
        Pr_old = Pr_new
        sinD_new = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        J = [-0.5 * sinD_new[j] * (v[j] + v[(j + 1) % N]) for j in range(N)]
        phase = "post" if event_step is not None else "pre"
        E_b_split[phase]["inflow"] += dt * (J[b - 1] - J[b])
        E_b_split[phase]["diss"] += gamma * dt * v[b] * v[b]
        E_b_split[phase]["inj"] += f * dt * v[b]
        sinD = sinD_new
        s += 1
        if event_step is None:
            if s % per_unit == 0:
                D = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
                if max(abs(D[j] - D0[j]) for j in range(N)) > 1.5 * math.pi:
                    event_step = s
                    n_total = min(n_total, s + int(round(after_event / dt)))
                    samples.append((0.0, P, P - v[b], v[b]))
                else:
                    h_pre = site_energy(th, v, A, N)
            continue
        Delta = (s - event_step) * dt
        if s % per_unit == 0:
            samples.append((Delta, P, P - v[b], v[b]))
        # lock-in / torque accumulators
        turn_now = math.floor(th[b] / (2 * math.pi))
        crossed = turn_now != turn_prev
        if crossed:
            # fraction of this step that lies BEFORE the crossing, by
            # linear interpolation of theta_b across the step (the
            # step-quantized window end leaked A_T dt / T_w, which at
            # Omega^3 / gamma scaling was K ~ 50; this is O(dt^2))
            th_prev_b = th[b] - dt * v[b]
            target = 2 * math.pi * (turn_now if turn_now > turn_prev else turn_prev)
            lam = (target - th_prev_b) / (th[b] - th_prev_b)
            lam = min(1.0, max(0.0, lam))
        turn_prev = turn_now
        for k, (d0, d1) in enumerate(windows):
            if d0 <= Delta < d1:
                ac = acc[k]
                ac["n"] += 1
                # reference = the driving bond's phase theta_b - theta_{b+1}
                # (the rotor's phase alone is detuned by the ring's
                # residual drift, ~1 percent over a 100-unit window)
                # P-48: reference="rotor" demodulates against theta_b
                # alone (the bond phase imports the neighbour's slow
                # displacement when the slip's long-wavelength
                # relaxation is still alive in the window)
                if reference == "rotor":
                    e = cmath.exp(complex(0.0, -th[b]))
                else:
                    e = cmath.exp(complex(0.0, -(th[b] - th[(b + 1) % N])))
                for d in offsets:
                    ac["lock"][d] += v[(b + d) % N] * e
                T = sinD[b] - sinD[b - 1]
                ac["torque"] += T
                ac["Tmax"] = max(ac["Tmax"], abs(T))
                ac["omega"] += v[b]
                if crossed:
                    if not ac["cyc_on"]:
                        ac["cyc_on"] = True
                        ac["cyc_omega_start"] = v[b]
                        ac["cyc_sum"] += T * (1.0 - lam)
                        ac["cyc_n"] += 1.0 - lam
                        continue
                    ac["cyc_turns"] += 1
                    ac["cyc_sum_at_last_turn"] = ac["cyc_sum"] + T * lam
                    ac["cyc_n_at_last_turn"] = ac["cyc_n"] + lam
                    ac["cyc_turns_at_last"] = ac["cyc_turns"]
                    ac["cyc_omega_at_last"] = v[b]
                if ac["cyc_on"]:
                    ac["cyc_sum"] += T
                    ac["cyc_n"] += 1
                if s % per_unit == 0:
                    vbar = (P - v[b]) / (N - 1)
                    ac["wave"] = max(ac["wave"], max(
                        abs(v[j] - vbar) for j in range(N)
                        if min(abs(j - b), N - abs(j - b)) >= 2))
                    for j in range(N):
                        if min(abs(j - b), N - abs(j - b)) >= 1 and j != b - 1:
                            c = math.cos(th[(j + 1) % N] - th[j] - A[j])
                            ac["cmin"] = min(ac["cmin"], c)
                            ac["cmax"] = max(ac["cmax"], c)
        if record and record["from"] - 1e-9 <= Delta <= record["to"] + 1e-9:
            if s % int(round(record["dtf"] / dt)) == 0:
                h = site_energy(th, v, A, N)
                frames["h"].append([round(h[j] - h_pre[j], 4) for j in range(N)])
                frames["J"].append([round(x, 4) for x in J])
                frames["v"].append([round(x, 4) for x in v])
    out = {"dt": dt, "event_t": (event_step * dt if event_step else None),
           "worst_recursion_ratio": worst_rec,
           "worst_ring_identity_ratio": worst_ring,
           "samples": samples, "E_b_split": E_b_split, "windows": []}
    for k, (d0, d1) in enumerate(windows):
        ac = acc[k]
        n = ac["n"]
        if n == 0:
            out["windows"].append({"window": [d0, d1], "empty": True})
            continue
        Tw = n * dt
        Om = ac["omega"] / n
        out["windows"].append({
            "window": [d0, d1], "T": Tw, "omega_bar": Om,
            # a real sinusoid A cos(theta + phi) demodulated against
            # e^{-i theta} averages to A/2: the factor 2 restores A
            # (the L-9 anchor caught the missing factor at -0.500)
            "A": {str(d): 2.0 * abs(ac["lock"][d]) / n for d in offsets},
            "torque_mean": ac["torque"] / n, "Tmax": ac["Tmax"],
            "torque_floor": 2 * ac["Tmax"] / (Tw * (Om - 2.0)),
            "cycle": cycle_readout(ac, dt),
            "wave_amp": ac["wave"],
            "lockin_floor": 2 * ac["wave"] / (Tw * (Om - 2.0)),
            # the demodulated product carries a 2 Omega term whose
            # average over a window not tied to whole periods leaks
            # A_d / (Omega T) (the anchors read 2e-4 and 1e-4 relative
            # at Omega T = 2000 and 4900, which is this floor)
            "self_floor": {str(d): 2.0 * abs(ac["lock"][d]) / n / (Om * Tw)
                           for d in offsets},
            "cmin": ac["cmin"], "cmax": ac["cmax"]})
    if record:
        out["frames"] = frames
    return out


def cycle_readout(ac, dt):
    """Mean torque over an integer number of rotor turns, with the
    derived chirp floor A_T |dOmega/dt| / Omega^2 (the residual of a
    sinusoid with slowly varying frequency integrated over whole
    periods: 2 pi Omega_dot / Omega^3 per period)."""
    n = ac["cyc_n_at_last_turn"]
    if n == 0 or ac["cyc_turns_at_last"] < 1:
        return {"turns": 0}
    Tw = n * dt
    mean = ac["cyc_sum_at_last_turn"] / n
    om0, om1 = ac["cyc_omega_start"], ac["cyc_omega_at_last"]
    om = 0.5 * (om0 + om1)
    omdot = abs(om1 - om0) / Tw
    return {"turns": ac["cyc_turns_at_last"], "T": Tw, "mean": mean,
            "omega_start": om0, "omega_end": om1,
            "chirp_floor": ac["Tmax"] * omdot / (om * om),
            # the interpolated crossing leaves O(dt^2) of a step: the
            # residual window-end error is A_T (dt Omega)^2 / T_w
            "step_floor": ac["Tmax"] * (dt * om) ** 2 / Tw}


def linear_anchor(N=32, Omega=20.0, c=1.0, gamma=0.1, dt=0.001, T=100.0,
                  t_settle=300.0):
    """L-9 anchor: linear semi-infinite chain (site 0 free end, site
    N-1 clamped), unit force sin(Omega t) on site 0, same Euler-
    Cromer; lock-in over [t_settle, t_settle + T] against the drive
    phase. Returns measured vs closed-form A_1 and A_2/A_1."""
    x = [0.0] * N
    v = [0.0] * N
    steps = int(round((t_settle + T) / dt))
    lock = [0j, 0j, 0j]
    n = 0
    for s in range(steps):
        t = (s + 1) * dt
        for j in range(N - 1):
            a = -gamma * v[j]
            if j > 0:
                a += c * (x[j - 1] - x[j])
            a += c * (x[j + 1] - x[j])
            if j == 0:
                a += math.sin(Omega * t)
            v[j] += dt * a
        for j in range(N - 1):
            x[j] += dt * v[j]
        if t >= t_settle:
            n += 1
            e = cmath.exp(complex(0.0, -Omega * t))
            for d in range(3):
                lock[d] += v[d] * e
    A = [2.0 * abs(z) / n for z in lock]
    w, A1 = evanescent(Omega, c, gamma, dt)
    return {"Omega": Omega, "c": c, "gamma": gamma, "dt": dt,
            "A_measured": A, "A1_formula": A1, "w_abs": abs(w),
            "A1_rel_err": A[0] / A1 - 1.0, "self_floor_rel": 1.0 / (Omega * T),
            "ratio21_measured": A[1] / A[0], "ratio21_rel_err": (A[1] / A[0]) / abs(w) - 1.0,
            "ratio32_measured": A[2] / A[1], "ratio32_rel_err": (A[2] / A[1]) / abs(w) - 1.0}


def main():
    t0 = time.time()
    out = {}
    # the derived table for the registered cells
    N = 64
    fold = fold_fc(N, -math.pi)
    f = fold + 0.005
    table = {}
    for g in (0.02, 0.04, 0.1):
        Om = f / g
        w, A1 = evanescent(Om, math.cos(math.pi / (N - 2)), g, 0.001)
        table[str(g)] = {"Omega_terminal": Om, "w_abs": abs(w), "A1": A1,
                         "A2": A1 * abs(w), "A3": A1 * abs(w) ** 2,
                         "drift_pre": f / (N * g),
                         "spin_up_time": 1.0 / g}
    out["registered_table"] = table
    print(json.dumps(table, indent=1))

    # L-9 anchor: the lock-in pipeline on a linear chain
    anc = [linear_anchor(Omega=20.0, gamma=0.1),
           linear_anchor(Omega=49.0, gamma=0.04, t_settle=700.0)]
    out["anchor"] = anc
    for a in anc:
        print("anchor Omega %.0f: A1 rel err %.2e (2-Omega leakage floor %.1e), ratio21 rel err %.2e, ratio32 rel err %.2e"
              % (a["Omega"], a["A1_rel_err"], a["self_floor_rel"], a["ratio21_rel_err"], a["ratio32_rel_err"]))

    # validation cells at N = 32: gamma 0.1 and 0.04, the floors and
    # the lock-in on the real nonlinear aftermath
    val = {}
    for g, wins, after in ((0.1, [(100.0, 200.0)], 200.0),
                           (0.04, [(150.0, 250.0), (300.0, 400.0)], 400.0),
                           (0.02, [(100.0, 300.0), (300.0, 400.0)], 400.0)):
        N2 = 32
        fold2 = fold_fc(N2, -math.pi)
        f2 = fold2 + 0.005
        t1 = time.time()
        r = integrate_aftermath(N2, True, 0, g, f2, 0.001, windows=wins,
                                after_event=after)
        r["seconds"] = time.time() - t1
        r["f"] = f2
        r["fold"] = fold2
        # drift transfer readout
        sm = {int(d): (P, Pr, vb) for d, P, Pr, vb in r["samples"] if abs(d - round(d)) < 1e-9}
        Pr10 = sm[10][1] if 10 in sm else None
        Om10 = sm[10][2] if 10 in sm else None
        r["drift"] = {"P_ring_event": sm[0][1], "P_ring_10": Pr10, "omega_10": Om10,
                      "checks": {}}
        for D in (100, 200, 300):
            if D in sm and Pr10 is not None:
                pred = Pr10 * math.exp(-g * (D - 10))
                r["drift"]["checks"][str(D)] = {
                    "P_ring": sm[D][1], "pred": pred, "dev": sm[D][1] - pred,
                    "bound_4_over_omega10": 4.0 / Om10, "P": sm[D][0], "v_b": sm[D][2]}
        for wnd in r["windows"]:
            if wnd.get("empty"):
                continue
            Om = wnd["omega_bar"]
            cm = 0.5 * (wnd["cmin"] + wnd["cmax"])
            w, A1 = evanescent(Om, cm, g, 0.001)
            wl, A1l = evanescent(Om, wnd["cmin"], g, 0.001)
            wh, A1h = evanescent(Om, wnd["cmax"], g, 0.001)
            wnd["pred"] = {"A1": A1, "A1_band": sorted([A1l, A1h]),
                           "w_abs": abs(w), "w_band": sorted([abs(wl), abs(wh)])}
            A = wnd["A"]
            wnd["read"] = {"A1_rel": A["1"] / A1 - 1.0,
                           "A1_self_floor_rel": 1.0 / (Om * wnd["T"]),
                           "ratio21": A["2"] / A["1"],
                           "ratio21_rel": (A["2"] / A["1"]) / abs(w) - 1.0,
                           "ratio32": A["3"] / A["2"],
                           "floor_over_A2": wnd["lockin_floor"] / (A1 * abs(w)),
                           "floor_over_A3": wnd["lockin_floor"] / (A1 * abs(w) ** 2),
                           "torque_over_floor": abs(wnd["torque_mean"]) / wnd["torque_floor"],
                           "torque_scale_1pct_drift": 0.01 * g * sm[0][1]}
            cy = wnd["cycle"]
            if cy.get("turns", 0) > 0:
                om = 0.5 * (cy["omega_start"] + cy["omega_end"])
                cy["K"] = cy["mean"] * om ** 3 / g
                cy["K_floor"] = (cy["chirp_floor"] + cy["step_floor"]) * om ** 3 / g
                print("   cycle torque: %d turns mean %.3e floors chirp %.1e step %.1e -> K = %.4f (K floor %.1e)"
                      % (cy["turns"], cy["mean"], cy["chirp_floor"], cy["step_floor"],
                         cy["K"], cy["K_floor"]))
            print("gamma %g window %s: Omega %.2f A1 rel %.2e ratio21 rel %.2e "
                  "(floor/A2 %.2f, floor/A3 %.1f) ratio32 %.2e vs |w| %.2e; "
                  "torque mean %.2e floor %.2e"
                  % (g, wnd["window"], Om, wnd["read"]["A1_rel"],
                     wnd["read"]["ratio21_rel"], wnd["read"]["floor_over_A2"],
                     wnd["read"]["floor_over_A3"], wnd["read"]["ratio32"],
                     abs(w), wnd["torque_mean"], wnd["torque_floor"]), flush=True)
        print("gamma %g: event %.1f recursion worst %.3f ring-identity worst %.3f drift checks %s (%.0f s)"
              % (g, r["event_t"], r["worst_recursion_ratio"], r["worst_ring_identity_ratio"],
                 json.dumps({k: round(c["dev"], 4) for k, c in r["drift"]["checks"].items()}),
                 r["seconds"]), flush=True)
        print("   E_b split:", json.dumps({k: {a: round(b, 1) for a, b in d.items()}
                                          for k, d in r["E_b_split"].items()}))
        r.pop("samples")
        val[str(g)] = r
    out["validation_N32"] = val
    out["seconds"] = time.time() - t0
    with open(os.path.join(HERE, "p46_derive.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote p46_derive.json in %.0f s" % out["seconds"])


if __name__ == "__main__":
    main()
