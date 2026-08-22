"""Carson's rule: a sinusoidally modulated FM signal carries >= 98% of its power within bandwidth 2 (Delta f + f_m); the sideband amplitudes are Bessel J_n(beta).
Source: Carson 1922; Bessel expansion cos(w_c t + beta sin w_m t) = sum J_n(beta) cos((w_c + n w_m) t). Checked for beta in {1, 2, 5} with J_n from the series. Mutant: bandwidth 2 f_m only."""
import math, sys
from _common import mutant_flag, finish

def J(n, x, terms=40):
    return sum((-1) ** k / (math.factorial(k) * math.factorial(k + n)) * (x / 2) ** (2 * k + n) for k in range(terms))
ok = True; out = []
for beta in (1.0, 2.0, 5.0):
    # power fraction within |n| <= N_c where N_c = floor(beta + 1) (Carson) or 1 (mutant: 2 f_m)
    Nc = 1 if mutant_flag() else int(math.floor(beta + 1))
    inside = J(0, beta) ** 2 + 2 * sum(J(n, beta) ** 2 for n in range(1, Nc + 1))
    total = J(0, beta) ** 2 + 2 * sum(J(n, beta) ** 2 for n in range(1, 60))   # = 1 by Bessel identity
    frac = inside / total
    out.append(f"beta={beta:.0f}: {frac:.4f}")
    ok &= frac >= 0.98
sys.exit(finish(ok, "power fraction inside Carson bandwidth: " + ", ".join(out)))
