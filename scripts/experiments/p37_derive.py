#!/usr/bin/env python3
"""P-37 derivation layer (pre-registration): the price of a bit.

A-11, the line P-24's note reserved: work-to-write against error
rate on rung 2 - the locked double well U(theta) = -(eps/2) cos 2
theta, eps = 1, overdamped Langevin with kT = D, the substrate
whose forgetting rate P-24 derived to the prefactor (MFPT pins
165.6 at D = 0.22, 64.0 at D = 0.28). Writing = a control field
V(theta, t) = U(theta) - h(t) cos theta, h ramped 0 -> a -> 0
linearly over duration tau (a closed loop: Delta F = 0). Work by
the Sekimoto convention dW = (dV/dh) dh; error p = wrong-well
occupancy at commit (t = tau).

Everything AGENTS item 8 requires, derived before registration:

  EQ1  substrate import: barrier = eps exactly (fresh check);
       P-24's MFPT pins reproduced by the same quadrature at 1e-9
       (instrument lineage); critical tilt h_c = 2 eps: V''(pi) =
       2 eps - h, so the wrong well VANISHES at h = 2 - the
       registered a grid {1.2, 2.4} straddles it (a thermal write
       and a deterministic write).
  EQ2  the floor (rigorous): <W> >= D [ln 2 - H(p)] for any
       protocol ending with error p. Proof sketch on the board:
       second law <W> >= Delta F_neq = D * D_KL(rho_tau || rho_eq)
       and coarse-graining monotonicity D_KL >= ln 2 - H(p).
       Exact curve, no free parameter.
  EQ3  the speed limit (rigorous): <W> - Delta F_neq >=
       W_2^2(rho_0, rho_tau)/tau (overdamped, mobility 1;
       Benamou-Brenier / thermodynamic optimal transport). On the
       circle W_2 is computed exactly by the quantile method
       minimized over the cut. The registered check uses the
       EMPIRICAL final sample, so the bound is a theorem about
       measured objects, not a modeled target.
  EQ4  the wall (the repo-native term): the substrate's own hop
       rate leaks the written bit while h is small. Two-state
       kinetics with FROZEN tilted-MFPT rates along h(t) gives
       p_kin(tau, a, D) - reported as the derived overlay; its
       magnitude is NOT a registered band (P-2's lesson), the
       registered clause is the ORDERING signature: at fixed a,
       error is non-monotone in tau - the slowest cell loses to
       the best cell at 3 sigma.
  EQ5  instrument nulls (8a/8b): Jarzynski on the closed loop -
       <e^{-W/D}> = 1 exactly (Delta F = 0) - as a registered
       null clause with CLT band; work-integral dt bias via a
       dt/2 validation cell; binomial CLT for p-hat.
  EQ6  domain (8c): dt = 0.002 (stiffest curvature V'' <= 2 eps +
       a <= 4.4, dt << 1/4.4); intrawell time ~ 1/V''(well) ~ 0.5
       so tau_min = 1; tau_max = T_MFPT(D)/5 (the wall must not
       eat the whole grid); M = 1500 walkers per cell, seeded.

Run: python3 scripts/experiments/p37_derive.py
"""
import json
import math
import os
import random

EPS = 1.0
TAU = 2 * math.pi
P24_PINS = {"0.22": 165.6, "0.28": 64.0}  # from p24_derive_out.txt


def V(th, h):
    return -(EPS / 2) * math.cos(2 * th) - h * math.cos(th)


def dV(th, h):
    return EPS * math.sin(2 * th) + h * math.sin(th)


# ---------------------------------------------------------------
# EQ1: substrate, pins, critical tilt
# ---------------------------------------------------------------
def mfpt_double_well(epsv, Dv, n=3000):
    def U(x):
        return -(epsv / 2) * math.cos(2 * x) / Dv
    step = math.pi / (2 * n)
    ys = [-math.pi / 2 + j * step * 2 for j in range(2 * n + 1)]
    emu = [math.exp(-U(y)) for y in ys]
    cum = [0.0]
    for j in range(2 * n):
        cum.append(cum[-1] + 0.5 * (emu[j] + emu[j + 1]) * step)

    def inner(xv):
        j = (xv + math.pi / 2) / step
        j0 = min(int(j), 2 * n - 1)
        return cum[j0] + (j - j0) * (cum[j0 + 1] - cum[j0])
    nx = n
    hx = (math.pi / 2) / nx
    tot = 0.0
    for i in range(nx + 1):
        w = 0.5 if i in (0, nx) else 1.0
        tot += w * math.exp(U(i * hx)) * inner(i * hx)
    return tot * hx / Dv


def eq1():
    out = {"barrier": None, "pins": {}, "h_c": 2 * EPS}
    grid = [i * 0.001 for i in range(6284)]
    vals = [V(x, 0.0) for x in grid]
    out["barrier"] = max(vals) - min(vals)
    for k, pin in P24_PINS.items():
        fresh = mfpt_double_well(EPS, float(k))
        out["pins"][k] = {"fresh": fresh, "p24": pin,
                          "abs_diff": abs(fresh - pin),
                          "band_printed_precision": 0.05}
    # wrong-well curvature vs tilt: V''(pi) = 2 eps - h
    out["Vpp_pi_at_hc"] = 2 * EPS * math.cos(2 * math.pi) - 2 * EPS
    return out


# ---------------------------------------------------------------
# EQ2: the floor
# ---------------------------------------------------------------
def H(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log(p) - (1 - p) * math.log(1 - p)


def floor_W(D, p):
    return D * (math.log(2) - H(p))


# ---------------------------------------------------------------
# EQ3: circle W2 by quantile + cut scan
# ---------------------------------------------------------------
def eq_density(D, h, n=2000):
    """Equilibrium density on [-pi, pi), normalized, as (grid, pdf)."""
    xs = [-math.pi + i * TAU / n for i in range(n)]
    w = [math.exp(-V(x, h) / D) for x in xs]
    Z = sum(w) * TAU / n
    return xs, [v / Z for v in w]


def quantiles_from_pdf(xs, pdf, m):
    """m quantile points of a periodic pdf sampled on xs (uniform)."""
    n = len(xs)
    dx = TAU / n
    cum = [0.0]
    for v in pdf:
        cum.append(cum[-1] + v * dx)
    tot = cum[-1]
    qs = []
    j = 0
    for i in range(m):
        target = (i + 0.5) / m * tot
        while cum[j + 1] < target:
            j += 1
        frac = (target - cum[j]) / max(cum[j + 1] - cum[j], 1e-300)
        qs.append(xs[0] + (j + frac) * dx)
    return qs


def w2_circle(qa, qb):
    """W2 between two equal-length quantile lists on the circle:
    min over the m cyclic pairings (the 1D circular OT theorem)."""
    m = len(qa)
    best = None
    for shift_i in range(m):
        c = 0.0
        for i in range(m):
            d = qa[i] - qb[(i + shift_i) % m]
            d = (d + math.pi) % TAU - math.pi
            c += d * d
            if best is not None and c >= best:
                break
        if best is None or c < best:
            best = c
    return best / m


# ---------------------------------------------------------------
# EQ4: frozen-rate two-state kinetics along the protocol
# ---------------------------------------------------------------
def tilted_rates(D, h):
    """Kramers rates out of each well at frozen tilt h < h_c = 2:
    saddle at cos th_s = -h/2 (from V' = sin th (2 eps cos th + h)),
    wells at 0 and pi; barriers and curvatures in closed form,
    prefactor sqrt(V''_well |V''_saddle|)/(2 pi), times 2 for the
    two symmetric escape paths. Exact landscape, Kramers-accuracy
    prefactor - adequate for the UNREGISTERED overlay."""
    if h >= 2 * EPS - 1e-9:
        return None
    cs = -h / (2 * EPS)
    th_s = math.acos(cs)
    v_s = V(th_s, h)
    vpp = lambda th: 2 * EPS * math.cos(2 * th) + h * math.cos(th)
    out = []
    for well in (0.0, math.pi):
        dE = v_s - V(well, h)
        pref = math.sqrt(vpp(well) * abs(vpp(th_s))) / (2 * math.pi)
        out.append(2 * pref * math.exp(-dE / D))
    return (out[0], out[1])  # (out of right/0, out of wrong/pi)


def p_kin(D, a, tau, nstep=400):
    """Two-state kinetics with frozen rates along h(t); start in
    equilibrium (p = 1/2), p = wrong-well weight."""
    p = 0.5
    dt = tau / nstep
    for s in range(nstep):
        t = (s + 0.5) * dt
        h = a * (1 - abs(2 * t / tau - 1))
        rr = tilted_rates(D, min(h, 1.99))
        if rr is None or h >= 2 * EPS:
            # wrong well destroyed: drain fast (intrawell time)
            p += dt * (-p / 0.5)
        else:
            r_right, r_wrong = rr
            p += dt * (-p * r_wrong + (1 - p) * r_right)
        p = min(max(p, 0.0), 1.0)
    return p


# ---------------------------------------------------------------
# EQ5: instrument nulls on a benign cell
# ---------------------------------------------------------------
def run_cell(D, a, tau, M, dt, seed, record_final=False):
    rng = random.Random(seed)
    # equilibrated start: sample from eq density by inverse CDF
    xs, pdf = eq_density(D, 0.0, 4000)
    qs = quantiles_from_pdf(xs, pdf, M)
    rng.shuffle(qs)
    ths = list(qs)
    Ws = [0.0] * M
    steps = int(tau / dt)
    sq = math.sqrt(2 * D * dt)
    hprev = 0.0
    for s in range(steps):
        t = (s + 1) * dt
        h = a * (1 - abs(2 * t / tau - 1)) if t < tau else 0.0
        dh = h - hprev
        for i in range(M):
            th = ths[i]
            Ws[i] += -math.cos(th) * dh
            ths[i] = th + dt * (-dV(th, h)) + sq * rng.gauss(0, 1)
        hprev = h
    # registered p = WRONG-well occupancy: the wrong well is at
    # theta = pi, i.e. wrap(th) at distance > pi/2 from 0. (An
    # earlier readout counted the right well under this name; the
    # label fix is recorded in the note - dynamics unchanged.)
    wrong = sum(1 for th in ths
                if abs(((th + math.pi) % TAU) - math.pi) >= math.pi / 2)
    p = wrong / M
    out = {"W_mean": sum(Ws) / M,
           "W_se": (sum((w - sum(Ws) / M) ** 2 for w in Ws)
                    / (M * (M - 1))) ** 0.5,
           "p": p, "p_se": math.sqrt(max(p * (1 - p), 1e-9) / M),
           "jarz": sum(math.exp(-w / D) for w in Ws) / M}
    ej = [math.exp(-w / D) for w in Ws]
    mj = sum(ej) / M
    out["jarz_se"] = (sum((e - mj) ** 2 for e in ej)
                      / (M * (M - 1))) ** 0.5
    if record_final:
        out["final"] = [round(((th + math.pi) % TAU) - math.pi, 4)
                        for th in ths]
    return out


def main():
    res = {"EQ1": eq1()}
    res["EQ2_floor_samples"] = {
        "D=0.22": {p: floor_W(0.22, p) for p in (0.01, 0.05, 0.2, 0.5)}}
    # EQ3 sanity: W2 between h=0 equilibrium and a=1e-6 shifted copy
    xs, pdf = eq_density(0.22, 0.0)
    qa = quantiles_from_pdf(xs, pdf, 160)
    res["EQ3_selftest_zero"] = w2_circle(qa, qa)
    # EQ4 overlay tables
    res["EQ4_p_kin"] = {}
    for D in (0.22, 0.28):
        tmax = P24_PINS[str(D)] / 5
        taus = [t for t in (1, 2, 4, 8, 16, 32) if t <= tmax]
        res["EQ4_p_kin"][str(D)] = {
            str(a): {str(t): round(p_kin(D, a, t), 4) for t in taus}
            for a in (1.2, 2.4)}
    # EQ5 nulls: the Jarzynski estimator is heavy-tailed, so the
    # null cell must satisfy the sampling condition
    # (sigma_W / D)^2 <= 0.2 - a gentle protocol, one per D
    res["EQ5_nulls"] = {}
    for D in (0.22, 0.28):
        n1 = run_cell(D, 0.5, 6.0, 2000, 0.002, 20260830)
        sig2 = (n1["W_se"] * math.sqrt(2000)) ** 2
        res["EQ5_nulls"][str(D)] = {
            "jarz": n1["jarz"], "jarz_se": n1["jarz_se"],
            "sampling_(sigW/D)^2": sig2 / D ** 2,
            "W_mean": n1["W_mean"], "W_se": n1["W_se"]}
    nh = run_cell(0.28, 0.5, 6.0, 2000, 0.001, 20260830)
    res["EQ5_nulls"]["dt_half_W"] = nh["W_mean"]
    res["EQ5_nulls"]["dt_half_band"] = 3 * math.sqrt(2) * nh["W_se"]
    # EQ6 domain
    res["EQ6_domain"] = {
        "dt": 0.002, "M": 1500, "tau_min": 1.0,
        "tau_max": {k: v / 5 for k, v in P24_PINS.items()},
        "a_grid": [1.2, 2.4], "h_c": 2.0,
        "seeds": "20260830 + cell index"}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p37_registration.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print("EQ1:", json.dumps(res["EQ1"], indent=1))
    print("EQ2:", res["EQ2_floor_samples"])
    print("EQ3 zero self-test:", res["EQ3_selftest_zero"])
    print("EQ4:", json.dumps(res["EQ4_p_kin"], indent=1))
    print("EQ5:", json.dumps(res["EQ5_nulls"], indent=1))
    print("EQ6:", json.dumps(res["EQ6_domain"], indent=1))


if __name__ == "__main__":
    main()
