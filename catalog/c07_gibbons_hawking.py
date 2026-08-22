"""Regularity of Euclidean de Sitter at the horizon fixes the imaginary-time period 2 pi/H, i.e. T = H/(2 pi).
Source: Gibbons & Hawking, Phys. Rev. D 15, 2738 (1977). Static patch f(r) = 1 - H^2 r^2; period beta = 4 pi/|f'(r_h)|."""
import sys
from _common import mutant_flag, finish
import math

H = 0.37
f = lambda r: 1 - H * H * r * r
r_h = 1 / H
h = 1e-6
fp = (f(r_h + h) - f(r_h - h)) / (2 * h)
beta = 4 * math.pi / abs(fp)
T = 1 / beta
claimed = H / math.pi if mutant_flag() else H / (2 * math.pi)
ok = abs(T - claimed) / claimed < 1e-6
sys.exit(finish(ok, f"T = 1/beta = {T:.6f}; claimed {claimed:.6f}"))
