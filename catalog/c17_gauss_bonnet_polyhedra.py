"""Gauss-Bonnet on polyhedra: the deficit angles of the tetrahedron, cube, octahedron and icosahedron each sum to 2 turns (4 pi = 2 pi chi(S^2)), with every deficit a rational number of turns - curvature without irrationals (Regge 1961).
Source: Descartes' theorem on total angular defect; Regge, Nuovo Cimento 19, 558 (1961). Mutant: claim the total is 1 turn."""
import math, sys
from fractions import Fraction
from _common import mutant_flag, finish

# (vertices, faces meeting at a vertex as (n-gon, count)) for the Platonic solids with regular faces
solids = {"tetrahedron": (4, [(3, 3)]), "cube": (8, [(4, 3)]), "octahedron": (6, [(3, 4)]),
          "icosahedron": (12, [(3, 5)])}
claimed_turns = 1 if mutant_flag() else 2
ok = True; out = []
for name, (V, corner) in solids.items():
    # interior angle of a regular n-gon in turns: (n-2)/(2n); deficit in turns = 1 - sum
    angle_sum = sum(Fraction(n - 2, 2 * n) * k for n, k in corner)
    deficit = 1 - angle_sum
    total = deficit * V
    out.append(f"{name}: deficit {deficit} turn x {V} = {total} turns")
    ok &= total == claimed_turns and deficit.denominator > 0
sys.exit(finish(ok, "; ".join(out)))
