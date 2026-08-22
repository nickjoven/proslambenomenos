"""A cycloid's cusp at the contact point is semicubical: |y| ~ |x|^(2/3) near the cusp.
Source: standard (x = r(t - sin t), y = r(1 - cos t); expand at t -> 0: x ~ r t^3/6, y ~ r t^2/2)."""
import math, sys
from _common import mutant_flag, finish

claimed = 0.5 if mutant_flag() else 2.0 / 3.0
r = 1.0
pts = [(r * (t - math.sin(t)), r * (1 - math.cos(t))) for t in (1e-2, 3e-3, 1e-3)]
# local exponent from successive pairs
exps = [math.log(pts[i][1] / pts[i + 1][1]) / math.log(pts[i][0] / pts[i + 1][0]) for i in range(2)]
ok = all(abs(e - claimed) < 1e-3 for e in exps)
sys.exit(finish(ok, f"local exponent d ln y/d ln x at the cusp = {exps[-1]:.4f} (claimed {claimed:.4f})"))
