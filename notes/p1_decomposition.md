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

## D4 proper (2D pair enumeration, d4_2d_pairs.py, 2026-08-21)

Design forced by E1: one autonomous flow has ONE rotation number, so
the honest 2D pair is (spatial parity class, temporal rational) with
b_x = x-winding parity around the orientation double loop and b_y =
uniform/staggered bond order. Cross-tab over 966 runs (two (K,J)
points, three seed branches, 161 Omega each):

    (bx,by)    n   q_odd  q_even   p_odd  p_even
    (0, 0)   147     124      23      86      61
    (0, 1)     1       1       0       0       1
    (1, 0)     4       2       2       2       2
    (1, 1)     1       1       0       1       0
    locked-but-defect (b_y undefined): 45

Findings, honestly stated:
1. Locking concentrates almost entirely in the spatially TRIVIAL
   sector (0,0) — which is an XOR-violating sector for gradients, but
   pinned locked states are not gradients; the gradient theorem does
   not constrain them. The XOR sectors (1,0) and (0,1) barely lock
   (n = 4 and 1): under pinning, winding sectors relax by phase
   slips (consistent with E1 step 1).
2. NO parity correlation between the spatial class and the parity of
   q (or p) of the locked rational is observable: the q_odd
   dominance in (0,0) mirrors the ordinary staircase composition
   (odd-q plateaus are wider), and the nontrivial cells have no
   statistics at all.
3. The sharpest reading is not under-determination but VACUOUS
   DOMAIN: in the corpus-canonical dynamics, no family of locked
   states indexed by arbitrary-denominator fraction PAIRS arises at
   all. Spatial windings live in (1/2)Z (theorem-let); temporal
   locking contributes one rational, parity-blind; nothing
   instantiates the (p1/q1, p2/q2) index set the conjectured rule
   quantifies over. A rule about states that do not exist is neither
   true nor false in the model - it is unfounded.

Limitations before any P-1 resolution is claimed: (a) the pinning
drive is an E1 addition; the corpus's own field equation used a
self-consistent mean field with no per-site pinning - the no-pinning
variant must be probed (expected: a single collective frequency and
NO rational structure at all, which would strengthen vacuity);
(b) nontrivial-sector statistics are near-zero - larger J or lattices
might stabilize winding sectors and deserve one check; (c) the D8
litcheck is still owed. Resolution shape if these hold: P-1 resolves
as expected (no canonical map), with the mechanism being domain
vacuity rather than map multiplicity - stronger than the
preregistered T- and requiring an honest R-entry saying so.

## D4 holes (a) and (b) — computed 2026-08-21

**(a) No-pinning variant (d4_nopin_meanfield.py, results in
d4_nopin_results.json).** Kuramoto lattice with quenched zero-mean
frequency offsets and no per-site drive, 4 x 4, twisted and control,
Delta in {0.05, 0.2}, 101 Omega each: max |rho - Omega| = 5.4e-14 over
all 404 runs. The "snaps" (7 per row against ~2.1 expected by chance)
are exactly the grid points where Omega itself is rational - not
plateaus. There is no mode-locking at all without a drive.

This is a theorem, not a finding (claim
klein-twisted-mean-frequency-identity, proven; fast check
scripts/verify/p1_mean_frequency.py): with antisymmetric coupling and
consistent seam offsets s_ab = -s_ba, each undirected edge contributes
sin(x) + sin(-x) = 0 to the sum of all phase advances, so the mean
advance per step is Omega + Delta*mean(G) = Omega identically, at every
step, regardless of the twist. The corpus's own no-drive field
equation therefore cannot produce any rational structure in Omega;
every temporal rational in this work enters via the pinning drive E1
added.

**(b) Nontrivial-sector stability (d4_sector_stability.py, results in
d4_sector_results.json).** XOR sectors seeded directly (uniform
half-integer x-winding -> (1,0); staggered -> (0,1)), J in {1.2, 2.0},
K = 1.0, 101 Omega per row:

    J    seed       retained  locked  locked&retained
    1.2  uniform       0/101    3       0
    1.2  staggered     4/101    5       0
    2.0  uniform       0/101    4       0
    2.0  staggered     6/101    4       0

Stronger coupling does not stabilize the sectors: the half-integer
winding sector is never retained, the staggered sector rarely, and no
run in any row both retains its sector and locks. The empty cells of
the D4-proper cross-tab are structural within the explored ranges.

## Resolution (draft against P-1; R-1 in PREDICTIONS.md)

Claim xor-bridge-domain-vacuity (proven, scoped to the explored K, J,
and 4 x 4 lattice for its driven leg; unconditional for its two
theorem-let legs): the corpus-canonical dynamics instantiates no
family of locked states indexed by fraction pairs with unbounded
denominators. The conjectured rule q1 + q2 odd is unfounded in the
model class - neither true nor false there. P-1's expectation (no
canonical map) holds; its predicted mechanism (map multiplicity, T-)
was wrong - the actual mechanism is domain vacuity. Recorded in R-1 as
a mechanism error. Canonicity criteria D5 are never reached: there is
no B-side object for Phi to land on.

Still owed before any novelty label: D8 litcheck (in progress, under
P-1). Not claimed: anything about other model classes (different
drives, larger lattices, continuum limits) - the vacuity statement is
bounded to what was computed, and the mean-frequency identity is the
only unconditional temporal result.

## D8 litcheck — LC-3 (2026-08-21)

Ring half-winding: classical (Bulaevskii 1977). Mean-frequency identity:
textbook (Kuramoto; Strogatz 2000; Acebron 2005). Both claims now carry
novelty = classical with citations. The 2D Klein enumeration was not
found in prior art and is labeled nothing: an elementary corollary.
E1's shrink-not-shift result is NOT labeled: adjacent 0-pi Josephson
literature (Frolov 2006; Lazarides 2008) reports the half-turn offset
CREATING half-integer steps under drive, the opposite sign - the
per-site-pinning vs bias-drive distinction and an N-parity check
(Lazarides predicts even/odd dependence; E1 ran N = 4 only) are owed
before the E1 observation can be claimed as more than a computation
in one model. The P-1 resolution does not depend on the sign of that
effect: vacuity rests on the theorem-lets plus the explored-range
cross-tab, and holds whichever way the plateaus move.
