"""A circle rolling inside a circle of twice its radius traces a straight diameter (Tusi couple).
Source: Nasir al-Din al-Tusi, Tadhkira (1247); hypocycloid with R = 2r."""
import math, sys
from _common import mutant_flag, finish

r = 1.0
R = 3.0 * r if mutant_flag() else 2.0 * r


def point(t):
    # hypocycloid: circle of radius r rolling inside circle of radius R
    x = (R - r) * math.cos(t) + r * math.cos((R - r) / r * t)
    y = (R - r) * math.sin(t) - r * math.sin((R - r) / r * t)
    return x, y


ys = [abs(point(2 * math.pi * k / 400)[1]) for k in range(400)]
xs = [point(2 * math.pi * k / 400)[0] for k in range(400)]
ok = max(ys) < 1e-12 and abs(max(xs) - R) < 1e-9 and abs(min(xs) + R) < 1e-9
sys.exit(finish(ok, f"hypocycloid R={R:.0f}r stays on y=0 (max|y|={max(ys):.1e}) spanning [-R, R]"))
