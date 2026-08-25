#!/usr/bin/env python3
"""Verification for the P-17 claim bell-ladder-priced, by independent
reimplementation - nothing read from the experiment's results:

  1. the local ceiling re-derived exhaustively (16 strategies);
  2. the quantum ceiling re-derived as the largest eigenvalue of the
     CHSH operator by direct 4x4 power iteration (2 sqrt 2 to 1e-10);
  3. the IC ladder recomputed from its closed form: bounded below 1
     at E = 1/sqrt 2 for k <= 20, broken by k = 8 at E = 0.73,
     f(1, 12) = 4096 at the PR box;
  4. fresh short simulations (seeded, 200k pairs): the rotor's CHSH
     within 5 sigma of 2; Toner-Bacon within 5 sigma of -cos at one
     angle; the detection machine's efficiency within 5 sigma of 1/2.

--mutant local-exceeds-two  asserts some deterministic local strategy
    beats S = 2 and must FAIL against the exhaustive enumeration.
--mutant ic-allows-pr       asserts information causality tolerates
    the PR box (f(1, 12) <= 1) and must FAIL: f(1, 12) = 4096.
"""
import itertools
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"local-exceeds-two", "ic-allows-pr"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


def main():
    # 1. local ceiling
    best = max(abs(a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1)
               for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4))
    if MUTANT == "local-exceeds-two":
        if best <= 2:
            print(f"FAIL: exhaustive local maximum is {best}, not above 2 - "
                  "no deterministic local strategy beats the ceiling")
            return 1
    elif best != 2:
        print(f"FAIL: exhaustive local maximum {best} != 2")
        return 1

    # 2. quantum ceiling by direct power iteration
    s2 = math.sqrt(2)
    Z = [[1, 0], [0, -1]]
    X = [[0, 1], [1, 0]]

    def kron(A, B):
        return [[A[i // 2][j // 2] * B[i % 2][j % 2] for j in range(4)] for i in range(4)]

    B0 = [[(Z[i][j] + X[i][j]) / s2 for j in range(2)] for i in range(2)]
    B1 = [[(Z[i][j] - X[i][j]) / s2 for j in range(2)] for i in range(2)]
    S = [[kron(Z, B0)[i][j] + kron(Z, B1)[i][j] + kron(X, B0)[i][j] - kron(X, B1)[i][j]
          for j in range(4)] for i in range(4)]
    rng = random.Random(7)
    v = [rng.gauss(0, 1) for _ in range(4)]
    lam = 0.0
    for _ in range(400):
        w = [sum(S[i][j] * v[j] for j in range(4)) for i in range(4)]
        w = [sum(S[i][j] * w[j] for j in range(4)) for i in range(4)]  # S^2: even powers
        lam = math.sqrt(sum(x * x for x in w))
        v = [x / lam for x in w]
    if abs(math.sqrt(lam) - 2 * s2) > 1e-10:
        print(f"FAIL: CHSH operator norm {math.sqrt(lam):.12f} != 2 sqrt 2")
        return 1

    # 3. IC ladder from its closed form
    def h(p):
        return 0.0 if p <= 0 or p >= 1 else -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def f(E, k):
        return (2 ** k) * (1 - h((1 + E ** k) / 2))

    if MUTANT == "ic-allows-pr":
        if f(1.0, 12) > 1.0:
            print(f"FAIL: f(PR box, k=12) = {f(1.0, 12):.0f} - information "
                  "causality does not tolerate the PR box")
            return 1
    else:
        if max(f(1 / s2, k) for k in range(1, 21)) >= 1.0:
            print("FAIL: IC quantity reaches 1 at Tsirelson")
            return 1
        if f(0.73, 8) <= 1.0:
            print("FAIL: IC not broken at E = 0.73, k = 8")
            return 1

    # 4. fresh short simulations
    rng = random.Random(424242)
    m = 200000

    def rotor_E(theta):
        acc = 0
        for _ in range(m):
            mu = rng.random() * 2 * math.pi
            acc += (1 if math.cos(mu) > 0 else -1) * (-1 if math.cos(mu - theta) > 0 else 1)
        return acc / m

    s_acc = 0.0
    for (x, y), th in (((0, 0), math.pi / 4), ((0, 1), math.pi / 4),
                       ((1, 0), math.pi / 4), ((1, 1), 3 * math.pi / 4)):
        s_acc += rotor_E(th) * (1 if (x, y) != (1, 1) else -1)
    sig_s = math.sqrt(4 * 0.75 / m)
    if abs(abs(s_acc) - 2.0) > 5 * sig_s:
        print(f"FAIL: fresh rotor CHSH {abs(s_acc):.4f} off 2 by > 5 sigma")
        return 1

    def sphere():
        while True:
            x, y, z = rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)
            n = math.sqrt(x * x + y * y + z * z)
            if n > 1e-9:
                return x / n, y / n, z / n

    th = 1.1
    cb, sb = math.cos(th), math.sin(th)
    acc = 0
    for _ in range(m):
        l1, l2 = sphere(), sphere()
        A = -1 if l1[0] > 0 else 1
        c = (1 if l1[0] > 0 else -1) * (1 if l2[0] > 0 else -1)
        B = 1 if cb * (l1[0] + c * l2[0]) + sb * (l1[1] + c * l2[1]) > 0 else -1
        acc += A * B
    q = -math.cos(th)
    if abs(acc / m - q) > 5 * math.sqrt((1 - q * q) / m):
        print(f"FAIL: fresh Toner-Bacon E {acc/m:.4f} off -cos({th}) by > 5 sigma")
        return 1
    ndet = 0
    for _ in range(m):
        l = sphere()
        if rng.random() < abs(cb * l[0] + sb * l[1]):
            ndet += 1
    if abs(ndet / m - 0.5) > 5 * math.sqrt(0.25 / m):
        print(f"FAIL: fresh detection efficiency {ndet/m:.4f} off 1/2 by > 5 sigma")
        return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: ceiling 2 exhaustive; operator norm 2 sqrt 2 to 1e-10; IC bounded "
          f"at Tsirelson and broken above; fresh rotor S = {abs(s_acc):.4f}, "
          f"Toner-Bacon on the cosine, detection at eta = {ndet/m:.4f} - every "
          "rung re-derived, every price re-paid")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
