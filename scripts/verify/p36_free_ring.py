#!/usr/bin/env python3
"""Verification for the P-36 claim holonomy-selects-the-slip-channel,
by independent live reimplementation: its own quasi-static fold
solver (fresh bisection structure), its own velocity-Verlet ring
integrator (different scheme and update ordering from the
experiment's Euler-Cromer), its own winding and event detection.
Nothing read from results files.

Checks: (1) the control fold from the own solver lands on the
closed form 2N/(N-1) at N = 64 within 1e-4; (2) the own-solver
twisted/control fold ratio lands within 2e-4 of the claimed
0.966290; (3) channel: at fold + 0.02 the control's first event
leaves the winding unchanged (paired) while the twisted ring's
first event moves it by exactly +-1 (single), with the twisted
winding on the half-integer lattice at 1e-9 beforehand; (4)
threshold separation: at f = 1.970 (between the two folds) the
twisted ring slips and the control does not.

--mutant channel-blind  asserts every first event changes the
    winding; the control's paired slip kills it.
--mutant naive-budget   asserts the fold ratio is the shortcut
    1 - sin(pi/N) = 0.950932 (the derivation error corrected
    before registration); the exact solver kills it.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"channel-blind", "naive-budget"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

TAU = 2.0 * math.pi
N = 64


def own_fold(total):
    """Largest f admitting sin(s_j) = c + m f/N, sum s_j = total."""
    def gap(f):
        # returns signed distance of the constraint at the best c,
        # or None if no c keeps all values inside (-1, 1)
        lo, hi = -1.0 + 1e-9, 1.0 - (N - 1) * f / N - 1e-9
        if hi <= lo:
            return None

        def total_of(c):
            return sum(math.asin(c + m * f / N) for m in range(N))

        tlo, thi = total_of(lo), total_of(hi)
        if (tlo - total) * (thi - total) > 0:
            return None
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            if (total_of(mid) - total) * (tlo - total) <= 0:
                hi = mid
            else:
                lo, tlo = mid, total_of(mid)
        return 0.5 * (lo + hi)

    f_lo, f_hi = 0.5, 3.5
    for _ in range(55):
        f_mid = 0.5 * (f_lo + f_hi)
        if gap(f_mid) is not None:
            f_lo = f_mid
        else:
            f_hi = f_mid
    return f_lo


def ring_run(twisted, f_target, t_total=700.0, t_ramp=200.0, dt=0.04):
    """Velocity-Verlet, returns (event, dW_first, worst_half_off)."""
    A = [math.pi if (twisted and j == 0) else 0.0 for j in range(N)]
    delta = (math.pi / N) if twisted else 0.0
    th = [0.0] * N
    for j in range(1, N):
        th[j] = th[j - 1] + delta + A[j - 1]
    s0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    v = [0.0] * N
    b, gamma = N // 2, 0.02

    def forces(t):
        f = f_target * min(1.0, t / t_ramp)
        out = []
        for j in range(N):
            r = math.sin(th[(j + 1) % N] - th[j] - A[j])
            l = math.sin(th[j] - th[j - 1] - A[j - 1])
            out.append(r - l - gamma * v[j] + (f if j == b else 0.0))
        return out

    def wind():
        tot = 0.0
        for j in range(N):
            d = th[(j + 1) % N] - th[j] - A[j]
            tot += (d + math.pi) % TAU - math.pi
        return tot / TAU

    W0 = round(wind() * 2.0) / 2.0
    acc = forces(0.0)
    event = False
    dW_first = None
    worst = 0.0
    steps = int(t_total / dt)
    for s in range(steps):
        t = s * dt
        for j in range(N):
            th[j] += v[j] * dt + 0.5 * acc[j] * dt * dt
        nxt = forces(t + dt)
        for j in range(N):
            v[j] += 0.5 * (acc[j] + nxt[j]) * dt
        acc = nxt
        if s % 25 == 0:
            if not event:
                emax = max(abs(th[(j + 1) % N] - th[j] - A[j] - s0[j])
                           for j in range(N))
                if emax > 1.5 * math.pi:
                    event = True
                elif emax < 0.9 * math.pi:
                    # settled sample: the winding sits on the
                    # half-integer (twisted) / integer lattice;
                    # a bond in transit is part of an event, not
                    # a between-events sample
                    W = wind()
                    off = (abs(W - (round(W - 0.5) + 0.5)) if twisted
                           else abs(W - round(W)))
                    worst = max(worst, off)
            if event and dW_first is None:
                dW = wind() - W0
                if abs(dW) > 0.6:
                    dW_first = round(dW)
    return event, dW_first, worst


def main():
    failures = []

    # (1) control fold vs closed form
    fc = own_fold(0.0)
    closed = 2.0 * N / (N - 1)
    print(f"control fold {fc:.6f} vs closed form {closed:.6f}")
    if abs(fc - closed) > 1e-4:
        print("FAIL: control fold does not land on 2N/(N-1)")
        failures.append("closed-form")

    # (2) the fold ratio
    ft = own_fold(math.pi)
    ratio = ft / fc
    target = 0.950932 if MUTANT == "naive-budget" else 0.966290
    print(f"twisted fold {ft:.6f}, ratio {ratio:.6f} vs {target:.6f}")
    if abs(ratio - target) > 2e-4:
        print(f"FAIL: fold ratio {ratio:.6f} is not {target:.6f}")
        failures.append("ratio")

    # (3) the channel, both configurations at fold + 0.02
    ev_c, dw_c, _ = ring_run(False, fc + 0.02)
    ev_t, dw_t, half_off = ring_run(True, ft + 0.02)
    print(f"control event {ev_c} dW_first {dw_c}; "
          f"twisted event {ev_t} dW_first {dw_t} "
          f"(pre-event half-lattice off {half_off:.1e})")
    if not (ev_c and ev_t):
        print("FAIL: no event just above the fold")
        failures.append("no-event")
    if MUTANT == "channel-blind":
        if dw_c is None:
            print("FAIL: asserted every first event changes the winding; "
                  "the control's paired slip left it unchanged")
            failures.append("channel")
    else:
        if dw_c is not None:
            print("FAIL: control first event changed the winding")
            failures.append("channel-c")
        if dw_t not in (1, -1):
            print("FAIL: twisted first event is not a single +-1 slip")
            failures.append("channel-t")
        if half_off > 1e-9:
            print("FAIL: twisted winding off the half-integer lattice")
            failures.append("lattice")

    # (4) threshold separation at f between the folds
    ev_t2, _, _ = ring_run(True, 1.970)
    ev_c2, _, _ = ring_run(False, 1.970)
    print(f"at f = 1.970: twisted event {ev_t2}, control event {ev_c2}")
    if not ev_t2 or ev_c2:
        print("FAIL: threshold separation between the folds not seen")
        failures.append("separation")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p36 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
