#!/usr/bin/env python3
"""P-26 derivation layer (pre-registration): the everpresent-Lambda
scorecard on DESI DR2 BAO. Sorkin's causal-set argument (catalog c31)
says Lambda fluctuates with sigma ~ 1/sqrt(V) of the observer's past
lightcone 4-volume; Das-Nasiri-Yazdi (arXiv 2307.13743) give the
concrete Model 1 update, and DESI DR2 (arXiv 2503.14738) is the live
dataset that prefers evolving dark energy. P-26 prices all three
stories - LCDM, w0waCDM, everpresent-Lambda Model 1 - in the bit
accounting against the one likelihood we can recompute honestly:
the DR2 BAO Table 4 Gaussian compression. Everything here has a
derivable answer and runs before the registered ensembles.

Derived facts:
  EQ1  the past-lightcone 4-volume closed forms: in exact matter
       domination (a ~ t^{2/3}) V(t) = (3 pi / 55) t^4 and in exact
       radiation domination (a ~ t^{1/2}) V(t) = (8 pi / 105) t^4,
       both from Beta-function integrals; the production incremental
       accumulator (eta-moment expansion, O(1) per step) reproduces
       both on its own log-a grid.
  EQ2  the dimensionless fluctuation amplitude of Model 1: with
       sigma_Lambda = 8 pi alpha / sqrt(V) (the DNY update's
       stationary std) the fluctuation RELATIVE TO CRITICAL is
       sigma_OmegaLambda = 2 sqrt(165 pi) alpha  = 45.535 alpha  (matter era)
       sigma_OmegaLambda = (8/3) sqrt(210 pi) alpha = 68.494 alpha (radiation era)
       - exact, era-dependent, alpha-linear. A Monte Carlo of the
       production walk on the EdS background must land on the matter
       coefficient. This is what 'everpresent' means quantitatively:
       a FIXED FRACTION of the total density at every epoch.
  EQ3  the bit identities and the source ledger: bits = dchi2/(2 ln 2)
       for a likelihood ratio; the DNY Pantheon+SH0ES result (best
       seed chi2 1481.9 vs LCDM 1485.3, 16 of 90000 seeds better)
       prices to 2.453 bits bought vs log2(90000/16) = 12.458 bits
       spent on seed selection: net -10.005 bits, computed from their
       published integers. Also the 2-dof sigma <-> dchi2 map (DESI
       eq. 22): 1.7 sigma <-> 4.835, 3.1 sigma <-> 12.50 - the second
       reproduces DESI's own published dchi2_MAP = -12.5, validating
       the map implementation against the source.
  EQ4  distance-instrument anchors: EdS closed forms D_M/D_H0 =
       2(1 - 1/sqrt(1+z)), D_H/D_H0 = (1+z)^{-3/2} against the
       quadrature to 1e-9; the w0waCDM dark-energy density closed
       form rho_DE(a)/rho_DE0 = a^{-3(1+w0+wa)} exp(-3 wa (1-a))
       (DESI eq. 10) against direct quadrature of the defining
       integral to 1e-12.
  EQ5  the scale profile-out: every Table 4 observable is
       proportional to s = c/(H0 r_d) at fixed shape E(z), so the
       generalized-least-squares minimum over s is the closed form
       s* = (m^T C^-1 d)/(m^T C^-1 m); verified against a golden-
       section scan. The 2x2 tracer blocks invert exactly.
  EQ6  estimator-noise feasibility (the P-22a/P-24a pass): at
       N_seeds = 20000 per cell, a beat count K >= 16 carries
       SE(log2 K) = 1/(ln 2 sqrt K) <= 0.36 bits, small against the
       expected O(10)-bit net margin; K = 0 leaves the derived floor
       price log2 N_seeds = 14.3 bits as a lower bound. The
       instantaneous-Gaussian collapse bound Phi(-1/sigma_OmegaLambda)
       gives the monotone-in-alpha survival expectation.
Pinned -> p26_registration.json.
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

FAILURES = []


def check(name, val, ref, tol):
    err = abs(val - ref)
    ok = err <= tol
    print(f"  {name}: {val:.10g} vs {ref:.10g}  err {err:.3g}  "
          f"{'ok' if ok else 'FAIL'}")
    if not ok:
        FAILURES.append(name)
    return ok


# ----------------------------------------------------------------- EQ1
# Past-lightcone 4-volume: V(t) = (4 pi/3) int_0^t dt' a(t')^3
#   [ eta(t) - eta(t') ]^3  with eta the conformal time.
# Matter (a = (t/t0)^{2/3}): substitution u = (t'/t)^{1/3} gives
#   int_0^t t'^2 (t^{1/3}-t'^{1/3})^3 dt' = 3 B(9,4) t^4 = t^4/660,
#   V = (4 pi/3) * 27 * t^4/660 = (3 pi/55) t^4.
# Radiation (a = (t/t0)^{1/2}): u = (t'/t)^{1/2} gives
#   int t'^{3/2}(sqrt t - sqrt t')^3 dt' = 2 B(5,4) t^4 = t^4/140,
#   V = (4 pi/3) * 8 * t^4/140 = (8 pi/105) t^4.

def beta_fn(a, b):
    return math.gamma(a) * math.gamma(b) / math.gamma(a + b)


class VAccumulator:
    """Incremental past-lightcone 4-volume on an expanding history.

    V(t) = (4 pi/3) [ eta^3 I0 - 3 eta^2 I1 + 3 eta I2 - I3 ]
    with Ik = int a(t')^3 eta(t')^k dt', updated per step. O(1)/step.
    """

    def __init__(self):
        self.eta = 0.0
        self.I = [0.0, 0.0, 0.0, 0.0]
        self.V = 0.0

    def step(self, a_mid, dt):
        # advance conformal time to the midpoint, accumulate moments
        self.eta += dt / a_mid
        e = self.eta - 0.5 * dt / a_mid  # midpoint eta
        w = a_mid ** 3 * dt
        self.I[0] += w
        self.I[1] += w * e
        self.I[2] += w * e * e
        self.I[3] += w * e * e * e
        eta = self.eta
        self.V = (4.0 * math.pi / 3.0) * (
            eta ** 3 * self.I[0] - 3 * eta ** 2 * self.I[1]
            + 3 * eta * self.I[2] - self.I[3])
        return self.V


def eq1():
    print("EQ1 lightcone 4-volume closed forms")
    coef_m = 4 * math.pi / 3 * 27 * 3 * beta_fn(9, 4)
    coef_r = 4 * math.pi / 3 * 8 * 2 * beta_fn(5, 4)
    check("EQ1 matter Beta coefficient = 3pi/55", coef_m,
          3 * math.pi / 55, 1e-14)
    check("EQ1 radiation Beta coefficient = 8pi/105", coef_r,
          8 * math.pi / 105, 1e-14)
    # production accumulator on each exact background, log-a grid
    for name, p, coef in (("matter", 2.0 / 3.0, 3 * math.pi / 55),
                          ("radiation", 0.5, 8 * math.pi / 105)):
        acc = VAccumulator()
        n = 40000
        a0, a1 = 1e-6, 1.0
        lna = [math.log(a0) + (math.log(a1) - math.log(a0)) * i / n
               for i in range(n + 1)]
        t_of_a = lambda a: a ** (1.0 / p)      # t0 = 1 units
        t_prev = t_of_a(math.exp(lna[0]))
        for i in range(1, n + 1):
            a_m = math.exp(0.5 * (lna[i - 1] + lna[i]))
            t_new = t_of_a(math.exp(lna[i]))
            acc.step(a_m, t_new - t_prev)
            t_prev = t_new
        check(f"EQ1 accumulator/{name} V(t0)/coef", acc.V / coef, 1.0, 2e-4)
    return {"V_matter_coef": 3 * math.pi / 55,
            "V_radiation_coef": 8 * math.pi / 105}


# ----------------------------------------------------------------- EQ2
# Model 1 (DNY eq. set): Lambda_t = [Lambda V + 8 pi alpha xi
# sqrt(dV)]/V_t, i.e. S = Lambda V is a Brownian walk in V-time with
# step variance (8 pi alpha)^2 dV, so sigma_Lambda = 8 pi alpha/sqrt V.
# With rho_L = Lambda/(8 pi G), rho_cr = 3 H^2/(8 pi G):
#   sigma_OmegaLambda = 8 pi alpha / (3 H^2 sqrt V).
# Matter era: H = 2/(3t), V = (3pi/55) t^4  ->  2 sqrt(165 pi) alpha.
# Radiation:  H = 1/(2t), V = (8pi/105) t^4 -> (8/3) sqrt(210 pi) alpha.

def eq2():
    print("EQ2 dimensionless walk amplitude")
    cm = 2 * math.sqrt(165 * math.pi)
    cr = 8.0 / 3.0 * math.sqrt(210 * math.pi)
    # closed-form assembly checks
    t = 0.37
    Vm = 3 * math.pi / 55 * t ** 4
    Hm = 2.0 / (3 * t)
    check("EQ2 matter coefficient assembly", 8 * math.pi
          / (3 * Hm ** 2 * math.sqrt(Vm)), cm, 1e-12)
    Vr = 8 * math.pi / 105 * t ** 4
    Hr = 1.0 / (2 * t)
    check("EQ2 radiation coefficient assembly", 8 * math.pi
          / (3 * Hr ** 2 * math.sqrt(Vr)), cr, 1e-12)
    # Monte Carlo of the production update on the EdS background
    rng = random.Random(202608)
    alpha = 0.01
    M = 4000
    n = 2000
    a0 = 1e-4
    lna0, lna1 = math.log(a0), 0.0
    finals = []
    for w in range(M):
        acc = VAccumulator()
        S = 0.0
        Vp = 0.0
        t_prev = a0 ** 1.5 * (2.0 / 3.0)
        for i in range(1, n + 1):
            la_m = lna0 + (lna1 - lna0) * (i - 0.5) / n
            a_new = math.exp(lna0 + (lna1 - lna0) * i / n)
            t_new = (2.0 / 3.0) * a_new ** 1.5
            V = acc.step(math.exp(la_m), t_new - t_prev)
            t_prev = t_new
            dV = V - Vp
            Vp = V
            S += 8 * math.pi * alpha * rng.gauss(0, 1) * math.sqrt(dV)
        finals.append(S / V / (3 * (2.0 / (3 * t_prev)) ** 2))
    mean = sum(finals) / M
    var = sum((x - mean) ** 2 for x in finals) / (M - 1)
    sig = math.sqrt(var)
    se = sig / math.sqrt(2 * (M - 1))
    ok = abs(sig - cm * alpha) <= 3 * se + 0.01 * cm * alpha
    print(f"  EQ2 MC sigma_OmegaLambda {sig:.5g} vs {cm * alpha:.5g}"
          f"  (3 SE + 1% grid = {3 * se + 0.01 * cm * alpha:.3g})"
          f"  {'ok' if ok else 'FAIL'}")
    if not ok:
        FAILURES.append("EQ2 MC amplitude")
    return {"sigma_over_alpha_matter": cm, "sigma_over_alpha_radiation": cr}


# ----------------------------------------------------------------- EQ3
def sigma_to_dchi2_2dof(nsig):
    """DESI eq. 22: CDF_chi2(dchi2 | 2 dof) = erf(N/sqrt2);
    2-dof CDF is 1 - exp(-x/2), so dchi2 = -2 ln(1 - erf(N/sqrt2))."""
    return -2.0 * math.log(1.0 - math.erf(nsig / math.sqrt(2.0)))


def eq3():
    print("EQ3 bit identities and the source ledger")
    bought = (1485.3 - 1481.9) / (2 * math.log(2))
    spent = math.log2(90000 / 16)
    check("EQ3 DNY SNe bits bought", bought, 2.4527, 5e-4)
    check("EQ3 DNY seed bits spent", spent, 12.4575, 5e-4)
    net = bought - spent
    print(f"  EQ3 DNY net = {net:+.3f} bits (from published integers)")
    d17 = sigma_to_dchi2_2dof(1.7)
    d31 = sigma_to_dchi2_2dof(3.1)
    check("EQ3 dchi2(1.7 sigma, 2 dof)", d17, 4.8352, 5e-3)
    check("EQ3 dchi2(3.1 sigma, 2 dof) vs DESI's -12.5", d31, 12.5, 0.05)
    return {"dny_bits_bought": bought, "dny_bits_spent": spent,
            "dny_net_bits": net, "dchi2_of_1p7sigma": d17,
            "dchi2_of_3p1sigma": d31}


# ----------------------------------------------------------------- EQ4
def distances_over_rd(zs, E_of_z, nz=4096, zmax=None):
    """D_M/D_H in units c/H0 at requested redshifts, trapezoid on a
    uniform z grid over [0, zmax]. E_of_z = H(z)/H0."""
    if zmax is None:
        zmax = max(zs)
    grid = [zmax * i / nz for i in range(nz + 1)]
    inv = [1.0 / E_of_z(z) for z in grid]
    cum = [0.0]
    for i in range(1, nz + 1):
        cum.append(cum[-1] + 0.5 * (inv[i - 1] + inv[i]) * (grid[1]))
    out = []
    for z in zs:
        x = z / zmax * nz
        i = min(int(x), nz - 1)
        f = x - i
        dm = cum[i] * (1 - f) + cum[i + 1] * f
        out.append((dm, 1.0 / E_of_z(z)))
    return out


def eq4():
    print("EQ4 distance-instrument anchors")
    zs = [0.295, 0.51, 2.33]
    eds = distances_over_rd(zs, lambda z: (1 + z) ** 1.5, nz=200000)
    worst = 0.0
    for z, (dm, dh) in zip(zs, eds):
        worst = max(worst, abs(dm - 2 * (1 - 1 / math.sqrt(1 + z))),
                    abs(dh - (1 + z) ** -1.5))
    check("EQ4 EdS closed-form worst error", worst, 0.0, 1e-8)
    w0, wa = -0.6, -1.2
    for a in (0.31, 0.77, 1.0):
        closed = a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
        n = 200000
        acc = 0.0
        for i in range(n):
            am = a + (1 - a) * (i + 0.5) / n
            acc += 3 * (1 + w0 + wa * (1 - am)) / am * ((1 - a) / n)
        check(f"EQ4 rho_DE(a={a}) closed vs quadrature",
              closed, math.exp(acc), max(1e-12, 1e-9 * closed))
    return {}


# ----------------------------------------------------------------- EQ5
def load_table4():
    with open(os.path.join(HERE, "desi_dr2_table4.json")) as f:
        return json.load(f)


def chi2_blocks(rows, model, s):
    """model: dict tracer -> (DV,) or (DM, DH) in c/H0 units;
    s = c/(H0 r_d). Exact 2x2 block inverses."""
    c2 = 0.0
    for r in rows:
        tr = r["tracer"]
        if "DV_over_rd" in r:
            m = s * model[tr][0]
            c2 += ((m - r["DV_over_rd"]) / r["DV_err"]) ** 2
        else:
            dm = s * model[tr][0] - r["DM_over_rd"]
            dh = s * model[tr][1] - r["DH_over_rd"]
            sm, sh, rho = r["DM_err"], r["DH_err"], r["r_MH"]
            det = 1 - rho * rho
            c2 += (dm * dm / sm ** 2 - 2 * rho * dm * dh / (sm * sh)
                   + dh * dh / sh ** 2) / det
    return c2


def profile_scale(rows, model):
    """Closed-form GLS minimum over s: s* = m^T C^-1 d / m^T C^-1 m."""
    num = den = 0.0
    for r in rows:
        tr = r["tracer"]
        if "DV_over_rd" in r:
            m, d, sd = model[tr][0], r["DV_over_rd"], r["DV_err"]
            num += m * d / sd ** 2
            den += m * m / sd ** 2
        else:
            mm, mh = model[tr]
            dm, dh = r["DM_over_rd"], r["DH_over_rd"]
            sm, sh, rho = r["DM_err"], r["DH_err"], r["r_MH"]
            det = 1 - rho * rho
            # C^-1 = [[1/sm^2, -rho/(sm sh)], [-rho/(sm sh), 1/sh^2]]/det
            num += (mm * dm / sm ** 2 - rho * (mm * dh + mh * dm)
                    / (sm * sh) + mh * dh / sh ** 2) / det
            den += (mm * mm / sm ** 2 - 2 * rho * mm * mh / (sm * sh)
                    + mh * mh / sh ** 2) / det
    return num / den


def model_from_E(rows, E_of_z, nz=4096):
    zs = sorted({r["zeff"] for r in rows})
    ds = dict(zip(zs, distances_over_rd(zs, E_of_z, nz=nz)))
    model = {}
    for r in rows:
        dm, dh = ds[r["zeff"]]
        if "DV_over_rd" in r:
            z = r["zeff"]
            model[r["tracer"]] = ((z * dm * dm * dh) ** (1.0 / 3.0),)
        else:
            model[r["tracer"]] = (dm, dh)
    return model


def eq5():
    print("EQ5 scale profile-out closed form")
    pin = load_table4()
    rows = pin["rows"]
    om = 0.3

    def E(z):
        return math.sqrt(om * (1 + z) ** 3 + 1 - om)
    model = model_from_E(rows, E)
    s_star = profile_scale(rows, model)
    from kernels.minimize import golden_max
    s_scan = golden_max(lambda s: -chi2_blocks(rows, model, s),
                        0.5 * s_star, 2.0 * s_star)[0]
    check("EQ5 s* closed form vs golden scan", s_star, s_scan, 1e-6 * s_star)
    return {"s_star_at_om0.3": s_star,
            "chi2_at_om0.3": chi2_blocks(rows, model, s_star)}


# ----------------------------------------------------------------- EQ6
def eq6(coefs):
    print("EQ6 feasibility: estimator noise and collapse bound")
    se16 = 1.0 / (math.log(2) * math.sqrt(16))
    check("EQ6 SE(log2 K) at K=16", se16, 0.3607, 1e-3)
    floor = math.log2(20000)
    print(f"  EQ6 zero-beat floor price log2(20000) = {floor:.3f} bits")
    cm = coefs["sigma_over_alpha_matter"]
    surv = {}
    for alpha in (0.005, 0.01, 0.02, 0.04):
        p_inst = 0.5 * (1 + math.erf(-1.0 / (cm * alpha) / math.sqrt(2)))
        surv[alpha] = p_inst
        print(f"  EQ6 alpha={alpha}: sigma_OL={cm * alpha:.3f}, "
              f"instantaneous P(rho_tot<0) = {p_inst:.3g}")
    return {"se_log2_at_K16": se16, "floor_bits_at_20000": floor,
            "instantaneous_collapse_prob": {str(k): v
                                            for k, v in surv.items()}}


def main():
    pins = {}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    pins["EQ5"] = eq5()
    pins["EQ6"] = eq6(pins["EQ2"])
    pins["data"] = load_table4()
    pins["ensemble_spec"] = {
        "seed0": 262626,
        "main_cells": [{"alpha": a, "Omega_m": 0.2975, "N_seeds": 20000}
                       for a in (0.005, 0.01, 0.02, 0.04)],
        "sensitivity_cells": [{"alpha": 0.02, "Omega_m": om,
                               "N_seeds": 5000} for om in (0.25, 0.35)],
        "n_cells_price_bits": math.log2(6),
        "a_init": 1e-5, "steps": 512, "z_eq_convention": 3400,
        "note": ("r_d and H0 enter only through the profiled scale s, "
                 "per realization - an upper bound on Model 1's BAO "
                 "performance, so the bit price charged is a lower "
                 "bound. Collapsed realizations (H^2 <= 0 before a=1) "
                 "count in N_seeds and cannot beat."),
    }
    out = os.path.join(HERE, "p26_registration.json")
    with open(out, "w") as f:
        json.dump(pins, f, indent=1)
    print(f"\npinned -> {out}")
    if FAILURES:
        print("DERIVATION FAILURES:", FAILURES)
        return 1
    print("all derivations ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
