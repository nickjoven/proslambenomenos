#!/usr/bin/env python3
"""P-26 experiment: the everpresent-Lambda scorecard on DESI DR2 BAO.

Runs AFTER the registration commit. Clauses (a)-(e) and the ensemble
spec are fixed in PREDICTIONS.md P-26 and p26_registration.json.

  (1) LCDM fit to the machine-parsed Table 4 (Omega_m free, scale
      s = c/(H0 r_d) profiled in closed form)         -> clause (a)
  (2) w0waCDM fit under the DESI priors               -> clause (b)
  (3) production-walk amplitude in no-backreaction
      EdS mode vs the derived 2 sqrt(165 pi) alpha    -> clause (c)
  (4) the Model 1 ensemble, cells and seeds as pinned -> (d), (e)

The beat threshold for (d) is the alpha = 0 realization at the LCDM
best-fit parameters run through the SAME native-grid pipeline, so
grid bias cancels in the comparison.

Results -> p26_results.json.  --bench runs the pre-registration
timing benchmark only (alpha 0.03, seed0 111, wall clock inspected).
"""
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import p26_derive as D
from kernels.minimize import golden_max, nelder_mead
from kernels.pmap import cell_seed, pmap

C_KMS = 299792.458
Z_EQ = 3400.0
A_INIT = 1e-5
STEPS = 512
SEED0 = 262626
ZEFFS = None  # filled from data


# ------------------------------------------------------------ realization
def init_lightcone_radiation(acc, a_i, t_i):
    """Initialize the eta-moment accumulator with the exact
    radiation-era closed forms at (a_i, t_i), so V starts at its
    physical value (8 pi/105) t_i^4 (DNY specify V_0 at the start;
    a zero-initialized V artificially amplifies early fluctuations).
    With a(t) = a_i (t/t_i)^{1/2}, eta(0..t) = (2/a_i) sqrt(t_i t):
      I0 = (2/5) a_i^3 t_i          I1 = (2/3) a_i^2 t_i^2
      I2 = (8/7) a_i   t_i^3        I3 = 2 t_i^4
    which reassemble to V(t_i) = (8 pi/105) t_i^4 exactly (EQ1)."""
    acc.eta = 2.0 * t_i / a_i
    acc.I = [0.4 * a_i ** 3 * t_i,
             (2.0 / 3.0) * a_i ** 2 * t_i ** 2,
             (8.0 / 7.0) * a_i * t_i ** 3,
             2.0 * t_i ** 4]
    eta = acc.eta
    acc.V = (4.0 * math.pi / 3.0) * (
        eta ** 3 * acc.I[0] - 3 * eta ** 2 * acc.I[1]
        + 3 * eta * acc.I[2] - acc.I[3])
    return acc.V


def run_realization(alpha, om, seed, steps=STEPS, a_init=A_INIT,
                    backreaction=True, keep_traj=False):
    """March the DNY Model 1 update self-consistently on a log-a grid.

    Units 8 pi G / 3 = 1: H^2 = rho_m + rho_r + rho_L with
    rho_m(a) = om a^-3, rho_r = (om/3400) a^-4, and S = rho_L V a
    Brownian walk with step (8 pi / 3) alpha xi sqrt(dV).
    Returns (alive, nodes) where nodes is the (a, E2) history
    (only if alive), plus the trajectory if keep_traj.
    """
    orad = om / Z_EQ
    rng = random.Random(seed)
    lna0, lna1 = math.log(a_init), 0.0
    acc = D.VAccumulator()
    S = 0.0
    rhoL = 0.0
    a_prev = a_init
    H0sq = om / a_init ** 3 + orad / a_init ** 4
    t = 1.0 / (2.0 * math.sqrt(H0sq))  # radiation-era age at a_init
    Vp = init_lightcone_radiation(acc, a_init, t)
    nodes_a = []
    nodes_E2 = []
    traj = [] if keep_traj else None
    for i in range(1, steps + 1):
        la_m = lna0 + (lna1 - lna0) * (i - 0.5) / steps
        a_new = math.exp(lna0 + (lna1 - lna0) * i / steps)
        a_m = math.exp(la_m)
        rho_bg = om / a_m ** 3 + orad / a_m ** 4
        H2 = rho_bg + (rhoL if backreaction else 0.0)
        if H2 <= 0.0:
            return False, None, None
        dt = (a_new - a_prev) / (a_m * math.sqrt(H2))
        t += dt
        V = acc.step(a_m, dt)
        dV = V - Vp
        Vp = V
        S += (8.0 * math.pi / 3.0) * alpha * rng.gauss(0.0, 1.0) \
            * math.sqrt(dV)
        rhoL = S / V
        # E2 always records rho_Lambda (the measurement); only the
        # marching H excludes it in no-backreaction validation mode
        E2 = om / a_new ** 3 + orad / a_new ** 4 + rhoL
        if backreaction and E2 <= 0.0:
            return False, None, None
        nodes_a.append(a_new)
        nodes_E2.append(E2)
        if keep_traj:
            traj.append((a_new, rhoL, rho_bg))
        a_prev = a_new
    return True, (nodes_a, nodes_E2), traj


def chi2_of_nodes(rows, nodes):
    """chi2 with s profiled, distances by cumulative trapezoid on the
    realization's own nodes (z ascending), E interpolated linearly in
    ln a on E^2 at the effective redshifts."""
    nodes_a, nodes_E2 = nodes
    E2_0 = nodes_E2[-1]
    zs = [1.0 / a - 1.0 for a in reversed(nodes_a)]
    E = [math.sqrt(e2 / E2_0) for e2 in reversed(nodes_E2)]
    # cumulative int dz / E from z = 0
    cum = [0.0]
    for i in range(1, len(zs)):
        cum.append(cum[-1] + 0.5 * (1.0 / E[i - 1] + 1.0 / E[i])
                   * (zs[i] - zs[i - 1]))
    def at(z):
        # find bracket (zs ascending)
        lo, hi = 0, len(zs) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if zs[mid] <= z:
                lo = mid
            else:
                hi = mid
        f = (z - zs[lo]) / (zs[hi] - zs[lo])
        dm = cum[lo] + f * (cum[hi] - cum[lo])
        e = E[lo] + f * (E[hi] - E[lo])
        return dm, 1.0 / e
    model = {}
    for r in rows:
        dm, dh = at(r["zeff"])
        if "DV_over_rd" in r:
            z = r["zeff"]
            model[r["tracer"]] = ((z * dm * dm * dh) ** (1.0 / 3.0),)
        else:
            model[r["tracer"]] = (dm, dh)
    s = D.profile_scale(rows, model)
    return D.chi2_blocks(rows, model, s), s


# ------------------------------------------------------------ smooth fits
def E2_w0wa(z, om, w0, wa):
    orad = om / Z_EQ
    a = 1.0 / (1.0 + z)
    fde = a ** (-3.0 * (1 + w0 + wa)) * math.exp(-3.0 * wa * (1 - a))
    return om * (1 + z) ** 3 + orad * (1 + z) ** 4 \
        + (1 - om - orad) * fde


def smooth_chi2(rows, om, w0=-1.0, wa=0.0, nz=4096):
    def E(z):
        return math.sqrt(E2_w0wa(z, om, w0, wa))
    model = D.model_from_E(rows, E, nz=nz)
    s = D.profile_scale(rows, model)
    return D.chi2_blocks(rows, model, s), s


def fit_lcdm(rows):
    om, _ = golden_max(lambda om: -smooth_chi2(rows, om)[0], 0.10, 0.60)
    chi2, s = smooth_chi2(rows, om)
    # s = (c/H0)/r_d with H0 = 100 h km/s/Mpc -> h r_d = (c/100)/s
    return {"Omega_m": om, "chi2": chi2, "s": s,
            "h_rd_Mpc": C_KMS / 100.0 / s}


def fit_w0wa(rows):
    scale = (0.03, 0.15, 0.4)

    def chi2_of(x):
        om, w0, wa = x
        pen = 0.0
        for v, lo, hi in ((om, 0.05, 0.7), (w0, -3.0, 1.0),
                          (wa, -3.0, 2.0)):
            if v < lo:
                pen += 1e4 * (lo - v) ** 2
            if v > hi:
                pen += 1e4 * (v - hi) ** 2
        return smooth_chi2(rows, min(max(om, 0.05), 0.7),
                           min(max(w0, -3), 1),
                           min(max(wa, -3), 2))[0] + pen
    best = None
    for x0 in ((0.30, -1.0, 0.0), (0.35, -0.5, -1.5),
               (0.30, -0.7, -1.0), (0.25, -0.9, -0.5),
               (0.40, -0.3, -2.5)):
        # nelder_mead maximizes with a scalar step: run in units of
        # the per-parameter scales
        g = lambda u: -chi2_of([x0[i] + scale[i] * u[i]
                                for i in range(3)])
        u_best, f_best = nelder_mead(g, [0.0, 0.0, 0.0], 1.0,
                                     iters=800)
        x = [x0[i] + scale[i] * u_best[i] for i in range(3)]
        if best is None or -f_best < best[1]:
            best = (x, -f_best)
    (om, w0, wa), chi2 = best
    _, s = smooth_chi2(rows, om, w0, wa)
    return {"Omega_m": om, "w0": w0, "wa": wa, "chi2": chi2, "s": s}


# ------------------------------------------------------------ ensemble
def shard_worker(cell):
    alpha, om, shard, n_shard, thresh, rows = cell
    n_alive = 0
    n_beat = 0
    best = (1e30, -1)
    chis = []
    for k in range(n_shard):
        seed = cell_seed(SEED0, repr(alpha), repr(om), shard, k)
        alive, nodes, _ = run_realization(alpha, om, seed)
        if not alive:
            continue
        n_alive += 1
        c2, _ = chi2_of_nodes(rows, nodes)
        chis.append(c2)
        if c2 < thresh:
            n_beat += 1
        if c2 < best[0]:
            best = (c2, seed)
    chis.sort()
    q = [chis[int(f * (len(chis) - 1))] for f in
         (0.05, 0.25, 0.5, 0.75, 0.95)] if chis else []
    return {"alpha": alpha, "om": om, "shard": shard,
            "n": n_shard, "alive": n_alive, "beat": n_beat,
            "best_chi2": best[0], "best_seed": best[1],
            "quantiles": q}


def run_ensemble(rows, thresh, spec):
    cells = []
    n_shards = 16
    for c in spec["main_cells"] + spec["sensitivity_cells"]:
        per = c["N_seeds"] // n_shards
        for sh in range(n_shards):
            cells.append((c["alpha"], c["Omega_m"], sh, per,
                          thresh, rows))
    results = pmap(shard_worker, cells, processes=16)
    agg = {}
    for r in results:
        key = (r["alpha"], r["om"])
        a = agg.setdefault(key, {"n": 0, "alive": 0, "beat": 0,
                                 "best_chi2": 1e30, "best_seed": -1,
                                 "median_chi2": []})
        a["n"] += r["n"]
        a["alive"] += r["alive"]
        a["beat"] += r["beat"]
        if r["best_chi2"] < a["best_chi2"]:
            a["best_chi2"] = r["best_chi2"]
            a["best_seed"] = r["best_seed"]
        if r["quantiles"]:
            a["median_chi2"].append(r["quantiles"][2])
    for a in agg.values():
        med = sorted(a["median_chi2"])
        a["median_chi2"] = med[len(med) // 2] if med else None
    return agg


# ------------------------------------------------------------ main
def main():
    pin = D.load_table4()
    rows = pin["rows"]
    reg = json.load(open(os.path.join(HERE, "p26_registration.json")))
    spec = reg["ensemble_spec"]
    out = {"clauses": {}}

    if "--bench" in sys.argv:
        t0 = time.time()
        n_dead = 0
        for k in range(200):
            alive, nodes, _ = run_realization(0.03, 0.2975,
                                              cell_seed(111, k))
            if alive:
                chi2_of_nodes(rows, nodes)
            else:
                n_dead += 1
        print(f"bench: 200 realizations in {time.time() - t0:.1f}s "
              f"(wall clock only)")
        return 0

    print("== (1) LCDM fit — clause (a)")
    lcdm = fit_lcdm(rows)
    h_rd = lcdm["h_rd_Mpc"]
    ok_a = (abs(lcdm["Omega_m"] - 0.2975) <= 0.0086
            and abs(h_rd - 101.54) <= 0.73)
    print(f"  Omega_m {lcdm['Omega_m']:.4f} (pub 0.2975 +- 0.0086), "
          f"h r_d {h_rd:.2f} Mpc (pub 101.54 +- 0.73), "
          f"chi2 {lcdm['chi2']:.2f}/11 dof  "
          f"{'ok' if ok_a else 'FAIL'}")
    out["lcdm"] = lcdm
    out["clauses"]["a"] = ok_a
    if not ok_a:
        print("clause (a) FAILED - instrument fault, halting scorecard "
              "per registration")
        json.dump(out, open(os.path.join(HERE, "p26_results.json"),
                            "w"), indent=1)
        return 1

    print("== (2) w0waCDM fit — clause (b)")
    ww = fit_w0wa(rows)
    dchi2 = lcdm["chi2"] - ww["chi2"]
    ok_b = (2.0 <= dchi2 <= 8.5 and ww["w0"] > -1.0 and ww["wa"] < 0.0)
    print(f"  w0 {ww['w0']:.3f}, wa {ww['wa']:.3f}, Omega_m "
          f"{ww['Omega_m']:.4f}, dchi2 {dchi2:.3f} "
          f"(band [2.0, 8.5], quadrant w0>-1, wa<0)  "
          f"{'ok' if ok_b else 'FAIL'}")
    out["w0wa"] = ww
    out["w0wa"]["dchi2"] = dchi2
    out["clauses"]["b"] = ok_b

    print("== (3) production-walk amplitude — clause (c)")
    alpha_c = 0.01
    M = 4000
    vals = []
    for w in range(M):
        alive, nodes, _ = run_realization(
            alpha_c, 1.0, cell_seed(SEED0, "eds", w),
            backreaction=False)
        # om=1 mode: E2 at a=1 is om + rhoL (orad = om/3400 small)
        nodes_a, nodes_E2 = nodes
        bg = 1.0 + 1.0 / Z_EQ
        vals.append((nodes_E2[-1] - bg) / bg)
    mean = sum(vals) / M
    var = sum((x - mean) ** 2 for x in vals) / (M - 1)
    sig = math.sqrt(var)
    cm = reg["EQ2"]["sigma_over_alpha_matter"]
    se = sig / math.sqrt(2 * (M - 1))
    tol = 3 * se + 0.01 * cm * alpha_c
    ok_c = abs(sig - cm * alpha_c) <= tol
    print(f"  sigma_OmegaLambda {sig:.5f} vs {cm * alpha_c:.5f} "
          f"(tol {tol:.5f})  {'ok' if ok_c else 'FAIL'}")
    out["amplitude"] = {"measured": sig, "derived": cm * alpha_c,
                        "tol": tol}
    out["clauses"]["c"] = ok_c

    print("== (4) beat threshold: best-fit LCDM E^2 on the native grid")
    # the LCDM best fit evaluated through the SAME native-node
    # pipeline as every realization, so grid bias cancels in the
    # beat comparison (an alpha = 0 realization is NOT LCDM - it is
    # Einstein-de Sitter, since the walk is the only dark energy)
    om_l = lcdm["Omega_m"]
    lna0, lna1 = math.log(A_INIT), 0.0
    nodes_a = [math.exp(lna0 + (lna1 - lna0) * i / STEPS)
               for i in range(1, STEPS + 1)]
    nodes_E2 = [E2_w0wa(1.0 / a - 1.0, om_l, -1.0, 0.0)
                for a in nodes_a]
    thresh, _ = chi2_of_nodes(rows, (nodes_a, nodes_E2))
    print(f"  native-grid LCDM chi2 = {thresh:.4f} "
          f"(smooth-grid {lcdm['chi2']:.4f}, grid bias "
          f"{thresh - lcdm['chi2']:+.4f})")
    out["thresh_native"] = thresh

    print("== (5) Model 1 ensemble")
    t0 = time.time()
    agg = run_ensemble(rows, thresh, spec)
    print(f"  ensemble wall clock {time.time() - t0:.0f}s")
    cells_out = []
    ok_d = True
    surv_main = []
    for (alpha, om), a in sorted(agg.items()):
        n = a["n"]
        K = a["beat"]
        if a["alive"] == 0:
            dbest = bought = None
        else:
            dbest = thresh - a["best_chi2"]
            bought = dbest / (2 * math.log(2))
        spent = math.log2(n / max(K, 1)) + spec["n_cells_price_bits"]
        # a cell with no survivor certainly cannot net positive
        net = (bought - spent) if bought is not None else -spent
        surv = a["alive"] / n
        if om == 0.2975:
            surv_main.append((alpha, surv))
        floor = (K == 0)
        cell = {"alpha": alpha, "Omega_m": om, "n": n,
                "alive": a["alive"], "survival": surv, "K_beat": K,
                "best_chi2": a["best_chi2"], "best_seed": a["best_seed"],
                "median_chi2": a["median_chi2"],
                "dchi2_best": dbest, "bits_bought": bought,
                "bits_spent": spent, "spent_is_floor": floor,
                "net_bits": net}
        cells_out.append(cell)
        if net > 0:
            ok_d = False
        bc = (f"{a['best_chi2']:8.3f}" if a["alive"] else "    none")
        bo = (f"{bought:+7.3f}" if bought is not None else "   none")
        print(f"  alpha {alpha:<6} om {om:<7} surv {surv:6.4f} "
              f"K {K:5d} best chi2 {bc} bought {bo} "
              f"spent {spent:6.3f}{'(floor)' if floor else '       '}"
              f" net {net:+8.3f}")
    out["cells"] = cells_out
    out["clauses"]["d"] = ok_d
    print(f"  clause (d) net <= 0 in every cell: "
          f"{'ok' if ok_d else 'FAIL'}")

    surv_main.sort()
    ok_e = all(surv_main[i][1] >= surv_main[i + 1][1] - 1e-9
               for i in range(len(surv_main) - 1))
    print(f"  clause (e) survival monotone in alpha: "
          f"{[f'{a}:{s:.3f}' for a, s in surv_main]}  "
          f"{'ok' if ok_e else 'FAIL'}")
    out["clauses"]["e"] = ok_e

    # context row (reported, not a clause): w0wa priced by the
    # declared MDL convention (k/2) log2(13)
    mdl = 2 / 2.0 * math.log2(13) * 2 / 2  # (k/2) log2(n), k=2
    out["w0wa_context"] = {
        "bits_bought": dchi2 / (2 * math.log(2)),
        "mdl_price_bits": math.log2(13),
        "net_bits": dchi2 / (2 * math.log(2)) - math.log2(13)}
    print(f"== context: w0wa bought {out['w0wa_context']['bits_bought']:.2f}"
          f" bits at MDL price {math.log2(13):.2f} -> net "
          f"{out['w0wa_context']['net_bits']:+.2f} bits (reported, "
          f"not a clause)")

    json.dump(out, open(os.path.join(HERE, "p26_results.json"), "w"),
              indent=1)
    print("results -> p26_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
