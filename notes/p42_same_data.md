<!-- evidence: scripts/experiments/p42_derive.py, scripts/experiments/p42_registration.json, scripts/experiments/p42_identity.py, scripts/experiments/p42_results.json -->
# P-42 working document: same data, different halves

Items 1 and 3 of the 2026-09-01 theoretical press (the owner's
conflated-or-underexplored survey), one machinery. Lessons L-9
consulted per AGENTS 8d.

## Finding 1: the switch's data IS GHZ's data

The P-38 switch model's triple-marginals equal the GHZ empirical
model at 1.4e-16, and the other six outputs factorize exactly:
deterministic copies plus fair coins (completion counts 8/2/2/2,
conditional nonuniformity 0.0 - a float zero produced by exact
uniformity, species one of the five kinds). Consequence, stated
plainly: in this scenario indefinite causal order generates no
correlations. The entire physics is in the EXCLUSION - the same
GHZ data rules out definite causal orders here (via the imported
reduction theorem) and local hidden states there. Resource
language for ICO that does not lead with this conflates data with
causal hypothesis. Two independent quantum routes agree
(statevector vs stabilizer-group arithmetic: the four signed
contexts +XXX, -XYY, -YXY, -YYX are elements of the size-8 GHZ
stabilizer group).

## Finding 2: the two halves are different objects (refused)

The switch's 1/2: the four parity equations over GF(2) have
coefficient rank 3, augmented rank 4 - inconsistent, an
all-vs-nothing system, hence (Abramsky-Brandenburger-Barbosa,
imported LC-31) a nonzero contextual obstruction: NO global
assignment of outcomes exists. The ring's 1/2 (P-35): one global
configuration - uniform covariant strain, spread 2.2e-15, winding
-1/2 - a section that plainly exists, obstruction zero. The graph
now carries the refused edge ring-order "not the same half": same
numeral, one is the absence of a global section, the other is a
global section's label. The refusal sharpens LC-26's earlier
observation that our winding sectors are the semifluxon doublet:
THAT identification (ring <-> semifluxon) stands - both are
sections; it is the contextual half that is the different animal.

## Instrument notes

The factorization check is exhaustive over the full outcome space
per context - no sampling anywhere in the line. The GHZ side runs
twice (statevector in the layer, stabilizer arithmetic in the
falsifier); the switch side runs twice (dense 64-dim in the
layer via P-38, branch expansion in the falsifier).
