"""Material spiral arms in a flat-rotation-curve disk wind up: pitch angle falls as 1/t, below 5 degrees within ~2 rotations.
Source: the winding dilemma (Lindblad; Binney & Tremaine sec. 6.1). Mutant: rigid rotation keeps the pitch angle fixed."""
import math, sys
from _common import mutant_flag, finish

rigid = mutant_flag()
v = 1.0
r1, r2 = 1.0, 1.01
Omega = (lambda r: v / r) if not rigid else (lambda r: v / 1.0)
# a radial line of matter at t=0; after time t the azimuth differs between r1 and r2
T_rot = 2 * math.pi * 1.0 / v            # one rotation at r = 1
pitch = []
for n in (1, 2, 5):
    t = n * T_rot
    dphi = (Omega(r1) - Omega(r2)) * t
    # pitch angle: tan i = dr / (r dphi)
    i = math.degrees(math.atan2((r2 - r1), (1.0 * abs(dphi)))) if dphi != 0 else 90.0
    pitch.append(i)
# the claim, evaluated identically in both modes: rigid rotation cannot satisfy it.
# 1/t law: tan(i_n) * n is constant across n = 1, 2, 5 (to 1e-9 - it is exact here)
tn = [math.tan(math.radians(p)) * n for p, n in zip(pitch, (1, 2, 5))]
law = max(tn) - min(tn) < 1e-9 * max(tn) if max(tn) < 1e9 else False
ok = pitch[1] < 5.0 and pitch[2] < pitch[1] < pitch[0] and law
sys.exit(finish(ok, f"pitch angle after 1, 2, 5 rotations: {[round(p, 2) for p in pitch]} deg ({'rigid' if rigid else 'flat curve'})"))
