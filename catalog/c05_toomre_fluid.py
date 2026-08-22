"""The WKB dispersion relation of a fluid disk admits growing modes iff sigma*kappa/(pi G Sigma) < 1 (Toomre's criterion, fluid form).
Source: Toomre, ApJ 139, 1217 (1964); Binney & Tremaine eq. 6.55. Mutant: threshold 2 instead of 1."""
import sys
from _common import mutant_flag, finish

G, Sigma, kappa = 1.0, 1.0, 1.0
threshold = 2.0 if mutant_flag() else 1.0


def unstable(sigma):
    # min over k of kappa^2 - 2 pi G Sigma k + k^2 sigma^2 is at k = pi G Sigma / sigma^2
    import math
    ks = [0.001 * j for j in range(1, 20000)]
    return min(kappa ** 2 - 2 * math.pi * G * Sigma * k + k * k * sigma * sigma for k in ks) < 0


import math
Qs = [0.5, 0.9, 0.99, 1.01, 1.1, 1.5]
results = {Q: unstable(Q * math.pi * G * Sigma / kappa) for Q in Qs}
ok = all(results[Q] == (Q < threshold) for Q in Qs)
sys.exit(finish(ok, f"unstable at Q = {[Q for Q in Qs if results[Q]]} (claimed: Q < {threshold:.0f})"))
