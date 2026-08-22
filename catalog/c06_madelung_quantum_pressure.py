"""For a Gaussian density, the Bohm quantum potential Q = -(hbar^2/2m^2) (lap sqrt(rho))/sqrt(rho) equals (hbar^2/2m^2)(1/(2 s^2) - x^2/(4 s^4)).
Source: Madelung 1927; Bohm 1952; fuzzy-DM fluid form (Hui et al. 2017 eq. 15). Mutant: drop the factor 1/2."""
import math, sys
from _common import mutant_flag, finish

hbar, m, s = 1.0, 1.0, 0.7
pref = (hbar ** 2 / m ** 2) if mutant_flag() else (hbar ** 2 / (2 * m ** 2))
amp = lambda x: math.exp(-x * x / (4 * s * s))        # sqrt(rho)
h = 1e-3
worst = 0.0
for x in (-1.2, -0.4, 0.0, 0.5, 1.3):
    lap = (amp(x + h) - 2 * amp(x) + amp(x - h)) / (h * h)
    Q_num = -pref * lap / amp(x)
    Q_formula = (hbar ** 2 / (2 * m ** 2)) * (1 / (2 * s * s) - x * x / (4 * s ** 4))
    worst = max(worst, abs(Q_num - Q_formula) / (abs(Q_formula) + 1e-9))
ok = worst < 1e-4
sys.exit(finish(ok, f"quantum potential numeric vs closed form, worst rel err {worst:.1e}"))
