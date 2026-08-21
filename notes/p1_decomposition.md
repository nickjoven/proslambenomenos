# P-1 working document: the XOR spectrum-to-tree bridge, decomposed

Governed by prediction P-1 (PREDICTIONS.md): expected outcome is
under-determination; the mind-change condition is a natural
construction fixing denominator parity uniquely. This document
decomposes the problem, records the discharge of its own checkable
ledger, and logs corrections made by that discharge. Prose here
carries no load: every factual line below is cited, scripted, or
mood-marked.

## The two sides

**Side A (proved; compendium C7, claims klein-orientation-bundle-
spectrum, klein-line-bundle-classification).** Twisted-bundle Fourier
modes on the flat Klein bottle, indexed (m, branch, n), m in Z or
Z + 1/2; allowed iff p_x + p_y = 1 (mod 2) with p_x = [m
half-integer], p_y = [sin branch]. Lowest-terms denominators of these
wavenumbers: 1 or 2 only.

**Side B (conjectured; v1 xor_derivation edition 2, sections 5-6).**
Locked states of nonlinear dynamics indexed by Stern-Brocot pairs
(p1/q1, p2/q2), arbitrary q; rule: allowed iff q1 + q2 odd. Edition 2
itself records that the parity object (numerator, denominator, sum)
is stipulated, not forced.

**The bridge**: a canonical map Phi from A-indexing to B-indexing
carrying one XOR to the other, or a proof that none exists.

## Decomposition

**D1 — domain.** A-objects are linear eigenmodes; B-objects are
nonlinear locked states; no common index set exists. Any Phi must
name its mechanism: linearization around locked states, a
renormalization limit, or symbolic orbit coding. The source corpus
never chose. SHARPENED by discharge (below): spatial windings on the
twisted lattice are constrained to (1/2)Z (theorem-let), while
arbitrary-denominator fractions in the tongue picture index TEMPORAL
rotation numbers. The bridge is not spatial-to-spatial at all; it
must connect spatial mode parity to temporal locking parity, a
distinction the corpus never draws.

**D2 — the twist on the nonlinear side.** Sub-problem: classify
states compatible with the antiperiodic x-loop. RESOLVED for the
uniform-gradient (spatial) sector by the theorem-let below: x-winding
in Z + 1/2 with uniform y, or in Z with pi-staggered y. The temporal
sector (rotation numbers under driving) remains open and is where
any fraction-level rule must live. Mood: the pi-junction /
frustrated-XY literature likely covers the spatial statement — D8
litcheck pending, preregistered under P-1.

**D3 — the reflection.** The deck map couples x-shift with
y-reflection, which acts on y-windings as W2 -> -W2 (mod M) — the
lattice form of the Farey involution p/q -> (q-p)/q (verified in
p1_gradient_bc.py). The spectral cos/sin branch corresponds to the
symmetric/antisymmetric combination over a reflection-orbit — the
C4/C5 involution and the C7 mode table are the same structure seen
from two sides. Any candidate Phi must be equivariant for it.

**D4 — the discriminating enumeration (not yet run).** Enumerate
actual admissible locked pairs of the twisted lattice DYNAMICS
(temporal locking, small N) and compare against the three candidate
parity objects. The corpus's cited simulations test the wavenumber
spectrum, not the fraction rule (edition 2's own statement). This is
the experiment that separates T+/T-/T0 and it remains the next step.

**D5 — canonicity criteria, fixed in advance.** Phi is canonical iff
(i) defined by the geometry/dynamics with no arbitrary choice, in
particular equivariant under the deck action and the D3 involution;
(ii) restricts on denominators {1, 2} to the proved Fourier rule;
(iii) the parity object is derived, not selected.

**D6 — resolution shapes.** T+: a forced rule (fires P-1's
mind-change). T-: two natural maps with different pushforwards
(under-determination; the preregistered expectation). T0: the D4
enumeration matches none of the three candidates and yields the true
admissibility rule, superseding the conjecture outright.

**D7 — the model, pinned.** The Kuramoto lattice with the
Klein-twisted boundary conditions (v1 klein_bottle.md's own
equations); attack routes: exact algebra on ansatz families, and
exhaustive small-N enumeration of locked states.

**D8 — prior-art check (pending).** Frustrated XY rings /
pi-junction arrays for the spatial statement; mode-locking under
twisted boundary conditions for the temporal one. Any novelty label
waits on this litcheck, which by LAW-6 requires its prediction
reference.

## Checkable ledger — discharged 2026-08-20

| Assertion | Result | Where |
|---|---|---|
| 1,764 pairs both ways at depth 6 (quoted from audit) | RECOMPUTED, passes: 63 interior fractions, splits 42/21 under both q- and p-parity, ordered XOR pairs 1764 both, sets share 882 and differ | scripts/verify/p1_depth6_pairs.py |
| Fourier denominators in {1, 2} | trivial, checked | C7 |
| Gradient compatibility algebra | CORRECTED BY DISCHARGE — see below | scripts/verify/p1_gradient_bc.py |
| Reflection = Farey involution on windings | verified | same script |
| pi-ring literature covers D2-spatial | mood-marked conjecture; litcheck pending | D8 |

## Corrections log (the mechanism working)

1. The first in-conversation algebra read the y-winding quantization
   as "b in (1/2)Z" in the continuum. Wrong: for continuous y the
   coefficient condition forces b = 0 outright; the second branch is
   lattice-only (the pi-staggered pattern), where discreteness
   loosens "for all y" to "for all j".
2. The first version of the verification script parametrized
   windings per-site rather than per-cycle and therefore tested a
   different family; the mismatch surfaced on the first run and the
   script was replaced with the exhaustive per-cycle version. Both
   versions' history is in git.
3. The framing "arbitrary p/q windings" conflated spatial windings
   (integers, or half-integers under the twist) with temporal
   rotation numbers (arbitrary rationals). This conflation is
   inherited from the source corpus and is now recorded as part of
   D1: the bridge's domain problem is spatial-to-temporal.

## First result under P-1

**Theorem-let (claims/klein-twisted-gradient-xor, proven).** On an
N x M lattice with theta_{i+N,j} = theta_{i,M+1-j} + pi and
theta_{i,j+M} = theta_{i,j}, M even, the compatible uniform-gradient
states theta = 2*pi*(W1*i/N + W2*j/M) are precisely W2 = 0 with
W1 in Z + 1/2, and W2 = M/2 (pi-staggered) with W1 in Z.

*Proof.* The boundary condition reads 2*pi*W1 + 2*pi*W2*(2j - M - 1)/M
= pi (mod 2*pi) for all j. The j-dependent increment between
consecutive j is 4*pi*W2/M, which must vanish mod 2*pi, forcing
2*W2 = 0 (mod M), i.e. W2 in {0, M/2}. For W2 = 0 the constant part
gives 2*pi*W1 = pi (mod 2*pi), so W1 in Z + 1/2. For W2 = M/2 the
j-terms contribute pi*(2j - M - 1), which is pi*(odd) and shifts the
constant condition to 2*pi*W1 = pi + pi*(M + 1) (mod 2*pi); for M
even this gives W1 in Z. Exhaustive verification at N = M = 12 over
all half-integer W1 and integer W2 agrees (24 = expected 24, no
extras). QED

Consequence for P-1: the spatial sector reproduces the spectral XOR
on denominator-<= 2 windings and admits nothing else; any
fraction-level parity rule must arise in the temporal locking sector,
whose enumeration (D4) is the next step. This is consistent with the
preregistered expectation and resolves nothing about it yet.

## E1 log (D4 probe, temporal sector)

- Step 1 (branch-seeded ICs, N=4): plateau structure is
  seed-independent at K=1, J=0.6 — phase slips erase initial winding;
  the temporal signature is intrinsic to the twisted dynamics.
- Step 2 (K/J sweep, 3x3, twisted vs control, results in
  scripts/experiments/d4_sweep_results.json): the 1/2-plateau
  suppression is ROBUST and strengthens with J (total extinction at
  K=1.4, J=1.2: 0 vs 51 grid hits); thirds suppressed likewise. The
  provisional odd/2N enhancement from the first run appears ONLY at
  the original parameter point (K=1.0, J=0.6) and is hereby retracted
  as a signature — single-point pattern-matching, caught by the sweep
  before hardening. X-2's Matsubara anchor demoted accordingly to
  "suggestive at one point, unsupported across the sweep."
- Open discriminator: grid-hit counting cannot distinguish plateau
  SHIFT (lattice offset — the bridge-relevant reading) from plateau
  SHRINKAGE (plain frustration). Step 3, edge-resolved staircases,
  decides it.
- Step 3 (edge-resolved plateaus, d4_edge_resolved.py, results in
  d4_edge_results.json): VERDICT — SHRINK, NOT SHIFT. Plateau centers
  are unmoved (1/2 center at 0.50000 control vs 0.49994/0.50008
  twisted, within averaging noise) and the locked rho on every
  measured twisted plateau equals p/q to <= 2e-4 (finite-averaging
  scale): widths shrink (1/2: x3.5 at K=1, x8.7 at K=1.4; thirds up
  to x27) but no lattice offset exists — the twist weakens temporal
  locking without displacing it. Combined with step 2: the temporal
  sector of this model class (N=4 pinned ring, single seam) shows NO
  parity-selective or shifted structure that could carry ANY
  fraction-parity rule. This leans T- for the 1D seam mechanism —
  honestly scoped: the conjecture concerns 2D pairs, so the 2D
  enumeration (D4 proper) remains the decisive test.
