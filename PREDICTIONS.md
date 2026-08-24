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

## R-4 — 2026-08-23 — resolves P-6
outcome: as expected. Exhaustive n <= 28: maximum density 2/3 (n =
22, 25, 28, contiguous S, q = 1); search to n = 64: 0.6744 (n = 44,
two-band S, q = 2); nothing above 0.6809; the maximum rises with n
toward the published value. All maximisers pass the independent
Jacobian check. Mind-change condition did not fire. Filed as the
verified claim circulant-twisted-max-density-small with an exhaustive
n <= 20 certificate (notes/p6_circulant.md). No contribution to the
open gap; a reproduction with tooling that now handles the object.

## P-8 — 2026-08-23 — the Gabor limit for mode-locking measurements
question: a rotation number measured over T iterations of the sine
circle map has resolution ~1/T, and near a plateau edge the orbit's
passage time diverges as pi/sqrt(mu) (claim saddle-node-passage-time).
A model-free measurement (grid scan + bisection of "|rho - p/q| < tol
over T iterations", the repo's own method in compendium C8/C9 and
notes/p1) therefore cannot distinguish a slowly drifting orbit from a
locked one when pi/sqrt(mu) > T. How does the measured plateau width
w(T) depend on T, and in which direction is the bias?
method: measure w(1/2), w(1/3) at K = 0.5 and K = 1 with T in {600,
1200, 2400, 4800, 9600} (transient T/4 excluded), tolerance fixed at
2e-5; fit w(T) = w_inf + c T^(-a).
expects: widths are OVERESTIMATED at finite T and converge from
above, with a ~ 2 (the saddle-node law: an orbit is misjudged locked
when mu < (pi/T)^2, so each edge is displaced outward by O(T^-2));
the residual bias at T = 9600 is below 1e-4 for the 1/2 plateau.
Secondary: the tongue CENTRE for q >= 3 is displaced from p/q by
O(K^2) (found while building the T1 notebook), so a bisection
started at p/q overstates q >= 3 widths by a factor that does NOT
vanish with T - a method bias, not a resolution bias.
changes-my-mind: widths converging from BELOW, or an exponent a ~ 1
(resolution-limited rather than passage-time-limited) robust across
K and plateau; either would mean the measurement error is not the
saddle-node mechanism.
not-claimed-in-advance: anything about model-based (fitted)
estimators, which can beat the model-free bound (Cramer-Rao).

## R-5 — 2026-08-23 — resolves P-8
outcome: as expected on the mechanism - fitted exponents 1.82, 2.00,
2.07, 2.06 (saddle-node T^-2, not resolution T^-1); convergence from
above in 3 of 4, the exception being the narrowest plateau at the
shortest T, where an unconverged transient near the edge
underestimates with the same scaling (recorded as a second mechanism,
not a refutation). Centre shift O(K^2) for q = 3 confirmed at two K.
Mind-change did not fire. Catalog c27 pins the data.

## P-9 — 2026-08-23 — N-parity of plateau shrinkage on the pinned twisted ring
question: LC-3 recorded that in driven 0-pi Josephson arrays the
half-turn offset CREATES half-integer steps with an even/odd-N
dependence (Lazarides, PRB 77, 214419 (2008)), opposite in sign to
E1's shrink-not-shift finding on the pinned circle-map ring, which
ran N = 4 only. Does the twisted ring's 1/2-plateau shrinkage (twisted
width / control width) depend on the parity of N?
method: E1's exact model (scripts/experiments/d4_edge_resolved.py:
per-site pinning K, sine coupling J, one pi seam), N = 4, 5, 6, 7, 8,
9 at (K, J) = (1.0, 0.6) and (1.4, 0.6); edge-resolved 1/2-plateau
widths for twisted and control; the ratio r(N) = w_twisted / w_control.
expects: NO parity alternation - r(N) varies smoothly (monotonically
or nearly) with N, because the drive here is per-site pinning to the
lab frame (Frenkel-Kontorova-like), not a bias coupling to phase
differences, and the pi offset relaxes to a uniform strain pi/N with
no kink/antikink selection; the sign discrepancy with the Josephson
literature is the drive type, as LC-3 proposed. Secondary: r(N) -> 1
as N grows (the seam's effect is diluted over more sites).
changes-my-mind: r(N) alternating with the parity of N by more than
the measurement resolution (~3% in width, P-8) at both (K, J), in the
same sense as Lazarides (even N more affected); that would mean the
ring does select kink configurations by parity and the E1 reading
must be redone with N-parity as a variable.
not-claimed-in-advance: anything about bias-driven arrays; the
absolute widths.

## R-6 — 2026-08-23 — resolves P-9
outcome: mixed, recorded as such. No even/odd alternation at either
coupling (mind-change did not fire; the LC-3 drive-type reading
stands). The secondary expectation r(N) -> 1 failed: shrinkage
saturates near 0.45 at K = 1.0 and is non-monotone at K = 1.4 with a
maximum at N = 7 - unexplained. Of record: E1's initial condition
theta_i = 0.13 i is not N-safe (it lands N >= 6 rings in winding
attractors, collapsing the control plateau); E1's N = 4 result is
unaffected; the method is corrected by attractor-controlled initial
conditions (notes/p9_nparity.md; catalog c28 pins the data).

## P-13 — 2026-08-24 — the acoustic metric and what it does not see, on a mass-spring chain
question: a chain of masses m(x) and springs J(x) is a substrate
carrying two independent local data: c(x) = sqrt(J/m) and Z(x) =
sqrt(mJ). The analogue-gravity reading (Unruh, PRL 46, 1351 (1981);
Barcelo, Liberati, Visser, Living Rev. Relativity 14, 3 (2011)) says
excitations propagate on the acoustic metric set by c(x) alone. Does
the counting observable "arrival time at each site" reproduce the
eikonal of that metric on the exact lattice (no continuum
approximation), and is the metric a complete summary of the
substrate - i.e. does anything measurable separate two chains with
identical c(x)?
method: Euler-Cromer integration of the chain m_i u_i'' =
J_i(u_{i+1}-u_i) + J_{i-1}(u_{i-1}-u_i), N = 1500, dt = 0.05, fixed
far end, half-sine displacement pulse (tau = 60) at site 0. Profiles
pinned in scripts/experiments/p13_profiles.py; every supporting
identity derived and machine-checked BEFORE this entry by the stdlib
symbolic layer (scripts/experiments/symb.py + p13_symbolic.py, EQ1-
EQ8 all passing; numbers pinned in p13_registration.json). Arrival =
time of peak |u_j| at checkpoints 200..1300; reflection = energy on
the launch side of a stated cut at a stated time over injected
energy. Nulls: control chain (flat metric); jz and zramp are the
scattering nulls for the impedance claim.
expects: (a) control (m = J = 1): fitted front speed within 0.5% of
c0 = 1 (EQ3); 0.1-threshold crossing spread grows as t^p with p in
[0.23, 0.43] (Airy precursor of the lattice front).
(b) ramp and lens: RMS relative deviation of peak arrival from the
discrete eikonal sum (EQ4, EQ5; time offset calibrated on the
control) below 2% over the checkpoints; the same statistic computed
against a block-shuffled profile's eikonal is larger by a factor of
at least 10.
(c) junction jc (c matched, Z jumps x4): measured energy reflection
within 0.05 of 0.360 (EQ6); junction jz (Z matched, c drops x4):
reflection below 0.01 (EQ6 lattice value 0.0014 at k = 0.05); smooth
zramp (Z = 1 while c halves): reflection below 0.01 AND its own
arrival eikonal still holding to 2%. Reading: arrival times measure
c(x) and are blind to Z(x); reflection measures Z(x) and is blind to
c(x); the metric is readable from the substrate and is not a
complete summary of it.
(d) halving dt moves every reported number by less than 0.2%.
changes-my-mind: zramp or jz reflection above 0.05 at converged dt
kills the metric/impedance split as stated; ramp RMS above 5% kills
the eikonal (geometric) reading of the chain at these scales; jc
reflection farther than 0.15 from 0.360 means the lattice matching
analysis (EQ6/EQ7) is wrong and the entry resolves against me.
not-claimed-in-advance: anything about Einstein equations or
dynamics of the metric (the einstein-from-kuramoto-chain-a
refutation stands); horizons or advection; dimensions above one;
quantum behaviour; real spacetime.

## R-8 — 2026-08-24 — resolves P-13
outcome: core as expected; two clauses failed as registered, both
diagnosed. Arrivals: RMS 0.31% / 0.32% / 0.30% (ramp / lens /
zramp) against 2% registered; shuffled substrate scores 85x / 16x
worse; control speed 0.99897. Scattering: jc 0.362 vs the impedance
law's 0.360; smooth Z-constant ramp 2e-4. changes-my-mind did not
fire. Failed as registered: (a2) front-width exponent 0.027 - the
half-sine pulse's intrinsic width dominates its dispersive
broadening; a labelled step-drive diagnostic gives 0.332, inside
the registered band; the observable was attached to the wrong
drive, and is not rescued. (c-jz) 0.036 against < 0.01: the
registered threshold came from the monochromatic lattice value,
but 2.9% of the pulse's flux lies above the slow side's band edge
omega_c = 0.5 and reflects regardless of impedance matching; the
flux-weighted exact lattice solve reproduces the measurement at 7%
with no free parameters (p13_jz_diagnosis.py). (d) max dt-halving
change 0.31% vs 0.2%; the culprit is zramp's RMS statistic, a
ratio of two ~3e-3 numbers - the clause was drafted over derived
statistics it should not have covered; every physical observable
moved by less. Filed as chain-arrivals-read-acoustic-metric and
junction-reflection-reads-impedance-not-metric.

## P-11 — 2026-08-24 — the representation decides the metric: Connes distance on cycles and circulants
question: the spectral distance d(p,q) = sup { f(q) - f(p) :
||[D, f]||_op <= 1 } (Connes 1994) turns algebra + Dirac + Hilbert
space into geometry with no paths anywhere in the definition. On
cycle graphs C_n with the incidence Dirac D = [[0, B^T], [B, 0]],
does the graph metric come back - and which piece of the spectral
triple decides? Two representations of the SAME algebra of vertex
functions: (A) f acts on l2(V) only, zero on l2(E); (B) f acts on
l2(V) and on l2(E) by source-pullback.
method: derivation layer scripts/experiments/p11_derive.py with
committed output p11_derive_out.txt (pre-registration): construction
A's commutator norm reduces to sqrt(lam_max(diag(f) L diag(f))), L
the cycle Laplacian, and construction B's to max_e |f(v) - f(u)|,
both checked to 1.75e-16 against explicitly built 2n x 2n
commutators; primal small-n table computed. Registered computation:
scripts/experiments/p11_spectral.py, stdlib, power iteration for
operator norms, BFS for hop distances.
expects: (a) construction B recovers hop distance EXACTLY on any
graph (the hop tent has commutator norm 1 and attains it; any
feasible f telescopes to <= d_hop): machine-checked on the three
P-6 maximiser circulants C_20({1..6}), C_22 (contiguous), C_44
(two-band, q = 2) - tent norm within 1e-9 of 1, and 200 random
feasible f per graph never exceed hop distance.
(b) construction A on cycles, n >= 4: d(0,1) = 2/sqrt(3) exactly -
upper bound from the 2x2 principal minor of the Gram matrix
(lam_max <= 1 forces f_1 - f_0 <= 2/sqrt(3) at the antisymmetric
point), lower bound from a primal witness, meeting within 1e-6;
every gauged feasible f has |g_i| <= 1/sqrt(2) + 1e-9 (diagonal
Rayleigh bound), hence diameter <= sqrt(2); a primal witness
reaches d(0, n/2) >= 1.40 for n in {8, 12, 16, 20}. The metric
saturates: nearest neighbours are resolved, everything farther
sits at ~sqrt(2).
(c) the dichotomy stands as registered: same algebra, same Dirac -
representation B returns the geodesic metric, representation A a
bounded one. The geometry is informed by how the algebra is
represented on H (how it couples), not by the graph alone.
changes-my-mind: a feasible construction-A f with f_1 - f_0 >
2/sqrt(3) + 1e-4 or any pair above sqrt(2) + 1e-4 (the minor and
diagonal bounds would be wrong, and (b) collapses); a random
feasible construction-B f exceeding hop distance by more than 1e-9
(the telescoping argument would be wrong, and (a) collapses).
not-claimed-in-advance: continuum limits; construction A beyond
cycles; other Dirac operators (the literature has many, with
different distances); anything about physical spacetime.

## R-9 — 2026-08-24 — resolves P-11
outcome: five of six clauses as expected; one failed as registered
and is diagnosed exactly. Construction A: both closed-form witnesses
carry Gram norm 1.0 to 1e-9 at every tested n - d(0,1) = 2/sqrt(3),
d(0,j>=2) = sqrt(2) - and the diagonal and minor caps held on every
random feasible f; the metric saturates as registered. Construction
B: no feasible f exceeded hop distance on any of the three
circulants (worst excess 0.0; the telescoping direction holds
everywhere), but the registered "tent norm = 1" holds only on the
cycle: on C_20({1..6}), C_22({1..7}) and C_44 (two-band) the tent's
norm is sqrt(6), sqrt(7), sqrt(15) = sqrt(in-degree), because the
B-rep commutator norm aggregates incoming gradients in l2. Exact
geodesic recovery is a property of in-degree-1 (chain-like) coupling
- the registration overgeneralized from the cycle derivation;
recorded, not rescued. The dichotomy survives with a sharpened
moral: one graph, three geometries, decided by the coupling. Filed
as connes-distance-representation-dichotomy.
