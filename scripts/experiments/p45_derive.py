#!/usr/bin/env python3
"""P-45 derive layer: the site-energy continuity identity of the
P-35/P-36 inertial pi ring, its floating-point residual bound, its
telescoping, the mutants that must fail (L-8: verified here, not
assumed), and the Euler-Cromer energy-balance defect ladder at two
validation cells - the smooth pre-onset regime and the rotor regime
the P-36 slip produces. Everything a registered clause of P-45
depends on is measured here BEFORE registration and written to
p45_derive.json; the runner (p45_continuity.py) imports this
module's definitions and reruns nothing from this file.

THE IDENTITY. Equation of motion (p36_ring.py, unchanged):
    theta_dd_j = -gamma v_j + sin(D_j) - sin(D_{j-1}) + f delta_{jb}
    D_j = theta_{j+1} - theta_j - A_j      (covariant bond strain)
Site energy and bond current in the lattice heat-transport
convention (Lepri-Livi-Politi 2003 eqs. 11 and 17 with a = 1,
V(D) = 1 - cos D, F = -V' = -sin D):
    u_j = 1 - cos(D_j)
    h_j = v_j^2 / 2 + (u_{j-1} + u_j) / 2
    J_j = -(1/2) sin(D_j) (v_j + v_{j+1})    (current from j to j+1)
Then, by the chain rule and nothing else,
    dh_j/dt + (J_j - J_{j-1}) = -gamma v_j^2 + f v_j delta_{jb}.
Local change plus current divergence equals local dissipation plus
local injection; summed over the ring the current telescopes away:
    dE/dt = f v_b - gamma sum_j v_j^2.
A enters only through D: the identity carries no seam term.

RESIDUAL BOUND (clauses a-c): the residual of the identity at a
random state is evaluated in double precision from ~30 rounded
operations on terms whose absolute sum T_j is computed alongside;
the registered bound is 32 eps T_j per site (eps = 2^-52), i.e.
the floating-point floor scaled by the state's own term
magnitudes - no fixed number is guessed, and the bound scales
with the velocity scale of the ensemble automatically.

DEFECT LADDER (clauses d, e): under Euler-Cromer (v' = v + dt a,
theta' = theta + dt v', the P-36 order), the discrete balance uses
force-times-displacement bookkeeping: injection f dt v'_b (exact
work of the load over the step), dissipation gamma dt v'_j^2,
current post-step. The defect D(dt) = sup over unit samples of
|E(t) - E(0) - W_inj + W_diss| is first order: D = C dt + O(dt^2),
so the ratio r(dt) = D(dt) / D(dt/2) = 2 + O(dt). The registered
statement is the convergence itself (L-3: not a value window at a
fixed resolution): monotone decrease along dt, dt/2, dt/4 with
both ratios in the order-one discrimination band [2^0.5, 2^1.5]
(see first_order below). The two validation cells here pin what
the ladder reads where the asymptotic regime is known to hold,
and the rotor cell argues the step size (8c): the torn-out node
spins at ~ f/gamma, so dt0 is chosen with dt0 f/gamma ~ 0.1 rad
per step.

Run: python3 scripts/experiments/p45_derive.py
"""
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc, ground_state  # noqa: E402

EPS = 2.0 ** -52
TAU = 2 * math.pi
GAMMA = 0.02
OPS = 32  # upper count of rounding operations in one residual


def strains(th, A, N):
    return [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]


def accel(th, v, A, gamma, f, b, N, sinD=None):
    if sinD is None:
        sinD = [math.sin(D) for D in strains(th, A, N)]
    return [sinD[j] - sinD[j - 1] - gamma * v[j] + (f if j == b else 0.0)
            for j in range(N)]


def site_energy(th, v, A, N, mutant=None):
    if mutant == "gauge-blind":
        u = [1.0 - math.cos(th[(j + 1) % N] - th[j]) for j in range(N)]
    else:
        u = [1.0 - math.cos(D) for D in strains(th, A, N)]
    return [0.5 * v[j] ** 2 + 0.5 * (u[j - 1] + u[j]) for j in range(N)]


def bond_current(th, v, A, N, sinD=None, mutant=None):
    if sinD is None:
        sinD = [math.sin(D) for D in strains(th, A, N)]
    if mutant == "current-blind":
        return [-sinD[j] * v[j] for j in range(N)]
    return [-0.5 * sinD[j] * (v[j] + v[(j + 1) % N]) for j in range(N)]


def residuals(th, v, A, gamma, f, b, N, mutant=None):
    """Per-site residual of the continuity identity at one state
    (derivatives by the chain rule from the EOM; no dt anywhere),
    the per-site term-magnitude sum T_j, and the global pieces.
    Returns (r, T, global_residual, global_T, telescoping_sum)."""
    D = strains(th, A, N)
    sinD = [math.sin(x) for x in D]
    if mutant == "gauge-blind":
        sin_u = [math.sin(th[(j + 1) % N] - th[j]) for j in range(N)]
    else:
        sin_u = sinD
    a = accel(th, v, A, gamma, f, b, N, sinD)
    J = bond_current(th, v, A, N, sinD, mutant)
    r, T = [], []
    for j in range(N):
        jn = (j + 1) % N
        # dh_j/dt by the chain rule: v a + (du_{j-1} + du_j)/2
        dh = (v[j] * a[j]
              + 0.5 * sin_u[j - 1] * (v[j] - v[j - 1])
              + 0.5 * sin_u[j] * (v[jn] - v[j]))
        div = J[j] - J[j - 1]
        sink = (0.0 if mutant == "sink-blind" else gamma * v[j] ** 2)
        src = f * v[j] if j == b else 0.0
        r.append(dh + div + sink - src)
        T.append(abs(v[j] * a[j]) + abs(0.5 * sin_u[j - 1] * (v[j] - v[j - 1]))
                 + abs(0.5 * sin_u[j] * (v[jn] - v[j])) + abs(J[j])
                 + abs(J[j - 1]) + abs(sink) + abs(src))
    # global: dE/dt straight from E = sum v^2/2 + sum u (a different
    # code path from the site sum), against injection - dissipation
    dE = sum(v[j] * a[j] for j in range(N)) + sum(
        sin_u[j] * (v[(j + 1) % N] - v[j]) for j in range(N))
    sink_tot = 0.0 if mutant == "sink-blind" else gamma * sum(x * x for x in v)
    g = dE - f * v[b] + sink_tot
    gT = (sum(abs(v[j] * a[j]) for j in range(N))
          + sum(abs(sin_u[j] * (v[(j + 1) % N] - v[j])) for j in range(N))
          + abs(f * v[b]) + sink_tot)
    tele = sum(J[j] - J[j - 1] for j in range(N))
    teleT = sum(abs(x) for x in J)
    return r, T, g, gT, tele, teleT


def random_state(rng, N, vmax):
    th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
    v = [rng.uniform(-vmax, vmax) for _ in range(N)]
    return th, v


def ensemble(rng, N, twisted, vmax, M, f, gamma=GAMMA, mutant=None):
    """Worst residual / bound ratios over M random states."""
    A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
    b = N // 2
    worst = 0.0        # max_j |r_j| / (OPS eps T_j)
    worst_abs = 0.0
    worst_seam = 0.0   # the two sites the pi bond touches (0 and 1)
    worst_g = 0.0
    worst_g_abs = 0.0
    worst_tele = 0.0
    worst_tele_ratio = 0.0
    for _ in range(M):
        th, v = random_state(rng, N, vmax)
        r, T, g, gT, tele, teleT = residuals(th, v, A, gamma, f, b, N, mutant)
        for j in range(N):
            q = abs(r[j]) / (OPS * EPS * T[j])
            worst = max(worst, q)
            worst_abs = max(worst_abs, abs(r[j]))
            if j in (0, 1):
                worst_seam = max(worst_seam, q)
        worst_g = max(worst_g, abs(g) / (OPS * EPS * gT))
        worst_g_abs = max(worst_g_abs, abs(g))
        worst_tele = max(worst_tele, abs(tele))
        worst_tele_ratio = max(worst_tele_ratio, abs(tele) / (OPS * EPS * teleT))
    return {"M": M, "N": N, "twisted": twisted, "vmax": vmax,
            "worst_site_ratio": worst, "worst_site_abs": worst_abs,
            "worst_seam_ratio": worst_seam,
            "worst_global_ratio": worst_g, "worst_global_abs": worst_g_abs,
            "worst_telescoping_abs": worst_tele,
            "worst_telescoping_ratio": worst_tele_ratio}


def integrate(N, twisted, sector, gamma, f_target, dt, t_ramp=200.0,
              t_hold=100.0, after_event=None):
    """Euler-Cromer exactly as p36_ring.run_level (same update order,
    same soft ramp), with the discrete energy bookkeeping. Runs for
    t_ramp + t_hold, or, when after_event is given, until the P-36
    bond-slip event (max_j |D_j - D_j(0)| > 1.5 pi at a unit sample)
    plus after_event units. Returns the sup-norm global and local
    defects, the event time, and the final per-site decomposition."""
    A, th = ground_state(N, twisted, sector)
    v = [0.0] * N
    b = N // 2
    D0 = strains(th, A, N)
    sinD = [math.sin(x) for x in D0]
    h0 = site_energy(th, v, A, N)
    E0 = sum(h0)
    inflow = [0.0] * N
    diss = [0.0] * N
    inj = 0.0
    n_ramp = int(round(t_ramp / dt))
    n_total = int(round((t_ramp + t_hold) / dt))
    sample_every = int(round(1.0 / dt))
    sup_g = 0.0
    sup_l = 0.0
    event_t = None
    h_pre = h0
    s = 0
    while s < n_total:
        f = f_target * min(1.0, (s + 1) / n_ramp)
        for j in range(N):
            acc = sinD[j] - sinD[j - 1] - gamma * v[j] + (f if j == b else 0.0)
            v[j] += dt * acc
        for j in range(N):
            th[j] += dt * v[j]
        sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        J = [-0.5 * sinD[j] * (v[j] + v[(j + 1) % N]) for j in range(N)]
        for j in range(N):
            inflow[j] += dt * (J[j - 1] - J[j])
            diss[j] += gamma * dt * v[j] * v[j]
        inj += f * dt * v[b]
        s += 1
        if s % sample_every:
            continue
        t_now = s * dt
        h = site_energy(th, v, A, N)
        E = sum(h)
        dis_tot = sum(diss)
        sup_g = max(sup_g, abs((E - E0) - (inj - dis_tot)))
        for j in range(N):
            local = (h[j] - h0[j]) - (inflow[j] - diss[j]
                                      + (inj if j == b else 0.0))
            sup_l = max(sup_l, abs(local))
        if after_event is not None:
            if event_t is None:
                D = strains(th, A, N)
                if max(abs(D[j] - D0[j]) for j in range(N)) > 1.5 * math.pi:
                    event_t = t_now
                    n_total = s + int(round(after_event / dt))
                else:
                    h_pre = h
    h = site_energy(th, v, A, N)
    excess = [h[j] - h_pre[j] for j in range(N)]
    peak = max(abs(x) for x in excess)
    jmax = max(range(N), key=lambda j: abs(excess[j]))

    def offset(j):
        return min(abs(j - b), N - abs(j - b))
    radius = None
    if peak > 0:
        radius = max((offset(j) for j in range(N)
                      if abs(excess[j]) >= 0.1 * peak), default=0)
    return {"dt": dt, "t_end": s * dt, "event_t": event_t,
            "sup_global_defect": sup_g, "sup_local_defect": sup_l,
            "E_change": sum(h) - E0, "injected": inj,
            "dissipated": sum(diss),
            "footprint": {"peak_excess": peak, "peak_site_offset": offset(jmax),
                          "radius_10pct": radius,
                          "excess_by_offset": [
                              excess[(b + k) % N] for k in range(0, N // 2 + 1)]},
            "site_decomposition_b": {"dh": h[b] - h0[b], "inflow": inflow[b],
                                     "dissipated": diss[b], "injected": inj}}


def ladder(N, twisted, sector, gamma, f, dt0, **kw):
    runs = [integrate(N, twisted, sector, gamma, f, dt0 / 2 ** k, **kw)
            for k in range(3)]
    Dg = [r["sup_global_defect"] for r in runs]
    Dl = [r["sup_local_defect"] for r in runs]
    out = {"dts": [r["dt"] for r in runs], "global_defects": Dg,
           "local_defects": Dl,
           "r1_global": Dg[0] / Dg[1], "r2_global": Dg[1] / Dg[2],
           "r1_local": Dl[0] / Dl[1], "r2_local": Dl[1] / Dl[2],
           "event_t": [r["event_t"] for r in runs],
           "runs": runs}
    out["contracts_global"] = abs(out["r2_global"] - 2) < abs(out["r1_global"] - 2)
    out["contracts_local"] = abs(out["r2_local"] - 2) < abs(out["r1_local"] - 2)
    out["first_order_global"] = first_order(Dg)
    out["first_order_local"] = first_order(Dl)
    return out


ORDER_BAND = (math.sqrt(2.0), 2.0 * math.sqrt(2.0))


def first_order(D):
    """The registered ladder verdict: the defect decreases
    monotonically along dt, dt/2, dt/4 and both successive ratios
    lie in the order-one discrimination band [2^0.5, 2^1.5] - the
    geometric midpoints between the ratio 2 of a first-order scheme
    and the ratios 1 (no convergence) and 4 (second order) of its
    neighbours. Order is discrete; the midpoint band is the derived
    classifier. Contraction of |r - 2| itself is reported, not
    registered: the rotor validation cell showed it at noise level
    (deviations ~1e-3 at dt0, not first-order dominated)."""
    r1, r2 = D[0] / D[1], D[1] / D[2]
    return (D[0] > D[1] > D[2]
            and ORDER_BAND[0] <= r1 <= ORDER_BAND[1]
            and ORDER_BAND[0] <= r2 <= ORDER_BAND[1])


def main():
    t0 = time.time()
    out = {"eps": EPS, "ops": OPS, "gamma": GAMMA}
    N = 64
    fold_c = fold_fc(N, 0.0)
    fold_t0 = fold_fc(N, -math.pi)
    f_slip = fold_t0 + 0.005   # first P-36 grid level above the fold
    out["folds"] = {"control_N64": fold_c, "closed_form_2N_over_N-1": 2 * N / (N - 1),
                    "twist0_N64": fold_t0, "f_slip_cell": f_slip}

    # (a)-(c): the identity at random states, control and twisted,
    # two velocity scales (band-speed and rotor-speed).
    rng = random.Random(20260901)
    ens = []
    for twisted in (False, True):
        for vmax in (2.0, 100.0):
            e = ensemble(rng, N, twisted, vmax, 20000, f_slip)
            ens.append(e)
            print("ensemble twisted=%s vmax=%g: site ratio %.3f (abs %.1e) "
                  "seam %.3f global %.3f (abs %.1e) tele %.1e (ratio %.3f)"
                  % (twisted, vmax, e["worst_site_ratio"], e["worst_site_abs"],
                     e["worst_seam_ratio"], e["worst_global_ratio"],
                     e["worst_global_abs"], e["worst_telescoping_abs"],
                     e["worst_telescoping_ratio"]), flush=True)
    out["ensembles"] = ens

    # L-8: each mutant must actually fail, deterministically, before
    # it is pinned. Record where and how big.
    muts = {}
    for m in ("current-blind", "sink-blind", "gauge-blind"):
        rec = {}
        for twisted in (False, True):
            e = ensemble(random.Random(7), N, twisted, 2.0, 200, f_slip, mutant=m)
            rec["twisted" if twisted else "control"] = {
                "worst_site_abs": e["worst_site_abs"],
                "worst_seam_ratio": e["worst_seam_ratio"],
                "worst_site_ratio": e["worst_site_ratio"],
                "worst_global_abs": e["worst_global_abs"]}
        muts[m] = rec
        print("mutant", m, json.dumps(rec), flush=True)
    out["mutants"] = muts

    # (d) validation cell i: smooth pre-onset, control N = 64,
    # f = fold - 0.10, the P-36 dt = 0.02 ladder.
    t1 = time.time()
    cell_i = ladder(N, False, 0, GAMMA, fold_c - 0.10, 0.02, t_ramp=200.0, t_hold=100.0)
    cell_i["seconds"] = time.time() - t1
    print("cell i (smooth): D_global", cell_i["global_defects"],
          "r1 %.4f r2 %.4f" % (cell_i["r1_global"], cell_i["r2_global"]),
          "local r1 %.4f r2 %.4f" % (cell_i["r1_local"], cell_i["r2_local"]),
          "first-order", cell_i["first_order_global"], cell_i["first_order_local"],
          "contracts", cell_i["contracts_global"], cell_i["contracts_local"], flush=True)
    out["validation_smooth"] = {k: v for k, v in cell_i.items() if k != "runs"}

    # (d)/(e) validation cell ii: the rotor regime at small N, control
    # N = 16 at fold + 0.02 (event guaranteed: no equilibrium exists
    # above the fold), dt0 from the resolution argument.
    N2 = 16
    fold2 = fold_fc(N2, 0.0)
    f2 = fold2 + 0.02
    dt0 = 0.001
    out["rotor_resolution"] = {"rotor_speed_f_over_gamma": f2 / GAMMA,
                               "dt0": dt0, "rad_per_step": dt0 * f2 / GAMMA}
    t1 = time.time()
    cell_ii = ladder(N2, False, 0, GAMMA, f2, dt0, t_ramp=200.0, t_hold=200.0,
                     after_event=40.0)
    cell_ii["seconds"] = time.time() - t1
    print("cell ii (rotor N=16): events", cell_ii["event_t"],
          "D_global", cell_ii["global_defects"],
          "r1 %.4f r2 %.4f" % (cell_ii["r1_global"], cell_ii["r2_global"]),
          "local", cell_ii["local_defects"],
          "r1 %.4f r2 %.4f" % (cell_ii["r1_local"], cell_ii["r2_local"]),
          "first-order", cell_ii["first_order_global"], cell_ii["first_order_local"],
          "contracts", cell_ii["contracts_global"], cell_ii["contracts_local"],
          flush=True)
    print("  rotor footprint at dt0:", json.dumps(cell_ii["runs"][0]["footprint"]))
    print("  loaded-site decomposition:", json.dumps(cell_ii["runs"][0]["site_decomposition_b"]))
    out["validation_rotor"] = {k: v for k, v in cell_ii.items() if k != "runs"}
    out["validation_rotor"]["footprint_dt0"] = cell_ii["runs"][0]["footprint"]
    out["validation_rotor"]["site_b_dt0"] = cell_ii["runs"][0]["site_decomposition_b"]
    out["seconds_total"] = time.time() - t0
    with open(os.path.join(HERE, "p45_derive.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote p45_derive.json in %.0f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
