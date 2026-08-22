"""Parallel transport around a latitude circle at polar angle theta on the unit sphere rotates a tangent vector by 2 pi (1 - cos theta) - the enclosed curvature (Gauss-Bonnet; the Foucault pendulum).
Source: Foucault 1851; holonomy = integral of K over the cap = 2 pi (1 - cos theta). Computed by discrete transport (project onto successive tangent planes). Mutant: 2 pi sin theta."""
import math, sys
from _common import mutant_flag, finish

def transport(theta, steps=20000):
    # start at phi = 0 with the tangent vector pointing along +phi; step along the circle,
    # projecting the carried vector onto the new tangent plane each step (Levi-Civita, discrete)
    s, c = math.sin(theta), math.cos(theta)
    v = [0.0, 1.0, 0.0]                                    # e_phi at phi = 0
    for k in range(1, steps + 1):
        phi = 2 * math.pi * k / steps
        n = [s * math.cos(phi), s * math.sin(phi), c]      # new point = new normal
        d = sum(a * b for a, b in zip(v, n))
        v = [a - d * b for a, b in zip(v, n)]
        L = math.sqrt(sum(a * a for a in v)); v = [a / L for a in v]
    # angle between transported v and e_phi at the start, signed about the normal
    e_phi = [0.0, 1.0, 0.0]; e_th = [c, 0.0, -s]
    return math.atan2(sum(a * b for a, b in zip(v, e_th)), sum(a * b for a, b in zip(v, e_phi)))

def circ_dist(a, b):
    d = (a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)
worst = 0.0
for theta in (0.4, 0.9, 1.3):
    got = transport(theta)
    pred = (2 * math.pi * math.sin(theta)) if mutant_flag() else (2 * math.pi * (1 - math.cos(theta)))
    # orientation of the rotation depends on the traversal sense; magnitude is the holonomy
    worst = max(worst, min(circ_dist(got, pred), circ_dist(got, -pred)))
ok = worst < 2e-3
sys.exit(finish(ok, f"holonomy vs prediction, worst |difference| = {worst:.2e} rad"))
