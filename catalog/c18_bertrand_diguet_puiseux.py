"""Bertrand-Diguet-Puiseux: on a surface of Gaussian curvature K a geodesic circle of radius r has circumference 2 pi r (1 - K r^2/6 + O(r^4)); curvature is the deviation of the measured pi, not its value.
Source: Bertrand, Diguet, Puiseux 1848 (see do Carmo, Differential Geometry of Curves and Surfaces, sec. 4-6). Checked on the unit sphere, C(r) = 2 pi sin r. Mutant: coefficient 1/3."""
import math, sys
from _common import mutant_flag, finish

coef = 1 / 3 if mutant_flag() else 1 / 6
K = 1.0
worst = 0.0
for r in (0.05, 0.1, 0.2):
    C = 2 * math.pi * math.sin(r)            # geodesic circle on the unit sphere
    ratio = C / (2 * math.pi * r)
    pred = 1 - coef * K * r * r
    worst = max(worst, abs(ratio - pred) / (r ** 4))   # residual must be O(r^4)
ok = worst < 0.02
sys.exit(finish(ok, f"|C/(2 pi r) - (1 - K r^2 coef)| / r^4 worst = {worst:.3f} (O(1) if the coefficient is right)"))
