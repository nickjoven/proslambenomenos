#!/usr/bin/env python3
"""P-20 registered computation: the eps budget and the frame-
separability map.

Instruments the P-19 waveguide (same constants, same arithmetic - the
loop below mirrors p19_alf_waveguide.simulate step for step and a
self-check requires the committed P-19 lock means to reappear to the
committed rounding) and, per registered cell, measures:

  P        lock period (dominant slip-onset cluster, as P-19)
  eps_meas P - T0*(1 + m*(1-beta)), in T0
  S        slipping samples per lock cycle (slip-flag samples in the
           window / dominant-cluster interval count) - the registered
           observable, independent of the period offsets
  eps_pred (filter delays + delay-line rounding + S)/loop, with the
           fixed part read from p20_registration.json (pinned before
           any S was measured; nothing tuned here)

and simulates 3000 fps frame histograms per m=1 cell against a
synthetic exact-doubling comparator, then scores every registered
clause. Outcomes are recorded as they land; failed clauses are for
the R entry to diagnose, not for this script to rescue.

Deterministic, stdlib only. Writes p20_results.json.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p19_alf_waveguide as wg  # noqa: E402

REG = json.loads((HERE / "p20_registration.json").read_text())
FPS = REG["clause_c"]["fps"]
LOOP = wg.FS / wg.F0
T0 = 1.0 / wg.F0


def simulate_instrumented(beta, force):
    """p19_alf_waveguide.simulate with recorders: returns (onsets in
    seconds, slip-flag sample count in the window). Arithmetic is
    identical; the self-check in main() enforces that."""
    rho_l = wg.DENSITY * math.pi * (wg.DIAMETER / 2) ** 2
    c = 2.0 * wg.LENGTH * wg.F0
    Z = rho_l * c
    Zt = wg.Z_TORS_RATIO * Z
    gamma = 1.0 / (2 * Z) + 1.0 / (2 * Zt)
    half_z, half_zt = 1.0 / (2 * Z), 1.0 / (2 * Zt)

    loop = wg.FS / wg.F0
    d_b = max(2, round(beta * loop))
    d_n = max(2, round((1 - beta) * loop))
    loop_t = wg.FS * 2.0 * wg.LENGTH / wg.C_TORS
    dt_b = max(2, round(beta * loop_t))
    dt_n = max(2, round((1 - beta) * loop_t))

    buf_b, buf_n = [0.0] * d_b, [0.0] * d_n
    tb, tn = [0.0] * dt_b, [0.0] * dt_n
    pb = pn = ptb = ptn = 0
    lp_b = lp_n = lp_tb = lp_tn = f_sm = 0.0
    slipping = False
    k = force * gamma
    thr = wg.MU_S * force * gamma
    ramp = int(0.01 * wg.FS)

    n_steps = int(wg.DURATION * wg.FS)
    rec_start = n_steps - int(wg.WINDOW * wg.FS)
    onsets = []
    slip_samples = 0
    episodes = []          # diagnostic: run-lengths of the slip flag
    cur_ep = 0

    for n in range(n_steps):
        x_b = buf_b[pb]
        lp_b = (1 - wg.A_BR) * x_b + wg.A_BR * lp_b
        vi_b = -wg.G_BR * lp_b
        lp_n = (1 - wg.A_NUT) * buf_n[pn] + wg.A_NUT * lp_n
        vi_n = -wg.G_NUT * lp_n
        lp_tb = (1 - wg.A_T) * tb[ptb] + wg.A_T * lp_tb
        lp_tn = (1 - wg.A_T) * tn[ptn] + wg.A_T * lp_tn
        vi_tb, vi_tn = -wg.G_T * lp_tb, -wg.G_T * lp_tn
        vh = vi_b + vi_n + vi_tb + vi_tn

        vb = wg.V_BOW * min(1.0, (n + 1) / ramp)
        cdiff = vb - vh
        cabs = abs(cdiff)
        s = 1.0 if cdiff >= 0 else -1.0

        stick_ok = cabs <= thr
        B = wg.V0 - cabs + k * wg.MU_D
        C = wg.V0 * (k * wg.MU_S - cabs)
        disc = B * B - 4 * C
        ambiguous = stick_ok and slipping and B < 0 and disc >= 0
        do_slip = (not stick_ok) or ambiguous

        if do_slip:
            x = 0.5 * (-B + math.sqrt(max(disc, 0.0)))
            vc = vb - s * max(x, 0.0)
        else:
            vc = vb
        F = (vc - vh) / gamma
        f_sm = (1 - wg.A_CONTACT) * F + wg.A_CONTACT * f_sm
        dv_tr, dv_to = f_sm * half_z, f_sm * half_zt

        slip_now = do_slip and abs(vc - vb) > 1e-9
        if n >= rec_start:
            if slip_now and not slipping:
                onsets.append(n / wg.FS)
            if slip_now:
                slip_samples += 1
                cur_ep += 1
            elif cur_ep:
                episodes.append(cur_ep)
                cur_ep = 0
        slipping = slip_now

        buf_b[pb] = vi_n + dv_tr
        buf_n[pn] = vi_b + dv_tr
        tb[ptb] = vi_tn + dv_to
        tn[ptn] = vi_tb + dv_to
        pb = (pb + 1) % d_b
        pn = (pn + 1) % d_n
        ptb = (ptb + 1) % dt_b
        ptn = (ptn + 1) % dt_n
    if cur_ep:
        episodes.append(cur_ep)
    return onsets, slip_samples, episodes


def cluster_intervals(onsets):
    """(dominant-cluster onset pairs, lock mean in T0, n_lock) with
    the P-19 cluster rule: intervals > 0.5 T0, within 15% of the
    median such interval."""
    iv = [((b - a) / T0, a, b) for a, b in zip(onsets, onsets[1:])]
    big = [t for t in iv if t[0] > 0.5]
    if len(big) < 3:
        return None
    med = sorted(x for x, _, _ in big)[len(big) // 2]
    lock = [t for t in big if abs(t[0] - med) < 0.15 * med]
    mean = sum(x for x, _, _ in lock) / len(lock)
    return lock, mean, len(lock)


def measure(beta, force, m):
    onsets, slip_samples, episodes = simulate_instrumented(beta, force)
    got = cluster_intervals(onsets)
    if got is None:
        print(f"no lock at beta={beta} F={force}", file=sys.stderr)
        sys.exit(1)
    lock, mean, n_lock = got
    eps_meas = mean - (1 + m * (1 - beta))
    S = slip_samples / n_lock
    return {"beta": beta, "force": force, "m": m,
            "P_T0": round(mean, 5),
            "eps_meas_T0": round(eps_meas, 5),
            "slip_samples_window": slip_samples,
            "n_lock": n_lock,
            "S_samples": round(S, 3),
            "episodes_per_cycle": round(len(episodes) / n_lock, 3),
            "episode_mean_samples": round(sum(episodes) / len(episodes), 3),
            "episode_max_samples": max(episodes),
            "_onsets": onsets, "_lock": lock}


def frame_support(pairs, fps):
    return sorted({math.floor(b * fps) - math.floor(a * fps)
                   for _, a, b in pairs})


def frame_hist(pairs, fps):
    h = {}
    for _, a, b in pairs:
        k = math.floor(b * fps) - math.floor(a * fps)
        h[k] = h.get(k, 0) + 1
    return {str(k): v for k, v in sorted(h.items())}


def doubling_comparator(first_onset, n_intervals, fps):
    us = [first_onset + k * 2 * T0 for k in range(n_intervals + 1)]
    pairs = [(None, a, b) for a, b in zip(us, us[1:])]
    return frame_support(pairs, fps), frame_hist(pairs, fps)


def main():
    out = {"cells": [], "clauses": {}, "mind_change": {}}
    band = REG["clause_a"]["band_T0"]
    fixed = {(c["beta"], c["m"]): c["fixed_samples"] for c in REG["cells"]}

    # ---- self-check: the instrumented loop reproduces committed P-19
    p19 = json.loads((HERE / "p19_results.json").read_text())
    for r in p19["runs"]:
        cell = measure(r["beta"], r["force"], r["m"])
        if round(cell["P_T0"], 5) != r["lock_mean_T0"]:
            print(f"self-check FAILED: {cell['P_T0']} vs "
                  f"{r['lock_mean_T0']}", file=sys.stderr)
            sys.exit(1)
        cell["p19_lock_mean_T0"] = r["lock_mean_T0"]
        out["cells"].append(cell)
    print("self-check: instrumented loop reproduces all four committed "
          "P-19 lock means")

    kaw = REG["known_anchors"]["kawano_point"]
    cell = measure(kaw["beta"], kaw["force"], 1)
    cell["anchor_P_T0"] = kaw["P_T0"]
    out["cells"].append(cell)

    # ---- clause (a): the budget, cell by cell
    a_rows, a_ok = [], True
    for cell in out["cells"]:
        fx = fixed[(cell["beta"], cell["m"])]
        eps_pred = (fx + cell["S_samples"]) / LOOP
        resid = cell["eps_meas_T0"] - eps_pred
        ok = abs(resid) <= band
        a_ok &= ok
        cell["eps_pred_T0"] = round(eps_pred, 5)
        cell["resid_T0"] = round(resid, 5)
        cell["within_band"] = ok
        a_rows.append(cell)
        print(f"beta={cell['beta']:.6f} m={cell['m']} F={cell['force']}: "
              f"P {cell['P_T0']:.5f} T0, S {cell['S_samples']:.2f} "
              f"samples, eps_meas {cell['eps_meas_T0']:.5f}, eps_pred "
              f"{eps_pred:.5f}, resid {resid:+.5f} T0 "
              f"[{'ok' if ok else 'OUTSIDE BAND'}]")

    m1 = [c for c in out["cells"] if c["m"] == 1
          and c["beta"] in (0.10, 0.13, 0.16)]
    m1.sort(key=lambda c: c["beta"])
    signs_ok = True
    for lo, hi in zip(m1, m1[1:]):
        dm = hi["eps_meas_T0"] - lo["eps_meas_T0"]
        dp = hi["eps_pred_T0"] - lo["eps_pred_T0"]
        same = (dm > 0) == (dp > 0)
        signs_ok &= same
        print(f"  sign {lo['beta']}->{hi['beta']}: d_eps_meas {dm:+.5f}, "
              f"d_eps_pred {dp:+.5f} [{'same' if same else 'OPPOSITE'}]")
    out["clauses"]["a_band"] = a_ok
    out["clauses"]["a_signs"] = signs_ok

    # ---- clause (b): force trend inside the plateaus
    b_ok = True
    drift = REG["clause_b"]["drift_band_T0"]
    floor_ = REG["clause_b"]["sign_floor_T0"]
    out["force_trend"] = {}
    for bkey, ladder in REG["clause_b"]["force_ladders"].items():
        beta = float(bkey)
        rows = []
        for F in ladder:
            c = next((c for c in out["cells"]
                      if c["beta"] == beta and c["force"] == F
                      and c["m"] == 1), None)
            if c is None:
                c = measure(beta, F, 1)
            rows.append({"F": F, "eps_meas_T0": c["eps_meas_T0"],
                         "S_samples": c["S_samples"]})
        es = [r["eps_meas_T0"] for r in rows]
        rng = max(es) - min(es)
        rng_ok = rng < drift
        de = rows[-1]["eps_meas_T0"] - rows[0]["eps_meas_T0"]
        dS = rows[-1]["S_samples"] - rows[0]["S_samples"]
        if abs(de) > floor_:
            dir_ok = (de > 0) == (dS > 0)
            dir_note = "tracks" if dir_ok else "OPPOSES"
        else:
            dir_ok, dir_note = True, "vacuous (|d eps| <= 0.002)"
        b_ok &= rng_ok and dir_ok
        out["force_trend"][bkey] = {
            "rows": rows, "range_T0": round(rng, 5),
            "range_ok": rng_ok, "direction": dir_note}
        print(f"plateau beta={bkey}: eps range {rng:.5f} T0 "
              f"[{'ok' if rng_ok else 'OVER'}], S-direction {dir_note} "
              f"(d_eps {de:+.5f}, d_S {dS:+.3f})")
    out["clauses"]["b"] = b_ok

    # ---- clause (c): frame histograms vs the doubling comparator
    c_ok = True
    out["frames"] = {}
    mind_c = False
    for cell in out["cells"]:
        if cell["m"] != 1:
            continue
        pairs = cell["_lock"]
        sup = frame_support(pairs, FPS)
        hist = frame_hist(pairs, FPS)
        dsup, dhist = doubling_comparator(cell["_onsets"][0],
                                          len(pairs), FPS)
        ov = sorted(set(sup) & set(dsup))
        reg_no = any(abs(cell["beta"] - b) < 1e-9
                     for b in REG["clause_c"]["no_overlap_betas"])
        reg_ov = any(abs(cell["beta"] - b) < 1e-9
                     for b in REG["clause_c"]["overlap_betas"])
        if reg_no:
            ok = not ov
            side = "no-overlap side"
        elif reg_ov:
            ok = bool(ov)
            side = "overlap side"
        else:
            ok, side = True, "inside margin band (untested)"
        c_ok &= ok
        Dreg = next(c["D_frames"] for c in REG["cells"]
                    if abs(c["beta"] - cell["beta"]) < 1e-9 and c["m"] == 1)
        if ov and Dreg is not None and Dreg >= 1.5:
            mind_c = True
        out["frames"][f"{cell['beta']:.6f}"] = {
            "lattice_hist": hist, "doubling_hist": dhist,
            "overlap_frames": ov, "registered_side": side,
            "D_frames_registered": Dreg, "ok": ok}
        print(f"frames beta={cell['beta']:.6f}: lattice {hist} vs "
              f"doubling {dhist} -> overlap {ov or 'none'} "
              f"({side}) [{'ok' if ok else 'AGAINST REGISTRATION'}]")
    out["clauses"]["c"] = c_ok

    # ---- mind-change conditions
    worst = max(abs(c["resid_T0"]) for c in out["cells"])
    mind_a = worst > 2 * band
    out["mind_change"] = {
        "eps_decomposition_killed": mind_a,
        "worst_resid_T0": round(worst, 5),
        "separability_arithmetic_killed": mind_c,
    }
    print(f"mind-change: eps decomposition "
          f"{'KILLED' if mind_a else 'stands'} (worst resid "
          f"{worst:.5f} T0 vs 0.030); separability arithmetic "
          f"{'KILLED' if mind_c else 'stands'}")

    for c in out["cells"]:
        c.pop("_onsets", None)
        c.pop("_lock", None)
    ok_all = a_ok and signs_ok and b_ok and c_ok
    out["all_registered_clauses_held"] = ok_all
    path = HERE / "p20_results.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print(f"all registered clauses held: {ok_all}")
    print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
