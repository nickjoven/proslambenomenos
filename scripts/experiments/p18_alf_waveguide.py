#!/usr/bin/env python3
"""P-18 experiment: ALF locked periods on a bowed-string waveguide lie
on the lattice T0*(1 + m*(1-beta)) + eps, not on integer subharmonics.

Model (four ingredients, each necessary by ablation - see the note):
travelling-wave string (two delay loops joined at the bow), exact
per-sample stick-slip against a near-Coulomb falling friction curve,
DC-lossless end reflections (-g * onepole), damped torsional pair,
one-pole contact-width smoothing of the force injection.  String:
steel G, f0 = 196.9 Hz, L = 325 mm, d = 0.8 mm, rho = 7700 (the
arXiv:2502.11902 string).

Runs: m=1 locks at beta = 0.10, 0.13, 0.16 (bow speed 0.05 m/s, bow
force at mid-window), plus the m=2 lock at beta = 0.13.  Observable:
inter-slip onset intervals in the final window; the dominant cluster
(+/-15% of median) is the lock.

Outputs scripts/experiments/p18_results.json:
  runs: [{beta, force, m, lock_mean_T0, lock_std_T0, n_lock, n_all}]
  slope_dP_dbeta_T0: least-squares slope of the m=1 lock vs beta
  spacing_m2_m1_T0:  P(m=2) - P(m=1) at beta = 0.13
Stdlib only.  Deterministic (no RNG).
"""
import json
import math
import sys
from pathlib import Path

FS = 88200.0
F0 = 196.9
LENGTH = 0.325
DIAMETER = 0.8e-3
DENSITY = 7700.0
MU_S, MU_D, V0 = 0.8, 0.25, 0.01
G_NUT, A_NUT = 0.999, 0.40
G_BR, A_BR = 0.998, 0.70
Z_TORS_RATIO, C_TORS = 2.0, 3200.0
G_T, A_T = 0.98, 0.60
A_CONTACT = 0.70
V_BOW = 0.05
DURATION, WINDOW = 2.0, 1.0

RUNS = [
    # (beta, force, target m); forces hand-found during development -
    # each sits mid-plateau, not knife-edge: see p18_force_scan.py
    # (m=1 windows 1.15-1.65 / 0.95-1.20 / 0.90-1.05, m=2 1.60-1.90;
    # period drift <= 0.0155 T0 across any plateau)
    (0.10, 1.50, 1),
    (0.13, 1.10, 1),
    (0.16, 0.95, 1),
    (0.13, 1.70, 2),
]


def simulate(beta, force):
    """Integrate one string; return slip-onset times (s) in the final
    WINDOW seconds."""
    rho_l = DENSITY * math.pi * (DIAMETER / 2) ** 2
    c = 2.0 * LENGTH * F0
    Z = rho_l * c
    Zt = Z_TORS_RATIO * Z
    gamma = 1.0 / (2 * Z) + 1.0 / (2 * Zt)
    half_z, half_zt = 1.0 / (2 * Z), 1.0 / (2 * Zt)

    loop = FS / F0
    d_b = max(2, round(beta * loop))
    d_n = max(2, round((1 - beta) * loop))
    loop_t = FS * 2.0 * LENGTH / C_TORS
    dt_b = max(2, round(beta * loop_t))
    dt_n = max(2, round((1 - beta) * loop_t))

    buf_b, buf_n = [0.0] * d_b, [0.0] * d_n
    tb, tn = [0.0] * dt_b, [0.0] * dt_n
    pb = pn = ptb = ptn = 0
    lp_b = lp_n = lp_tb = lp_tn = f_sm = 0.0
    slipping = False
    k = force * gamma
    thr = MU_S * force * gamma
    ramp = int(0.01 * FS)

    n_steps = int(DURATION * FS)
    rec_start = n_steps - int(WINDOW * FS)
    onsets = []

    for n in range(n_steps):
        x_b = buf_b[pb]
        lp_b = (1 - A_BR) * x_b + A_BR * lp_b
        vi_b = -G_BR * lp_b
        lp_n = (1 - A_NUT) * buf_n[pn] + A_NUT * lp_n
        vi_n = -G_NUT * lp_n
        lp_tb = (1 - A_T) * tb[ptb] + A_T * lp_tb
        lp_tn = (1 - A_T) * tn[ptn] + A_T * lp_tn
        vi_tb, vi_tn = -G_T * lp_tb, -G_T * lp_tn
        vh = vi_b + vi_n + vi_tb + vi_tn

        vb = V_BOW * min(1.0, (n + 1) / ramp)
        cdiff = vb - vh
        cabs = abs(cdiff)
        s = 1.0 if cdiff >= 0 else -1.0

        stick_ok = cabs <= thr
        B = V0 - cabs + k * MU_D
        C = V0 * (k * MU_S - cabs)
        disc = B * B - 4 * C
        ambiguous = stick_ok and slipping and B < 0 and disc >= 0
        do_slip = (not stick_ok) or ambiguous

        if do_slip:
            x = 0.5 * (-B + math.sqrt(max(disc, 0.0)))
            vc = vb - s * max(x, 0.0)
        else:
            vc = vb
        F = (vc - vh) / gamma
        f_sm = (1 - A_CONTACT) * F + A_CONTACT * f_sm
        dv_tr, dv_to = f_sm * half_z, f_sm * half_zt

        slip_now = do_slip and abs(vc - vb) > 1e-9
        if n >= rec_start and slip_now and not slipping:
            onsets.append(n / FS)
        slipping = slip_now

        buf_b[pb] = vi_n + dv_tr
        buf_n[pn] = vi_b + dv_tr
        tb[ptb] = vi_tn + dv_to
        tn[ptn] = vi_tb + dv_to
        pb = (pb + 1) % d_b
        pn = (pn + 1) % d_n
        ptb = (ptb + 1) % dt_b
        ptn = (ptn + 1) % dt_n
    return onsets


def lock_stats(onsets):
    """Dominant-cluster mean/std of inter-onset intervals, in T0."""
    T0 = 1.0 / F0
    iv = [(b - a) / T0 for a, b in zip(onsets, onsets[1:])]
    big = [x for x in iv if x > 0.5]
    if len(big) < 3:
        return None
    med = sorted(big)[len(big) // 2]
    lock = [x for x in big if abs(x - med) < 0.15 * med]
    m = sum(lock) / len(lock)
    var = sum((x - m) ** 2 for x in lock) / len(lock)
    return m, math.sqrt(var), len(lock), len(big)


def main():
    out = {"runs": []}
    m1 = []
    for beta, force, m in RUNS:
        st = lock_stats(simulate(beta, force))
        if st is None:
            print(f"beta={beta} F={force}: no lock", file=sys.stderr)
            sys.exit(1)
        mean, std, n_lock, n_all = st
        pred = 1 + m * (1 - beta)
        print(f"beta={beta:.2f} F={force:.2f} m={m}: "
              f"lock {mean:.4f}+/-{std:.4f} T0  lattice {pred:.3f}  "
              f"(n={n_lock}/{n_all})")
        out["runs"].append({"beta": beta, "force": force, "m": m,
                            "lock_mean_T0": round(mean, 5),
                            "lock_std_T0": round(std, 5),
                            "n_lock": n_lock, "n_all": n_all})
        if m == 1:
            m1.append((beta, mean))

    xs = [b for b, _ in m1]
    ys = [p for _, p in m1]
    xbar, ybar = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / \
        sum((x - xbar) ** 2 for x in xs)
    p1 = next(r["lock_mean_T0"] for r in out["runs"]
              if r["beta"] == 0.13 and r["m"] == 1)
    p2 = next(r["lock_mean_T0"] for r in out["runs"]
              if r["beta"] == 0.13 and r["m"] == 2)
    out["slope_dP_dbeta_T0"] = round(slope, 4)
    out["spacing_m2_m1_T0"] = round(p2 - p1, 4)
    print(f"slope dP/dbeta = {slope:.3f} T0 (lattice: -1)")
    print(f"m2-m1 spacing at beta=0.13: {p2 - p1:.3f} T0 "
          f"(lattice: {1 - 0.13:.2f})")

    path = Path(__file__).with_name("p18_results.json")
    path.write_text(json.dumps(out, indent=1))
    print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
