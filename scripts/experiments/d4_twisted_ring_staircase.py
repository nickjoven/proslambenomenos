#!/usr/bin/env python3
"""D4 probe E1: does the half-turn twist reshape TEMPORAL locking?

System: N coupled, externally pinned circle maps on a ring (phases in
turns, mod 1):

    theta_i' = theta_i + Omega - (K/2pi) sin(2pi theta_i)
               + (J/2pi)[ sin(2pi(theta_{i+1} - theta_i + s_i))
                        + sin(2pi(theta_{i-1} - theta_i - s_{i-1})) ]

with seam offsets s_i = 0 except s_N = 1/2 across the seam in the
TWISTED ring (0 everywhere in the control). The pinning term supplies
the drive that makes temporal mode-locking possible; the coupling
carries the twist. Measured: collective rotation number
rho = mean phase advance per step, swept over Omega; plateaus =
temporal lockings. Question: which rational plateaus survive, shift,
or split under the twist, versus the untwisted control?

Exploration script (not a verify): output is data for D4's
discriminating comparison, interpretation happens in the notes.
"""

import math
import sys

TWO_PI = 2 * math.pi


def rho(N, Omega, K, J, twisted, iters=4000, trans=1000):
    th = [0.13 * i for i in range(N)]
    total = 0.0
    for t in range(iters + trans):
        adv = []
        for i in range(N):
            up = (i + 1) % N
            dn = (i - 1) % N
            s_up = 0.5 if (twisted and i == N - 1) else 0.0
            s_dn = 0.5 if (twisted and dn == N - 1) else 0.0
            c = (J / TWO_PI) * (
                math.sin(TWO_PI * (th[up] - th[i] + s_up)) +
                math.sin(TWO_PI * (th[dn] - th[i] - s_dn)))
            a = Omega - (K / TWO_PI) * math.sin(TWO_PI * th[i]) + c
            adv.append(a)
        for i in range(N):
            th[i] += adv[i]
        if t >= trans:
            total += sum(adv) / N
    return total / iters


def plateaus(N, K, J, twisted, n_omega=600, tol=5e-4):
    hits = {}
    for k in range(n_omega + 1):
        Om = k / n_omega
        r = rho(N, Om, K, J, twisted)
        # snap to rationals with small denominator
        for q in range(1, 9):
            p = round(r * q)
            if abs(r - p / q) < tol and math.gcd(p, q) == 1 and 0 <= p <= q:
                key = (p, q)
                hits[key] = hits.get(key, 0) + 1
                break
    return hits


def main():
    N, K, J = int(sys.argv[1]) if len(sys.argv) > 1 else 3, 1.0, 0.6
    for twisted in (False, True):
        h = plateaus(N, K, J, twisted)
        label = "twisted " if twisted else "control "
        rows = sorted(h.items(), key=lambda kv: (kv[0][1], kv[0][0]))
        wide = [(f"{p}/{q}", n) for (p, q), n in rows if n >= 4]
        print(f"{label} N={N}: plateaus (>=4 grid pts): "
              + "  ".join(f"{f}:{n}" for f, n in wide))


if __name__ == "__main__":
    main()
