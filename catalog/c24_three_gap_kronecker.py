"""Irrational rotation: N points {k alpha mod 1} have at most three distinct gap lengths (Steinhaus three-gap theorem) and the largest gap -> 0, so the orbit is dense; a rational rotation p/q revisits q points forever.
Source: Sos 1958; Swierczkowski 1959 (three-gap); Kronecker-Weyl density. Checked at the golden mean and at 3/7. Mutant: claim the rational orbit is dense too."""
import math, sys
from _common import mutant_flag, finish

def gaps(alpha, N):
    pts = sorted((k * alpha) % 1.0 for k in range(N))
    g = [b - a for a, b in zip(pts, pts[1:])] + [1 - pts[-1] + pts[0]]
    return g
phi = (math.sqrt(5) - 1) / 2
distinct = lambda g: len({round(x, 9) for x in g})
g_irr = gaps(phi, 500); g_rat = gaps(3 / 7, 500)
three_gap = distinct(g_irr) <= 3
dense_irr = max(g_irr) < 0.01
dense_rat = max(g_rat) < 0.01            # false: only 7 distinct points, largest gap 1/7
claim = (dense_rat if mutant_flag() else (not dense_rat))
ok = three_gap and dense_irr and claim
sys.exit(finish(ok, f"golden mean: {distinct(g_irr)} gap lengths, max gap {max(g_irr):.4f}; 3/7: max gap {max(g_rat):.4f}"))
