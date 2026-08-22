"""Adler's equation d(theta)/dt = delta - K sin(theta) locks (theta settles) iff |delta| <= K; beyond that the beat frequency is sqrt(delta^2 - K^2).
Source: Adler, Proc. IRE 34, 351 (1946). Lock must emerge from integration, not from the threshold. Mutant: locking range K/2."""
import math, sys
from _common import mutant_flag, finish

def beat(delta, K, T=4000.0, dt=0.002):
    th, last, rot = 0.0, 0.0, 0
    n = int(T / dt)
    for i in range(n):
        th += dt * (delta - K * math.sin(th))
        if th - last > 2 * math.pi: rot += 1; last += 2 * math.pi
    return rot * 2 * math.pi / T
K = 1.0
rng = K / 2 if mutant_flag() else K
pred = lambda d: 0.0 if abs(d) <= rng else math.sqrt(d * d - rng * rng)
ok = True; out = []
for d in (0.7, 0.95, 1.05, 1.5):
    b = beat(d, K); p = pred(d)
    out.append(f"delta={d}: beat {b:.3f} pred {p:.3f}")
    ok &= abs(b - p) < 0.03
sys.exit(finish(ok, "; ".join(out)))
