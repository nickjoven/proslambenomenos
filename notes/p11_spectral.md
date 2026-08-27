<!-- evidence: scripts/experiments/p11_derive.py, scripts/experiments/p11_spectral.py, scripts/experiments/p11_results.json, scripts/verify/p11_spectral_metric.py -->
# P-11: the representation decides the metric

Symbols: see the VOCABULARY.md symbol graph - geodesic distance falls out of the commutator only in the source-pullback representation (a verified refusal otherwise).

Registered before computing (PREDICTIONS.md P-11); resolution R-9.
Distance with no paths anywhere in its definition: d(p,q) =
sup { f(q) - f(p) : ||[D, f]|| <= 1 } (Connes 1994; finite-space
computations: Iochum, Krajewski, Martinetti, J. Geom. Phys. 37, 100
(2001); graphs: arXiv:2105.09056). Same algebra (functions on
vertices), same incidence Dirac, two representations.

## What computed

**Source-pullback representation (f acts on vertices and edges).**
On the cycle the commutator norm collapses to max|df| (checked to
1.75e-16 against the explicit commutator) and the spectral distance
IS hop distance: the hop tent is feasible and extremal, telescoping
caps everything else. Geometry with no paths recovers the path
metric exactly.

**Vertex-only representation (edge action zero).** The norm becomes
sqrt(lam_max(diag(f) L diag(f))) - it feels the *values* of f, not
only its differences. The gauged distance is bounded, with closed
forms met by exact witnesses (all Gram norms 1.0 to 1e-9):

    d(0,1)      = 2/sqrt(3) = 1.1547   witness (-1/sqrt(3), +1/sqrt(3), 0, ...)
    d(0,j >= 2) = sqrt(2)   = 1.4142   witness (-1/sqrt(2), 0, ..., +1/sqrt(2))

Neighbours are resolved; everything farther saturates at sqrt(2)
(diagonal Rayleigh cap 2g_i^2 <= 1; 2x2 principal-minor cap at
2/sqrt(3)). A bounded geometry from an unbounded graph.

**Where the registration overreached (R-9).** The registered "tent
norm = 1 on any graph" holds only where each vertex has one incoming
edge. On the P-6 maximiser circulants the B-norm aggregates incoming
gradients in l2: tent norms sqrt(6), sqrt(7), sqrt(15) =
sqrt(in-degree) on C_20({1..6}), C_22({1..7}), C_44(two-band). The
<= hop direction held everywhere (worst feasible excess 0.0). Exact
geodesic recovery is a property of chain-like coupling, not of the
representation alone.

## Reading (commentary within an evidence note, no load)

This is the algebraic face of the P-13 lesson. There, two chains
with the same metric scattered differently: the substrate holds more
than its geometry. Here, one graph carries three geometries -
geodesic (chain coupling), l2-deformed (dense coupling), bounded-
saturating (value coupling) - decided entirely by how the algebra
couples to the Hilbert space. "Which metric exists" is not a
property of the point set; it is a property of the coupling. Scope:
finite graphs, this Dirac; nothing about continuum limits or
physical spacetime (PREDICTIONS.md P-11 not-claimed-in-advance).
