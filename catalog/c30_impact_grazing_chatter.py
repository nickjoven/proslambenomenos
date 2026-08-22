"""Impact oscillator x'' + 2 zeta x' + x = cos(omega t) with a wall at sigma and restitution r: (i) the first impact of the orbit grazing a wall at A - d has velocity v with v^2/d -> 2 A omega^2 (the square-root singularity of the impact map, Nordmark 1991); (ii) under slow forcing the impacts accumulate with gap ratio -> r (complete chatter, Budd & Dux 1994).
Source: Shaw & Holmes, J. Sound Vib. 90, 129 (1983); Nordmark, J. Sound Vib. 145, 279 (1991); Budd & Dux, Phil. Trans. R. Soc. A 347, 365 (1994). Mutant: claim a linear law v/d -> const (no singularity)."""
import math, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "scripts/experiments"))
from _common import mutant_flag, finish
from impact_oscillator import next_impact, run, ZETA

omega = 2.8
A = 1 / math.sqrt((1 - omega ** 2) ** 2 + (2 * ZETA * omega) ** 2)
phi = math.atan2(2 * ZETA * omega, 1 - omega ** 2)
t0 = (phi + math.pi) / omega
ratios = []
for d in (0.001, 0.004, 0.016):
    ti, vi = next_impact(-A, 0.0, t0, omega, A - d, t0 + 2 * math.pi / omega, h=0.005)
    ratios.append((vi * vi / d) if not mutant_flag() else (abs(vi) / d))
sqrt_law = max(ratios) / min(ratios) < 1.1 and abs(ratios[0] - 2 * A * omega ** 2) / (2 * A * omega ** 2) < 0.05
_, allimp = run(0.5, 0.3, 0.5, n_periods=2, skip=0)
gaps = [b - a for (a, _), (b, _) in zip(allimp, allimp[1:])]
imin = min(range(len(gaps)), key=lambda i: gaps[i])          # end of the first accumulation
tail = [gaps[i + 1] / gaps[i] for i in range(imin - 5, imin)]   # the five ratios leading into it
chatter = bool(tail) and max(abs(x - 0.5) for x in tail) < 0.02
ok = sqrt_law and chatter
sys.exit(finish(ok, f"v^2/d (or v/d under mutant) = {[round(x, 3) for x in ratios]} vs 2Aw^2 = {2*A*omega**2:.3f}; chatter tail ratios {[round(x, 3) for x in tail]}"))
