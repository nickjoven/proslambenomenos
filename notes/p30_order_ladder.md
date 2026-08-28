<!-- evidence: scripts/experiments/p30_derive.py, scripts/experiments/p30_registration.json, scripts/experiments/p30_ladder.py, scripts/experiments/p30_results.json, scripts/verify/p30_order_ladder.py -->
# P-30: the order ladder

## What was asked

A-16: indefinite causal order attacks the symbol graph's deepest
primitive — order itself. Price it Bell-ladder style with the
P-17 machinery: enumerate the causally-ordered polytope, compute
the quantum values, expose the cost.

## The two games (LC-20)

- **OCB causal game** (Oreshkov–Costa–Brukner 2012): causal bound
  3/4; their process matrix W = ¼[1 + (σz^A2 σz^B1 +
  σz^A1 σx^B1 σz^B2)/√2] achieves (2+√2)/4. No physical
  realization known; maximality open in the source.
- **VLBC inequality** (van der Lugt–Barrett–Chiribella 2023):
  under Definite Causal Order + Relativistic Causality + Free
  Interventions, a three-term expression ≤ 7/4; the quantum
  switch with control entangled to a spacelike observer achieves
  1 + (2+√2)/4 — proven maximal there via Tsirelson. The 2026
  photonic experiment (24σ, loopholes flagged) implements this.

## The result (R-27, all clauses first run, 0.6 s)

| rung | OCB | VLBC | Bell (P-17) |
|---|---|---|---|
| ordered/local | 3/4 (8192 strategies, exhaustive) | 7/4 (131072, exhaustive) | 2 (16, exhaustive) |
| quantum | (2+√2)/4 | 1+(2+√2)/4 | 2√2 |
| algebraic | 1 | 2 | 4 |

**S = 8p − 4 (OCB) and S = 8(p−1) − 4 (VLBC) send both computed
ladders onto {2, 2√2, 4} at 1e-12.** OCB themselves noted the
number coincidence; the derive layer made it an exact affine map
before anything was computed. For these games, giving up definite
order buys precisely what giving up local realism bought — the
same √2 geometry, one affine transform apart.

## The null that prices the switch

The coherent switch's Alice-marginal p(a₁a₂|x₁x₂) equals the
50/50 classical mixture of the two fixed-order wirings entrywise
at machine zero (worst cell 0.0; density-matrix route 2.2e-16).
Order coherence is bipartitely invisible — consistent with the
imported theorems that the switch violates no bipartite causal
inequality — and becomes visible only through the entangled
spacelike observer, at exactly a Tsirelson cost. The registered
halt-and-audit trigger (a nonzero cell would contradict the
imported theorems) stayed quiet.

## Derive-layer gifts

- The OCB spectrum in closed form: the two Pauli strings
  anticommute (σzσx = −σxσz on B1), so M² = 2 and the spectrum is
  {0 ×8, ½ ×8} — positivity by algebra, not diagonalization.
- Process validity as trace-and-replace identities, with a pinned
  loop perturbation (¼ σz⊗σz⊗σz⊗σz) that breaks them — kept as
  the loop-blind falsifier mutant.
- The switch's third term is literally a CHSH game riding inside
  the causal game: with the target frozen, Bob–Charlie hold |Φ+⟩
  and measure at the CHSH angles.

## Relation to the symbol graph

The order primitive survives priced, not refuted: within known
physics (the switch), coherent order costs a Tsirelson violation
to certify and is otherwise indistinguishable from classical
order mixing at the bipartite level; beyond known physics (the
OCB process), the extra √2 is exactly the Bell √2. The VOCABULARY
edge: causal-inequality quantum values, where proven, fall out of
Tsirelson's bound — not out of new order physics.
