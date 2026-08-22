# PREDICTIONS — preregistration ledger (append-only)

A prediction is registered BEFORE the work it covers runs: what will
be attempted, the expected outcome, and what result would change the
author's mind. The gate (scripts/check_predictions.py) enforces the
"pre-": the commit that registers a prediction must be an ancestor of
the commit that introduces the claim citing it, and the protected
remote makes that ordering third-party-attested (history behind a
pushed commit cannot be rewritten). Resolutions are appended as R-n
entries; nothing is edited in place.

Scope rule (mechanical): claims created after this ledger's first
commit that carry numeric_match or novelty checked-novel MUST cite a
prediction; LITCHECKS entries added after it MUST cite one. Everything
else may cite one, and any citation is checked for existence and
ordering.

## P-1 — 2026-08-20 — the XOR spectrum-to-tree bridge
expects: no canonical map exists from the twisted-bundle Fourier
parity to Stern-Brocot denominator parity - the attempt resolves as
an under-determination result (the audit's 1,764-pairs-both-ways
evidence and the source doc's own admission that the parity object
is not forced both point there).
changes-my-mind: an explicit, natural construction that fixes
denominator parity uniquely from the orientation-bundle character,
with a proof that rival parity objects (numerator, sum) are excluded
rather than unconsidered.

## P-2 — 2026-08-20 — the two-anchor minimum
expects: partial rigorization - the non-smoothness of the locked
measure at K = 1 (Jensen-Bak-Bohr) is provable as a statement about
the circle-map family, but the physical framing ("two dimensional
anchors are therefore the minimum") remains interpretive and does
not follow from the lemma alone.
changes-my-mind: a derivation in which the anchor count is forced by
the lemma without an added modeling premise; or a counterexample
showing the locked measure is smoother at K = 1 than the classical
result is being read to say.

## P-3 — 2026-08-20 — the Iwasawa one-stage claim
expects: the v1 statement ("every nontrivial continuous subgroup
kills exactly one Iwasawa stage") is FALSE as stated - 2-dimensional
Borel subgroups absorb two factors - and a corrected, weaker
statement is provable; the dimension-3 conclusion survives under the
corrected version.
changes-my-mind: a proof of the original statement handling the
Borel case, or a failure to salvage any corrected version, which
would also reopen the dimension conclusion's support.

## R-1 — 2026-08-21 — resolves P-1
outcome: the headline expectation held - no canonical map exists from
the proven spectral XOR to Stern-Brocot denominator parity. The
MECHANISM differs from the one predicted: P-1 expected
under-determination (two natural maps with different pushforwards);
the work found domain vacuity instead - the fraction-pair index set
the conjectured rule quantifies over is never instantiated by the
corpus-canonical dynamics (claims klein-twisted-gradient-xor,
klein-twisted-mean-frequency-identity, xor-bridge-domain-vacuity;
notes/p1_decomposition.md). The mind-change condition did not fire.
Scope of the empirical leg is stated in the vacuity claim (explored
K, J, lattice size); the two theorem-lets are unconditional.
Mechanism correction recorded as a prediction error, not an
expectation error.

## P-4 — 2026-08-21 — holonomy vs gate on a twisted inertial ring
question: on a ring of N second-order phase oscillators (Kuramoto with
inertia / Frenkel-Kontorova with mass) carrying one pi-offset bond and
one stick-slip node driven at constant velocity, does the holonomy
change the gating threshold at which the slip pattern doubles its
period (the Kawano/Guettler f0/2 mechanism), or does gating occur at
the same threshold with the holonomy only relabeling which orbits
close on the base vs the double cover?
expects: the threshold is UNCHANGED to within the sweep resolution -
the holonomy is kinematic (available counts) and the gate is dynamic
(selection); the twisted ring differs from the control only in
which spectral lines are present (half-integer lines always on),
not in WHEN period doubling onsets. Secondary expectation: an N-parity
dependence of the twisted case (Lazarides 2008 analog), absent in
the control.
changes-my-mind: a threshold shift between twisted and control that
survives changing N, friction law parameters, and drive velocity,
with sign and magnitude reproducible by an independent
reimplementation; that would mean the bundle class does dynamical
selection and X-8's reading is wrong.
not-claimed-in-advance: anything about real strings; the model is a
phase ring, not Kawano's FE string, and its stick-slip law will be a
Coulomb threshold, not Bellante's velocity-dependent mu.

## P-5 — 2026-08-22 — the a0 / cH0 literature pointer
question: does the published literature contain a derivation (not a
heuristic) of Milgrom's a0 from the de Sitter / Gibbons-Hawking
temperature, such that a0-tracks-hubble-conjecture could be promoted
from coincidence-unruled to imported-with-mechanism?
expects: NO - Milgrom 1999 is a heuristic identification of a0 with
the acceleration at which the Unruh temperature matches the de Sitter
temperature, and no later work derives MOND phenomenology from it;
the claim stays coincidence-unruled and gains only a literature
pointer (LC-6).
changes-my-mind: a peer-reviewed derivation producing the MOND
interpolating function, or the BTFR normalisation, from de Sitter
thermodynamics without fitted parameters.

## R-2 — 2026-08-22 — resolves P-3
outcome: as expected. The v1 statement is false (the 2-dimensional
Borel subgroup AN kills two stages; the one-parameter-or-discrete
dichotomy omits dimensions 2 and 3), the corrected classification
of connected subgroups of SL(2,R) is proven (claim
sl2r-connected-subgroups, classical), and the dimension-3 conclusion
survives because it only ever used dim H >= 1. The mind-change
condition did not fire. Resolution produced by a context-free
auditor and reviewed; the physics premises of the source are not
touched by the mathematics and remain unsupported.

## R-3 — 2026-08-22 — resolves P-4
outcome: model-class vacuity. A context-free audit showed the
clamped variant - the only one in which a corner propagates - has no
loop and hence no holonomy: the pi bond next to the clamp is a
boundary phase difference, gauge-equivalent to a uniform strain
pi/N, so twisted and control are the same linear system to
O(1/N^2). "Threshold unchanged" held by construction, the N-parity
expectation had no mechanism, and no run exhibited the gate at all.
The mind-change condition could not fire: a prediction-design error,
recorded as such (notes/p4_twisted_inertial_ring.md, audit section).
Also retracted with it: the "integrator fix" diagnosis (the chatter
is the massive bow node's own period, physical) and the
mu_d-independence of the loading formula (catalog c13).

## P-6 — 2026-08-23 — dense circulant graphs that do not synchronize
question: on circulant graphs C_n(S) with identical Kuramoto
oscillators, which (n, S, q) admit a linearly stable q-twisted state
theta_j = 2 pi q j / n, and what is the largest edge density at which
one exists? Known: Townsend, Stillman, Strogatz (Chaos 30, 083142,
2020) exhibit non-synchronizing circulant graphs at density ~ 0.6809;
Kassabov, Strogatz, Townsend (Chaos 31, 073135, 2021) prove every
graph of density > 0.75 synchronizes globally. The gap is open.
method: exhaustive over all symmetric connection sets S for n <= 28
(stability from the closed-form circulant eigenvalues lambda_m =
sum_{k in S} cos(2 pi q k/n)(1 - cos(2 pi m k/n)) >= 0 for all m != 0);
greedy/random search for 28 < n <= 64; independent check of any
reported stable state by direct Jacobian eigenvalues.
expects: the maximal circulant density with a stable twisted state
is reproduced at ~0.68 and does NOT exceed 0.6809 + 1e-3 for n <= 64:
the circulant family was already optimised by the 2020 authors and
the open gap lives in non-circulant graphs. Secondary: the maximising
S are the "near-half" families (offsets concentrated where cos(2 pi q
k/n) > 0), and the density maximum approaches from below as n grows.
changes-my-mind: a circulant C_n(S), n <= 64, with a twisted state
whose Jacobian has all non-trivial eigenvalues strictly negative at
density > 0.6819, verified by the independent Jacobian check - that
would move the published lower bound and be reported as such. Any
stable twisted state above 0.75 is a bug, not a result (theorem).
not-claimed-in-advance: anything about non-circulant graphs; the
global-sync threshold itself.
