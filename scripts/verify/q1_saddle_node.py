#!/usr/bin/env python3
"""Q1 verification: saddle-node passage time T(mu) = pi/sqrt(mu).

Integrates dx/dt = mu + x^2 from -X to +X with RK4 and compares the
passage time to pi/sqrt(mu). The finite cutoff contributes
2*arctan(X/sqrt(mu))/sqrt(mu) - pi/sqrt(mu) -> 0 as X/sqrt(mu) -> inf,
so with X = 100 and mu <= 1e-2 the truncation error is < 0.2%.

Exit 0 iff every case matches within 0.5%.
"""

import math
import sys


def passage_time(mu, X=100.0, dt_scale=1e-3):
    x, t = -X, 0.0
    dt = dt_scale * math.sqrt(mu)  # resolve the bottleneck
    f = lambda x: mu + x * x
    while x < X:
        k1 = f(x)
        k2 = f(x + 0.5 * dt * k1)
        k3 = f(x + 0.5 * dt * k2)
        k4 = f(x + dt * k3)
        x += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += dt
    return t


MUTANT = sys.argv[sys.argv.index("--mutant") + 1] if "--mutant" in sys.argv and sys.argv.index("--mutant") + 1 < len(sys.argv) else ("--mutant" in sys.argv or None)
KNOWN_MUTANTS = {"wrong-exponent"}
if MUTANT is not None and MUTANT not in KNOWN_MUTANTS:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN_MUTANTS)}")
    sys.exit(2)


def main() -> int:
    ok = True
    # LAW-11 mutant 'wrong-exponent': claim T = pi / mu^(1/3) instead;
    # the RK4 integration is independent of the claim and must reject it.
    expo = 1.0 / 3.0 if MUTANT == "wrong-exponent" else 0.5
    for mu in (1e-2, 1e-3, 1e-4):
        T = passage_time(mu)
        pred = math.pi / mu ** expo
        rel = abs(T - pred) / pred
        line = f"mu={mu:g}: T={T:.4f}  pi/sqrt(mu)={pred:.4f}  rel err={rel:.2e}"
        print(line + ("  ok" if rel < 5e-3 else "  FAIL"))
        ok &= rel < 5e-3
    # scaling exponent from the two extreme cases
    T1, T2 = passage_time(1e-2), passage_time(1e-4)
    slope = math.log(T2 / T1) / math.log(1e-4 / 1e-2)
    print(f"scaling exponent d ln T / d ln mu = {slope:.4f} (theory: -0.5)")
    ok &= abs(slope + expo) < 0.01
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
