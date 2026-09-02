#!/usr/bin/env python3
"""Verification for the P-45 claim ring-energy-continuity, by
independent reimplementation: the time derivative of the site
energy is taken by FORWARD-MODE DUAL NUMBERS (h evaluated on
theta + eps v, v + eps a; the eps coefficient is dh/dt), not by
the hand-written chain rule of the experiment; own random states
(own seed, N = 48, a different ring size from the registered
cells); own bond current; the global balance from E directly; a
short own-integrator trajectory (velocity-Verlet with the damping
force at the old velocity, a different scheme and ordering from
the experiment's Euler-Cromer) whose discrete balance defect must
decrease along a three-rung ladder at a ratio of at least 2^0.5.
Nothing read from results files.

Checks: (1) per-site residual of the identity within the
floating-point bound 32 eps T_j at every one of 3000 random
states on the control ring and 3000 on the twisted ring, at two
velocity scales; (2) global balance dE/dt = f v_b - gamma sum v^2
and the telescoping current sum within their bounds; (3) the two
seam sites of the twisted ring at the same bound (A enters only
through D); (4) the own velocity-Verlet ladder on both rings
BELOW their folds (F_SMOOTH = 1.85 against folds 2.0426 control /
1.9497 twisted at N = 48): global and per-site sup-defects
decrease monotonically with ratios >= 2^0.5 - a convergence
sanity check on a second-order scheme, NOT the order test;
(5) the order test the claim's clause (2) is about: an own
Euler-Cromer integrator in the P-36 order (v += dt a, then
th += dt v) with force-times-displacement bookkeeping, on a
twisted N = 16 ring one step ABOVE its own fold, run THROUGH the
slip to event + 20 on the dt = 0.001 / 0.0005 / 0.00025 ladder
(0.09 rad per step at the rotor speed f/gamma = 92): the event at
every rung, both sup-defects decreasing, both successive ratios
inside the two-sided order band [2^0.5, 2^1.5].

History (R-45a): the first pinned version ran check (4) at
F = 1.97, above the twisted fold at N = 48, so its twisted cell
slipped at t = 29 of 60 with the rotor at 47 (0.94 rad per step)
and passed only because the check was one-sided; the claim's
through-slip clause had no reimplementation behind it. LAW-54.

--mutant current-blind  J = -sin(D_j) v_j (no velocity average);
    O(1) per-site residual kills it.
--mutant sink-blind     drops gamma v^2 from the balance; the
    global check kills it (and the per-site one).
--mutant gauge-blind    u from theta_{j+1} - theta_j with A
    dropped; identical on the control ring, O(1) at the twisted
    ring's seam sites - the seam check kills it.
--mutant share-blind    the ladder's site energy assigns each bond
    wholly to its left site (h_j = v_j^2/2 + u_j) instead of the
    half-and-half convention; the residual checks do not see it
    (they use the identity's own h), the global ladder does not
    see it (the sum is unchanged), and the per-site slip ladder
    kills it: an O(1) per-site defect at every dt, ratios near 1.
"""
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"current-blind", "sink-blind", "gauge-blind", "share-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

EPS = 2.0 ** -52
OPS = 32
GAMMA = 0.02
F = 1.97          # the residual checks (any f: the identity holds for all)
F_SMOOTH = 1.85   # the smooth ladder: below both N = 48 folds (R-45a)
N = 48
B = N // 2
ROOT2 = math.sqrt(2.0)
ORDER_BAND = (ROOT2, 2.0 * ROOT2)   # two-sided: 1 | 2 | 4 discriminated


class Dual:
    """a + b eps with eps^2 = 0: forward-mode derivative carrier."""
    __slots__ = ("a", "b")

    def __init__(self, a, b=0.0):
        self.a, self.b = a, b

    def __add__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return Dual(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.a * o.a, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__


def dcos(x):
    return Dual(math.cos(x.a), -math.sin(x.a) * x.b)


def bond_energy(th, A, j, mutant):
    """u_j = 1 - cos D_j on duals (or theta-difference if gauge-blind)."""
    d = th[(j + 1) % N] - th[j]
    if mutant != "gauge-blind":
        d = d - A[j]
    return 1.0 - dcos(d)


def site_residuals(th, v, A, mutant):
    """Returns per-site residual list, per-site term sums, and the
    global residual / term sum / telescoping residual / |J| sum."""
    D = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    sD = [math.sin(x) for x in D]
    acc = [sD[j] - sD[j - 1] - GAMMA * v[j] + (F if j == B else 0.0)
           for j in range(N)]
    # duals: theta -> theta + eps v, v -> v + eps acc
    thd = [Dual(th[j], v[j]) for j in range(N)]
    vd = [Dual(v[j], acc[j]) for j in range(N)]
    u = [bond_energy(thd, A, j, mutant) for j in range(N)]
    h = [0.5 * vd[j] * vd[j] + 0.5 * (u[j - 1] + u[j]) for j in range(N)]
    if mutant == "current-blind":
        J = [-sD[j] * v[j] for j in range(N)]
    else:
        J = [-0.5 * sD[j] * (v[j] + v[(j + 1) % N]) for j in range(N)]
    res, T = [], []
    for j in range(N):
        sink = 0.0 if mutant == "sink-blind" else GAMMA * v[j] * v[j]
        src = F * v[j] if j == B else 0.0
        res.append(h[j].b + (J[j] - J[j - 1]) + sink - src)
        # term-magnitude sum from the pieces the dual computation
        # exposes: v a, the two half bond-energy rates, the two
        # currents, sink and source (the bound is 32 eps T_j)
        T.append(abs(v[j] * acc[j]) + 0.5 * abs(u[j - 1].b) + 0.5 * abs(u[j].b)
                 + abs(J[j]) + abs(J[j - 1]) + abs(sink) + abs(src))
    E = 0.5 * sum(x * x for x in vd) + sum(u, Dual(0.0))
    sink_tot = 0.0 if mutant == "sink-blind" else GAMMA * sum(x * x for x in v)
    g = E.b - F * v[B] + sink_tot
    gT = (sum(abs(v[j] * acc[j]) for j in range(N)) + sum(abs(x.b) for x in u)
          + abs(F * v[B]) + abs(sink_tot))
    tele = sum(J[j] - J[j - 1] for j in range(N))
    teleT = sum(abs(x) for x in J)
    return res, T, g, gT, tele, teleT


def check_states(twisted, vmax, M, rng):
    A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
    worst = worst_seam = worst_g = worst_tele = 0.0
    for _ in range(M):
        th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
        v = [rng.uniform(-vmax, vmax) for _ in range(N)]
        res, T, g, gT, tele, teleT = site_residuals(th, v, A, MUTANT)
        for j in range(N):
            q = abs(res[j]) / (OPS * EPS * T[j])
            worst = max(worst, q)
            if j in (0, 1):
                worst_seam = max(worst_seam, q)
        worst_g = max(worst_g, abs(g) / (OPS * EPS * gT))
        worst_tele = max(worst_tele, abs(tele) / (OPS * EPS * teleT))
    return worst, worst_seam, worst_g, worst_tele


def trajectory(dt, twisted, t_total=60.0, t_ramp=20.0, f_target=F_SMOOTH):
    """Own integrator: velocity-Verlet on the conservative + load
    part with the damping force taken at the old velocity. Discrete
    balance bookkeeping: injection f * displacement of the loaded
    site, dissipation gamma * v_old * displacement, current at the
    midpoint velocity. Returns the sup over unit samples of the
    global and the per-site defects."""
    A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
    delta = (math.pi / N) if twisted else 0.0
    th = [0.0] * N
    for j in range(1, N):
        th[j] = th[j - 1] + delta + A[j - 1]
    v = [0.0] * N

    def energies(th, v):
        thd = [Dual(x, 0.0) for x in th]
        u = [bond_energy(thd, A, j, None).a for j in range(N)]
        return [0.5 * v[j] * v[j] + 0.5 * (u[j - 1] + u[j]) for j in range(N)]

    def cons_acc(th):
        sD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        return [sD[j] - sD[j - 1] for j in range(N)], sD

    h0 = energies(th, v)
    E0 = sum(h0)
    inflow = [0.0] * N
    diss = [0.0] * N
    inj = 0.0
    steps = int(round(t_total / dt))
    per_unit = int(round(1.0 / dt))
    a_c, sD = cons_acc(th)
    sup_g = sup_l = 0.0
    for s in range(steps):
        f = f_target * min(1.0, (s + 1) * dt / t_ramp)
        acc = [a_c[j] - GAMMA * v[j] + (f if j == B else 0.0) for j in range(N)]
        vh = [v[j] + 0.5 * dt * acc[j] for j in range(N)]
        disp = [dt * vh[j] for j in range(N)]
        th_new = [th[j] + disp[j] for j in range(N)]
        a_c2, sD2 = cons_acc(th_new)
        acc2 = [a_c2[j] - GAMMA * v[j] + (f if j == B else 0.0) for j in range(N)]
        v_new = [vh[j] + 0.5 * dt * acc2[j] for j in range(N)]
        J = [-0.5 * sD2[j] * (vh[j] + vh[(j + 1) % N]) for j in range(N)]
        for j in range(N):
            inflow[j] += dt * (J[j - 1] - J[j])
            diss[j] += GAMMA * v[j] * disp[j]
        inj += f * disp[B]
        th, v, a_c, sD = th_new, v_new, a_c2, sD2
        if (s + 1) % per_unit:
            continue
        h = energies(th, v)
        sup_g = max(sup_g, abs((sum(h) - E0) - (inj - sum(diss))))
        for j in range(N):
            local = (h[j] - h0[j]) - (inflow[j] - diss[j] + (inj if j == B else 0.0))
            sup_l = max(sup_l, abs(local))
    return sup_g, sup_l


def own_fold(n, total):
    """Largest f with a quasi-static solution sin(s_j) = c + m f/n,
    sum s_j = total (fresh bisection structure, as in the P-46
    verify; nothing imported from the experiments)."""
    def feasible(f):
        lo, hi = -1.0 + 1e-9, 1.0 - (n - 1) * f / n - 1e-9
        if hi <= lo:
            return False

        def tot(c):
            return sum(math.asin(c + m * f / n) for m in range(n))
        return (tot(lo) - total) * (tot(hi) - total) <= 0
    f_lo, f_hi = 0.5, 3.5
    for _ in range(55):
        mid = 0.5 * (f_lo + f_hi)
        if feasible(mid):
            f_lo = mid
        else:
            f_hi = mid
    return f_lo


def euler_cromer_slip(dt, f_target, n=16, t_ramp=20.0, after=20.0,
                      t_cap=320.0, mutant=None):
    """Own Euler-Cromer in the P-36 order on a twisted ring of n
    sites (sector 0: every bond carries pi/n, A_0 = pi), dead-loaded
    at n/2 with a soft ramp, the discrete balance kept by
    force-times-displacement bookkeeping (injection f dt v', sink
    gamma dt v'^2, current from the post-step state). Runs to the
    P-36 event (max |D_j - D_j(0)| > 1.5 pi at a unit sample) plus
    `after`. Returns (event time or None, sup global defect, sup
    per-site defect) over the unit samples."""
    b = n // 2
    A = [math.pi if j == 0 else 0.0 for j in range(n)]
    th = [0.0] * n
    for j in range(1, n):
        th[j] = th[j - 1] + math.pi / n + A[j - 1]
    v = [0.0] * n

    def strains(th):
        return [th[(j + 1) % n] - th[j] - A[j] for j in range(n)]

    def energies(th, v):
        u = [1.0 - math.cos(x) for x in strains(th)]
        if mutant == "share-blind":
            return [0.5 * v[j] * v[j] + u[j] for j in range(n)]
        return [0.5 * v[j] * v[j] + 0.5 * (u[j - 1] + u[j]) for j in range(n)]

    D0 = strains(th)
    sinD = [math.sin(x) for x in D0]
    h0 = energies(th, v)
    E0 = sum(h0)
    inflow = [0.0] * n
    diss = [0.0] * n
    inj = 0.0
    per_unit = int(round(1.0 / dt))
    n_total = int(round(t_cap / dt))
    sup_g = sup_l = 0.0
    event = None
    s = 0
    while s < n_total:
        f = f_target * min(1.0, (s + 1) * dt / t_ramp)
        for j in range(n):
            v[j] += dt * (sinD[j] - sinD[j - 1] - GAMMA * v[j]
                          + (f if j == b else 0.0))
        for j in range(n):
            th[j] += dt * v[j]
        sinD = [math.sin(x) for x in strains(th)]
        J = [-0.5 * sinD[j] * (v[j] + v[(j + 1) % n]) for j in range(n)]
        for j in range(n):
            inflow[j] += dt * (J[j - 1] - J[j])
            diss[j] += GAMMA * dt * v[j] * v[j]
        inj += f * dt * v[b]
        s += 1
        if s % per_unit:
            continue
        h = energies(th, v)
        sup_g = max(sup_g, abs((sum(h) - E0) - (inj - sum(diss))))
        for j in range(n):
            local = (h[j] - h0[j]) - (inflow[j] - diss[j] + (inj if j == b else 0.0))
            sup_l = max(sup_l, abs(local))
        if event is None:
            D = strains(th)
            if max(abs(D[j] - D0[j]) for j in range(n)) > 1.5 * math.pi:
                event = s * dt
                n_total = s + int(round(after / dt))
    return event, sup_g, sup_l


def in_band(D):
    r1, r2 = D[0] / D[1], D[1] / D[2]
    return (D[0] > D[1] > D[2] and ORDER_BAND[0] <= r1 <= ORDER_BAND[1]
            and ORDER_BAND[0] <= r2 <= ORDER_BAND[1]), (r1, r2)


def main():
    failed = False
    rng = random.Random(4545)
    for twisted in (False, True):
        for vmax in (2.0, 100.0):
            w, ws, wg, wt = check_states(twisted, vmax, 3000, rng)
            print(f"twisted={twisted} vmax={vmax:g}: site {w:.3f} seam {ws:.3f} "
                  f"global {wg:.3f} telescoping {wt:.3f} (ratios to the bound)")
            if w > 1.0:
                print("FAIL: per-site residual above the floating-point bound")
                failed = True
            if wg > 1.0 or wt > 1.0:
                print("FAIL: global balance or telescoping sum above the bound")
                failed = True
            if twisted and ws > 1.0:
                print("FAIL: seam sites of the twisted ring above the bound")
                failed = True
    if not failed:
        for twisted in (False, True):
            Dg, Dl = [], []
            for k in range(3):
                g, l = trajectory(0.02 / 2 ** k, twisted)
                Dg.append(g)
                Dl.append(l)
            rg = (Dg[0] / Dg[1], Dg[1] / Dg[2])
            rl = (Dl[0] / Dl[1], Dl[1] / Dl[2])
            print(f"own integrator twisted={twisted}: global defects "
                  f"{Dg[0]:.3e} {Dg[1]:.3e} {Dg[2]:.3e} ratios {rg[0]:.3f} {rg[1]:.3f}; "
                  f"per-site {Dl[0]:.3e} {Dl[1]:.3e} {Dl[2]:.3e} ratios {rl[0]:.3f} {rl[1]:.3f}")
            if not (Dg[0] > Dg[1] > Dg[2] and min(rg) >= ROOT2):
                print("FAIL: global balance defect does not converge on the own integrator")
                failed = True
            if not (Dl[0] > Dl[1] > Dl[2] and min(rl) >= ROOT2):
                print("FAIL: per-site balance defect does not converge on the own integrator")
                failed = True
    if not failed:
        # (5) the order test through the slip, own Euler-Cromer
        n_slip = 16
        f_slip = own_fold(n_slip, -math.pi) + 0.02
        evs, Dg, Dl = [], [], []
        for k in range(3):
            ev, g, l = euler_cromer_slip(0.001 / 2 ** k, f_slip, n=n_slip,
                                         mutant=MUTANT)
            evs.append(ev)
            Dg.append(g)
            Dl.append(l)
        okg, rg = in_band(Dg)
        okl, rl = in_band(Dl)
        print(f"own Euler-Cromer through the slip (N = {n_slip}, f = {f_slip:.4f}, "
              f"f/gamma = {f_slip / GAMMA:.0f}): events {evs}; global defects "
              f"{Dg[0]:.3e} {Dg[1]:.3e} {Dg[2]:.3e} ratios {rg[0]:.3f} {rg[1]:.3f}; "
              f"per-site {Dl[0]:.3e} {Dl[1]:.3e} {Dl[2]:.3e} ratios {rl[0]:.3f} {rl[1]:.3f}")
        if any(e is None for e in evs):
            print("FAIL: no slip on some rung above the fold")
            failed = True
        if not okg:
            print("FAIL: global balance through the slip is not first order "
                  f"(band [{ORDER_BAND[0]:.3f}, {ORDER_BAND[1]:.3f}])")
            failed = True
        if not okl:
            print("FAIL: per-site balance through the slip is not first order "
                  f"(band [{ORDER_BAND[0]:.3f}, {ORDER_BAND[1]:.3f}])")
            failed = True
    if MUTANT is not None:
        if failed:
            print(f"mutant {MUTANT} broke the verification as it must")
            sys.exit(1)
        print(f"mutant {MUTANT} did not break the verification")
        sys.exit(3)
    if failed:
        sys.exit(1)
    print("p45 verification ok")


if __name__ == "__main__":
    main()
