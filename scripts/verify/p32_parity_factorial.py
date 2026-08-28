#!/usr/bin/env python3
"""Verification for the P-32/P-33 claim frustration-classes-
organize-the-pinned-ring, by independent live reimplementation:
its own ring integrator (vectorized over a phase list with its own
update ordering), its own plateau-edge search, and its own check
of the telescoping identity. Nothing read from results files.

Checks: (1) the telescoping identity rho = I on the bias family at
1e-14 (three geometries, two drives) - the R-30 finding
reproduced; (2) the K = 1.2 ALT class hierarchy on the spot set
N in {4, 6, 7, 8}: w(4) and w(8) within 3e-3 of each other, and
w(4) - w(6) > 0.05, w(6) - w(7) > 0.005 (clean > half > both);
(3) the seam+pinning N = 4 width lands within 5e-3 of the P-9 pin
0.02225.

--mutant telescope-blind  asserts a bias cell locks (width above
    twice the smear); the identity kills it.
--mutant class-blind      asserts w(6) within 3e-3 of w(4) at
    K = 1.2; the 0.13 class gap kills it.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"telescope-blind", "class-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

TWO_PI = 2 * math.pi
TOL = 4e-4


def offsets(geom, N):
    if geom == "control":
        return [0.0] * N
    if geom == "seam":
        return [0.0] * (N - 1) + [0.5]
    return [0.5 if b % 2 == 1 else 0.0 for b in range(N)]


def run_rho(N, geom, K, J, I, A, nu, th, iters=3200, trans=900):
    s = offsets(geom, N)
    th = list(th)
    tot = 0.0
    for t in range(iters + trans):
        drv = (A / TWO_PI) * math.sin(TWO_PI * nu * t) if A else 0.0
        new = []
        step_sum = 0.0
        for i in range(N):
            c = (J / TWO_PI) * (
                math.sin(TWO_PI * (th[(i + 1) % N] - th[i] + s[i]))
                + math.sin(TWO_PI * (th[(i - 1) % N] - th[i]
                                     - s[(i - 1) % N])))
            pin = (K / TWO_PI) * math.sin(TWO_PI * th[i]) if K else 0.0
            a = I + drv - pin + c
            new.append(th[i] + a)
            step_sum += a
        th = new
        if t >= trans:
            tot += step_sum / N
    return tot / iters


def width_pin(N, geom, K, lo=0.30, hi=0.85, n=160):
    if geom == "seam":
        th0 = [i / (2 * N) for i in range(N)]
    elif geom == "alt":
        # damped relaxation for the ALT ground state
        s = offsets("alt", N)
        th = [0.001 * i * (N - i) for i in range(N)]
        for _ in range(6000):
            for i in range(N):
                g = (math.sin(TWO_PI * (th[(i + 1) % N] - th[i]
                                        + s[i]))
                     + math.sin(TWO_PI * (th[(i - 1) % N] - th[i]
                                          - s[(i - 1) % N])))
                th[i] += 0.25 * g / TWO_PI
        th0 = th
    else:
        th0 = [0.0] * N

    def r(Om):
        return run_rho(N, geom, K, 0.6, Om, 0.0, 0.0, th0)
    xs = [lo + (hi - lo) * k / n for k in range(n + 1)]
    inside = [x for x in xs if abs(r(x) - 0.5) < TOL]
    if not inside:
        return 0.0
    a, b = inside[0], inside[-1]
    step = (hi - lo) / n

    def bis(out, inn):
        for _ in range(30):
            m = 0.5 * (out + inn)
            if abs(r(m) - 0.5) < TOL:
                inn = m
            else:
                out = m
        return inn
    return bis(b + step, b) - bis(a - step, a)


def main():
    failures = []

    # (1) telescoping identity
    worst = 0.0
    for geom in ("control", "seam", "alt"):
        for I, A in ((0.031, 0.9), (0.0625, 1.3)):
            th0 = [0.01 * i for i in range(6)]
            r = run_rho(6, geom, 0.0, 0.6, I, A, 0.125, th0)
            worst = max(worst, abs(r - I))
    print(f"telescoping identity: worst |rho - I| = {worst:.2e}")
    if MUTANT == "telescope-blind":
        # assert some bias cell locks: width of the nu/2 window
        # beyond twice the smear (smear = 2 TOL / 1)
        lo, hi, n = 0.0625 - 0.06, 0.0625 + 0.06, 120
        th0 = [0.01 * i for i in range(6)]
        inside = [lo + (hi - lo) * k / n for k in range(n + 1)
                  if abs(run_rho(6, "alt", 0.0, 0.6,
                                 lo + (hi - lo) * k / n, 0.9, 0.125,
                                 th0) - 0.0625) < TOL]
        w = (inside[-1] - inside[0]) if inside else 0.0
        if w <= 2 * (2 * TOL):
            print(f"FAIL: asserted bias locking but width {w:.5f} "
                  f"is within the smear")
            failures.append("telescope")
    elif worst > 1e-14:
        print("FAIL: telescoping identity violated")
        failures.append("identity")

    # (2) the K = 1.2 class hierarchy on the spot set
    w = {N: width_pin(N, "alt", 1.2) for N in (4, 6, 7, 8)}
    print(f"K=1.2 ALT widths: {[f'{N}:{w[N]:.5f}' for N in w]}")
    if MUTANT == "class-blind":
        if abs(w[6] - w[4]) > 3e-3:
            print(f"FAIL: asserted w(6) ~ w(4) but they differ by "
                  f"{abs(w[6] - w[4]):.4f}")
            failures.append("class")
    else:
        if abs(w[4] - w[8]) > 3e-3:
            print("FAIL: clean pair {4, 8} not within 3e-3")
            failures.append("clean-pair")
        if not (w[4] - w[6] > 0.05):
            print("FAIL: clean - half gap below 0.05")
            failures.append("gap-ch")
        if not (w[6] - w[7] > 0.005):
            print("FAIL: half - both gap below 0.005")
            failures.append("gap-hb")

    # (3) the P-9 pin
    w4 = width_pin(4, "seam", 1.0)
    print(f"seam+pinning N=4: {w4:.5f} (pin 0.02225)")
    if abs(w4 - 0.022249756399542298) > 5e-3:
        print("FAIL: P-9 N=4 reproduction off")
        failures.append("p9")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p32/p33 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
