#!/usr/bin/env python3
"""Verification for the P-47 claim quench-counts-share-one-density,
by independent reimplementation on a small cell (N = 16): the
shared density computed NOT by the characteristic-function integral
of the experiment but by direct N-fold numerical convolution of the
wrapped single-bond density on a grid; its own Langevin ring
(velocity-Verlet with the noise applied at the half step, a
different scheme and ordering); its own equilibrium sampler and
quench. Nothing read from results files.

Checks: (1) the covariant winding sits on its lattice (integer
control, half-integer twisted) at every sample of every run, at
1e-12 - the count is arithmetic; (2) equilibrium anchor at T = 0.5:
both rings' <W^2> within 3 model-SE of the convolution's lattice
moments, with the twisted moment predicted from the control's
through the curve; (3) the half-quantum floor: the twisted ring's
W^2 >= 1/4 at every sample, and at T = 0.2 the twisted <W^2> reads
0.25 while the shift-free prediction from the control would be
under 0.02; (4) a quench at tau_Q = 20: the twisted <W^2> within 3
combined SE of the value predicted from the control's.

--mutant shift-blind   predicts the twisted moment equal to the
    control's (no lattice shift); check (3) kills it at T = 0.2.
--mutant count-blind   reads the unwrapped strain sum instead of
    the winding: that is the topological constant -sum A / 2 pi,
    zero variance at every temperature; check (2) kills it.
"""
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"shift-blind", "count-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

TAU = 2 * math.pi
N = 16
GAMMA = 1.0
DT = 0.02


def wrap(x):
    return (x + math.pi) % TAU - math.pi


# ---------- the shared density by direct convolution ----------

def bond_density(T, n):
    h = TAU / n
    w = [math.exp((math.cos(-math.pi + (i + 0.5) * h) - 1.0) / T) for i in range(n)]
    Z = sum(w) * h
    return [x / Z for x in w], h


def convolve(a, b, h):
    """Linear convolution of two sampled densities on the same grid."""
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0.0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return [x * h for x in out]


def sum_density(T, n=160):
    """Density of S = sum of N wrapped strains, on a grid from -N pi
    to N pi, by repeated convolution (N = 16: four doublings)."""
    d, h = bond_density(T, n)
    cur, lo = d, -math.pi
    k = 1
    while k < N:
        cur = convolve(cur, cur, h)
        lo *= 2
        k *= 2
    return cur, lo, h


def lattice(T):
    rho, lo, h = sum_density(T)

    def at(S):
        x = (S - lo) / h - 0.5
        i = int(math.floor(x))
        if i < 0 or i + 1 >= len(rho):
            return 0.0
        f = x - i
        return rho[i] * (1 - f) + rho[i + 1] * f
    nmax = N // 2
    Pc = {n: at(TAU * n) for n in range(-nmax, nmax + 1)}
    Pt = {n - 0.5: at(TAU * (n - 0.5)) for n in range(-nmax + 1, nmax + 1)}
    Zc, Zt = sum(Pc.values()), sum(Pt.values())
    Pc = {k: v / Zc for k, v in Pc.items()}
    Pt = {k: v / Zt for k, v in Pt.items()}
    Ec = sum(w * w * p for w, p in Pc.items())
    Et = sum(w * w * p for w, p in Pt.items())
    return Ec, Et, Pc, Pt


def model_se(P, M):
    e2 = sum(w * w * p for w, p in P.items())
    e4 = sum(w ** 4 * p for w, p in P.items())
    # floor at the smallest resolvable moment so a degenerate
    # prediction (every sample at one lattice point) reads as an
    # enormous z rather than a division by zero
    return max(math.sqrt(max(e4 - e2 * e2, 0.0) / M), 1e-9)


def predict_tw(Ec_meas):
    lo, hi = 0.03, 2.0
    for _ in range(18):
        mid = 0.5 * (lo + hi)
        Ec, Et, _, _ = lattice(mid)
        if Ec < Ec_meas:
            lo = mid
        else:
            hi = mid
    T = 0.5 * (lo + hi)
    Ec, Et, Pc, Pt = lattice(T)
    if MUTANT == "shift-blind":
        return T, Ec, Pc
    return T, Et, Pt


# ---------- own Langevin ring ----------

def winding_of(th, A):
    if MUTANT == "count-blind":
        return sum(th[(j + 1) % N] - th[j] - A[j] for j in range(N)) / TAU
    return sum(wrap(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)) / TAU


def run(twisted, rng, T_sched, dt=DT):
    """Velocity-Verlet with the noise kick at the half step. T_sched
    maps step -> temperature. Returns the final winding and the worst
    lattice offset seen at unit samples."""
    A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
    th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
    T0 = T_sched(0)
    v = [rng.gauss(0.0, math.sqrt(T0)) for _ in range(N)]

    def force(th):
        sD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        return [sD[j] - sD[j - 1] for j in range(N)]
    F = force(th)
    worst = 0.0
    s = 0
    per_unit = int(round(1.0 / dt))
    while True:
        T = T_sched(s)
        if T is None:
            break
        sig = math.sqrt(2 * GAMMA * T * dt) if T > 0 else 0.0
        vh = [v[j] + 0.5 * dt * (F[j] - GAMMA * v[j]) + (sig * rng.gauss(0, 1) if sig else 0.0)
              for j in range(N)]
        th = [th[j] + dt * vh[j] for j in range(N)]
        F = force(th)
        v = [vh[j] + 0.5 * dt * (F[j] - GAMMA * vh[j]) for j in range(N)]
        s += 1
        if s % per_unit == 0:
            W = winding_of(th, A)
            off = abs(W - (round(W - 0.5) + 0.5)) if twisted else abs(W - round(W))
            worst = max(worst, off)
    return winding_of(th, A), worst


def equilibrium(twisted, T, rng, M=100, t_therm=40.0, t_gap=20.0):
    n_th = int(round(t_therm / DT))
    n_gap = int(round(t_gap / DT))
    total = n_th + M * n_gap
    Ws = []
    # single long run, sampled every gap: implemented by a schedule
    # that stops at each sample point is awkward, so run once and
    # collect via a closure over the step counter
    A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
    th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
    v = [rng.gauss(0.0, math.sqrt(T)) for _ in range(N)]

    def force(th):
        sD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        return [sD[j] - sD[j - 1] for j in range(N)]
    F = force(th)
    sig = math.sqrt(2 * GAMMA * T * DT)
    worst = 0.0
    for s in range(1, total + 1):
        vh = [v[j] + 0.5 * DT * (F[j] - GAMMA * v[j]) + sig * rng.gauss(0, 1) for j in range(N)]
        th = [th[j] + DT * vh[j] for j in range(N)]
        F = force(th)
        v = [vh[j] + 0.5 * DT * (F[j] - GAMMA * vh[j]) for j in range(N)]
        if s > n_th and (s - n_th) % n_gap == 0:
            W = winding_of(th, A)
            off = abs(W - (round(W - 0.5) + 0.5)) if twisted else abs(W - round(W))
            worst = max(worst, off)
            Ws.append(W)
    return Ws, worst


def main():
    failed = False
    tol = 1e-12
    floor = 0.25
    rng = random.Random(4747)
    # (2) anchor at T = 0.5
    Ec, Et, Pc, Pt = lattice(0.5)
    Wc, offc = equilibrium(False, 0.5, rng)
    Wt, offt = equilibrium(True, 0.5, rng)
    mc = sum(w * w for w in Wc) / len(Wc)
    mt = sum(w * w for w in Wt) / len(Wt)
    zc = (mc - Ec) / model_se(Pc, len(Wc))
    Teff, Et_pred, Pt_pred = predict_tw(mc)
    zt = (mt - Et_pred) / model_se(Pt_pred, len(Wt))
    print(f"anchor T 0.5: control <W^2> {mc:.3f} vs convolution {Ec:.3f} (z {zc:.2f}); "
          f"twisted {mt:.3f} vs predicted-from-control {Et_pred:.3f} at T_eff {Teff:.3f} (z {zt:.2f}); "
          f"lattice offsets {offc:.1e} {offt:.1e}")
    if max(offc, offt) > tol:
        print("FAIL: winding off its lattice")
        failed = True
    if abs(zc) > 3 or abs(zt) > 3:
        print("FAIL: equilibrium moments off the shared density")
        failed = True
    # (3) the floor at T = 0.2
    Wt2, offt2 = equilibrium(True, 0.2, rng, M=60, t_therm=40.0, t_gap=10.0)
    Wc2, offc2 = equilibrium(False, 0.2, rng, M=60, t_therm=40.0, t_gap=10.0)
    mt2 = sum(w * w for w in Wt2) / len(Wt2)
    mc2 = sum(w * w for w in Wc2) / len(Wc2)
    minW2 = min(w * w for w in Wt2)
    _, Et2_pred, _ = predict_tw(mc2)
    print(f"floor T 0.2: twisted <W^2> {mt2:.4f} (min W^2 {minW2:.4f}), control {mc2:.4f}, "
          f"predicted twisted {Et2_pred:.4f}")
    if minW2 < floor - 1e-12:
        print("FAIL: a twisted sample below the half-quantum floor")
        failed = True
    if abs(mt2 - Et2_pred) > 0.1:
        print("FAIL: twisted moment at T = 0.2 is not the shifted-lattice value")
        failed = True
    if max(offt2, offc2) > tol:
        print("FAIL: winding off its lattice at T = 0.2")
        failed = True
    # (4) a quench, tau_Q = 20, M = 60 each
    T_i, tau, burn, settle = 2.0, 20.0, 20.0, 20.0
    n_b, n_r, n_s = int(burn / DT), int(tau / DT), int(settle / DT)

    def sched(s):
        if s < n_b:
            return T_i
        if s < n_b + n_r:
            return T_i * (1.0 - (s - n_b + 1) / n_r)
        if s < n_b + n_r + n_s:
            return 0.0
        return None
    Wqc, Wqt = [], []
    worst = 0.0
    for _ in range(60):
        W, off = run(False, rng, sched)
        Wqc.append(W)
        worst = max(worst, off)
        W, off = run(True, rng, sched)
        Wqt.append(W)
        worst = max(worst, off)
    mqc = sum(w * w for w in Wqc) / 60
    mqt = sum(w * w for w in Wqt) / 60
    Tq, Etq, Ptq = predict_tw(mqc)
    se = math.sqrt(model_se(Ptq, 60) ** 2 + (sum(w ** 4 for w in Wqc) / 60 - mqc ** 2) / 60)
    zq = (mqt - Etq) / se
    print(f"quench tau_Q 20: control <W^2> {mqc:.3f}, twisted {mqt:.3f} vs predicted {Etq:.3f} "
          f"at T_eff {Tq:.3f} (z {zq:.2f}); lattice offset {worst:.1e}")
    if worst > tol:
        print("FAIL: winding off its lattice in the quench")
        failed = True
    if abs(zq) > 3:
        print("FAIL: quenched twisted moment off the shared-density prediction")
        failed = True
    if MUTANT is not None:
        if failed:
            print(f"mutant {MUTANT} broke the verification as it must")
            sys.exit(1)
        print(f"mutant {MUTANT} did not break the verification")
        sys.exit(3)
    if failed:
        sys.exit(1)
    print("p47 verification ok")


if __name__ == "__main__":
    main()
