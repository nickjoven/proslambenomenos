#!/usr/bin/env python3
"""Verification for the P-26 claim everpresent-lambda-prices-out-
on-dr2-bao, by independent live reimplementation: its own distance
integrator (Simpson, not trapezoid), its own explicit 2x2-block
chi2, its own grid-scan LCDM fit, its own Model 1 marcher with its
own volume bookkeeping, and its own analytic-volume EdS amplitude
route that never touches the incremental accumulator. Only the
machine-parsed data file desi_dr2_table4.json is shared - data,
not code.

Checks: (1) EdS-mode walk amplitude on the ANALYTIC matter-era
volume V = (3 pi/55) t^4 lands on the derived 2 sqrt(165 pi) alpha
within 3 SE + 1 percent; (2) the LCDM grid fit recovers Omega_m in
[0.2889, 0.3061] (the published band) with chi2 in [9.5, 11.6];
(3) an 800-seed miniature ensemble at alpha = 0.01 (its own seed
stream, seed0 373737, its own 256-step marcher with closed-form
radiation V_0): survival within [0.13, 0.26] (4-sigma binomial
band around R-23's 0.194) and ZERO realizations beating the
native-grid LCDM threshold.

--mutant three-volume    sources the walk with sqrt(dV^(3/4))
    scaling (the wrong power of the lightcone volume); the derived
    matter-era amplitude coefficient kills it at check (1).
--mutant eds-threshold   scores the miniature ensemble against a
    no-dark-energy expansion instead of LCDM (the design error
    R-23 records and corrects); survivors beat it easily, so the
    zero-beat check kills it.

(A covariance-blind mutant was tried and DISCARDED as
non-discriminating: zeroing the printed D_M-D_H correlations moves
the LCDM chi2 by only 0.92 and Omega_m by 0.002 - this table is
error-dominated per block - so it cannot serve as a falsifier
mutant, and that subdominance is recorded in the notes instead.)
"""
import json
import math
import random
import sys
from pathlib import Path

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"three-volume", "eds-threshold"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

DATA = Path(__file__).resolve().parents[1] / "experiments" \
    / "desi_dr2_table4.json"
Z_EQ = 3400.0


def rows():
    return json.load(open(DATA))["rows"]


# ---------------------------------------------------------- chi2 side
def simpson_dm(E, z, n=512):
    if n % 2:
        n += 1
    h = z / n
    acc = 1.0 / E(0.0) + 1.0 / E(z)
    for i in range(1, n):
        acc += (4.0 if i % 2 else 2.0) / E(i * h)
    return acc * h / 3.0


def chi2_table(rws, E, corr_scale=1.0):
    """chi2 with the single scale profiled in closed form, blocks
    inverted explicitly. corr_scale = 0 is the covariance-blind
    mutant's knob."""
    num = den = 0.0
    mods = []
    for r in rws:
        z = r["zeff"]
        dm = simpson_dm(E, z)
        dh = 1.0 / E(z)
        if "DV_over_rd" in r:
            mods.append((r, ((z * dm * dm * dh) ** (1.0 / 3.0),)))
        else:
            mods.append((r, (dm, dh)))
    for r, m in mods:
        if "DV_over_rd" in r:
            num += m[0] * r["DV_over_rd"] / r["DV_err"] ** 2
            den += m[0] ** 2 / r["DV_err"] ** 2
        else:
            sm, sh = r["DM_err"], r["DH_err"]
            rho = r["r_MH"] * corr_scale
            det = 1 - rho * rho
            dmv, dhv = r["DM_over_rd"], r["DH_over_rd"]
            num += (m[0] * dmv / sm ** 2
                    - rho * (m[0] * dhv + m[1] * dmv) / (sm * sh)
                    + m[1] * dhv / sh ** 2) / det
            den += (m[0] ** 2 / sm ** 2
                    - 2 * rho * m[0] * m[1] / (sm * sh)
                    + m[1] ** 2 / sh ** 2) / det
    s = num / den
    c2 = 0.0
    for r, m in mods:
        if "DV_over_rd" in r:
            c2 += ((s * m[0] - r["DV_over_rd"]) / r["DV_err"]) ** 2
        else:
            sm, sh = r["DM_err"], r["DH_err"]
            rho = r["r_MH"] * corr_scale
            det = 1 - rho * rho
            x = s * m[0] - r["DM_over_rd"]
            y = s * m[1] - r["DH_over_rd"]
            c2 += (x * x / sm ** 2 - 2 * rho * x * y / (sm * sh)
                   + y * y / sh ** 2) / det
    return c2


def E_lcdm(om):
    orad = om / Z_EQ
    return lambda z: math.sqrt(om * (1 + z) ** 3
                               + orad * (1 + z) ** 4
                               + (1 - om - orad))


def E_scdm(om):
    orad = om / Z_EQ
    norm = om + orad
    return lambda z: math.sqrt((om * (1 + z) ** 3
                                + orad * (1 + z) ** 4) / norm)


# ---------------------------------------------------------- walk side
def eds_amplitude(alpha, M=2500, n=1500, seed0=474747):
    """The DNY update on the ANALYTIC matter-era volume: t marches
    uniformly in log from t_i to t_0 = 1, V = (3 pi/55) t^4 exactly,
    sigma measured as std of rho_L / rho_cr at t_0. No incremental
    accumulator anywhere."""
    coef = 3 * math.pi / 55
    out = []
    t_i, t_0 = 1e-4, 1.0
    for w in range(M):
        rng = random.Random((seed0, w).__hash__() & 0x7fffffff)
        S = 0.0
        Vp = coef * t_i ** 4
        for k in range(1, n + 1):
            t = t_i * (t_0 / t_i) ** (k / n)
            V = coef * t ** 4
            dV = V - Vp
            Vp = V
            if MUTANT == "three-volume":
                step = math.sqrt(dV ** 0.75)
            else:
                step = math.sqrt(dV)
            S += (8 * math.pi / 3) * alpha * rng.gauss(0, 1) * step
        rho_cr = (2.0 / (3.0 * t_0)) ** 2  # H^2 in 8piG/3=1 units
        out.append(S / V / rho_cr)
    mean = sum(out) / M
    sig = math.sqrt(sum((x - mean) ** 2 for x in out) / (M - 1))
    se = sig / math.sqrt(2 * (M - 1))
    return sig, se


def march(alpha, om, seed, steps=256, a_init=1e-5):
    """Independent Model 1 marcher: its own O(1) volume bookkeeping
    via the lookback expansion, radiation closed-form start."""
    orad = om / Z_EQ
    rng = random.Random(seed)
    t = 1.0 / (2.0 * math.sqrt(om / a_init ** 3 + orad / a_init ** 4))
    a = a_init
    eta = 2.0 * t / a_init
    J = [0.4 * a_init ** 3 * t, (2 / 3) * a_init ** 2 * t * t,
         (8 / 7) * a_init * t ** 3, 2.0 * t ** 4]
    S = 0.0
    rhoL = 0.0
    Vp = (4 * math.pi / 3) * (eta ** 3 * J[0] - 3 * eta * eta * J[1]
                              + 3 * eta * J[2] - J[3])
    la0, la1 = math.log(a_init), 0.0
    hist = []
    for i in range(1, steps + 1):
        a_new = math.exp(la0 + (la1 - la0) * i / steps)
        a_mid = math.sqrt(a * a_new)
        H2 = om / a_mid ** 3 + orad / a_mid ** 4 + rhoL
        if H2 <= 0:
            return None
        dt = (a_new - a) / (a_mid * math.sqrt(H2))
        eta_mid = eta + 0.5 * dt / a_mid
        eta += dt / a_mid
        w = a_mid ** 3 * dt
        J[0] += w
        J[1] += w * eta_mid
        J[2] += w * eta_mid ** 2
        J[3] += w * eta_mid ** 3
        V = (4 * math.pi / 3) * (eta ** 3 * J[0] - 3 * eta * eta * J[1]
                                 + 3 * eta * J[2] - J[3])
        S += (8 * math.pi / 3) * alpha * rng.gauss(0, 1) \
            * math.sqrt(V - Vp)
        Vp = V
        rhoL = S / V
        E2 = om / a_new ** 3 + orad / a_new ** 4 + rhoL
        if E2 <= 0:
            return None
        hist.append((a_new, E2))
        a = a_new
    return hist


def chi2_hist(rws, hist):
    E0 = hist[-1][1]
    zs = [1 / a - 1 for a, _ in reversed(hist)]
    Es = [math.sqrt(e2 / E0) for _, e2 in reversed(hist)]

    def E(z):
        lo, hi = 0, len(zs) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if zs[mid] <= z:
                lo = mid
            else:
                hi = mid
        f = (z - zs[lo]) / (zs[hi] - zs[lo])
        return Es[lo] + f * (Es[hi] - Es[lo])
    return chi2_table(rws, E)


def main():
    rws = rows()
    failures = []

    # (1) analytic-volume EdS amplitude
    alpha = 0.01
    sig, se = eds_amplitude(alpha)
    want = 2 * math.sqrt(165 * math.pi) * alpha
    tol = 3 * se + 0.01 * want
    print(f"amplitude: {sig:.5f} vs derived {want:.5f} (tol {tol:.5f})")
    if abs(sig - want) > tol:
        print("FAIL: EdS walk amplitude off the derived "
              "2 sqrt(165 pi) alpha")
        failures.append("amplitude")

    # (2) LCDM grid fit
    corr = 1.0
    best = (1e30, None)
    om = 0.20
    while om <= 0.40:
        c2 = chi2_table(rws, E_lcdm(om), corr_scale=corr)
        if c2 < best[0]:
            best = (c2, om)
        om += 0.0005
    c2min, om_best = best
    print(f"lcdm grid fit: Omega_m {om_best:.4f}, chi2 {c2min:.3f}")
    if not (0.2889 <= om_best <= 0.3061) or not (9.5 <= c2min <= 11.6):
        print("FAIL: LCDM fit off the published DR2 values")
        failures.append("lcdm-fit")

    # (3) miniature ensemble
    thresh_E = E_scdm(0.297) if MUTANT == "eds-threshold" \
        else E_lcdm(om_best if 0.2 < om_best < 0.4 else 0.297)
    thresh = chi2_table(rws, thresh_E, corr_scale=corr)
    n_try, alive, beat = 800, 0, 0
    best_c2 = 1e30
    for k in range(n_try):
        seed = (373737, k).__hash__() & 0x7fffffff
        hist = march(0.01, 0.297, seed)
        if hist is None:
            continue
        alive += 1
        c2 = chi2_hist(rws, hist)
        best_c2 = min(best_c2, c2)
        if c2 < thresh:
            beat += 1
    surv = alive / n_try
    print(f"mini-ensemble: survival {surv:.3f}, beats {beat} "
          f"(threshold {thresh:.2f}, best {best_c2:.2f})")
    if not (0.13 <= surv <= 0.26):
        print("FAIL: survival off the R-23 band")
        failures.append("survival")
    if beat != 0:
        print("FAIL: a realization beat the reference - the zero-beat "
              "verdict does not reproduce")
        failures.append("beats")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p26 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
