#!/usr/bin/env python3
"""Verification for the P-48 claim stiffness-is-a-clock, by
independent reimplementation on small cells. Nothing imported from
the experiment scripts, nothing read from results files.

Checks: (1) the map identity: one Euler-Cromer step of the
stiffness-kappa ring, (kappa, gamma, f, dt) on (theta, v), against
one step of the unit-stiffness ring, (1, gamma/sqrt kappa, f/kappa,
sqrt kappa dt) on (theta, v/sqrt kappa), at 2000 random states on
an N = 16 twisted ring for kappa in {0.5, 2, 3}: residuals within
32 eps of the summands' magnitudes; (2) the same identity along a
whole trajectory through the slip at kappa = 3 (a non-dyadic root,
so the roundings differ): identical event step and the phase
deviation within 32 eps times the step count times the largest
phase; (3) the tail law near the band on an own N = 16 ring at
gamma = 0.5 (rotor at Omega ~ 3.7, band top 2): the offset-2 ratio
demodulated against the rotor's phase lies in the |w| band of a
direct complex tridiagonal solve at the window's stiffness range,
widened by the run's own floors, and the same ratio demodulated
against the bond phase lies within the band plus those floors plus
the derived mixing term (A_1/(2 Omega)) v_slow. Coverage (L-13):
on a ring this small the slip's long-wavelength mode is underdamped
and gone by the window, so the mixing term is 0.2 percent of A_2
here and cannot be made to bite - the N = 64 mixing reading (27
percent at gamma 0.5) rests on the experiment layer alone.

--mutant kappa-blind      scales gamma by 1/kappa instead of
    1/sqrt kappa in the identity; check (1) kills it.
--mutant load-blind       scales f by 1/sqrt kappa instead of
    1/kappa; check (1) kills it.
(A reference-blind mutant - the bond-phase reading asserted to be
the tail with no mixing term - was tried at N = 16 and N = 32 and
did not break: recorded, not pinned, per L-8.)
"""
import cmath
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"kappa-blind", "load-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

EPS = 2.0 ** -52
OPS = 32
N = 16
B = N // 2


def twisted_ring():
    A = [math.pi if j == 0 else 0.0 for j in range(N)]
    th = [0.0] * N
    for j in range(1, N):
        th[j] = th[j - 1] + math.pi / N + A[j - 1]
    return A, th


def step(th, v, A, gamma, f, kappa, dt):
    sD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
    v2 = [v[j] + dt * (kappa * (sD[j] - sD[j - 1]) - gamma * v[j]
                       + (f if j == B else 0.0)) for j in range(N)]
    th2 = [th[j] + dt * v2[j] for j in range(N)]
    return th2, v2


def own_fold(n, total):
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


def scaled(gamma, f, kappa):
    s = math.sqrt(kappa)
    g2 = gamma / (kappa if MUTANT == "kappa-blind" else s)
    f2 = f / (s if MUTANT == "load-blind" else kappa)
    return g2, f2, s


def check_identity(rng, kappa, gamma=0.1, f=1.9, dt=0.001, M=2000):
    A, _ = twisted_ring()
    g2, f2, s = scaled(gamma, f, kappa)
    worst = 0.0
    for _ in range(M):
        th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
        v = [rng.uniform(-3.0, 3.0) for _ in range(N)]
        thA, vA = step(th, v, A, gamma, f, kappa, dt)
        thB, uB = step(th, [x / s for x in v], A, g2, f2, 1.0, s * dt)
        for j in range(N):
            bv = OPS * EPS * (abs(v[j]) / s + s * dt * (2.0 + g2 * abs(v[j]) / s + abs(f2)))
            bt = OPS * EPS * (abs(th[j]) + s * dt * abs(uB[j]))
            worst = max(worst, abs(vA[j] / s - uB[j]) / bv, abs(thA[j] - thB[j]) / bt)
    return worst


def run_ring(gamma, f, kappa, dt, n_ramp, sample, after_steps, cap, lock=None):
    """Own trajectory of the kappa ring; optional lock-in over a step
    window [w0, w1) after the event with both references, returning
    the per-offset amplitudes and the slow (period-averaged) velocity."""
    A, th = twisted_ring()
    v = [0.0] * N
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    event = None
    n_total = cap
    samples = []
    acc_b = {d: 0j for d in (1, 2, 3)}
    acc_r = {d: 0j for d in (1, 2, 3)}
    n_lock = 0
    om = 0.0
    wave = 0.0
    cmin, cmax = 1.0, -1.0
    slow_series = {1: [], 2: []}
    s = 0
    while s < n_total:
        f_now = f * min(1.0, (s + 1) / n_ramp)
        th, v = step(th, v, A, gamma, f_now, kappa, dt)
        s += 1
        if s % sample == 0:
            samples.append((s, list(th), list(v)))
            if event is None:
                D = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
                if max(abs(D[j] - D0[j]) for j in range(N)) > 1.5 * math.pi:
                    event = s
                    n_total = s + after_steps
        if lock and event is not None and event + lock[0] <= s < event + lock[1]:
            eb = cmath.exp(complex(0.0, -(th[B] - th[(B + 1) % N])))
            er = cmath.exp(complex(0.0, -th[B]))
            for d in (1, 2, 3):
                acc_b[d] += v[(B + d) % N] * eb
                acc_r[d] += v[(B + d) % N] * er
            n_lock += 1
            om += v[B]
            for d in (1, 2):
                slow_series[d].append(v[(B + d) % N])
            if s % sample == 0:
                vbar = (sum(v) - v[B]) / (N - 1)
                wave = max(wave, max(abs(v[j] - vbar) for j in range(N)
                                     if min(abs(j - B), N - abs(j - B)) >= 2))
                for j in range(N):
                    if j not in (B, B - 1):
                        c = math.cos(th[(j + 1) % N] - th[j] - A[j])
                        cmin, cmax = min(cmin, c), max(cmax, c)
    out = {"event": event, "samples": samples}
    if lock and n_lock:
        Om = om / n_lock
        Tw = n_lock * dt
        per = max(1, int(round(2 * math.pi / Om / dt)))
        slow = {}
        for d in (1, 2):
            ser = slow_series[d]
            means = [sum(ser[k:k + per]) / per for k in range(0, len(ser) - per + 1, per)]
            slow[d] = math.sqrt(sum(m * m for m in means) / len(means)) if means else 0.0
        out.update({"Omega": Om, "T": Tw,
                    "A_bond": {d: 2.0 * abs(acc_b[d]) / n_lock for d in acc_b},
                    "A_rotor": {d: 2.0 * abs(acc_r[d]) / n_lock for d in acc_r},
                    "wave_floor": 2.0 * wave / (Tw * (Om - 2.0)), "cmin": cmin, "cmax": cmax,
                    "slow": slow})
    return out


def chain_response(Omega, c, gamma, M=12):
    z = complex(Omega * Omega, -gamma * Omega)
    a = [0.0] * M
    d = [0j] * M
    e = [0.0] * M
    rhs = [0j] * M
    for j in range(M):
        d[j] = -z + c * (1 if j == 0 else 2)
        if j > 0:
            a[j] = -c
        if j < M - 1:
            e[j] = -c
    rhs[0] = 1.0 + 0j
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


def main():
    failed = False
    rng = random.Random(4848)
    # (1) the map identity
    for kappa in (0.5, 2.0, 3.0):
        w = check_identity(rng, kappa)
        print(f"map identity kappa {kappa:g}: worst residual {w:.3f} of the floor")
        if w > 1.0:
            print("FAIL: the stiffness scaling is not an identity of the map")
            failed = True
    # (2) the trajectory identity at kappa = 3, through the slip
    kappa, gamma, dt = 3.0, 0.1, 0.001
    f1 = own_fold(N, -math.pi) + 0.02
    g2, f2, s = scaled(gamma, kappa * f1, kappa)
    n_ramp = int(round(50.0 / dt))
    ra = run_ring(gamma, kappa * f1, kappa, dt, n_ramp, int(round(1.0 / dt)),
                  int(round(30.0 / dt)), int(round(400.0 / dt)))
    rb = run_ring(g2, f2, 1.0, s * dt, n_ramp, int(round(1.0 / dt)),
                  int(round(30.0 / dt)), int(round(400.0 / dt)))
    dev = 0.0
    thmax = 0.0
    for (sa, tha, va), (sb, thb, vb) in zip(ra["samples"], rb["samples"]):
        dev = max(dev, max(abs(tha[j] - thb[j]) for j in range(N)))
        thmax = max(thmax, max(abs(x) for x in tha))
    nsteps = ra["samples"][-1][0] if ra["samples"] else 1
    bound = OPS * EPS * nsteps * thmax
    print(f"trajectory kappa {kappa:g}: events {ra['event']} / {rb['event']} steps; "
          f"max phase deviation {dev:.2e} against {bound:.2e}")
    if ra["event"] is None or ra["event"] != rb["event"] or dev > bound:
        print("FAIL: the scaled trajectories part through the slip")
        failed = True
    # (3) the tail law near the band, two references
    gamma3 = 0.5
    f3 = own_fold(N, -math.pi) + 0.02
    r = run_ring(gamma3, f3, 1.0, dt, int(round(50.0 / dt)), int(round(1.0 / dt)),
                 int(round(80.0 / dt)), int(round(1500.0 / dt)),
                 lock=(int(round(30.0 / dt)), int(round(80.0 / dt))))
    if r["event"] is None:
        print("FAIL: no slip above the fold at gamma 0.5")
        sys.exit(1)
    Om = r["Omega"]
    ws = []
    for c in (r["cmin"], r["cmax"]):
        resp = chain_response(Om, c, gamma3)
        ws.append(resp[1] / resp[0])
    Ab, Ar = r["A_bond"], r["A_rotor"]
    self2 = Ar[2] / (Om * r["T"])
    fl2 = (r["wave_floor"] + self2) / Ar[1]
    ratio_r = Ar[2] / Ar[1]
    ratio_b = Ab[2] / Ab[1]
    mixing2 = 0.5 * (Ab[1] / Om) * r["slow"][2]
    fl2b = (r["wave_floor"] + Ab[2] / (Om * r["T"])) / Ab[1]
    print(f"near-band cell gamma {gamma3}: Omega {Om:.3f}, c in [{r['cmin']:.4f}, {r['cmax']:.4f}], |w| band "
          f"[{min(ws):.4e}, {max(ws):.4e}] floor {fl2:.1e}; ratio21 rotor-ref {ratio_r:.4e}, "
          f"bond-ref {ratio_b:.4e}; slow rms at 2 {r['slow'][2]:.2e}, mixing term {mixing2:.2e} "
          f"({mixing2 / Ab[2]:.1%} of A_2)")
    if not (min(ws) - fl2 <= ratio_r <= max(ws) + fl2):
        print("FAIL: offset-2 ratio under the rotor reference off the tail law")
        failed = True
    if not (min(ws) - fl2b - mixing2 / Ab[1] <= ratio_b <= max(ws) + fl2b + mixing2 / Ab[1]):
        print("FAIL: the bond-reference ratio is outside the band plus floors plus the mixing term")
        failed = True
    if MUTANT is not None:
        if failed:
            print(f"mutant {MUTANT} broke the verification as it must")
            sys.exit(1)
        print(f"mutant {MUTANT} did not break the verification")
        sys.exit(3)
    if failed:
        sys.exit(1)
    print("p48 verification ok")


if __name__ == "__main__":
    main()
