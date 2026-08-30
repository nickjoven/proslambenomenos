#!/usr/bin/env python3
"""Verification for the P-37 claim writing-a-bit-pays-its-floors,
by independent live reimplementation: its own Langevin integrator
(rejection-sampled equilibrium start, its own update ordering and
RNG usage), its own entropy/floor arithmetic, its own circle-W2
with a fixed barrier cut (an overestimate of W2, so the speed-limit
check it feeds is STRICTER than the registered one). Nothing read
from results files.

Checks: (1) closed forms - the critical tilt (V''(pi, h) = 2 - h
vanishes at h = 2), floor symmetry floor(p) = floor(1-p), and
floor(1/2) = 0; (2) the Jarzynski null on a gentle closed loop:
|<e^{-W/D}> - 1| <= 4 SE; (3) both floors on a working cell
(D = 0.28, a = 2.4, tau = 4): mean work above D[ln2 - H(p)] and
above D[ln2 - H(p)] + W2^2/tau, each minus 4 SE.

--mutant half-work     drops the work booked during the down-ramp
    (a plausible bookkeeping error); the Jarzynski identity
    kills it.
--mutant entropy-blind asserts the floor without the H(p) refund
    (W >= D ln 2 always); the cheap noisy write kills it.
"""
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"half-work", "entropy-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

TAU = 2.0 * math.pi
EPS = 1.0


def V(th, h):
    return -(EPS / 2) * math.cos(2 * th) - h * math.cos(th)


def dV(th, h):
    return EPS * math.sin(2 * th) + h * math.sin(th)


def Hent(p):
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1 - p) * math.log(1 - p)


def floor_W(D, p):
    return D * (math.log(2) - Hent(p))


def sample_eq(D, M, rng):
    """Rejection sampling from e^{-V(.,0)/D} on [-pi, pi)."""
    peak = math.exp(EPS / (2 * D))
    out = []
    while len(out) < M:
        x = rng.uniform(-math.pi, math.pi)
        if rng.random() * peak <= math.exp(-V(x, 0.0) / D):
            out.append(x)
    return out


def cell(D, a, tau, M, dt, seed):
    rng = random.Random(seed)
    ths = sample_eq(D, M, rng)
    Ws = [0.0] * M
    steps = int(round(tau / dt))
    sq = math.sqrt(2 * D * dt)
    h = 0.0
    for s in range(steps):
        t = (s + 1) * dt
        hn = a * (1.0 - abs(2.0 * t / tau - 1.0))
        dh = hn - h
        if MUTANT == "half-work" and t > tau / 2:
            dh_book = 0.0
        else:
            dh_book = dh
        for i in range(M):
            Ws[i] -= math.cos(ths[i]) * dh_book
            ths[i] += -dV(ths[i], hn) * dt + sq * rng.gauss(0.0, 1.0)
        h = hn
    wrong = sum(1 for th in ths
                if abs(((th + math.pi) % TAU) - math.pi) >= math.pi / 2)
    p = wrong / M
    mW = sum(Ws) / M
    seW = math.sqrt(sum((w - mW) ** 2 for w in Ws) / (M * (M - 1)))
    ej = [math.exp(-w / D) for w in Ws]
    mj = sum(ej) / M
    sej = math.sqrt(sum((e - mj) ** 2 for e in ej) / (M * (M - 1)))
    finals = [((th + math.pi) % TAU) - math.pi for th in ths]
    return mW, seW, p, mj, sej, finals


def w2_cut(D, finals, m=64):
    """W2 with the cut fixed at the barrier -pi/2: quantiles on the
    unrolled interval [-pi/2, 3pi/2). Any fixed cut >= true W2."""
    def unroll(x):
        return x + TAU if x < -math.pi / 2 else x
    n = 3000
    xs = [-math.pi / 2 + (i + 0.5) * TAU / n for i in range(n)]
    w = [math.exp(-V(x, 0.0) / D) for x in xs]
    Z = sum(w)
    cum, c = [], 0.0
    for v in w:
        c += v / Z
        cum.append(c)
    qa = []
    j = 0
    for i in range(m):
        t = (i + 0.5) / m
        while cum[j] < t:
            j += 1
        qa.append(xs[j])
    fs = sorted(unroll(x) for x in finals)
    M = len(fs)
    qb = [fs[min(int((i + 0.5) / m * M), M - 1)] for i in range(m)]
    return sum((x - y) ** 2 for x, y in zip(qa, qb)) / m


def main():
    failures = []

    # (1) closed forms
    vpp = lambda th, h: 2 * EPS * math.cos(2 * th) + h * math.cos(th)
    hc = 2.0 * EPS
    print(f"V''(pi, h_c) = {vpp(math.pi, hc):.2e}; "
          f"floor(1/2) = {floor_W(0.28, 0.5):.2e}; "
          f"symmetry gap = {abs(floor_W(0.28, 0.1) - floor_W(0.28, 0.9)):.2e}")
    if abs(vpp(math.pi, hc)) > 1e-12:
        print("FAIL: critical tilt is not 2 eps")
        failures.append("hc")
    if abs(floor_W(0.28, 0.5)) > 1e-12 or \
            abs(floor_W(0.28, 0.1) - floor_W(0.28, 0.9)) > 1e-12:
        print("FAIL: floor arithmetic broken")
        failures.append("floor-form")

    # (2) the Jarzynski null
    _, _, _, mj, sej, _ = cell(0.28, 0.5, 6.0, 800, 0.004, 91)
    print(f"jarzynski {mj:.4f} +- {sej:.4f}")
    if abs(mj - 1.0) > 4 * sej:
        print(f"FAIL: closed-loop Jarzynski off unity by "
              f"{abs(mj - 1) / sej:.1f} SE")
        failures.append("jarzynski")

    # (3) both floors on a working cell
    mW, seW, p, _, _, finals = cell(0.28, 2.4, 4.0, 800, 0.004, 92)
    if MUTANT == "entropy-blind":
        # the mutant books the floor without the H(p) refund and
        # applies it to the cheap noisy write
        mW2, seW2, p2, _, _, _ = cell(0.28, 1.2, 1.0, 800, 0.004, 93)
        fl = 0.28 * math.log(2)
        print(f"cheap cell W {mW2:.4f}, asserted floor {fl:.4f}")
        if mW2 < fl - 4 * seW2:
            print("FAIL: the H(p) refund is load-bearing - the "
                  "blind floor exceeds the measured work")
            failures.append("entropy")
    fl = floor_W(0.28, p)
    w2 = w2_cut(0.28, finals)
    both = fl + w2 / 4.0
    print(f"cell W {mW:.4f}(+-{seW:.4f}) p {p:.4f} "
          f"floor {fl:.4f} floor+sl {both:.4f}")
    if mW < fl - 4 * seW:
        print("FAIL: Landauer-with-errors floor violated")
        failures.append("floor")
    if mW < both - 4 * seW:
        print("FAIL: floor plus speed limit violated")
        failures.append("speed-limit")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p37 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
