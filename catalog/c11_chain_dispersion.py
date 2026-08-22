"""A nearest-neighbour mass chain has dispersion omega(k) = 2 sqrt(J/m) |sin(k/2)|; a sharp front therefore spreads (Schrodinger 1914).
Source: Schrodinger, Ann. Phys. 349, 916 (1914); any solid-state text. Mutant: the continuum law omega = sqrt(J/m) k."""
import math, sys
from _common import mutant_flag, finish

J, m, N = 1.0, 1.0, 64
worst = 0.0
for n in (1, 5, 13, 31):
    k = 2 * math.pi * n / N
    # eigenvalue of the discrete Laplacian on a plane wave
    lam = (2 - 2 * math.cos(k)) * J / m
    omega_num = math.sqrt(lam)
    omega_claim = math.sqrt(J / m) * k if mutant_flag() else 2 * math.sqrt(J / m) * abs(math.sin(k / 2))
    worst = max(worst, abs(omega_num - omega_claim) / omega_num)
ok = worst < 1e-12
sys.exit(finish(ok, f"worst relative deviation of claimed omega(k) from the chain eigenfrequency: {worst:.1e}"))
