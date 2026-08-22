"""Descent time along an inverted cycloid to its bottom is independent of the start point: T = pi*sqrt(r/g).
Source: Huygens, Horologium Oscillatorium (1673). Mutant: a circular arc is not isochronous."""
import math, sys
from _common import mutant_flag, finish

g, r = 9.81, 1.0


def descent_time(t0, circle):
    # curve parameter t in [t0, pi]; height drop from start h(t) - h(t0)
    if circle:
        # circular arc of radius r, angle measured from the bottom
        y = lambda t: r * (1 - math.cos(t))
        ds = lambda t: r
    else:
        y = lambda t: r * (1 + math.cos(t))       # inverted cycloid, bottom at t = pi
        ds = lambda t: 2 * r * math.sin(t / 2)
    # time = integral ds / sqrt(2 g (y(t0) - y(t))); plain midpoint rule, n = 200000 - the
    # 1/sqrt endpoint singularity is integrable and converges by brute force, O(sqrt(h))
    n = 200000
    T = 0.0
    a, b = t0, math.pi if not circle else 0.0
    lo, hi = (a, b) if a < b else (b, a)
    for k in range(n):
        t = lo + (hi - lo) * (k + 0.5) / n
        drop = y(t0) - y(t)
        if drop <= 0:
            continue
        T += ds(t) / math.sqrt(2 * g * drop) * (hi - lo) / n
    return T


circle = mutant_flag()
Ts = [descent_time(t0, circle) for t0 in (0.3, 1.0, 2.0)]
pred = math.pi * math.sqrt(r / g)
spread = (max(Ts) - min(Ts)) / pred
ok = spread < 5e-3 and (circle or abs(Ts[0] - pred) / pred < 5e-3)
sys.exit(finish(ok, f"descent times from three starts: {[round(T, 4) for T in Ts]} (pi*sqrt(r/g) = {pred:.4f}; spread {spread:.1e})"))
