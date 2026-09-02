#!/usr/bin/env python3
"""Verification for the P-46 claim slip-aftermath-is-off-band, by
independent reimplementation on a small cell (N = 16, gamma = 0.1,
f = fold + 0.02): own velocity-Verlet integrator with the damping
force at the old velocity (a different scheme and ordering from the
experiment's Euler-Cromer), own event detector, own lock-in, and
the evanescent response obtained NOT from the closed-form root but
by a direct complex tridiagonal solve of the driven damped chain -
a different route to the same linear physics. Nothing read from
results files.

Checks: (1) the exact discrete momentum recursion of the own
scheme, P' = P + dt (f_avg - gamma P), at the floor at every step
(the bond forces telescope for velocity-Verlet too); (2) the ring
share's exact identity P_ring' = P_ring + dt (-gamma P_ring - T)
with T = sin D_b - sin D_{b-1} the two-bond rotor torque; (3) drift
transfer: P_ring at Delta = 20 and 30 (2/gamma and 3/gamma) within
4 / Omega(10) of P_ring(10) e^{-gamma (Delta - 10)}; (4) evanescence: lock-in
amplitudes at offsets 1 and 2 over Delta in [100, 160] against the
tridiagonal solve, within the run's own lock-in floor plus the
stiffness band.

--mutant bond-blind   the ring-share identity with one rotor bond
    only (drops sin D_{b-1}); O(1) residual kills it.
--mutant rate-blind   asserts the ring's drift decays at 2 gamma;
    check (3) kills it.
--mutant band-blind   asserts the per-site tail ratio is 1 / Omega
    instead of the evanescent root ~ c / Omega^2; check (4) kills
    it by two orders of magnitude.
"""
import cmath
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"bond-blind", "rate-blind", "band-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

EPS = 2.0 ** -52
OPS = 32
N = 16
B = N // 2
GAMMA = 0.1
DT = 0.0005
TAU = 2 * math.pi


def own_fold(total):
    """Largest f with a quasi-static solution sin(s_j) = c + m f/N,
    sum s_j = total (fresh bisection structure)."""
    def feasible(f):
        lo, hi = -1.0 + 1e-9, 1.0 - (N - 1) * f / N - 1e-9
        if hi <= lo:
            return False

        def tot(c):
            return sum(math.asin(c + m * f / N) for m in range(N))
        return (tot(lo) - total) * (tot(hi) - total) <= 0
    f_lo, f_hi = 0.5, 3.5
    for _ in range(55):
        mid = 0.5 * (f_lo + f_hi)
        if feasible(mid):
            f_lo = mid
        else:
            f_hi = mid
    return f_lo


def chain_response(Omega, c, gamma, M=12):
    """Driven damped chain of M sites with a unit force on site 0 and
    site M-1 clamped, solved directly: (-z I + c L) x = F with
    z = Omega^2 - i gamma Omega, L the semi-infinite-end Laplacian.
    Returns velocity amplitudes |i Omega x_d| for d = 0, 1, 2."""
    z = complex(Omega * Omega, -gamma * Omega)
    # tridiagonal: row 0 has one neighbour, rows 1..M-2 two
    a = [0.0] * M   # sub
    d = [0j] * M    # diag
    e = [0.0] * M   # super
    rhs = [0j] * M
    for j in range(M):
        nb = 1 if j == 0 else 2
        d[j] = -z + c * nb
        if j > 0:
            a[j] = -c
        if j < M - 1:
            e[j] = -c
    rhs[0] = 1.0 + 0j
    # Thomas algorithm
    cp = [0j] * M
    dp = [0j] * M
    cp[0] = e[0] / d[0]
    dp[0] = rhs[0] / d[0]
    for j in range(1, M):
        den = d[j] - a[j] * cp[j - 1]
        cp[j] = e[j] / den if j < M - 1 else 0j
        dp[j] = (rhs[j] - a[j] * dp[j - 1]) / den
    x = [0j] * M
    x[M - 1] = dp[M - 1]
    for j in range(M - 2, -1, -1):
        x[j] = dp[j] - cp[j] * x[j + 1]
    return [abs(Omega * x[k]) for k in range(3)]


def run(f_target, t_ramp=100.0, after=160.0, dt=DT, lock_window=(100.0, 160.0)):
    A = [math.pi if j == 0 else 0.0 for j in range(N)]
    delta = math.pi / N
    th = [0.0] * N
    for j in range(1, N):
        th[j] = th[j - 1] + delta + A[j - 1]
    v = [0.0] * N
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]

    def cons(th):
        sD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        return [sD[j] - sD[j - 1] for j in range(N)], sD
    a_c, sD = cons(th)
    per_unit = int(round(1.0 / dt))
    steps_cap = int(round((t_ramp + 400.0) / dt))
    worst_P = worst_R = 0.0
    P = 0.0
    Pr = 0.0
    event = None
    samples = {}
    lock = [0j, 0j, 0j]
    nlock = 0
    om_acc = 0.0
    wave = 0.0
    cmin, cmax = 1.0, -1.0
    s = 0
    n_total = steps_cap
    while s < n_total:
        f0 = f_target * min(1.0, s * dt / t_ramp)
        f1 = f_target * min(1.0, (s + 1) * dt / t_ramp)
        T_old = sD[B] - sD[B - 1]
        acc = [a_c[j] - GAMMA * v[j] + (f0 if j == B else 0.0) for j in range(N)]
        vh = [v[j] + 0.5 * dt * acc[j] for j in range(N)]
        th = [th[j] + dt * vh[j] for j in range(N)]
        a_c2, sD2 = cons(th)
        acc2 = [a_c2[j] - GAMMA * v[j] + (f1 if j == B else 0.0) for j in range(N)]
        v_new = [vh[j] + 0.5 * dt * acc2[j] for j in range(N)]
        T_new = sD2[B] - sD2[B - 1]
        P_new = sum(v_new)
        pred = P + dt * (0.5 * (f0 + f1) - GAMMA * P)
        bound = OPS * EPS * (abs(P) + sum(abs(x) for x in v_new) + dt * (abs(f1) + GAMMA * abs(P))
                             + dt * (sum(abs(x) for x in sD) + sum(abs(x) for x in sD2)))
        worst_P = max(worst_P, abs(P_new - pred) / bound)
        Pr_new = P_new - v_new[B]
        if MUTANT == "bond-blind":
            torque = 0.5 * (sD[B] + sD2[B])
        else:
            torque = 0.5 * (T_old + T_new)
        pred_r = Pr + dt * (-GAMMA * Pr - torque)
        bound_r = OPS * EPS * (abs(P_new) + abs(v_new[B]) + sum(abs(x) for x in v_new)
                               + abs(Pr) + dt * (GAMMA * abs(Pr) + 2.0)
                               + dt * (sum(abs(x) for x in sD) + sum(abs(x) for x in sD2)))
        worst_R = max(worst_R, abs(Pr_new - pred_r) / bound_r)
        v, a_c, sD, P, Pr = v_new, a_c2, sD2, P_new, Pr_new
        s += 1
        if event is None:
            if s % per_unit == 0:
                D = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
                if max(abs(D[j] - D0[j]) for j in range(N)) > 1.5 * math.pi:
                    event = s
                    n_total = s + int(round(after / dt))
                    samples[0] = (P, Pr, v[B])
            continue
        Delta = (s - event) * dt
        if s % per_unit == 0:
            samples[int(round(Delta))] = (P, Pr, v[B])
        if lock_window[0] <= Delta < lock_window[1]:
            # reference = the driving bond's own phase
            e = cmath.exp(complex(0.0, -(th[B] - th[(B + 1) % N])))
            for d in range(3):
                lock[d] += v[(B + 1 + d) % N] * e
            nlock += 1
            om_acc += v[B]
            if s % per_unit == 0:
                vbar = Pr / (N - 1)
                wave = max(wave, max(abs(v[j] - vbar) for j in range(N)
                                     if min(abs(j - B), N - abs(j - B)) >= 2))
                for j in range(N):
                    if j not in (B, B - 1):
                        c = math.cos(th[(j + 1) % N] - th[j] - A[j])
                        cmin, cmax = min(cmin, c), max(cmax, c)
    Om = om_acc / nlock
    Tw = nlock * dt
    return {"event": event * dt if event else None, "worst_P": worst_P, "worst_R": worst_R,
            "samples": samples, "A": [2.0 * abs(z) / nlock for z in lock],
            "omega": Om, "floor": 2 * wave / (Tw * (Om - 2.0)), "cmin": cmin, "cmax": cmax}


def main():
    failed = False
    fold = own_fold(-math.pi)
    closed = 2.0 * N / (N - 1)
    f = fold + 0.02
    r = run(f)
    print(f"twisted fold {fold:.5f} (control closed form {closed:.5f}); f = {f:.5f}; "
          f"event at {r['event']}")
    if r["event"] is None:
        print("FAIL: no event above the fold")
        sys.exit(1)
    print(f"momentum recursion worst {r['worst_P']:.3f} of floor; ring-share identity "
          f"worst {r['worst_R']:.3f} of floor")
    if r["worst_P"] > 1.0:
        print("FAIL: total momentum recursion above the floor")
        failed = True
    if r["worst_R"] > 1.0:
        print("FAIL: ring-share identity (two-bond torque) above the floor")
        failed = True
    sm = r["samples"]
    rate = 2.0 * GAMMA if MUTANT == "rate-blind" else GAMMA
    Pr10, Om10 = sm[10][1], sm[10][2]
    for D in (20, 30):
        pred = Pr10 * math.exp(-rate * (D - 10))
        dev = sm[D][1] - pred
        print(f"drift transfer Delta {D}: P_ring {sm[D][1]:.4f} vs {pred:.4f} "
              f"(dev {dev:.2e}, bound {4.0 / Om10:.2e})")
        if abs(dev) > 4.0 / Om10:
            print("FAIL: ring drift does not decay at the asserted rate")
            failed = True
    Om = r["omega"]
    A1s, ws = [], []
    for c in (r["cmin"], r["cmax"]):
        resp = chain_response(Om, c, GAMMA)
        A1s.append(resp[0])
        ws.append(resp[1] / resp[0])
    if MUTANT == "band-blind":
        ws = [1.0 / Om, 1.0 / Om]
    A = r["A"]
    # the run's own lock-in floor plus the scheme's amplitude error:
    # velocity-Verlet is second order, its amplitude error is below
    # (dt Omega)^2 relative (the undamped oscillator's is zero, the
    # frequency error (dt Omega)^2 / 24)
    # ... and the 2-Omega leakage of the demodulated product, A_d / (Omega T)
    fl = r["floor"] + A[0] * (DT * Om) ** 2 + A[0] / (Om * 60.0)
    fl2 = r["floor"] + A[1] * (DT * Om) ** 2 + A[1] / (Om * 60.0)
    print(f"lock-in over [100,160): Omega {Om:.3f}, A1 {A[0]:.4e} vs solve "
          f"[{min(A1s):.4e}, {max(A1s):.4e}] floor {fl:.1e}; A2/A1 {A[1] / A[0]:.3e} vs "
          f"[{min(ws):.3e}, {max(ws):.3e}]")
    if not (min(A1s) - fl <= A[0] <= max(A1s) + fl):
        print("FAIL: end-site amplitude off the linear response")
        failed = True
    pred2 = [A[0] * x for x in ws]
    if not (min(pred2) - fl2 <= A[1] <= max(pred2) + fl2):
        print("FAIL: offset-2 amplitude off the evanescent tail")
        failed = True
    if MUTANT is not None:
        if failed:
            print(f"mutant {MUTANT} broke the verification as it must")
            sys.exit(1)
        print(f"mutant {MUTANT} did not break the verification")
        sys.exit(3)
    if failed:
        sys.exit(1)
    print("p46 verification ok")


if __name__ == "__main__":
    main()
