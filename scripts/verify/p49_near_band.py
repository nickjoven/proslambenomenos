#!/usr/bin/env python3
"""Verification for the P-49 claim late-window-tail-law, by
independent reimplementation on own small rings. Nothing imported
from the experiment scripts, nothing read from results files.

Checks: (1) the smear identity: on an own N = 48 twisted ring at
gamma = 0.5 (the k = 1 mode is overdamped there, omega_1 = 0.131 <
gamma/2, decaying at 0.034 per unit, and alive in an early window;
at N = 32 the smear was 0.9 percent inside a 1.1 percent tolerance
and the smear-blind mutant did not bite - recorded), the rotor-phase lock-in of
the neighbour's velocity equals the bond-phase lock-in times the
characteristic function |<e^{-i x_1}>| of the neighbour's own
displacement about its window mean, within a tolerance of the slow
part's rms times the reference's own mean resultant |<e^{-i theta_b}>|
plus twice the 2-Omega self floor, capped at 5 percent of the
fundamental (LAW-60: LAW-59's tolerance used the slow part's own
rotor phasor and a DC offset inflated it; LAW-56's used the whole
remainder and passed on any series); (2) the late-window tail law in band: on
an own N = 16 ring at gamma = 1 (rotor at Omega ~ 1.7, band top 2),
in a window starting 300 units after the slip, the drive-locked
A_2/A_1 lies in the band of a direct complex tridiagonal solve at
the window's stiffness range - the lower end reduced by the
describing-function factor 2 J_1(delta)/delta of the drive-frequency
strain amplitude delta - widened by the self floors; (3) the same
above the band on the N = 16 ring at gamma = 0.5.

--mutant smear-blind  asserts no smear (rotor reading = bond
    reading); check (1) kills it.
--mutant band-blind   asserts the in-band tail ratio is 1/Omega
    instead of the propagating root; check (2) kills it.
"""
import cmath
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"smear-blind", "band-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

DT = 0.001


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


def j1_ratio(x):
    s, term, k = 1.0, 1.0, 0
    x2 = (x / 2.0) ** 2
    while k < 30:
        k += 1
        term *= -x2 / (k * (k + 1))
        s += term
    return s


def chain_response(Omega, c, gamma, M=24):
    """Driven damped chain, unit force on site 0, site M-1 clamped;
    velocity amplitudes at sites 0, 1, 2 (M long enough that the
    clamped end is invisible even for a propagating tail with
    damping: |w|^M < 1e-6 for the cells used)."""
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
    return [abs(Omega * x[k]) for k in range(3)], x[1] / x[0]


def run(n, gamma, f, win, t_ramp=50.0, cap=1500.0):
    """Own Euler-Cromer twisted sector-0 ring, dead-loaded at n/2;
    records theta and v at b, b+1, b+2 at every step over the window
    [event + win0, event + win1); stiffness range over the ring."""
    b = n // 2
    A = [math.pi if j == 0 else 0.0 for j in range(n)]
    th = [0.0] * n
    for j in range(1, n):
        th[j] = th[j - 1] + math.pi / n + A[j - 1]
    v = [0.0] * n
    D0 = [th[(j + 1) % n] - th[j] - A[j] for j in range(n)]
    sD = [math.sin(x) for x in D0]
    per_unit = int(round(1.0 / DT))
    n_ramp = int(round(t_ramp / DT))
    n_total = int(round(cap / DT))
    event = None
    TH, V = [], []
    cmin, cmax = 1.0, -1.0
    s = 0
    while s < n_total:
        fn = f * min(1.0, (s + 1) / n_ramp)
        for j in range(n):
            v[j] += DT * (sD[j] - sD[j - 1] - gamma * v[j] + (fn if j == b else 0.0))
        for j in range(n):
            th[j] += DT * v[j]
        sD = [math.sin(th[(j + 1) % n] - th[j] - A[j]) for j in range(n)]
        s += 1
        if event is None:
            if s % per_unit == 0:
                D = [th[(j + 1) % n] - th[j] - A[j] for j in range(n)]
                if max(abs(D[j] - D0[j]) for j in range(n)) > 1.5 * math.pi:
                    event = s
                    n_total = s + int(round(win[1] / DT)) + 1
            continue
        Delta = (s - event) * DT
        if win[0] <= Delta < win[1]:
            TH.append((th[b], th[(b + 1) % n], th[(b + 2) % n]))
            V.append((v[b], v[(b + 1) % n], v[(b + 2) % n]))
            if s % per_unit == 0:
                for j in range(n):
                    if j not in (b, b - 1):
                        c = math.cos(th[(j + 1) % n] - th[j] - A[j])
                        cmin, cmax = min(cmin, c), max(cmax, c)
    return event, TH, V, cmin, cmax


def fundamental(series, ref):
    c = [math.cos(r) for r in ref]
    s_ = [math.sin(r) for r in ref]
    cc = sum(x * x for x in c)
    ss = sum(x * x for x in s_)
    cs = sum(x * y for x, y in zip(c, s_))
    yc = sum(x * y for x, y in zip(series, c))
    ys = sum(x * y for x, y in zip(series, s_))
    det = cc * ss - cs * cs
    a = (yc * ss - ys * cs) / det
    bb = (ys * cc - yc * cs) / det
    return math.hypot(a, bb), [a * x + bb * y for x, y in zip(c, s_)]


def lockin_phasor(series, ref):
    return sum(x * cmath.exp(-1j * r) for x, r in zip(series, ref)) / len(series)


def main():
    failed = False
    # (1) the smear identity, N = 32, gamma 0.5, early window
    n = 48
    f = own_fold(n, -math.pi) + 0.02
    ev, TH, V, cmin, cmax = run(n, 0.5, f, (10.0, 50.0))
    if ev is None:
        print("FAIL: no slip")
        sys.exit(1)
    ref_b = [t[0] - t[1] for t in TH]
    ref_r = [t[0] for t in TH]
    v1 = [x[1] for x in V]
    A1b, fund1 = fundamental(v1, ref_b)
    Om = (ref_r[-1] - ref_r[0]) / ((len(ref_r) - 1) * DT)
    T = len(v1) * DT
    x1 = [t[1] for t in TH]
    m = sum(x1) / len(x1)
    smear_pred = 1.0 if MUTANT == "smear-blind" else abs(sum(cmath.exp(-1j * (x - m)) for x in x1)) / len(x1)
    z_tot = lockin_phasor(v1, ref_r)
    z_fund = lockin_phasor(fund1, ref_r)
    # LAW-59 (A-32): the tolerance names its terms instead of taking the
    # reading's own remainder (which absorbed any series, R-48a). The slow
    # part of v_1 (running mean over one rotor period of the non-fundamental
    # remainder) leaks through the rotor reference by its own phasor; the
    # harmonic rest is bounded by the 2-Omega self floor 1/(Omega T).
    per = max(1, int(round(2 * math.pi / Om / DT)))
    rem = [a - b for a, b in zip(v1, fund1)]
    half = per // 2
    slow1 = [sum(rem[max(0, k - half):min(len(rem), k + half + 1)]) / (min(len(rem), k + half + 1) - max(0, k - half))
             for k in range(len(rem))]
    # LAW-60: the slow part's leak is bounded by a quantity of the
    # REFERENCE alone - the window's mean resultant of the rotor phase,
    # |<e^{-i theta_b}>|, times the slow part's rms - never by the slow
    # part's own rotor phasor (LAW-59's tolerance was still the series'
    # own and a DC offset inflated it). And the bound is capped: if the
    # slow leak allowed exceeds 5 percent of the fundamental the cell
    # cannot test the identity and the check fails as untestable.
    slow_rms = math.sqrt(sum(x * x for x in slow1) / len(slow1))
    ref_resultant = abs(sum(cmath.exp(-1j * r) for r in ref_r)) / len(ref_r)
    slow_bound = 2.0 * slow_rms * ref_resultant / A1b
    meas = 2.0 * abs(z_tot) / A1b
    tol = slow_bound + 2.0 / (Om * T)
    if slow_bound > 0.05:
        print(f"FAIL: the slow part's allowed leak ({slow_bound:.4f} of the fundamental) is too large to test the smear identity")
        failed = True
    print(f"smear identity (N = {n}, gamma 0.5, window [10, 50), Omega {Om:.3f}): x_1 rms "
          f"{math.sqrt(sum((x - m) ** 2 for x in x1) / len(x1)):.3f}; rotor/bond {meas:.4f} vs |<e^-ix1>| "
          f"{smear_pred:.4f}, tolerance {tol:.4f}")
    if abs(meas - smear_pred) > tol:
        print("FAIL: the rotor-reference reading is not the smeared drive-locked fundamental")
        failed = True
    # (2), (3): the late-window tail law on N = 16, in band and above
    for gamma, label in ((1.0, "in band"), (0.5, "above the band")):
        n = 16
        f = own_fold(n, -math.pi) + 0.02
        ev, TH, V, cmin, cmax = run(n, gamma, f, (300.0, 360.0))
        if ev is None:
            print(f"FAIL: no slip at gamma {gamma}")
            sys.exit(1)
        ref_b = [t[0] - t[1] for t in TH]
        Om = (TH[-1][0] - TH[0][0]) / ((len(TH) - 1) * DT)
        T = len(TH) * DT
        A1, _ = fundamental([x[1] for x in V], ref_b)
        A2, _ = fundamental([x[2] for x in V], ref_b)
        _, w_mid = chain_response(Om, 0.5 * (cmin + cmax), gamma)
        delta = A1 * abs(1.0 - w_mid) / Om
        df = j1_ratio(delta)
        ws = []
        for c in (cmin * df, cmax):
            resp, w = chain_response(Om, c, gamma)
            ws.append(1.0 / Om if MUTANT == "band-blind" else resp[1] / resp[0])
        ratio = A2 / A1
        fl = (A2 / (Om * T) + ratio * A1 / (Om * T)) / A1
        print(f"late window {label} (N = {n}, gamma {gamma}, Omega {Om:.3f}, delta {delta:.3f}, c in [{cmin:.4f}, {cmax:.4f}]): "
              f"A2/A1 {ratio:.4e} vs band [{min(ws):.4e}, {max(ws):.4e}] floor {fl:.1e}")
        if not (min(ws) - fl <= ratio <= max(ws) + fl):
            print(f"FAIL: late-window tail ratio off the root band {label}")
            failed = True
    if MUTANT is not None:
        if failed:
            print(f"mutant {MUTANT} broke the verification as it must")
            sys.exit(1)
        print(f"mutant {MUTANT} did not break the verification")
        sys.exit(3)
    if failed:
        sys.exit(1)
    print("p49 verification ok")


if __name__ == "__main__":
    main()
