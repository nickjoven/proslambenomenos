#!/usr/bin/env python3
"""P-35 derivation layer (pre-registration): the reopened P-4.

R-3 resolved P-4 as model-class vacuity: the clamp cut the loop, so
no run ever had both a holonomy and a gate, and the registered
threshold question was unanswerable by construction. The audit tail
(notes/p4_twisted_inertial_ring.md) states the reopen recipe: keep
the loop (no clamp), a massless/overdamped contact (no S2 chatter
oscillator), N >= 64, low damping, and an observable the background
half-winding can actually reach. This layer derives, before any
registered cell runs, everything AGENTS.md item 8 requires:

  8a  detector null responses  -> EQ2 (linear strain null), EQ6
      (contact-timescale exclusion band)
  8b  observable conservation identities -> EQ3 (telescoping mean:
      the site-mean is holonomy-blind by Newton pairs - P-33's
      lesson derived up front, not diagnosed after a firing)
  8c  search-domain validity -> EQ7 (every sweep window from a
      derived bound; R-32 corollary honored)

Model (free ring, both variants):
  theta_j, j = 0..N-1 on a ring, m = 1, J = 1,
  dd(theta_j) = -gamma d(theta_j) + sin(D_j - A_j) - sin(D_{j-1} -
  A_{j-1}) + delta_{j,b} f_c,   D_j = theta_{j+1} - theta_j,
  A_j = pi delta_{j,0} (twisted) or 0 (control), bow node b = N/2
  (antipodal to the pi bond). Contact: stick = kinematic velocity
  constraint d(theta_b) = v while |lambda| <= mu_s F_N (lambda the
  tracked constraint force - the contact carries NO state of its
  own, i.e. massless); slip = -mu_d F_N sgn(rel), re-stick only on
  a velocity crossing WITH the force test (S6's vacuous-re-stick
  bug does not recur).

Derived facts:
  EQ1  winding sectors, exact: equilibria have uniform covariant
       strain delta_n = (2 pi n - pi)/N (twisted) vs 2 pi n / N
       (control); the covariant winding W = sum wrap(D_j - A_j) /
       (2 pi) is n - 1/2 twisted, n control. HALF-INTEGER SECTORS
       are the kinematic content of the holonomy, and W is an
       observable the half-winding reaches. The two twisted ground
       sectors n = 0, 1 (delta = -+ pi/N) are exactly degenerate.
  EQ2  linear detector null: stiffness about sector n is
       J cos(delta_n); twisted ground sectors: J cos(pi/N). Any
       twisted-vs-control frequency ratio inside
       [sqrt(cos(pi/N)), 1] is ground-state strain, not dynamics.
       1 - sqrt(cos(pi/64)) = 6.0e-4: the derived frequency null.
  EQ3  conservation identity: sum_j (bond forces) = 0 exactly
       (Newton pairs on a loop), so N*dd(mean) = -gamma N d(mean)
       + f_c: the site-mean obeys the SAME rigid-body equation for
       twisted and control given the same contact-force history.
       The site-mean is holonomy-blind by identity; registered
       observables are W(t), the bond-strain field, and the spatial
       DFT of e^{i theta}.
  EQ4  the strain budget, the load-bearing derivation: the
       quasi-static fold of the point-loaded ring, solved exactly
       (sin(s_j) = c + m f/N around the loop, loop constraint
       sum s_j = 2 pi n - pi twisted vs 0 control, fold = largest
       f admitting a root). Twisted / control fold ratio 0.9663
       at N = 64: an O(1/N) SHIFT WITH DERIVED SIGN, SIZE, AND
       N-SCALING - this is what the clamp destroyed. Theorem-let:
       ring reflection about the pi bond exchanges the two twisted
       sectors at the same drive, so their folds are EXACTLY
       degenerate; any measured sector split is instrument noise
       (a self-calibrating null floor). A naive helping/hurting
       sector asymmetry was derived first and REFUTED by this
       solver: kept in the record as a derivation error corrected
       before registration. Numeric anchor: overdamped staircase
       at N = 64, all three configurations, one-sided bias
       (staircase can only overshoot the fold: level step 0.01
       plus finite hold).
  EQ5  spectral address, exact: the spatial DFT of u_j =
       e^{i theta_j} in sector n peaks at fractional mode index
       n - 1/2 (twisted) vs n (control) - half-integer lines exist
       ONLY in this observable (the S1 corollary, now the design).
  EQ6  contact-timescale exclusion band (8a): a released stuck
       node rings at omega = sqrt(2 J cos delta), period 4.443 at
       N = 64. Slip-gap structure within [0.8, 1.2] x this period
       is instrument, not holonomy; gap statistics are reported as
       min/median/max (S6's median bias does not recur).
  EQ7  domain validity (8c): steady stuck co-rotation needs
       constraint force gamma N v, so stick-slip lives at
       F_N >= gamma N v / mu_s (below: never sticks... above:
       sticks); bond capacity bounds the transmissible load at
       ~ 2J so F_N sweeps cap at 2 J / mu_d; drive stays sub-sonic
       v <= 0.1 sqrt(cos(pi/N)); steady state needs gamma T_meas
       >= 5; windows printed with the numbers substituted.

Run: python3 scripts/experiments/p35_derive.py
"""
import json
import math
import os
from fractions import Fraction

TAU = 2 * math.pi


def wrap(x):
    return (x + math.pi) % TAU - math.pi


# ---------------------------------------------------------------
# EQ1: winding sectors, exact and numeric
# ---------------------------------------------------------------
def eq1_sectors():
    out = {"exact": [], "numeric": []}
    for N in (64, 96, 128):
        for n in (0, 1):
            # covariant strain delta_n = (2 pi n - pi)/N: winding
            # W = (N * delta_n) / (2 pi) = n - 1/2, exact fraction
            W = Fraction(2 * n - 1, 2)
            out["exact"].append({"N": N, "sector": n, "W": str(W)})
            assert W - Fraction(n) == Fraction(-1, 2)
    # numeric: damped relaxation from noise, N = 64, twisted and
    # control; measure W and (twisted) sector degeneracy
    import random
    random.seed(35)
    N = 64
    for twisted in (True, False):
        A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
        th = [random.uniform(-0.5, 0.5) for _ in range(N)]
        w = [0.0] * N
        dt, gamma = 0.05, 1.0
        for _ in range(int(400 / dt)):
            acc = []
            for j in range(N):
                Dr = th[(j + 1) % N] - th[j] - A[j]
                Dl = th[j] - th[j - 1] - A[j - 1]
                acc.append(math.sin(Dr) - math.sin(Dl) - gamma * w[j])
            for j in range(N):
                w[j] += dt * acc[j]
                th[j] += dt * w[j]
        W = sum(wrap(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)) / TAU
        half = abs(W - round(W - 0.5) - 0.5)
        out["numeric"].append(
            {"twisted": twisted, "W": W,
             "dist_half_int": half if twisted else None,
             "dist_int": None if twisted else abs(W - round(W))})
    # degeneracy of the two twisted ground sectors: energy
    # E_n = -sum cos(delta_n) = -N cos(pi/N) for n = 0 and 1 alike
    e0 = -64 * math.cos((-math.pi) / 64)
    e1 = -64 * math.cos((math.pi) / 64)
    out["degeneracy_gap"] = abs(e0 - e1)
    return out


# ---------------------------------------------------------------
# EQ2: linear strain null
# ---------------------------------------------------------------
def eq2_null():
    out = {}
    for N in (64, 96, 128):
        c = math.cos(math.pi / N)
        out[str(N)] = {"stiffness_ratio": c,
                       "freq_null_width": 1 - math.sqrt(c)}
    return out


# ---------------------------------------------------------------
# EQ3: telescoping identity on a driven run
# ---------------------------------------------------------------
def eq3_telescoping():
    # driven twisted ring, verify sum of bond forces = 0 at every
    # step to machine precision, and that the mean obeys the rigid
    # body equation
    N = 64
    A = [math.pi if j == 0 else 0.0 for j in range(N)]
    th = [j * (math.pi / N) for j in range(N)]  # sector n = 1
    w = [0.0] * N
    dt, gamma, b = 0.01, 0.02, N // 2
    worst = 0.0
    worst_mean = 0.0
    for step in range(20000):
        fc = 0.4 * math.sin(0.05 * step * dt)  # benign probe force
        bond = 0.0
        acc = []
        for j in range(N):
            Dr = th[(j + 1) % N] - th[j] - A[j]
            Dl = th[j] - th[j - 1] - A[j - 1]
            t_j = math.sin(Dr) - math.sin(Dl)
            bond += t_j
            acc.append(t_j - gamma * w[j] + (fc if j == b else 0.0))
        worst = max(worst, abs(bond))
        mean_acc = sum(acc) / N
        rigid = -gamma * (sum(w) / N) + fc / N
        worst_mean = max(worst_mean, abs(mean_acc - rigid))
        for j in range(N):
            w[j] += dt * acc[j]
            th[j] += dt * w[j]
    return {"worst_bond_sum": worst, "worst_mean_residual": worst_mean}


# ---------------------------------------------------------------
# EQ4: the strain budget - profile prediction and overdamped ramp
# ---------------------------------------------------------------
def fold_fc(N, total):
    """Exact quasi-static fold. In overdamped steady drift
    (theta_dot = force), force balance gives sin(s_j) = c + m f/N
    with m = 0..N-1 climbing around the whole ring and the single
    drop at the contact; the loop constraint sum_j s_j = total
    (= 2 pi n - pi twisted, 0 control) pins c. The fold is the
    largest f for which a principal-branch root c exists. A naive
    'hottest bond reaches capacity 1 - sin(delta)' shortcut is
    WRONG near the fold (arcsin is strongly nonlinear there) and
    is superseded by this solver. Theorem-let: ring reflection
    about the pi bond maps sector W = +1/2 to W = -1/2 at the
    same drive, so fold_fc(N, +pi) = fold_fc(N, -pi) EXACTLY -
    the two twisted sectors are degenerate, statically and
    dynamically. Any measured sector split is instrument noise:
    a self-calibrating null floor (AGENTS item 8b).
    """
    def sum_s(c, f):
        s = 0.0
        for m in range(N):
            x = c + m * f / N
            if x <= -1.0 or x >= 1.0:
                return None
            s += math.asin(x)
        return s

    def has_root(f):
        lo, hi = -0.999999, 1.0 - (N - 1) * f / N - 1e-12
        if hi <= lo:
            return False
        slo, shi = sum_s(lo, f), sum_s(hi, f)
        if slo is None or shi is None:
            return False
        if (slo - total) * (shi - total) > 0:
            return False
        return True

    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if has_root(mid):
            lo = mid
        else:
            hi = mid
    return lo


def eq4_budget():
    out = {"prediction": {}}
    for N in (64, 96, 128):
        f0 = fold_fc(N, 0.0)
        f1 = fold_fc(N, math.pi)
        fm = fold_fc(N, -math.pi)
        out["prediction"][str(N)] = {
            "fc_control": f0,
            "fc_sector1": f1,
            "fc_sector0": fm,
            "sector_degeneracy_gap": abs(f1 - fm),
            "ratio_twisted": f1 / f0,
            "naive_1_minus_sin": 1 - math.sin(math.pi / N)}
    # numeric anchor: overdamped STAIRCASE at N = 64, both sectors
    # and control (theta_dot = force). Ground-state init has
    # uniform COVARIANT strain: theta_{j+1} - theta_j = delta +
    # A_j (the earlier uniform-raw-strain init put bond 0 a full
    # pi off equilibrium - wrong). Each f level is held long
    # enough to pass or fail; slip detector = any raw covariant
    # strain past pi (runaway beyond the saddle), theta unwrapped.
    N, b = 64, 32
    dt, hold = 0.1, 250.0
    anchors = {}
    for tag, twisted, sector in (("control", False, 0),
                                 ("sector1", True, 1),
                                 ("sector0", True, 0)):
        A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
        delta = ((2 * sector - 1) * math.pi / N) if twisted else 0.0
        th, acc_off = [], 0.0
        for j in range(N):
            th.append(acc_off)
            acc_off += delta + A[j]
        pred = fold_fc(N, (2 * sector - 1) * math.pi if twisted else 0.0)
        fc_hit = None
        f = round(pred - 0.15, 2)
        while f < pred + 0.25 and fc_hit is None:
            slipped = False
            for s in range(int(hold / dt)):
                new = list(th)
                for j in range(N):
                    Dr = th[(j + 1) % N] - th[j] - A[j]
                    Dl = th[j] - th[j - 1] - A[j - 1]
                    force = (math.sin(Dr) - math.sin(Dl)
                             + (f if j == b else 0.0))
                    new[j] = th[j] + dt * force
                th = new
                if s % 100 == 0:
                    m = max(abs(wrap(th[(j + 1) % N] - th[j] - A[j])
                                - delta)
                            for j in range(N))
                    if m > 2.6:
                        slipped = True
                        break
            if slipped:
                fc_hit = f
            f = round(f + 0.01, 2)
        anchors[tag] = {"fc_measured": fc_hit, "fc_predicted": pred}
    out["anchor_N64"] = anchors
    return out


# ---------------------------------------------------------------
# EQ5: spectral address
# ---------------------------------------------------------------
def eq5_address():
    out = {}
    N = 64
    for tag, twisted, n in (("control", False, 0), ("twist0", True, 0),
                            ("twist1", True, 1)):
        delta = ((2 * n - 1) * math.pi / N) if twisted else (TAU * n / N)
        th = [j * delta for j in range(N)]
        # fractional mode index by phase regression of u_j
        # u_{j+1}/u_j = e^{i delta} -> index = N delta / (2 pi)
        idx = N * delta / TAU
        # DFT peak check on a fine fractional grid
        best, bidx = 0.0, None
        for kk in [x / 8.0 for x in range(-2 * 8, 2 * 8 + 1)]:
            re = sum(math.cos(th[j] - TAU * kk * j / N) for j in range(N))
            im = sum(math.sin(th[j] - TAU * kk * j / N) for j in range(N))
            a = math.hypot(re, im)
            if a > best:
                best, bidx = a, kk
        out[tag] = {"index_exact": idx, "dft_peak_index": bidx,
                    "dft_peak_amp_over_N": best / N}
    return out


# ---------------------------------------------------------------
# EQ6 / EQ7: exclusion band and derived windows
# ---------------------------------------------------------------
def eq67_windows():
    out = {}
    for N in (64, 96, 128):
        c = math.cos(math.pi / N)
        t_contact = TAU / math.sqrt(2 * c)
        gamma, mu_s, mu_d = 0.02, 1.0, 0.5
        cw = math.sqrt(c)
        v_max = 0.1 * cw
        out[str(N)] = {
            "contact_period": t_contact,
            "exclusion_band": [0.8 * t_contact, 1.2 * t_contact],
            "gamma": gamma,
            "v_max_subsonic": v_max,
            "FN_stick_floor(v)": "gamma*N*v/mu_s = %.4f at v=0.05"
                                 % (gamma * N * 0.05 / mu_s),
            "FN_cap": 2.0 / mu_d,
            "T_meas_min": 5.0 / gamma,
            "round_trip": N / cw}
    return out


def main():
    res = {"EQ1": eq1_sectors(), "EQ2": eq2_null(),
           "EQ3": eq3_telescoping(), "EQ4": eq4_budget(),
           "EQ5": eq5_address(), "EQ67": eq67_windows()}
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "p35_derive.json")
    with open(path, "w") as f:
        json.dump(res, f, indent=1)
    print("EQ1 numeric:", res["EQ1"]["numeric"])
    print("EQ1 degeneracy gap:", res["EQ1"]["degeneracy_gap"])
    print("EQ2:", res["EQ2"])
    print("EQ3:", res["EQ3"])
    for N in ("64", "96", "128"):
        print("EQ4 prediction N=%s:" % N, res["EQ4"]["prediction"][N])
    print("EQ4 anchors:", json.dumps(res["EQ4"]["anchor_N64"], indent=1))
    print("EQ5:", json.dumps(res["EQ5"], indent=1))
    print("EQ67 N=64:", json.dumps(res["EQ67"]["64"], indent=1))


if __name__ == "__main__":
    main()
