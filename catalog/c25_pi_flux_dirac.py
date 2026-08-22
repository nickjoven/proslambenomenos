"""The square lattice with flux 1/2 quantum per plaquette (the pi-flux lattice) has two bands E = +-2 sqrt(cos^2 kx + cos^2 ky) touching at isolated Dirac points, so the density of states vanishes linearly: the count of states with |E| < eps scales as eps^2.
Source: Affleck & Marston 1988 (flux phase); Lieb, PRL 73, 2158 (1994); Hofstadter 1976 at alpha = 1/2. Mutant: zero flux, where the zero-energy set is a curve (van Hove) and the count scales as eps."""
import math, sys
from _common import mutant_flag, finish

flux_half = not mutant_flag()
def energies(kx, ky):
    if flux_half:
        e = 2 * math.sqrt(math.cos(kx) ** 2 + math.cos(ky) ** 2)
        return (e, -e)
    return (2 * (math.cos(kx) + math.cos(ky)),)
def count(eps, M=400):
    c = 0
    for i in range(M):
        for j in range(M):
            kx, ky = math.pi * (i + 0.5) / M, math.pi * (j + 0.5) / M
            c += sum(1 for e in energies(kx, ky) if abs(e) < eps)
    return c
c1, c2 = count(0.2), count(0.4)
exponent = math.log(c2 / c1) / math.log(2)
ok = abs(exponent - 2) < 0.15
sys.exit(finish(ok, f"states with |E|<eps: {c1} at 0.2, {c2} at 0.4 -> scaling exponent {exponent:.2f} (Dirac: 2)"))
