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
## P-10 — 2026-08-24 — dimension from pure order (Myrheim-Meyer)
question: a Poisson sprinkle into a causal interval of d-dimensional
Minkowski space retains only its order relation. Myrheim (CERN
TH-2538, 1978) and Meyer (MIT thesis, 1988): the related-pair
fraction f = E[R]/C(N,2) is a function of d alone, so inverting it
reads dimension off pure order (Sorkin's "order + number =
geometry"). Does the inversion recover d = 2, 3, 4 from finite
sprinkles, within bands derived before any sprinkle runs, and does
scrambling the order destroy the estimate?
method: null derived FIRST by direct integration
(scripts/experiments/p10_symbolic.py, output committed as
p10_symbolic_out.txt, same commit as this entry; EQ ids below are
its printed lines): f(1) = 1, f(2) = 1/2, f(3) = 8/35, f(4) = 1/10,
equal to twice the Gamma form Gamma(d+1)Gamma(d/2)/(4 Gamma(3d/2))
(EQ 11-14; the Gamma form as usually quoted is the ORDERED-pair
probability - a factor-2 convention, both appear in the literature;
E[R]/C(N,2) with R counting unordered related pairs is 2x it).
Estimator: d_hat = F^-1(R/C(N,2)) by bisection on the Gamma form
anchored at the integrals (EQ 15-18). Sprinkles: fixed seed
20260824, fixed-N accept-reject into the interval from a unit box;
the acceptance rate must match the derived volume fraction (EQ 1-3:
1/2, pi/12 = 0.2618, pi/24 = 0.1309) within 4 binomial sigma. Grid:
d in {2,3,4}, N = 2^7..2^13, M(N) = 40,40,40,40,24,16,12 sprinkles
per cell. Variance derived, not guessed: Var(R) = C(N,2) f(1-f) +
6 C(N,3) (E[g^2]-f^2), g = tau_p^d + tau_q^d, E[g^2] = 5/18 (d=2,
EQ 19), 0.0742857 (d=3, EQ 21), 1/50 (d=4, EQ 20); the binomial
term alone underestimates sigma_f by a factor growing from 5.4
(N=2^7) to 43 (N=2^13) - registered so the narrower band cannot be
substituted later. Bands (full BAND table in p10_symbolic_out.txt):
|mean_M d_hat - d| <= |bias| + 4 sigma_d / sqrt(M), sigma_d =
sigma_f/|F'|, delta-method bias (largest 0.018, at d=4 N=2^7);
e.g. 0.052 / 0.099 / 0.153 at N=2^7 and 0.011 / 0.021 / 0.031 at
N=2^13 for d = 2 / 3 / 4.
expects: (1) mean d_hat inside its band at all 21 (d, N) cells;
(2) sample SD inside [0.4, 2.2] x sigma_d at every cell - a
binomial-only sigma would sit outside this window at every N
(factor 5.4 at N=2^7 already), which is what the variance
derivation is for; (3) spread shrinks ~ N^(-1/2): per d, sample SD
at N=2^13 below that at N=2^7; the derived inversion bias (< 0.019
everywhere, decreasing in N) stays below the noise floor, so mean
errors are consistent with zero throughout. Secondary: RMS-across-d
of the mean error smaller at N=2^13 than at N=2^7 (noise risk ~1 in
10, registered as such). (4) mutant shuffled-order (random
permutation of the time coordinate across points, spatial parts
kept): mean d_hat lands near the derived scrambled nulls
d* = F^-1(f_shuf), f_shuf(3) = 0.2141 -> d* = 3.080, f_shuf(4) =
0.0824 -> d* = 4.230 (EQ 26-27), within 0.3 of d* (the mutant
spread is not derived); OUTSIDE every band for d = 4, and outside
every d = 3 band with N >= 2^8. Registered blind spots, derived in
advance, not post hoc: at (d=3, N=2^7) the derived displacement
0.080 is inside the 0.099 band, so that cell is uninformative for
the mutant; and at d = 2 order scrambling is undetectable in the
mean - permuting a lightcone coordinate is a distributional
symmetry of the 2d sprinkle (EQ 22), and permuting t leaves f
centred at 1/2 because the time and space marginals of the diamond
are the same triangle density (EQ 23-25) - so the d = 2 mutant
means stay INSIDE the band (variant shuffled-lightcone runs at
d = 2 to exhibit the symmetry).
changes-my-mind: a cell outside its band, or a sample SD outside
the [0.4, 2.2] window, means the closed form or the variance
derivation is wrong - diagnose which EQ fails before trusting
anything downstream. A d=3 (N >= 2^8) or d=4 mutant mean inside its
band means the estimator does not respond to order structure at the
registered resolution and the prediction fails as registered. A
d=2 mutant mean OUTSIDE its band refutes the derived symmetry
(EQ 22-25). No parameter moves after this entry; a failed band is
recorded, not rescued.
not-claimed-in-advance: curved spacetimes or any non-flat interval;
spectral or any other dimension estimator; non-integer d; Poisson-N
sprinkles (what runs is fixed-N binomial sampling); the d=2 mutant
beyond its mean; anything about our universe. Novelty status:
classical reproduction (Myrheim 1978; Meyer 1988; Sorkin).

## R-7 — 2026-08-24 — resolves P-10
outcome: as expected except one registered mutant cell; recorded as
such. Nulls: all 21 (d, N) cells inside their bands (largest mean
error +0.079 at d=4, N=2^7, band 0.153); sample SD inside 0.72-1.34
x the derived sigma_d at every cell (a binomial-only sigma would sit
at 1/5 to 1/43 of the observed spread - the derived shared-point
covariance term carries the variance); spreads shrink ~ N^(-1/2)
and the RMS mean error falls 0.049 -> 0.004 from N=2^7 to 2^13;
acceptance rates match the derived volume fractions everywhere.
Mutants: d=4 shuffled-order outside every band, means 4.22-4.32
against the derived scrambled null d* = 4.230; both d=2 shuffles
stay inside the band, as the registered symmetry derivation said
they must (EQ 22-25). The failure: (d=3, N=2^8) shuffled-order mean
3.051, band 0.068 - inside. Diagnosis, not rescue: the derived
displacement 0.080 clears that band by only 0.013 = 0.9 sigma of
the mutant mean at M=40, so the registered "outside every d=3 band
with N >= 2^8" ignored the mutant's own sampling noise - a
registration design error, same family as R-3's; the paired
mutant-minus-null difference at that cell is 0.073, consistent with
the derived 0.080, and the other six d=3 cells (including the
registered-uninformative N=2^7 one) fall outside. No parameter
moved after registration. Data: p10_results.json, seed 20260824;
note notes/p10_order_dimension.md.

## P-14 — 2026-08-24 — the commutator kernel is spectrally audible
question: P-13 showed the metric is a lossy summary of the substrate;
P-11 located the loss in the commutator with the algebra. Where does
the discarded data go? Claim to test: into the spectrum. Two chains
share the metric c(x) (P-13's ramp profile) and differ only in
impedance - ramp (Z = 1/c) and zramp (Z = 1): they should be
isometric in every commutator-visible sense yet NOT isospectral, and
the spectral difference should be EXACTLY the first-order shift of
the travel-time impedance potential, with zero free parameters.
method: derivation layer scripts/experiments/p14_derive.py (run
first, output committed): in travel-time coordinates the wave
equation takes Schrodinger form with V = (sqrt Z)''/sqrt Z; the CAS
(symb.py) checks that for c = 1 + bx, Z = 1/c this V is the CONSTANT
b^2/4 (EQ2), zramp has V = 0 identically (EQ3), and the k-resolved
first-order Dirichlet shifts have the closed form pinned in
p14_registration.json (EQ5): shift_k -> Vbar = V0 T_r/T =
3.416182e-08. Eigensolves: Sturm-sequence bisection on the
symmetrized tridiagonal (exact linear algebra, no timestep),
validated against the uniform chain's closed-form spectrum to 1e-12
(EQ6). Grids n = 1499 and 2999; lowest 80 eigenvalues each;
Richardson extrapolation in a^2 for the difference.
expects: (a) commutator isometry: the weighted seminorm end-to-end
distance agrees between ramp and zramp within 5e-3 relative,
shrinking with n (derived at registration: 1.18e-4 at n = 1499,
5.91e-5 at n = 2999, both converging to T = 2113.553233).
(b) the metric is the leading spectral data: for BOTH profiles,
|omega_k T/(k pi) - 1| < 2e-3 for k <= 60 at n = 2999 (Weyl).
(c) not isospectral: max_k |omega_k^2(ramp) - omega_k^2(zramp)| >
1e-9 (the derived signal is ~3.4e-8, the eigensolver resolves
~1e-12).
(d) the difference IS the impedance potential, k-resolved: after
Richardson extrapolation over the two grids, RMS over k in [5, 60]
of (Delta omega_k^2 - shift_k) is below 0.3 x Vbar, with shift_k
the pinned zero-free-parameter closed form.
changes-my-mind: mean Delta omega_k^2 with the wrong sign, or RMS
above 1.0 x Vbar at converged grids, kills the "loss goes to the
spectrum as the impedance potential" reading; a k-dependence
tracking the metric-split model 2 omega^2 (T_z - T_r)/T instead of
the flat shift_k means the isometry bookkeeping, not the physics,
made the difference.
not-claimed-in-advance: anything beyond first order in V; other
boundary conditions; dimensions above one; drums, manifolds, or
physical spacetime; isospectrality questions beyond this pair.

## R-10 — 2026-08-24 — resolves P-14
outcome: two of four clauses as expected; one failed where the
prediction's own effect exceeded the clause's tolerance; the
k-resolved clause failed and the mind-change condition FIRED.
(a) as registered (derived and pinned at registration). (b) failed
at k = 1-2 for the ramp: worst 3.0e-3 vs the 2e-3 tolerance - the
deviation IS the predicted V-shift, a 0.9% relative effect at
k = 1 that the clause's flat tolerance ignored; for k >= 5 both
profiles pass (worst 1.13e-3). (c) as registered: max
|Delta omega_k^2| = 2.31e-7 against an eigensolver resolving
1e-12 - same commutator data, different spectra. (d) NOT as
registered: RMS residual 2.89 x Vbar against 0.3 registered and
1.0 mind-change - fired, recorded, not rescued. Post-firing
diagnosis (labelled, computed): the window mean matches the
impedance potential at 0.9% (3.443e-8 vs 3.414e-8); the named
metric-split alternative is excluded, corr(residual, k^2) = 0.003;
the residual is a bounded sign-alternating oscillation consistent
with lattice scattering off the ramp profile's two derivative
discontinuities, which first-order continuum theory does not
model. The k-resolved zero-free-parameter reading is dead at these
grids; the honest retest is a C^2 ramp with no kinks, queued as an
open item and not run. Filed as isometric-not-isospectral-chain,
covering clauses (a) and (c) only - the mean-level agreement stays
a post-hoc observation in the note.
## P-15 — 2026-08-24 — the spectral-dimension instrument
question: spectral dimension d_s(t) = -2 dlnP/dlnt (P the mean
return probability of the Laplacian walk) is the counting observable
behind the quantum-gravity "dimensional flow" literature (CDT:
Ambjorn, Jurkiewicz, Loll, PRL 95, 171301 (2005); asymptotic safety:
Lauscher, Reuter; reviews: Carlip, CQG 34, 193001 (2017)) and is
also, by Weyl, the spectrum's leading metric data. Can the repo
carry a general instrument for it whose every anchor is exact, and
does the instrument inherit the P-13/P-14 lossiness structure -
blind to impedance at leading order, sensitive at second order as a
derived trace effect?
method: derivation layer scripts/experiments/p15_derive.py (run
first, all EQ green, output committed): d_s computed as the EXACT
log-derivative of exact eigen-sums, no fitting; anchors pinned in
p15_registration.json - the line curve at five t values (two
independent routes, eigen-sum vs Bessel continued fraction, agreeing
to 1.1e-14), the 1/t coefficient 0.1255, product additivity, the
window rule t < 0.5/lambda_1 with the exact two-mode decay past it,
and the dense-circulant crossover (peak d_s = 2.95 at t = 0.2,
plateau 1.0 by t = 80). Registered computation
scripts/experiments/p15_specdim.py: a fresh implementation plus a
Monte Carlo walker route and the P-14 chains via Sturm spectra
(lowest 250 modes, truncation bounded).
expects: (a) the fresh implementation reproduces every pinned
anchor within 1e-9. (b) the continuous-time walker Monte Carlo
(400k walkers, binomial error derived) lands within 4 sigma of the
exact P(t) at t = 0.2, 1.0, 5.0 on C_4096({1..6}) - the stochastic
tier that later runs on objects with no computable spectrum.
(c) chains: over t in [100, 1000] (within the k <= 250 truncation
window), |d_s^ramp(t) - d_s^zramp(t)| < 1e-3: the instrument is
blind at leading order to the impedance split that P-14 proved
present in the spectrum. (d) the second-order sensitivity is the
derived trace drift: Delta d_s(t) lies within a factor of 2 of
2 Vbar t (Vbar = 3.416e-8 from P-14's registration) for t in
[300, 1000] - the P-14 kink oscillations should average out in the
trace as they did in the window mean.
changes-my-mind: an anchor missed at 1e-6 kills the instrument;
the chain identity broken above 1e-3 in-window falsifies "d_s is
metric-level data" as stated; Delta d_s with the wrong sign or
outside a factor of 5 of 2 Vbar t kills the trace-drift reading
and sends the kink question back ahead of any C^2 retest.
not-claimed-in-advance: causal sets and their definitional
disagreement (that is P-16, not this line); any continuum limit;
Monte Carlo precision beyond its derived bands; anything about
physical spacetime.

## R-11 — 2026-08-24 — resolves P-15
outcome: all four clauses as expected; the mind-change did not
fire. (a) fresh implementation reproduces every pinned anchor with
zero measured deviation. (b) the walker Monte Carlo lands at 0.02,
0.25, 0.04 sigma from the exact P(t) at the three registered
t-values. (c) leading-order blindness: max |Delta d_s| = 6.93e-5
over t in [100, 1000] against the 1e-3 tolerance - the instrument
does not see the impedance split that P-14 proved present in the
same spectra. (d) the second-order trace drift: Delta d_s /
(2 Vbar t) = 1.008 - 1.015 across the whole [300, 1000] window,
inside the registered factor-2 band with 1.5% to spare - the P-14
kink oscillations average out in the trace, and the trace-level
form of "the loss goes to the spectrum as the impedance potential"
holds as registered where the k-resolved form (R-10) fired. Filed
as spectral-dimension-instrument. The causal-set definitional
disagreement remains P-16, not started.

## P-17 — 2026-08-24 — the Bell ladder: expansion is cheap, contraction is a theorem
question: the 2022 Nobel experiments (Aspect, Clauser, Zeilinger)
honour a theorem about mechanical models. How sophisticated can an
honest mechanical model be? Design principle: it is easier to expand
than contract. Expanding the correlation set is one purchasable
resource per rung, priced exactly; contracting it back down is where
the theorems live, and the only known principled contraction lands
exactly on the quantum boundary.
method: derivation layer scripts/experiments/p17_derive.py (run
first, EQ1-EQ8 all green, output committed; pins in
p17_registration.json): the local ceiling 2 by exhaustive
enumeration of all 16 deterministic strategies; mixtures buy nothing
(linearity); the quantum ceiling 2 sqrt 2 from Landau's identity
S^2 = 4I - [A0,A1]x[B0,B1] (entrywise to 8.9e-16) with norm and
singlet expectation both 2 sqrt 2 to 1e-12; the rotor LHV's zigzag
E = 2 theta/pi - 1 saturating S = 2 at the same angles where the
cosine reaches 2 sqrt 2; one blunt bit giving deterministic S = 4;
the detection rung's two sphere identities (E[(b.l) sign(a.l)] =
cos/2, E|b.l| = 1/2) giving post-selected E = -cos exactly at mean
efficiency 3/4, below the Garg-Mermin threshold 2/(1+sqrt 2) =
0.8284; van Dam's collapse (n-bit inner product from one bit with
PR boxes, exhaustive at n = 8); the information-causality ladder
f(E,k) = 2^k(1 - h((1+E^k)/2)) bounded below 1 at E = 1/sqrt 2
(max 0.7982 at k = 1, decreasing to 1/(2 ln 2) = 0.7213), crossing
1 at k = 8 for E = 0.73, exploding as 2^k at the PR box.
Registered computation scripts/experiments/p17_bell.py: the Monte
Carlo tiers, 1e6 pairs each, seed 20260824, angles 0.4, 1.1, 2.0,
2.8, binomial error bands derived.
expects: (a) the rotor machine's simulated E lands within 4 sigma
of the zigzag at every registered angle and its CHSH at the pinned
angles within 4 sigma of exactly 2. (b) the Toner-Bacon protocol
(shared lambda1, lambda2 on the sphere; one bit c = sign(a.l1)
sign(a.l2); Bob outputs sign(b.(l1 + c l2))) reproduces E = -cos
theta within 4 sigma at every registered angle - one bit buys the
exact singlet curve (Toner, Bacon, PRL 91, 187904 (2003)). (c) the
detection machine's post-selected correlations land within 4 sigma
of -cos theta AND its measured Bob efficiency within 4 sigma of
1/2 (mean 3/4) - a mechanical fake of the quantum curve, priced at
25% of the detections, legal only below the 0.8284 threshold the
loophole-free 2015 experiments enforced. (d) catalog c32: the
measured history - AGR 1982 S = 2.697 +/- 0.015 sits 46 sigma
above the local ceiling and at 95.4% of Tsirelson; FC 1972 delta =
0.050 +/- 0.008 sits 6 sigma above its bound (litcheck LC-10) -
self-tests with a mutant asserting local compatibility.
changes-my-mind: any MC tier off its exact curve by more than 4
sigma at converged sample size (the constructions would be wrong,
not the statistics); the Toner-Bacon simulation NOT matching -cos
would falsify the priced-expansion reading of the one-bit rung.
not-claimed-in-advance: anything about why nature stops at
Tsirelson beyond what information causality states for this slice
(the full quantum boundary needs the NPA hierarchy, not attempted);
loophole-free experimental analysis; memory-loophole finite
statistics; interpretations of quantum mechanics.

## R-12 — 2026-08-24 — resolves P-17
outcome: all clauses as expected; the mind-change did not fire;
worst Monte Carlo deviation 1.41 sigma over twelve million pairs.
(a) the rotor machine rides the zigzag at every registered angle
and its CHSH lands at 2.00050 (0.29 sigma from its exact ceiling).
(b) Toner-Bacon: one shared-randomness bit reproduces -cos theta
at every angle (worst 0.91 sigma) - the one-bit rung is priced and
paid. (c) the detection machine fakes the quantum curve at
eta_B = 0.500 within 1.2 sigma everywhere - mean efficiency 3/4,
legal only below the 0.8284 threshold that the loophole-free 2015
experiments enforced. (d) c32 self-tests: AGR 1982 sits 46.5 sigma
above the exhaustively-derived local ceiling and at 95.35% of
Tsirelson; FC 1972 at 6.25 sigma. The ladder stands as registered:
expansion is one purchasable resource per rung (0 bits -> 2; one
blunt bit -> 4; one clever bit -> the exact singlet; a quarter of
the detections -> a fake 2 sqrt 2), the expansion extreme collapses
communication complexity (van Dam, exhaustive at n = 8), and the
one principled contraction - information causality - is bounded
below 1 exactly at Tsirelson and broken everywhere above it. Filed
as bell-ladder-priced.

## P-18 — 2026-08-25 — the C2 retest of the fired clause (A-6)
question: P-14's k-resolved zero-free-parameter clause d died at RMS
2.89 x Vbar and the recorded diagnosis blamed the linear ramp's C1
corners (where c' jumps, the travel-time potential has distributional
spikes; corr(residual, k^2) = 0.003 excluded the metric-split
alternative). That diagnosis is itself a claim and stays a story
until tested. If the corners are the culprit, replacing the ramp with
a C2 profile must recover the first-order shifts with no parameters.
method: derivation layer scripts/experiments/p18_derive.py (run
first, output committed): quintic smoothstep c(x) = 1 - 0.5 s(u),
s = 6u^5 - 15u^4 + 10u^3 over the same [150, 1350]; the CAS checks
the general closed form V = c'^2/4 - c c''/2 for Z = 1/c (EQ1), the
linear limit b^2/4 recovering P-14 (EQ2), that s' = s'' = 0 at both
ends so V is globally continuous and vanishes at the ramp edges (EQ3),
the boundary-term identity int V dtau = int c'^2/(4c) dx that fails
for C1 corners (EQ5), and the Fourier decay of shift_k - Vbar_s that
only a continuous V produces (EQ8). Pinned before any eigensolve:
T = 2160.746347, Vbar_s = 4.720552e-08, and the 80 k-resolved shifts
including the derived SIGN FLIP shift_1 = -7.999903e-08 (the linear
case had no such structure). Eigensolves: same Sturm bisection
(validated to 1e-12, EQ7), grids n = 1499 and 2999, lowest 80
eigenvalues, Richardson extrapolation in a^2, sramp (Z = 1/c) minus
szramp (Z = 1) with the C2 profile; the P-14 linear pair rerun on the
same grids as a positive control.
expects: (a) Weyl over k in [5, 60] at n = 2999 for both C2 profiles:
|omega_k T/(k pi) - 1| < 2e-3 (k = 1..4 excluded by the recorded
P-14 clause-b lesson: the shift itself is a percent-scale relative
effect at the lowest modes). (b) not isospectral: max_k
|Delta omega_k^2| > 1e-9. (c) k-resolved match: RMS over k in [5, 60]
of (Richardson Delta omega_k^2 - shift_k) below 0.3 x Vbar_s - the
SAME bar clause d originally registered and failed. (d) the derived
sign flip: Richardson Delta omega_1^2 < -4e-8. (e) window mean within
3 percent of the mean pinned shift. (f) positive control: the linear
pair on the same grids reproduces the failure, RMS > 2.0 x Vbar_lin,
and the improvement factor (linear RMS/Vbar_lin) / (C2 RMS/Vbar_s)
exceeds 5.
changes-my-mind: C2 RMS above 1.0 x Vbar_s at converged grids kills
the corner diagnosis (the kink story was a rescue, and R-10's honest
reading becomes "first-order perturbation fails on this substrate
class"); linear control RMS below 1.5 x Vbar_lin means R-10's own
measurement does not reproduce and P-14's resolution needs reopening;
measured Delta omega_1^2 > 0 kills the derived sign structure and
with it the V = c'^2/4 - c c''/2 reading of the spectral difference.
not-claimed-in-advance: higher order in V; other boundary conditions
or profiles; dimensions above one; any mechanism story for the
C1 residual beyond its absence here; continuum limits beyond the two
registered grids.

## R-13 — 2026-08-25 — resolves P-18
outcome: all six clauses as registered; the mind-change did not
fire. (a) Weyl holds for both C2 profiles over k in [5, 60], worst
below 2e-3. (b) max |Delta omega_k^2| = 1.3e-7 against a solver
resolving 1e-12. (c) the per-mode zero-parameter match: RMS over
k in [5, 60] of (Richardson Delta omega_k^2 - shift_k) = 0.004 x
Vbar_s against the 0.3 bar that P-14's clause d registered and
failed - the same first-order theory, on a substrate with no
corners, lands at half a percent of the potential scale. (d) the
derived sign flip at k = 1 is in the data: Delta omega_1^2 =
-1.04e-7 (pinned -8.00e-8; the 2.4e-8 excess is second-order
territory at the lowest mode, outside the window and not claimed).
(e) window mean 4.6709e-8 vs pinned 4.6620e-8, 0.19 percent apart.
(f) the positive control reproduces R-10's failure on the same
grids: linear RMS = 2.893 x Vbar_lin (R-10 recorded 2.89);
improvement factor 756. Reading: P-14's fired clause was the C1
corners, not the first-order theory - the corner diagnosis
survives its registered test. A-6 closes. Filed as
c2-profile-recovers-first-order-shifts.

## P-21 — 2026-08-26 — Hardy's maximum is the fifth power of the golden mean
question: Hardy's nonlocality paradox (Hardy, PRL 71, 1665 (1993);
Mermin, Am. J. Phys. 62, 880 (1994)): two qubits, local projective
binary measurements A0/A1 and B0/B1, three zero-constraints
P(A0+,B0+) = 0, P(A1+,B0-) = 0, P(A0-,B1+) = 0, and the paradox
event p_Hardy = P(A1+,B1+), which every local hidden-variable model
obeying the constraints sends to zero. What is the maximum of
p_Hardy over all two-qubit pure states and measurement choices, and
does it land on the pinned (5 sqrt 5 - 11)/2 = phi^5 - the one
golden-mean physics number that survived the Otto mechanization
(notes/otto25_mechanization.md, A-9) as a theorem rather than a fit?
method: derivation layer scripts/experiments/p21_derive.py (run
first, output committed): real Schmidt form psi = c|00> + s|11>,
k = c/s; the LHV exhaustion over all 16 deterministic assignments
(EQ1); the three constraints eliminated analytically into tangents
(a, -k/a, -k^2/a, ka), CAS-checked to kill all three amplitudes
(EQ2); the reduced p_Hardy in closed form (EQ3); the measurement
freedom minimized EXACTLY via the square identity D - (1+k^3)^2 =
k^2(a - k/a)^2 (EQ4); the envelope p_env(k) = k^2(1-k)^2 /
((1+k^2)(1-k+k^2)^2) with its k <-> 1/k tie (EQ5); stationarity
polynomial k^5 - 2k^4 - 2k + 1 (EQ6), factored over the integers
(EQ7), collapsed in y = k + 1/k to y^2 - 3y + 1 = 0 (EQ8-EQ9); the
maximum (y-2)/(y(y-1)^2) at y* = (3+sqrt5)/2 computed in exact
Q(sqrt5) arithmetic (EQ10-EQ11) with the optimal Schmidt structure
c s = phi^2, {c^2, s^2} = (1 -+ sqrt(6 sqrt5 - 13))/2 (EQ12), and
the vanishing maximally-entangled slice (EQ13). Everything pinned
in p21_registration.json BEFORE the second route runs. Route 2,
scripts/experiments/p21_hardy.py: blind seeded multi-start
Nelder-Mead (implemented in-repo, stdlib) over the FULL 5-parameter
space (Schmidt angle + 4 measurement angles), 200 starts, seed
20260826, maximizing p_Hardy - lambda * sum of squared constraint
probabilities on the registered schedule lambda = 1e3, 1e5, 1e7,
1e9, then polished with constraints eliminated (envelope in k,
golden-section to 1e-12).
expects: (a) the blind search's polished global maximum lands
within 1e-9 of the pinned (5 sqrt 5 - 11)/2 = 0.090169943749...;
(b) the optimizer's canonicalized Schmidt weights land within 1e-6
of the pinned golden values (1 -+ sqrt(6 sqrt5 - 13))/2 =
{0.177351636840, 0.822648363160}; (c) the maximally-entangled
slice - the constraint-eliminated p(k = 1, a) over the registered
grid and polish - stays below 1e-12.
changes-my-mind: a blind-search maximum exceeding the pinned phi^5
by more than 1e-9 (the classical result or the constraint algebra
is wrong - record, do not rescue); a maximum found below
phi^5 - 1e-6 after the registered 200 starts (optimizer
inadequacy - record as method failure, not physics).
not-claimed-in-advance: more than two qubits or two settings per
side; POVMs beyond projective measurements; the Hardy ladder
generalizations; any connection between phi here and phi numerology
elsewhere - notes/otto25_mechanization.md records why that
separation matters, and this line exists to isolate the ONE
theorem-grade golden number.

## R-16 — 2026-08-26 — resolves P-21
outcome: all three clauses as registered; neither mind-change fired.
(a) the blind search's polished maximum lands at 0.090169943749474,
within 2.4e-16 of the pinned (5 sqrt 5 - 11)/2 = phi^5 (bar 1e-9).
(b) the optimizer's canonicalized Schmidt weights land at
0.177351636381 / 0.822648363619, within 4.6e-10 of the pinned
golden values (1 -+ sqrt(6 sqrt5 - 13))/2 (bar 1e-6); found
k = 0.464312612477 against the pinned 0.464312613208 (the envelope
is quadratically flat at its top, so the 7.3e-10 offset in k costs
nothing in p). (c) the maximally-entangled slice tops out at
1.2e-32 over the registered grid and polish (bar 1e-12) - Hardy's
paradox vanishes on the maximally entangled state, as derived in
EQ13 before the search ran. Search behavior: 200/200 starts reach
the global basin; the best penalized-stage point sits ABOVE the
pinned maximum by 3.3e-4 at worst constraint probability 1.7e-7 -
the standard penalty-method infeasibility offset of order
C^2/(4 lambda), removed by the registered constraint-eliminated
polish; no feasible exceedance of phi^5 anywhere in the run. Filed
as hardy-maximum-is-phi-fifth.
## P-22 — 2026-08-26 — locked references: the Adler skeleton of squeezed-light stabilization
question: PRB 111, 184519 (Danner, Hoehe, Padurariu, Ankerhold,
Kubala 2025) stabilizes dc-biased Josephson-photonic squeezed
microwaves by injecting a weak reference, names the Adler/Kuramoto
class as the universal frame (their ref [52] is Adler 1946), and
states the striking feature that the squeezed state locks to a
reference at TWICE the emission frequency. Claim to test on the
named model class: the two-photon locking equation dtheta/dt =
delta - eps sin(2 theta) + noise shares the fundamental's Arnold
tongue exactly, carries TWO locked phases pi apart, hops between
them at a rate derived in advance from first-passage quadrature,
and the mod-pi phase observable survives the hopping that scrambles
the bare phase - the classical skeleton of "locking preserves
squeezing".
method: derivation layer scripts/experiments/p22_derive.py (run
first, output committed): beat-period closed form checked by
quadrature (EQ1), fixed-point count and pi-separation by CAS
stability signs (EQ2), the phi = 2 theta reduction to Adler (EQ3),
the constant-flux Fokker-Planck mobility v(delta, eps, D) in
log-domain quadrature validated on four exact limits including
sqrt(delta^2 - eps^2) at D -> 0 (EQ4), the von Mises locked
variance with asymptote D/(2 eps) (EQ5), the pi-hop rate from
exact MFPT double quadrature with the Kramers form (eps/pi)
exp(-eps/D) recovered at small D (EQ6), and simulation tolerance
bands DERIVED from hop-count Poisson budgets and a dt-halving
bias estimate rather than chosen (EQ7). Registered computation:
seeded Euler-Maruyama at dt = 0.002, pinned seeds, pinned grids
(p22_registration.json).
expects: (a) deterministic tongue: at eps = 1, measured beat
frequency lands on sqrt(delta^2 - 1) within 2e-3 relative for
delta in {1.05, 1.2, 1.5, 2.0} and no phase slip over the full run
for delta in {0.2, 0.6, 0.9}, in BOTH scenarios (the two-photon
case after theta -> 2 theta). (b) noisy mobility: on the six
pinned (delta, eps, D) cells the simulated drift lands within 4
percent of the pinned quadrature values. (c) locked variance
(two-photon, delta = 0): within 5 percent of the pinned von Mises
quadrature on the D-ladder {0.05, 0.1, 0.2, 0.4}. (d) pi-hops
(two-photon, delta = 0): measured hop rate within the derived
Poisson band of the pinned MFPT rate at D in {0.2, 0.25, 0.3},
and at least 98 percent of hops have size pi, not 2 pi. (e) the
protected observable: at (eps, D) = (1, 0.25), long-run
|<cos 2 theta>| > 0.8 while |<cos theta>| < 0.2 - the mod-pi
alignment survives hopping that scrambles the bare phase.
changes-my-mind: simulated mobility off the quadrature by more
than twice the band at converged dt kills the constant-flux FPE
construction as implemented; a tongue edge scaling differently
from eps or a beat exponent differing from 1/2 kills the Adler
reduction; pi-hops scrambling cos 2 theta (clause e failing) kills
the mod-pi protection reading and with it the classical-skeleton
account of why locking preserves squeezing.
not-claimed-in-advance: anything quantum - squeezing spectra,
entanglement measures, photon statistics, the paper's specific
device coefficients or cavity parameters; multi-mode dynamics;
mutual synchronization; the direct-cavity-injection scenario;
dimensional units.

## P-22a — 2026-08-26 — pre-computation amendment to P-22 clause (b)
Before any registered simulation ran, a feasibility check of clause
(b) against its own estimator noise showed the flat 4-percent
relative band is unachievable on five of the six pinned cells: the
winding estimator has standard deviation sqrt(2 D / (T M)) that
exceeds the band wherever the drift is small, and the delta = 0
cell gets a band of width zero. EQ7 budgeted hop counts but not the
mobility estimator - a registration design error, corrected here
rather than discovered post hoc. Clause (b) as amended: each cell
is measured as the mean winding rate over M = 12 independent seeded
runs of length T = 3000, and must land within
max(0.04 |v_pin|, 3 sqrt(2 D/(T M))) of the pinned quadrature
value; the delta = 0 cell must satisfy |v| < 3 sqrt(2 D/(T M)).
Everything else in P-22 stands unchanged. Ancestry: this amendment
precedes the registered computation commit.

## R-17 — 2026-08-26 — resolves P-22 (mind-change FIRED on two clauses)
outcome: the quantitative heart held; two clauses failed as
registered and the mind-change condition fired - recorded, then
diagnosed with labels, not rescued.
(b) as amended by P-22a, all six mobility cells: worst case
0.9_1.0_0.25 at 0.38735 vs pinned 0.37400 (inside the derived
band); the noise-activated deep-tongue cell lands 0.04578 vs
0.04778 and the delta = 0 cell at -0.0012 against a 3-sigma bound
of 0.0032. The constant-flux FPE construction is quantitatively
confirmed by simulation across activated, marginal, and running
regimes. (c) all four variance cells inside 5 percent of the von
Mises quadrature. (d) all three hop cells: rates 0.00204/0.00484/
0.00984 vs pinned 0.00188/0.00496/0.00940 inside the Poisson
bands, and the committed-hop size distribution is PURE pi - 1337
hops observed across cells, zero 2 pi events. Two locked phases pi
apart, hopping at the first-passage rate: the Z2 skeleton stands.
(a) FAILED as registered at the two tongue-edge cells only
(delta = 1.05, both scenarios): residuals -3.7e-3 and -2.4e-3
against the 2e-3 band, while all twelve other cells pass at 2e-5
to 3e-4. Post-firing diagnosis (labelled): the winding count over
a finite run is quantized, bounding the velocity estimator by
2 pi/T = 3.1e-3 absolute - larger than the band exactly at the
edge where the beat is slow. EQ7 budgeted hop counts and dt bias
but not winding quantization: a registration design error of the
same class P-22a caught for clause (b), this one not caught in
time. The beat law itself shows no deviation beyond the estimator
bound.
(e) FAILED as registered: measured <cos 2 theta> = 0.6971 against
the registered threshold 0.8, with |<cos theta>| = 0.035 and 399
hops. Post-firing diagnosis (labelled): the registered 0.8 was an
UNDERIVED threshold - the stationary von Mises density fixes the
equilibrium value exactly at I1(kappa)/I0(kappa) with kappa =
eps/(2D) = 2, i.e. 0.69777, and the measurement sits 9e-4 from it.
The observable did precisely what the stationary theory says; the
clause died because the registration asked for more alignment than
the equilibrium possesses. The protection reading is therefore NOT
claimed from P-22; it is re-registered properly as P-23 with the
Bessel-ratio value derived in advance and fresh seeds.

## P-23 — 2026-08-26 — the protection clause, derived this time
question: R-17 killed P-22's clause (e) because the registered
threshold 0.8 was underived taste; the measured mod-pi alignment
landed 9e-4 from the von Mises equilibrium I1(2)/I0(2) = 0.69777
that COULD have been derived in advance. Does the protection
statement hold when registered properly: the mod-pi observable
sits at its derived Bessel-ratio equilibrium on a D-ladder while
the bare phase averages to its derived value of zero, on fresh
seeds the diagnosis never touched?
method: derivation layer scripts/experiments/p23_derive.py (run
first, committed): <cos 2 theta> = I1(kappa)/I0(kappa) with
kappa = eps/(2D), computed two independent ways - the P-15
continued-fraction instrument and direct von Mises quadrature,
agreeing to 1e-12 (EQ1); <cos theta> = 0 exactly by symmetry
(EQ2); per-cell durations sized so each ensemble member expects
more than 50 committed pi-hops (EQ3). Registered computation:
M = 8 fresh-seeded Euler-Maruyama members per cell, dt = 0.002,
cells (eps, D) = (1, 0.2), (1, 0.25), (1, 0.3).
expects: per cell, the ensemble mean of <cos 2 theta> lands
within 4 SEM of the pinned Bessel ratio (0.75823 / 0.69777 /
0.64686 as pinned in p23_registration.json) with SEM below 0.01;
the ensemble mean of <cos theta> satisfies |mean| < 4 SEM; every
member logs at least 50 committed hops.
changes-my-mind: a cell mean outside 4 SEM of its pinned ratio
kills the stationary von Mises account of the locked two-photon
phase; |<cos theta>| exceeding its band with hops present kills
the symmetry argument and with it the mod-pi protection reading -
this time with the equilibrium derived, there is nothing left to
blame on the registration.
not-claimed-in-advance: same exclusions as P-22; additionally no
claim about relaxation TIMES (only stationary averages), and no
quantum statement.

## P-23a — 2026-08-26 — transcription correction, before any run
The P-23 expects: prose quoted the pins as "0.75823 / 0.69777 /
0.64686"; the derivation layer's actual pinned values, committed in
the same commit and produced by EQ1's two agreeing routes, are
0.76500 / 0.69777 / 0.63472 (kappa = 2.5, 2, 5/3). The prose
numbers at the first and third cells were hand-transcription
errors; p23_registration.json governs, as the entry itself states.
Recorded before the registered computation ran.

## R-18 — 2026-08-26 — resolves P-23
outcome: all cells as registered; the mind-change did not fire.
Ensemble means of <cos 2 theta> against the derived Bessel-ratio
pins on fresh seeds: D = 0.2: 0.76437 +/- 0.00135 vs 0.76500
(0.47 SEM); D = 0.25: 0.69819 +/- 0.00170 vs 0.69777 (0.24 SEM);
D = 0.3: 0.63334 +/- 0.00112 vs 0.63472 (1.23 SEM). The bare-phase
means sit inside their 4-SEM bands around the derived zero
(worst 2.7 SEM at D = 0.3) with every member logging at least 84,
84, 150 committed pi-hops respectively. The protection statement
that died in R-17 under an underived threshold holds when the
threshold is the derived equilibrium: the mod-pi observable sits
on I1(eps/2D)/I0(eps/2D) while hopping scrambles the bare phase to
its derived null. Filed as locking-protects-mod-pi-observable;
the P-22 core is filed separately as two-photon-locking-z2-skeleton.

## R-18a — 2026-08-26 — transcription correction to R-18
The D = 0.2 row in R-18 was transcribed from memory instead of from
the committed output: the correct figures are 0.76468 +/- 0.00045
vs pin 0.76500 (0.70 SEM), and the per-cell minimum committed hop
counts are 65 / 84 / 150, not 84 / 84 / 150. Every clause verdict
is unchanged (the corrected row passes more comfortably than the
mistyped one); p23_results.json is authoritative. Two transcription
slips in one line (P-23a, this) are a process signal: ledger numbers
must be pasted from the artifact, never retyped - recorded here so
the habit has a name and a cost.

## P-24 — 2026-08-26 — the memory hierarchy: how substrates forget
question: from a computational standpoint the fundamental objects
in this repo's verified stock are not bits but the dynamical and
topological structures bits are read off from. Claim to test: three
classical substrates - an untended phase, a locked phase (the P-22
Z2 doublet as a bit), and a winding number on an N-ring - hold one
piece of information with lifetimes whose FORMS are derivable in
advance: exponential-of-nothing (1/D), exponential-of-a-barrier
(Kramers, barrier = eps exactly), and exponential-of-a-barrier that
grows with N only until it saturates at 2K, with an N-fold
nucleation penalty - so classical 1D topology buys NO extensive
protection, and the lifetime ordering between rings of different
sizes INVERTS at a derived noise crossover. A chat-level guess that
the topological barrier scales extensively with N died in the
derivation layer before this registration (EQ5); what is registered
is the closed form that killed it.
method: derivation layer scripts/experiments/p24_derive.py (run
first, committed): rung-1 exact decay e^{-Dt} by CAS eigenfunction
identity (EQ1); rung-2 telegraph autocorrelation e^{-2rt} with
r from exact MFPT quadrature and barrier = eps by CAS (EQ2);
rung-3 saddle in CLOSED FORM - clamp one bond, the relaxed rest is
uniform (verified by numeric relaxation), saddle at Delta* =
pi(N-3)/(N-2), barrier Delta_E(N) = E(Delta*) - N K(1-cos(2pi/N))
(EQ3); the full Langer rate with derived prefactor - both Hessians
from the closed-form configurations, cyclic-Jacobi eigenvalues,
global-rotation zero mode dropped from both determinants, unstable
curvature, times N nucleation sites (EQ4); the saturation
Delta_E -> 2K and the size-ordering crossover (EQ5); Poisson/CLT
bands and event budgets > 60 per cell (EQ6). All pins in
p24_registration.json. Registered simulations: seeded
Euler-Maruyama / Langevin at the pinned dt, seeds, grids.
expects: (a) rung 1: ensemble <cos theta> at the four pinned times
lands inside its derived CLT band around e^{-Dt} at D = 0.5,
M = 4000 walkers. (b) rung 2: committed-telegraph hop counts at
D = 0.22 and 0.28 inside Poisson bands of the pinned MFPT rates,
and the two-point Arrhenius slope reproduces the CAS barrier
inside the propagated band. (c) rung 3, five (N, D) cells:
measured committed slip rates inside |ln r_meas - ln r_Langer| <
2/sqrt(N_events) + 0.7 (absolute, finite-barrier allowance
declared); the two same-D ratio clauses (16 vs 8 at D = 0.16,
32 vs 16 at D = 0.30) inside 0.35 nat + Poisson of the derived
ratios; slip purity: at least 98 percent of committed winding
changes are single steps. (d) the crossover: the measured
lifetime ORDER between N = 8 and N = 32 at D = 0.16 (32 wins)
agrees in SIGN with the derived 128x, tested at the same seeds
budget - and the derived inversion at D = 0.6 is recorded as a
pinned prediction for the figure, not simulated to convergence
(budget declared).
changes-my-mind: any rung-3 cell off the Langer rate by more than
a factor e^{0.7} at converged dt kills the derived-prefactor
account; a ratio clause failing kills the N-scaling law
(nucleation x N against saturating barrier); slip purity below 98
percent kills the single-slip picture; rung-2 Arrhenius missing
the CAS barrier kills the Kramers reading of the locked bit.
not-claimed-in-advance: quantum or 2D substrates; extensivity
statements beyond this ring class; optimized/engineered
protection (error correction); any Landauer/work accounting
(a later line); electron clouds (out of scope for this classical
line - declared per request).

## P-24a — 2026-08-26 — two protocol corrections before any run
Caught at feasibility review, before the registered computation ran:
(i) clause (d) as worded names N = 32 at D = 0.16, a cell whose
event budget (about 1e6 time units) is outside the registered T3
table; the order test is hereby the two BUDGETED cells N = 8 vs
N = 16 at D = 0.16, whose derived lifetime ratio from the pinned
Langer rates is 23.6; the N = 32 and D = 0.6 entries stay derived-
only pins for the figure, as the entry already declared for D=0.6.
(ii) clause (c)'s implied free-running slip count would spend most
of the run in the w = 0 sector, whose slip barrier (approaching 2K)
exceeds the w = 1 escape barrier that the pinned Langer rates
price; the registered protocol is therefore escape-from-w-equals-1
with reset: start at the uniform twist, integrate to the first
committed winding change, record the escape time and size, reset,
repeat within the same T3 budget. This is the quantity Langer
computes. Overwind escapes (w: 1 to 2) are counted but derived
negligible (barrier about 3.7 at N = 16). Ancestry: this amendment
precedes the computation commit.

## R-19 — 2026-08-26 — resolves P-24
outcome: all four clauses as registered (protocol per P-24a);
the mind-change did not fire. Numbers pasted from
p24_results.json by script, per the R-18a rule.
(a) rung 1, M = 4000 walkers at D = 0.5: t=0.5: 0.7762 vs 0.7788, t=1.0: 0.5989 vs 0.6065, t=2.0: 0.3598 vs 0.3679, t=4.0: 0.1082 vs 0.1353 - every point
inside its CLT band around the CAS-derived e^(-Dt).
(b) rung 2: D=0.22: 185 hops vs 181 predicted, D=0.28: 476 hops vs 469 predicted; two-point Arrhenius slope 0.970
against the quadrature pin 0.976 and the CAS barrier
1 (band 0.245).
(c) rung 3, escape-from-w=1 with reset: 8_0.16: 114 escapes, rate 0.04560 vs Langer 0.04686 (0.027 nat, purity 1.000); 16_0.16: 107 escapes, rate 0.00238 vs Langer 0.00199 (0.180 nat, purity 1.000); 16_0.24: 163 escapes, rate 0.02329 vs Langer 0.02105 (0.101 nat, purity 1.000); 16_0.3: 147 escapes, rate 0.04900 vs Langer 0.05412 (0.099 nat, purity 1.000); 32_0.3: 160 escapes, rate 0.03200 vs Langer 0.03355 (0.047 nat, purity 0.994). Both ratio
clauses inside their bands: ratio_16_0.16_over_8_0.16: -2.954 vs -3.161 (band 0.731); ratio_32_0.3_over_16_0.3: -0.426 vs -0.478 (band 0.673). Every committed escape but one
was a single winding step.
(d) the order clause: tau16/tau8 measured 19.2 against the
derived 23.6 at D = 0.16 - size helps exactly as the
saturating-barrier law says, and the derived inversion at D = 0.6
(ratio 0.87) stands as a pinned prediction on the figure
page. Reading: the memory hierarchy is derived physics end to end -
the untended phase forgets at 1/D, the locked bit at the exact
MFPT with barrier eps, and the 1D winding number at the Langer
rate under a barrier that saturates at 2K: no extensive
topological protection, a closed-form crossover instead. Filed as
memory-hierarchy-of-substrates; figure page p24_plots.html.

## P-7 — 2026-08-27 — the golden flux ladder (the number reserved since A-1, now worded)
question: the VOCABULARY phi taxonomy admits phi as ADDRESS (the
most-irrational winding) and refuses it as a fitted constant; ln phi
was filed as UNEARNED - no artifact computes an entropy/growth edge.
This line is the queued door: Harper / almost-Mathieu at critical
coupling on the Fibonacci-approximant fluxes F_m/F_{m+1} -> 1/phi.
Claim to test: the total bandwidth S(q) contracts per ladder step at
the rate ln phi - earned as CLOCK (the Fibonacci ratio) times
FLATNESS (Thouless's plateau q S(q) -> 32 G/pi, G Catalan's
constant, IMPORTED not derived) - while the exact anchors, the gap
parity rule, and the plateau approach hold as registered. phi
remains the address; the plateau constant is Catalan's, not phi's -
the taxonomy's shape, now computed.
method: derivation layer scripts/experiments/p7_derive.py (run
first, committed): q = 2 closed form by CAS Bloch determinant -
bands +-[0, 2 sqrt 2] touching at the c25 pi-flux Dirac point (the
interop edge); q = 3 exact via the CAS transfer trace tr M +
2 cos 3 theta = E^3 - 6E and integer factorizations of D = -+4;
the Bloch construction (q x q, corner +-1, k2 in {0, pi/q}, bands =
consecutive sorted edge pairs, cyclic Jacobi) validated against
both anchors to 1e-10; Catalan's G from its own accelerated series
(two depths to 1e-13) giving the imported plateau 32 G/pi =
9.3299489290 (LC-14); the gap parity rule verified at the anchors;
the small-q trend q S(q) = 11.3137 / 8.7846 / 9.2171 / 9.6168 at
q = 2, 3, 5, 8 pinned, from which the clause bands derive.
Registered computation: the ladder (8,13), (13,21), (21,34),
(34,55), (55,89), (89,144), same construction, Jacobi residual
guard 1e-8.
expects: (a) the ladder code reproduces the q = 2, 3 anchors to
1e-10. (b) parity rule along the ladder: odd q - all q-1 gaps
open (> 1e-8); even q - the central gap closed (< 1e-8), all
others open. (c) plateau: the mean of q S(q) over the terminal
even/odd pair (55/89 and 89/144) lands within 0.25 of 9.3299489.
(d) the ln phi clock: |ln(S(89)/S(144)) - ln phi| < 0.05, with
ln phi = 0.4812118 - the edge that moves ln phi from unearned to
earned in the symbol graph.
changes-my-mind: plateau off by more than 0.9 kills either the
Thouless import or the construction (the anchors decide which);
clock slope off by more than 0.15 kills the clock reading; a
closed gap at odd q or an open central gap at even q kills the
parity rule and with it the band-counting; a Jacobi residual above
1e-8 voids the affected cell rather than the clause (declared).
not-claimed-in-advance: the Cantor structure of the irrational
limit (Ten Martini - imported literature, not computed); the
Thouless limit itself (imported; only the APPROACH is measured);
Chern labels; lambda away from 1; theta-averages beyond the two
Chambers extremes; any dimensionful statement.

## R-20 — 2026-08-27 — resolves P-7
outcome: all four clauses as registered; the mind-change did not
fire. Numbers pasted from p7_results.json by script (R-18a rule).
(a) anchors reproduced by the ladder code (S at q = 2, 3 within
1e-10 of the CAS closed forms 4 sqrt 2 and 4 sqrt 3 - 4).
(b) parity along the ladder, all cells (Jacobi residuals below
1e-12): q=13: qS = 9.2509, min gap 1.62e-02; q=21: qS = 9.3199, min gap 3.05e-03; q=34: qS = 9.3608, min gap 5.15e-15; q=55: qS = 9.3208, min gap 3.33e-04; q=89: qS = 9.3290, min gap 6.49e-05; q=144: qS = 9.3330, min gap 1.48e-14 - the even-q central gaps close to 1e-14, every
odd-q gap stays open.
(c) plateau: terminal-pair mean 9.3310 against the imported
32 G/pi = 9.3299 - deviation +0.0011 against the
registered 0.25: the plateau is Catalan's to four digits.
(d) the ln phi clock: ln(S(89)/S(144)) = 0.48075 against
ln phi = 0.48121, deviation -4.6e-04 against the registered
0.05. The edge is earned: ln phi enters the symbol graph as the
Fibonacci-approximant clock of the critical Harper bandwidth -
clock (the F ratio) times flatness (the imported Thouless
plateau). phi stays the address; the plateau constant is
Catalan's, not phi's - the taxonomy's shape, now computed. A-1
closes. Filed as harper-golden-ladder; figure page
p7_plots.html.
## P-19 — 2026-08-25 — the ALF period lattice
question: anomalous-low-frequency (ALF) locks on a bowed string are
conventionally read as exact pitch halving - period 2.000 T0, an
integer subharmonic. Do the locks instead sit on the two-generator
period lattice P(m, beta) = T0*(1 + m*(1-beta)) + eps, with bow
position beta a live control knob and every lock strictly off
2.000 T0?
method: a four-ingredient digital-waveguide bowed string (two
travelling-wave delay loops joined at the bow point, DC-lossless
one-pole reflection filters at nut and bridge, a damped torsional
pair, exact per-sample stick-slip against a falling friction curve
with one-pole contact smoothing; steel G, f0 = 196.9 Hz, L = 325 mm,
the arXiv:2502.11902 string), run at the m=1 lock for beta = 0.10,
0.13, 0.16 plus the m=2 lock at beta = 0.13; observable one is
slip-onset interval clustering (dominant cluster = the lock), and an
independent miniature at half the sample rate measures observable
two, bridge-waveform autocorrelation, with per-beta force selected
only by lock quality over a band that contains 2.0 T0.
expects: on the four-ingredient bowed-string waveguide (origin:
harmonics archive session 2026-08-24/25, commits e045ab8..105cd3c),
the in-repo experiment and an independent miniature (half the sample
rate, a different observable - bridge-waveform autocorrelation vs
slip-onset clustering - and per-beta force selected only by lock
quality over a band that contains 2.0 T0) both find the m=1
anomalous-low-frequency lock at T0*(2 - beta) + eps with eps in
[0.03, 0.07] T0: slope dP/dbeta within [-1.35, -0.65] T0, every lock
at least 0.04 T0 away from 2.000 T0, m-spacing (1-beta)*T0 within
0.03. The subsequent litcheck is expected to find Guettler's wave
analysis contains the extra-rounds mechanism and possibly the period
formula (then the lattice labels classical-with-citation), but not
the dP/dbeta slope discriminator or a bow-position pitch protocol.
changes-my-mind: a lock within measurement jitter of 2.000 T0 at any
bow position, or a slope consistent with 0, kills the lattice
reading and vindicates the halving reading of arXiv:2502.11902. On
the instrument side (future claim, not this one): an audio
measurement showing ALF pitch independent of bow position (period
ratio 1.000 +/- 0.010 between beta = 0.10 and 0.16, where the
lattice predicts 1.033) does the same.
not-claimed-in-advance: real-string behavior (this is an in-model
line; the audio protocol above is future work, not this claim); the
torsional trigger family and which perturbation starts an ALF
episode; any decomposition of the eps offset into mechanisms; other
strings, tunings, or bow models; anything beyond the four-ingredient
model.

## R-14 — 2026-08-26 — resolves P-19
outcome: every clause as registered; the mind-change did not fire.
The m=1 locks measure 1.9413/1.9036/1.8811 T0 at beta = 0.10/0.13/
0.16 (cluster jitter <= 0.0011) and the m=2 lock at beta = 0.13
measures 2.7950 T0; eps = P - T0*(1 + m*(1-beta)) lands at 0.041/
0.034/0.041/0.055 T0, all inside the registered [0.03, 0.07]. Slope
dP/dbeta = -1.004 T0 in the experiment and -0.926 T0 in the
half-rate autocorrelation miniature (miniature residuals 0.036-
0.041), both inside the registered [-1.35, -0.65]. Every lock sits
at least 0.0587 T0 from 2.000 T0 against the registered floor of
0.04. The m-spacing lands at 0.891 T0 against the lattice's 0.87,
off by 0.021 against the registered 0.03. No lock within jitter of
2.000 T0 at any bow position and no slope consistent with 0, so the
mind-change clause stayed quiet. The litcheck expectation resolved
as registered too: LC-11 finds Guettler's extra-rounds mechanism is
prior art (two trigger families, transverse and torsional), the
period-formula question stays open behind the CASJ paywall, and
neither the dP/dbeta discriminator nor a bow-position pitch
protocol appears in any accessible source. Filed as
alf-period-lattice.
lineage: this line was first registered as P-18 on branch
alf-lattice (commit 98c33f3, 2026-08-25), before its computation
commit as the gate requires; it was renumbered to P-19 at the
rebuild because main's P-18 slot had meanwhile gone to the C2
retest. The question, method, and not-claimed-in-advance fields
were added at the rebuild; the expects and changes-my-mind text is
verbatim from the original registration.

## P-20 — 2026-08-26 — the eps budget and the frame-separability map
question: the alf-period-lattice claim carries a scope sentence
asserting that eps - the lattice offset, measured 0.034-0.055 T0 -
is "slip-episode duration plus reflection-filter group delay". That
was asserted, never computed. Does a zero-parameter budget
eps_pred = (one-pole filter delays on the trigger path) +
(delay-line rounding) + (measured mean slipping samples per cycle)
actually reproduce eps cell by cell? And where, in (beta, fps), does
single-interval frame counting separate the lattice from exact
doubling - the boundary behind the session observation that 3000 fps
frame histograms split 29 vs 30-31 at beta = 0.154?
method: derivation layer scripts/experiments/p20_derive.py (run
first, output p20_registration.json committed with this entry): the
CAS checks the one-pole DC phase delay a/(1-a) (EQ1-EQ2), a live run
of the recursion reproduces it (EQ4), and the stuck-bow junction
algebra (EQ3) shows one extra nut-side round trip passes the nut
one-pole plus the contact one-pole (3.000 samples) while the base
loop passes bridge plus nut one-poles (3.000 samples); delay-line
rounding is computed per cell from d_b, d_n. The slip term S is to
be MEASURED as slip-flag sample counts per lock cycle - an
observable independent of the period offsets - by
scripts/experiments/p20_eps_budget.py instrumenting the p19 model
across the P-19 RUNS grid plus the Kawano beta = 50/325 cell (that
cell's lock 1.8887 T0, force plateau [0.90, 1.15], and 29-vs-30/31
frame histograms are session-known anchors from 2026-08-25, inputs
here and not predictions). Frame histograms are simulated at 3000
fps from the same deterministic runs, against a synthetic
exact-doubling comparator quantized identically.
expects: (a) per cell, |eps_meas - eps_pred| <= 0.015 T0 with
nothing tuned - equivalently, given the committed eps values, the
measured S must land at 12.61/8.71/12.63/14.99/13.03 samples in the
five cells (beta 0.10/0.13/0.16 m=1, beta 0.13 m=2, Kawano m=1) to
within the band - and eps_pred reproduces the sign of eps variation
between adjacent m=1 grid betas (the fixed filter+rounding part is
nearly flat, so the budget says the beta-to-beta wiggle of eps
lives in the slip term). (b) within each committed m=1 force
plateau, eps_meas ranges less than 0.016 T0 across the registered
ladder (from the committed force-scan drift bound), and between
ladder endpoints S moves in the same direction as eps_meas whenever
|delta eps_meas| > 0.002 T0. (c) the separability map: D =
(beta - eps/T0)*fps/f0 frames; single-interval separation needs
D >= 1, i.e. beta >= f0/fps + eps/T0 = 0.10675 at 3000 fps, f0 =
196.9, grid-median eps; with a registered margin of 0.02 in beta,
cells at beta = 0.13, 0.16, and 50/325 show ZERO frame-histogram
overlap with the doubling comparator and the beta = 0.10 cell
(D = 0.894 < 1) shows overlap. All bands, ladders, cell partitions,
and the S targets are pinned in p20_registration.json before any
slip duration or histogram is computed.
changes-my-mind: any cell with |eps_meas - eps_pred| > 0.030 T0
(double the band) kills the claimed eps decomposition - the
alf-period-lattice scope sentence then needs a DECLINED-style
correction recorded in the R entry, not a rescue. A histogram
overlap in a cell whose derived separation is >= 1.5 frames (beta =
0.16 and the Kawano cell) kills the separability arithmetic.
not-claimed-in-advance: real strings; the torsional trigger family;
frame rates other than 3000 fps; force dependence beyond the
committed plateaus; other strings, tunings, or bow models; any
mechanism story for WHY the slip episode lasts as long as it does.

## R-15 — 2026-08-26 — resolves P-20
outcome: the eps budget is dead as registered; the separability map
held in three of four cells. Clause by clause, from committed
p20_results.json:
(a) FAILED, every cell, and the mind-change FIRED. The measured slip
term is one episode per cycle (1.01 episodes/cycle in all five
cells) lasting 50.9/62.0/75.4/61.9/73.7 samples - a few samples
above beta*loop (44.8/58.2/71.7/58.2/68.9), i.e. the slip episode is
the Helmholtz-style flyback, whose duration scales with the
BRIDGE-side transit, not the 12.61/8.71/12.63/14.99/13.03 samples
the additive budget required. eps_pred lands at 0.127-0.181 T0
against eps_meas 0.034-0.055; residuals -0.085 to -0.140 T0, all
outside the 0.015 band, worst 0.140 = 4.7x the 0.030 mind-change
line. The adjacent-beta sign clause also failed (0.10 -> 0.13:
eps_meas falls, eps_pred rises). The claimed decomposition of the
alf-period-lattice scope sentence - eps as "slip-episode duration
plus reflection-filter group delay" - is hereby recorded as WRONG in
its additive reading: the slip episode is 3-5x longer than all of
eps, so eps cannot contain it as a term. What survives unclaimed:
the fixed filter+rounding part (5.79-9.64 samples) is smaller than
every eps_meas (15.1-24.6 samples), so filter delay alone
under-explains eps and the remainder is an emergent property of the
locked orbit, not a sum of transit-time corrections. The correction
stands in this entry per the registration (record, not rescue); the
lattice claim's measured content (locks, slope, spacing) is
untouched.
(b) FAILED overall. Ranges: 0.0182/0.0079/0.0045 T0 at beta
0.10/0.13/0.16 against the 0.016 bound - the 0.10 failure traces to
a registration design error: the registered ladder point F = 1.20
sits in a HOLE of the committed plateau (the force scan classifies
it m=None, std 0.0395), so the range there compared a non-locked
point; the two clean plateaus sit inside the bound. The direction
sub-clause OPPOSES at 0.10 and 0.13 (S falls as force rises while
eps_meas rises) and tracks only at 0.16 - consistent with (a): the
slip term does not carry eps's force dependence either.
(c) HELD in three of four cells: beta 0.10 (D = 0.894 < 1) shows
the registered overlap (lattice frames {29: 42, 30: 58} vs doubling
{30, 31}); beta 0.16 and the Kawano beta = 50/325 cell show zero
overlap as registered (28/29 vs 30/31 - the session's 29-vs-30/31
observation reproduced from the registered protocol). beta 0.13
FAILED the zero-overlap clause: 2 of 103 intervals quantize to
frame 30 (support {28, 29, 30} vs {30, 31}) at derived separation
D = 1.469 frames - below the 1.5-frame mind-change line, which did
NOT fire. Diagnosis: D >= 1 plus a 0.02 beta margin does not
guarantee empty support intersection when the lattice period sits
essentially on an integer frame count (29.004 frames at beta 0.13);
the honest boundary statement is D >= 1 plus distance of P*fps from
the nearest shared integer, and at 3000 fps the certified-separable
region of the tested grid is beta >= 0.154 (Kawano) and 0.16, with
0.13 separable in 101 of 103 intervals but not certified.
No claim is filed from P-20 (the registration's condition for
filing was the eps clauses holding; they did not). The frame map
and the flyback finding stay available for a future registered
line; the diagnosis above is recorded as diagnosis, not as claimed
science.

## P-16 — 2026-08-27 — the two spectral dimensions of a causal set (the reserved number, worded)
question: the literature disagrees with itself about the small-scale
spectral dimension of causal sets: Eichhorn-Mizera (CQG 31, 125007)
walk a random walker on the sprinkled causet's undirected Hasse
graph and find d_s INCREASING at short scales, while Belenchia-
Benincasa-Marciano-Modesto (PRD 93, 044017) take the heat kernel of
the regularised nonlocal d'Alembertian and find universal reduction
to 2 - and BBMM's own conclusion names the gap ("might be a hint of
a universal description which interpolates"). Claim to test: on the
SAME substrate family, both definitions computed side by side
diverge at short scale in DIRECTION (walk to 0 through a growing
superdiffusive peak; d'Alembertian to 2) and in REFINEMENT trend
(the walk peak grows with N; the continuum curve is N-independent)
- the disagreement is definitional and computable, and no winner is
crowned.
method: derivation layer scripts/experiments/p16_derive.py (run
first, committed): K0 to 1e-10; the d = 2 minimal operator taken
from the SOURCE closed form (Aslanbeigi-Saravani-Sorkin JHEP 1406,
024 eq. 5: g = -Z e^{Z/2} E2(Z/2)) with exact IR/UV asymptotics
-z and -2 + 8/z - 48/z^2, after the derive layer caught that
BBMM's printed eq. (15) fails its own IR limit by exactly
4/sqrt(pi) - 2 = 0.256758 (psi-sum derivation, numerically
confirmed to 1e-6; recorded as LC-15 - their numerics evidently
used the correct source operator, since our source-operator curve
reproduces their Fig. 2: maximum 2.260 at s = 1.34, slow
approach to 2 from above). Heat-kernel instrument d_s(s) =
-2s<g_reg>_P exact to 1.2e-7 against finite differences; the
unregularised identity d_s = 4 rho s (their eq. 14) reproduced at
1.000 with a deep cutoff. Walk side: sprinklings into the unit
causal square (lightcone coordinates, seeded), Hasse links by
bitset interval-emptiness, links null pinned by EXACT quadrature
E[links] = N(N-1) int (1-a)(1-b)(1-ab)^{N-2}; both walk
instruments (continuous-time 2t<lambda>_P and even-step discrete
from the same normalized-Laplacian spectrum, cyclic Jacobi)
anchored on the cycle graph at d_s = 1. Registered ensembles:
N in {64, 128, 256}, three seeds each, seed0 160016.
expects: (a) measured link counts inside 6 sigma-heuristic of the
exact quadrature pins (180.3 / 444.7 / 1060.5) at every cell.
(b) walk superdiffusion on our sprinklings - the EM signature:
window-peak d_s above 2.15 at every N >= 128, and the seed-mean
peak grows from N = 64 to N = 256 by more than 0.10.
(c) instrument agreement: even-step and continuous-time walk d_s
within 0.15 at the window centre, every cell.
(d) the divergence, as derived at EQ7: walk d_s at the lattice
scale falls below 1 while the d'Alembertian curve stays within 0.1
of 2 as s -> 0; the walk peak is N-dependent while the continuum
curve is N-independent by construction. Both curves published side
by side; neither crowned.
changes-my-mind: no superdiffusive peak (walk d_s never above 2.15
at N = 256) kills the EM reproduction and the nonlocality account
(the link-count null decides whether the substrate or the
instrument failed); a peak SHRINKING with N kills the
refinement-trend reading; the d'Alembertian curve missing its own
derived limits kills the quadrature and voids clause (d);
instrument disagreement beyond 0.15 kills the transfer of P-15's
tool to irregular graphs and voids clause (b) rather than the
physics.
not-claimed-in-advance: which definition is the right one (the
registered output is the divergence, not a verdict); dimensions
above 2; curved sprinklings; the meeting-probability causal d_s;
BBMM's d = 3, 4 curves; Chern or continuum limits of the walk;
any claim that the interpolation BBMM speculate about exists.

## R-21 — 2026-08-27 — resolves P-16 (mind-change FIRED on the instrument clause)
outcome: the three physics clauses held; the instrument-agreement
clause failed as registered and the mind-change fired - recorded,
diagnosed with a labeled computation, not rescued. Numbers pasted
from p16_results.json by script.
(a) every cell inside the quadrature band: N64_r0: links 192 (pin 180.3); N64_r1: links 157 (pin 180.3); N64_r2: links 177 (pin 180.3); N128_r0: links 458 (pin 444.7); N128_r1: links 438 (pin 444.7); N128_r2: links 419 (pin 444.7); N256_r0: links 1092 (pin 1060.5); N256_r1: links 1068 (pin 1060.5); N256_r2: links 1063 (pin 1060.5).
(b) the EM signature on our own sprinklings: seed-mean window
peaks 2.664 / 3.222 / 3.687 at N = 64/128/256 -
growth 1.023 against the registered 0.10 floor. The walk
spectral dimension INCREASES with refinement, far above 2, exactly
as Eichhorn-Mizera report and as the ln N degree growth predicts.
(d) the divergence as derived at EQ7: walk d_s at the lattice
scale peaks at 0.198 (all cells below 1) while the
d'Alembertian curve sits at 2.031 at its smallest s - opposite
directions, neither crowned.
(c) FAILED as registered: continuous-time vs even-step values
differed by up to 2.9. Post-firing diagnosis (labeled, computed on
a fresh N = 96 graph): the CLAUSE compared the instruments at
different diffusion scales - ct at t = 0.2/lambda_1 (about 0.5)
against disc at the floor n = 4. At MATCHED scales, ct(t = n) vs
disc(n) agree to 0.08/0.09/0.04/0.01 at n = 8/12/16/24, with the
n = 4 residual 0.60 identified as Poisson smearing (the exact
identity e^{-t lambda} = e^{-t} sum t^k (1-lambda)^k / k! makes
ct a Poisson-mean-n mixture of disc powers; spread sqrt(n) across
the curve's steepest region). A registration design error of the
P-22a class, not caught pre-run this time; the matched-clock
clause is re-registered properly as P-25 on fresh seeds. The
physics claims are filed on clauses (a), (b), (d) only.

## P-25 — 2026-08-27 — the matched clocks
question: R-21's fired clause compared the two walk instruments at
mismatched diffusion scales. Registered properly: with the clocks
matched (continuous time t evaluated AT the step count n), do the
continuous-time and even-step spectral-dimension readings of the
SAME sprinkled causet agree within a band DERIVED from the exact
Poissonization identity - so that P-15's instrument transfers to
irregular graphs with its error budget known rather than assumed?
method: derivation layer inside scripts/experiments/p25_clocks.py
(derive block runs and prints before the fresh-seed ensembles):
the identity e^{-t lambda} = e^{-t} sum_k t^k (1 - lambda)^k / k!
checked per-eigenvalue on a concrete spectrum (exact algebra), so
Tr e^{-tL} at t = n is the Poisson-mean-n mixture of even/odd step
returns; the agreement band at each n is the derived smearing
bound band(n) = n |D2(n)| / 2 + 0.06, with D2 the second central
difference of ln Pbar in step count computed from the measured
spectrum itself (fit-free), plus the small odd-step contribution.
Cells: fresh seeds (seed0 251251), N in {64, 128}, two seeds each,
n in {4, 6, 8, 12, 16, 24}.
expects: for every cell and every n, |ds_ct(t = n) - ds_disc(n)|
inside band(n); and the large-n tail (n >= 16) inside 0.06
absolute.
changes-my-mind: any cell violating its derived band by more than
a factor 2 kills the Poissonization account of the residual and
with it the claim that the two clocks measure one object; a tail
violation kills the instrument transfer outright.
not-claimed-in-advance: anything about which clock is preferable;
lazy or weighted walks; scales below n = 4 (the smearing bound is
the statement there, not agreement).

## R-22 — 2026-08-27 — resolves P-25 (mind-change FIRED; the line stops here)
outcome: both clauses failed as registered and the mind-change
fired - the second consecutive firing on instrument agreement,
which is itself the finding. Numbers pasted by script.
(bands/tail) N64_r0: worst 0.274 vs band 0.160, tail 0.274/0.087; N64_r1: worst 0.547 vs band 0.350, tail 0.200/0.052; N128_r0: worst 0.592 vs band 0.397, tail 0.076/0.061; N128_r1: worst 0.536 vs band 0.408, tail 0.110/0.061 - three of four cells
exceed the 0.06 tail bound at n = 16.
Post-firing diagnosis (labeled, computed): the derived band
carried only the Poisson-smearing term; the omitted contribution
is PARITY. Hasse graphs are triangle-free and near-bipartite (the
mu-spectrum of the N = 128 cell is +--symmetric to 0.043), so
odd-step returns are suppressed - measured odd/even ratios 0.195
at n = 5 recovering to 0.996 at n = 23 - and the Poisson mixture
(all k) systematically differs from the even-step clock by a
cell-dependent amount of exactly the size that fired the bands.
Decision: no third registration. Two firings establish the honest
result - on sprinkled causal sets at accessible N, the walk
spectral dimension is PROTOCOL-DEPENDENT even within the walk
definition (clock choice and parity handling), which sharpens
P-16's thesis: the short-scale d_s of a causal set is a
convention-laden quantity, and cross-paper disagreement is the
expected condition, not an anomaly. The P-16 claim is filed on
its physics clauses only; the clock non-identity is recorded here
as a negative result with its mechanism demonstrated.

## P-26 — 2026-08-28 — the everpresent-Lambda scorecard on DESI DR2 BAO
question: catalog c31 records that Sorkin's causal-set mechanism
lands within 0.4 orders of magnitude of the observed Lambda, and
DESI DR2 now prefers evolving dark energy over LCDM (contested;
LC-16). Scored in the bit accounting on the one likelihood this
repo can recompute honestly — the DR2 Table 4 BAO Gaussian
compression — does the concrete everpresent-Lambda dynamics
(Das-Nasiri-Yazdi Model 1, the Zwane-Afshordi-Sorkin lineage) buy
more surprisal than it spends in seed and grid selection, or does
it price out the way its own SNe record (16 winning seeds of
90000) suggests?
method: derivation layer scripts/experiments/p26_derive.py runs
first and pins scripts/experiments/p26_registration.json: the
past-lightcone 4-volume closed forms V = (3 pi/55) t^4 (matter) and
(8 pi/105) t^4 (radiation) by Beta-function integrals, the exact
dimensionless walk amplitude sigma_OmegaLambda = 2 sqrt(165 pi)
alpha (matter era) and (8/3) sqrt(210 pi) alpha (radiation era),
the bit identities bits = dchi2/(2 ln 2) and the 2-dof sigma<->dchi2
map validated against DESI's own published -12.5, distance anchors
(EdS closed forms; the w0wa rho_DE closed form vs quadrature), and
the closed-form profile-out of the single scale s = c/(H0 r_d).
Data: Table 4 of arXiv 2503.14738v3, machine-parsed (13 points:
BGS D_V plus six tracer 2x2 (D_M, D_H) blocks with their printed
correlations; LRG3/ELG1 rows excluded per the table's own caption).
Experiment scripts/experiments/p26_score.py: (1) LCDM fit (Omega_m
free, s profiled in closed form); (2) w0waCDM fit under the DESI
priors w0 in [-3, 1], wa in [-3, 2]; (3) Model 1 ensemble — the
DNY update S -> S + (8 pi/3) alpha xi sqrt(dV) on S = rho_Lambda V
in 8 pi G/3 = 1 units, V by the incremental eta-moment accumulator,
self-consistent Friedmann marching on 512 log-a steps from
a = 1e-5, Omega_r = Omega_m/3400 convention, per-realization s
profiled (this absorbs each realization's early history into r_d —
generous to the model, so the bit price charged is a lower bound);
cells and seeds exactly as pinned in the registration JSON
(seed0 262626: alpha in {0.005, 0.01, 0.02, 0.04} at
Omega_m = 0.2975 with 20000 seeds each; Omega_m in {0.25, 0.35} at
alpha = 0.02 with 5000 each; realizations with H^2 <= 0 before
a = 1 are dead and cannot beat but stay in N_seeds). A 200-seed
wall-clock benchmark at alpha = 0.03, seed0 111 (not a registered
cell) sized the ensemble; only its timing was inspected.
expects: (a) instrument validation — the LCDM fit recovers the
published eq. (17) values within their own 1 sigma: |Omega_m -
0.2975| <= 0.0086 and |h r_d - 101.54 Mpc| <= 0.73 (h r_d =
2997.92458/s*); (b) the w0waCDM improvement on BAO alone lands
dchi2 in [2.0, 8.5] (derived center 4.84 from the paper's own
1.7 sigma via their eq. 22) with the best fit in the published
quadrant w0 > -1, wa < 0; (c) the production walk in
no-backreaction EdS mode (Omega_m = 1, alpha = 0.01, 4000 walkers)
reproduces sigma_OmegaLambda = 2 sqrt(165 pi) alpha within 3 SE +
1 percent; (d) THE QUESTION — in every cell, net bits =
dchi2_best/(2 ln 2) - log2(N_seeds/max(K_beat, 1)) - log2(6) <= 0,
where dchi2_best is the best realization's improvement over the
LCDM minimum and K_beat the number of realizations beating it;
(e) the surviving fraction is monotone non-increasing in alpha
across the four main cells.
changes-my-mind: any cell with net bits > 0 — then everpresent-
Lambda genuinely outperforms LCDM on DR2 BAO at fair prices, c31
upgrades from a coincidence entry to live phenomenology, and the
A-14 premise dies; (a) failing halts the scorecard (instrument
fault — report, do not score); (b) above 11 contradicts the
source's own 1.7 sigma characterization and voids the data
compression; (c) failing voids the walk implementation and
everything downstream.
not-claimed-in-advance: CMB and SNe verdicts (imported: DNY's
Model 1 CMB dchi2 >= +156 against LCDM stands, uncontested here);
DNY Models 2/3; bouncing continuations of dead realizations; the
physical correctness of w0waCDM (only its price); parameter
inference beyond the 13-point Gaussian compression; the parameter-
codebook price of w0wa's two extra parameters (reported context
under a declared (k/2) log2(13) MDL convention, not a clause).

## R-23 — 2026-08-28 — resolves P-26 (all clauses; the scorecard is decisive)
First full run: clause (c) read exactly zero — the no-backreaction
validation mode excluded rho_Lambda from the recorded E^2 as well
as from the dynamics, so the measurement read back its own omission
— and per the registration a (c) failure voids the walk
implementation and everything downstream; that run is void. Three
implementation corrections, all made before any clause was
accepted, none touching a band: (1) the recorded E^2 now always
carries rho_Lambda (only the marching H drops it in validation
mode); (2) the lightcone volume now initializes to its exact
radiation-era closed form at a_init via the eta-moments I0 =
(2/5) a^3 t, I1 = (2/3) a^2 t^2, I2 = (8/7) a t^3, I3 = 2 t^4
(which reassemble to (8 pi/105) t^4, EQ1) — DNY themselves specify
V_0 at the start, and the zero-initialized volume artificially
amplified the first steps' fluctuations, killing 99.3 percent of
alpha = 0.005 realizations at birth; (3) the beat threshold as
first coded used an alpha = 0 realization, which is not LCDM but
Einstein-de Sitter (the walk is the only dark energy; chi2 1457.2
on the native grid) — replaced by the LCDM best fit injected
through the same native-node pipeline (grid bias +0.020, cancelled
in the comparison). A units slip in the reported h r_d conversion
(c vs c/100) was also fixed; the fit itself was never wrong.
Second run, all clauses: (a) Omega_m 0.2970 and h r_d 101.56 Mpc
against the published 0.2975 +- 0.0086 and 101.54 +- 0.73, chi2
10.55 on 11 dof — the 13-point Gaussian compression reproduces the
source fit; (b) w0waCDM buys dchi2 = 4.74 on BAO alone (registered
band [2.0, 8.5], derived center 4.84 from the source's own
characterization via their eq. 22), best fit in the published
quadrant (w0 = -0.18 > -1, wa = -2.70 < 0, prior-railed exactly as
the source warns); (c) production-walk amplitude 0.45444 against
the derived 2 sqrt(165 pi) alpha = 0.45535 at alpha = 0.01, inside
3 SE + 1 percent; (d) THE ANSWER — of 90000 registered
realizations, ZERO beat the LCDM minimum. Survivors to a = 1:
19873 of 20000 at alpha = 0.005, 3873 of 20000 at alpha = 0.01,
0 of 30000 at alpha in {0.02, 0.04} across all three Omega_m
values. Best surviving chi2: 33.37 (alpha 0.005) and 41.88 (alpha
0.01) against threshold 10.57 — the LUCKIEST of 19873 survivors
sits dchi2 = +22.8 on the wrong side; the MEDIAN survivor sits at
chi2 1555, i.e. the typical everpresent realization fails DR2 BAO
about as badly as a no-dark-energy universe, because the walk's
mean is zero and a sustained ~3-sigma-of-its-own-amplitude
excursion is what mimicking Lambda requires. Net bits: -33.3 to
-39.5 where anything survived, -14.9 to -16.9 at the floor
elsewhere. Every cell negative; clause (e) survival monotone
(0.994, 0.194, 0.000, 0.000). The squeeze is the mechanism: small
alpha converges to Einstein-de Sitter (chi2 1457), large alpha
dies before today (radiation-era sigma_OmegaLambda = 68.5 alpha),
and no in-between realization holds a lucky Omega_Lambda both
large enough and steady enough across z < 2.33. Context rows: the
same currency prices DNY's own published SNe record at net -10.0
bits (16 winners in 90000, dchi2 3.4), and w0waCDM on BAO alone at
net -0.28 bits under the declared MDL codebook — the DR2
preference for evolving dark energy lives in the CMB-lensing and
SNe combinations (imported: LC-16), not in the BAO likelihood
scored here. c31's coincidence entry stays a coincidence entry:
the ORDER OF MAGNITUDE of Lambda is the one thing the mechanism
gets right, and the dynamics that produce that magnitude are what
DR2 BAO excludes. Results: scripts/experiments/p26_results.json.

## P-27 — 2026-08-28 — the classical-gravity squeeze windows
question: A-15 - Oppenheim's postquantum classical gravity is the
rival worldview with a COMPUTABLE exposure: the decoherence-
diffusion trade-off (LC-17) squeezes the spacetime diffusion D2
between interferometric coherence (below) and force-noise
experiments (above). Computed from the pinned sources and the
machine-parsed Janse Table I: what parameter space actually
survives, per kernel class, under each inclusion rule for the
contested differential measurements - and what figure of merit
closes each window?
method: derivation layer scripts/experiments/p27_derive.py runs
first and pins scripts/experiments/p27_registration.json:
mechanized dimensional analysis of the three squeeze inequalities
(D2 in kg^2 s m^-3, lambda in every lower bound's denominator),
the six OSSW printed bounds recomputed from their own stated
inputs (lower bounds exact; upper bounds carry signed deltas
+2.26/-1.35/+1.65 orders, pinned), the 46-row Table I audit, the
FOM rescaling rule bound_new = bound_OSSW x FOM/1e14, and the
closure figures of merit. Experiment
scripts/experiments/p27_score.py then computes the window table:
for each kernel class (ultra-local continuous, ultra-local
discrete, nonlocal continuous) x input set (OSSW 2022 printed;
Janse direct-on-Earth best row; plus the questioned rows Asenbaum
and Armano), the surviving window in orders of magnitude
log10(upper/lower), under both lower-bound conventions where they
differ (OSSW printed 1e-40 vs Janse eq. (5) 1e-35, both pinned),
with every bound traced to its pinned row and rule. No ensembles,
no estimator noise: all arithmetic is exact given the pins.
expects: (a) the derive layer's unit mechanization and bound
recomputation stand as pinned (any failure halts the line); (b)
the ultra-local continuous class has NEGATIVE window under every
input set (the OSSW verdict, reproduced); (c) the discrete-class
window is positive at ~9-10 orders under the direct-on-Earth rule
(Gisler) and NEGATIVE if the Asenbaum row is admitted as a valid
upper bound; (d) the nonlocal-continuous window stays positive
under every rule, landing within 1.5 orders of Janse's stated
"one order" gap when computed with their own 1e-35 convention
against the Asenbaum row; (e) the closure figures of merit stand
as pinned (discrete closes at FOM = 1e-10 m^2 s^-3; nonlocal at
1e-17 under the OSSW lower bound, 1e-12 under Janse's).
changes-my-mind: any window changing SIGN when a printed bound is
replaced by our recomputed value (the 1.3-2.7-order deltas must
not flip a verdict - if one does, the order-of-magnitude squeeze
is too soft to support any verdict and the line records that
instead); a Table I inconsistency spreading beyond the single
Monteiro row on recheck.
not-claimed-in-advance: whether differential/relative acceleration
measurements validly bound D2 (imported open question - the crux,
left two-sided); whether one experiment can serve as both bounds
(their own open question); the viability of postquantum classical
gravity (windows are computed, worldviews are not adjudicated);
relativistic completions; other hybrid models (Tilloy-Diosi,
Kafri-Taylor-Milburn); the correct V_lambda / R_lambda superposition-
volume conventions (recorded as the source of the 1e-35 vs 1e-40
discrepancy, not resolved).

## R-24 — 2026-08-28 — resolves P-27 (mind-change FIRED on sign stability; recorded, not rescued)
Clauses (a)-(e) all held: the unit mechanization and six-bound
recomputation stand; the ultra-local continuous class is excluded
under every rule (window -17.0 at OSSW-2022 down to -41.6 with
Asenbaum); the discrete class survives the direct-on-Earth rule at
+9.5 orders (Gisler FOM 0.298) and reads -0.6 with Asenbaum
admitted; the nonlocal class is positive everywhere on printed
bounds, with the Asenbaum/Janse-convention cell at +1.4 against
their stated "one order"; the closure figures of merit stand
(discrete shuts at FOM = 1e-10 m^2 s^-3, nonlocal at 1e-17 under
the OSSW lower bound, 1e-12 under Janse's 1e-35).
THE FIRING: the registered sign-stability check found three
verdict flips between the printed bounds and the same bounds
recomputed from the sources' own stated inputs - all three in the
contested Asenbaum rows: discrete/OSSW-lower -0.62 -> +0.73,
discrete/Fein-lower -1.11 -> +0.24, nonlocal/Janse-e35 +1.38 ->
-0.27. Per the registration, those cells' verdicts are recorded as
UNDECIDABLE AT SOURCE PRECISION rather than rescued: the question
"does atom interferometry close the discrete class" has its answer
living entirely inside the sources' own order-of-magnitude
arithmetic (printed upper bounds sit +2.26/-1.35/+1.65 orders from
their own inputs, EQ2), on top of the already-imported
applicability question (differential/relative measurements as D2
bounds) and the underivable 1e-35 lower-bound convention. What
survives both arithmetics and every inclusion rule: continuous
EXCLUDED (margin >= 14 orders); discrete SURVIVES the
uncontested rule (margin >= 8 orders) and is UNDECIDED under
Asenbaum; nonlocal SURVIVES (margin >= 4 orders except the one
fragile cell). The decisive next number is not incremental: the
discrete class needs FOM = 1e-10 m^2 s^-3 from an UNCONTESTED
absolute on-Earth measurement (Gisler sits at 3e-1; nine orders),
or a settled ruling on whether relative measurements count -
at which point Asenbaum-class data either closes the discrete
window or does not, with nothing in between at current precision.
Results: scripts/experiments/p27_results.json.

## P-28 — 2026-08-28 — the gap integers of the golden ladder
question: A-12 - P-7 computed the golden flux ladder's spectra and
deliberately left Chern content not-claimed. Do the ladder's gaps
carry their Diophantine/Streda labels in the computed spectra -
principal gaps at t = +-1, the Fibonacci map r = F_j <-> |t| =
F_{n-j} (derived exactly in EQ2, including the edge gap's LARGE
Fibonacci Chern |t| = F_{n-2}), exact integer Streda slopes across
Farey-neighbor rungs from independent band counting, and a gap
hierarchy ordered by |t|?
method: derivation layer scripts/experiments/p28_derive.py runs
first and pins scripts/experiments/p28_registration.json: label
existence/uniqueness with the even-q central ambiguity landing on
P-7's closed gap (EQ1), the Fibonacci congruence F_{n-1} F_j =
(-1)^{j+1} F_{n-j} (mod F_n) and THE MAP with sign-flipped mirrors
(EQ2, exhaustive, q = 2 vacuous), kernels.eig.eigh anchored
against the P-7 Jacobi route at 3.6e-15 and the c25 q = 2 closure
(EQ3 - first experiment-side kernels consumer), unimodularity of
consecutive rungs and the exact rational Streda slope identity
(EQ4), and the feasibility pins (EQ5: width floor 1e-9, hierarchy
tiers |t| in {1,2,3}, edge-gap resolution required only through
q = 13 since |t(r=1)| = F_{n-2} grows along the ladder).
Experiment scripts/experiments/p28_labels.py: for each rung q in
{3,5,8,13,21,34,55,89,144}, spectra by kernels.eigh at the two
P-7 Chambers corners (corner +-1, k2 in {0, pi/q}), bands as
consecutive sorted edge pairs, gaps with widths, every open gap
(width > 1e-9) assigned its (s, t).
expects: (a) at every rung q >= 5, the two WIDEST open gaps sit at
r = F_{n-1} and F_{n-2} carrying t = +1 and -1; (b) hierarchy:
median open-gap width strictly decreasing across tiers |t| = 1, 2,
3 at every rung q >= 13; (c) every open Fibonacci-position gap
obeys the EQ2 map, and the edge gap r = 1 is resolved (open at
floor) through q = 13 carrying |t| = F_{n-2}; the rung where r = 1
drops below the floor is reported, not scored; (d) Streda from
independent band counting: for consecutive rung pairs from 5/8 up
and labels t in {+1, -1, +2}, the two gaps' energy windows overlap
and counting bands below the overlap midpoint at the finer rung
returns r' with (r'/q' - r/q)/(p'/q' - p/q) = t exactly; (e) the
even-q central gap width stays below 1e-12 at q in {8, 34, 144}
(parity interop re-verified in this pipeline).
changes-my-mind: any open principal gap carrying a label other
than +-1 kills the labeling claim outright; any open
Fibonacci-position gap off the EQ2 map kills the Fibonacci-Chern
statement; any overlapping Streda pair returning a non-integer or
wrong-integer slope kills the Streda mechanization; hierarchy
inversion between tiers 1 and 2 at two or more rungs kills the
hierarchy clause (a single-rung inversion is recorded and the
clause fails for that rung).
not-claimed-in-advance: the irrational limit (Cantor spectrum,
dry Ten Martini - LC-18 context); gaps below the 1e-9 floor;
Hall conductance in physical units or by Kubo (TKNN meaning
imported, not recomputed); lambda != 1; tiers |t| >= 4 (their
positions are not Fibonacci and no claim is registered about
them); gap-width scaling exponents along the ladder (reported for
the P-7 ln-phi context, unscored).

## R-25 — 2026-08-28 — resolves P-28 (all clauses, first run)
All five clauses held with no amendments: (a) at every rung q >= 5
the two widest gaps are the principal pair at r = F_{n-1} (t = +1)
and r = F_{n-2} (t = -1); the t = +1 width saturates along the
ladder at 1.5391, 1.6474, 1.6691, 1.6816, 1.6834, 1.6848, 1.6850,
1.6851 (q = 5..144) - an O(1) gap surviving toward the irrational
limit. (b) The tier hierarchy holds at every rung q >= 13; at
q = 89 the medians are 1.685 / 0.332 / 0.147 for |t| = 1/2/3.
(c) Every open Fibonacci-position gap obeys the EQ2 map, and the
edge gap r = 1 - required resolved only through q = 13 - stayed
above the floor through q = 144, carrying the full alternating
Fibonacci Chern sequence t = -1, +2, -3, +5, -8, +13, -21, +34,
-55 with widths 1.27, 0.157, 9.06e-2, 2.25e-2, 8.25e-3, 2.46e-3,
8.14e-4, 2.55e-4, 8.21e-5: per-rung ratio ~ 0.324, i.e. width ~
q^{-2.34} (unscored context: the critical point's power-law gap
scaling is exactly why a |t| = 55 gap is still open at q = 144;
exponential closing would have killed it at q = 21). (d) Streda
mechanized: 18 Farey-neighbor gap pairs (t in {+1, -1, +2}, rungs
5/8 through 89/144), every energy window overlapping and every
band-counted slope landing on its integer exactly - Fractions
arithmetic, no tolerance. (e) The even-q central gaps close at
2.6e-15 / 7.8e-15 / 1.5e-14 (q = 8/34/144) while EQ1 shows their
Diophantine label is the single AMBIGUOUS case t = +-q/2: the
number theory and the spectrum point at the same gap. P-7's
not-claimed Chern scope is now an earned claim
(golden-ladder-gap-integers). Runtime 0.5 s - kernels.eigh's
first experiment-side consumer. Results:
scripts/experiments/p28_results.json.

## P-29 — 2026-08-28 — the Farey bridge (first premises-bearing composite)
question: A-13 - Arnold tongues and Hofstadter bands are both
organized by the rationals. The composite claim under test: they
share the MEDIANT skeleton because they share a premise
(first-harmonic two-frequency competition) - in every registered
Farey interval the mediant hosts the largest substructure on BOTH
instruments, the grading agrees beyond the winner, and the
correspondence breaks exactly where the premise is broken, in the
direction derived in advance.
method: derivation layer scripts/experiments/p29_derive.py runs
first and pins scripts/experiments/p29_registration.json: the
interval table (all Farey-neighbor pairs bc - ad = 1 inside
(0, 1/2] with b + d <= 8: 10 intervals, 8 with >= 4 competitors;
mediant minimality exhaustive to q = 40), tongue-instrument
anchors (exact rho = 0 width K/pi at 1e-10; the 1/3-2/3 symmetry;
K^q resonance ratios 3.998/7.992 vs 4/8), butterfly anchors
(S(1/2) = 4 sqrt 2 at 1e-12; S(8/13) equal to the P-7 pipeline at
1e-9), and the DERIVED control: the pure-second-harmonic map is
exactly conjugate to the standard map at (2 Omega, 2K) (verified
1e-8), which pins the inversion Delta_std(3/4, 1) >
Delta_std(4/5, 1) - so under sin(4 pi theta) forcing the
competitor 3/8 must beat the mediant 2/5 in [1/3, 1/2] BEFORE the
registered run. Experiment scripts/experiments/p29_bridge.py at
K = 0.5: tongue widths by tangency bisection (Omega to 1e-12) and
bandwidths S by the two-corner eigh pipeline, for every mediant
and competitor (q <= 13, width floor 1e-9) of every registered
interval.
expects: (a) tongues - in all 10 intervals, Delta(mediant) >
Delta(r) for every competitor; (b) butterfly - in all 10
intervals, S(mediant) > S(r) for every competitor; (c) grading -
Spearman rank correlation between {Delta(r)} and {S(r)} over
mediant + competitors is >= 0.5 in every interval with >= 4
competitors (8 intervals); (d) the control - under second-harmonic
forcing in [1/3, 1/2], Delta_2(3/8) > Delta_2(2/5), the derived
inversion, while the butterfly side (untouched by the forcing
change) keeps S(2/5) largest: the bridge breaks on exactly one
side, in the pinned direction; (e) instrument floors - every
scored width above 1e-9 and every scored S above 1e-6 (report
any exclusions).
changes-my-mind: any interval where the mediant loses on EITHER
instrument kills the composite's mechanism claim (resemblance
would survive; mechanism would not); a median Spearman below 0
kills the grading clause outright; the control FAILING to invert
(mediant still winning under second-harmonic forcing) would mean
the mediant ordering does not come from first-harmonic
competition and the premise story is wrong - that is the
composite's designed kill switch.
not-claimed-in-advance: criticality (K = 1) or supercritical
overlap; irrational-limit statements; tongue-butterfly
correspondence at the level of WIDTH VALUES or scaling exponents
(only orderings and ranks are claimed; the log-log width relation
is reported unscored); the kneading-tree systems recorded in
LC-19 (Bernoulli convolutions - a different skeleton, queued as
its own candidate line); any physical identification between
driven oscillators and electrons in fields beyond the shared
premise named above.

## R-26 — 2026-08-28 — resolves P-29 (all clauses; one instrument-domain correction)
First run: clause (e) fired on three competitors (1/11, 1/12,
1/13) whose tongue widths read 0.0 while their bandwidths were
healthy - an instrument fault, not physics: the Omega bracket
0.6 K/q missed windows displaced by the rho = 0 tongue, whose
K/(2 pi) = 0.0796 width shifts the whole staircase (at Omega =
1/11 the eleventh-iterate deficit is 0.165 - the window sits far
right of the naive center). The bracket was replaced by the
RIGOROUS per-step bound |Omega - rho| <= K/(2 pi) + 1e-3, under
which the crossing is unique by monotonicity; no registered band
was touched, and the earlier feasibility estimate (K/2)^q in EQ5
is recorded as wrong-but-harmless (the true small parameter is
nearer K/(4 pi); all scored widths sit above the floor).
Second run, all clauses: (a) the mediant carries the WIDEST
TONGUE against every competitor in all 10 registered intervals;
(b) the mediant carries the LARGEST BANDWIDTH against every
competitor in all 10 intervals; (c) the grading transfers beyond
the winner: Spearman between tongue widths and bandwidths over
mediant + competitors is 0.891-1.000 across the 8 eligible
intervals; (d) the control broke the bridge on exactly one side
in the direction derived at registration: under pure-second-
harmonic forcing (exactly conjugate to the standard map at
(2 Omega, 2K), EQ4 at 1e-8), the competitor 3/8 beats the
mediant 2/5 in [1/3, 1/2] (7.93e-3 vs 4.66e-3) while the
untouched butterfly keeps S(2/5) = 1.8434 > S(3/8) = 1.2021;
(e) every scored width above 1e-9, every S above 1e-6. The
composite mechanism claim stands on its named premise: the
mediant ordering follows from first-harmonic two-frequency
competition - remove the first harmonic and the ordering follows
the CONJUGATED denominators instead, exactly as the conjugacy
demands. First premises-bearing claim filed
(farey-bridge-mediant-mechanism, premises: harper-golden-ladder,
golden-ladder-gap-integers). Results:
scripts/experiments/p29_results.json.

## P-30 — 2026-08-28 — the order ladder
question: A-16 - indefinite causal order attacks the symbol
graph's deepest primitive. Priced with the P-17 machinery: is the
order ladder, computed end to end (causal bound by exhaustive
enumeration, the OCB process value from the pinned eq.-7 matrix
and eq.-20-23 protocol, the VLBC switch value from an exact
circuit, the switch's bipartite invisibility), the Bell ladder
under the derived affine map p = (S+4)/8 - and does the coherent
switch buy NOTHING over a classical order mixture until a
spacelike observer is added?
method: derivation layer scripts/experiments/p30_derive.py runs
first and pins scripts/experiments/p30_registration.json: the
affine Bell-order correspondence (EQ1, exact), the OCB process
spectrum {0 x8, 1/2 x8} by anticommutation (EQ2), process
validity as trace-and-replace identities with a pinned invalid
loop perturbation (EQ3), the reduced-process anchor P(y|a,b'=1) =
(1/2)[1+(-1)^{y+a}/sqrt2] (EQ4), and the switch third-term anchor
(2+sqrt2)/4 with Kraus completeness (EQ5). Experiment
scripts/experiments/p30_ladder.py, all exact complex arithmetic
at 1e-12, no stochastics: (1) OCB causal rung by EXHAUSTIVE
enumeration over deterministic one-way-signalling strategies
(message bit, both orders, 4 x 4 x 256 each; vertex maximum
suffices for mixtures by linearity); (2) the OCB process rung
from eqs. (7) + (20)-(23); (3) the VLBC rung: exhaustive
deterministic DRF strategies for Theorem 1's inequality (both
lambda orders, Bob spacelike) AND the exact switch circuit
(|Phi+> control-Bob, target |0>, measure-reprepare Alices, the
pinned Bob/Charlie angles); (4) the separability null: the
switch's Alice-marginal p(a1 a2 | x1 x2) with |+> control and
B, C discarded, against the 50/50 classical mixture of the two
fixed-order wirings, entrywise.
expects: (a) OCB causal maximum = 3/4 exactly, both orders,
enumeration counts reported; (b) OCB process value = (2+sqrt2)/4
within 1e-12, with validity checks passing; (c) VLBC: exhaustive
DRF maximum = 7/4 exactly; switch value = 1 + (2+sqrt2)/4 within
1e-12; algebraic maximum = 2 (unconstrained assignments); (d) the
separability null: switch Alice-marginal equals the classical
order mixture entrywise within 1e-12 for all 16 cells - order
coherence is bipartitely invisible; (e) the ladder assembly: both
computed ladders land on the Bell rungs under S = 8p - 4 (OCB)
and S = 8(p - 1) - 4 (VLBC) within 1e-12, with the two-sided
honesty imported: the OCB middle rung's maximality is OPEN in the
source, the VLBC middle rung's maximality is PROVEN there via
Tsirelson for commuting-Bob.
changes-my-mind: any enumeration exceeding its registered bound
kills the implementation (halt, audit); the process value or
switch value missing its pinned target kills the respective
import; the separability null FAILING would contradict the
imported no-bipartite-violation theorems - that is
discovery-grade and mandates a halt-and-audit, not a claim.
not-claimed-in-advance: physicality of the OCB process (open in
the source; CTC realizations break linearity per their
discussion); global maxima over all processes or games beyond the
imported statements; the 24-sigma experiment's loophole status
(imported as flagged); any gravitational-order-superposition
story; an information-causality-style contraction for order (the
P-17 analog is noted as a future line, not attempted).

## R-27 — 2026-08-28 — resolves P-30 (all clauses, first run)
All five clauses held with no amendments, 0.6 s wall clock: (a)
the OCB causal maximum is 3/4 over 8192 exhaustive deterministic
one-way-signalling strategies (both orders; mixtures bounded by
vertex linearity); (b) the pinned eq.-7 process with the
eq.-20-23 protocol yields 0.853553390593 = (2+sqrt2)/4 at 1e-12,
with the process valid (spectrum {0 x8, 1/2 x8} from the EQ2
anticommutation closed form, trace-and-replace identities
passing); (c) the VLBC DRF maximum is 7/4 over 131072 exhaustive
deterministic strategies (two lambda orders, Bob spacelike), the
exact switch circuit gives 1/2 + 1/2 + 0.853553390593 =
1 + (2+sqrt2)/4, and the algebraic maximum is 2; (d) THE NULL
THAT LANDS THE POINT: the coherent switch's Alice-marginal
p(a1 a2 | x1 x2) equals the 50/50 classical mixture of the two
fixed-order wirings ENTRYWISE AT MACHINE ZERO (worst cell 0.0) -
order coherence is bipartitely invisible, and the entangled
spacelike observer is what makes it visible, at exactly a
Tsirelson price; (e) the ladder assembly: S = 8p - 4 sends the
computed OCB ladder to (2.0000000000, 2.8284271247, 4.0000000000)
and S = 8(p-1) - 4 sends the computed VLBC ladder to the same
three numbers - the order ladder IS the Bell ladder under the
derived affine maps, for these two games. Two-sided honesty as
registered: the OCB middle rung's maximality is OPEN in the
source (so the order-Tsirelson identification is proven only on
the VLBC side, where van der Lugt et al. prove it via Tsirelson
for commuting-Bob); the OCB process has no known physical
realization; the 24-sigma experiment (LC-20) is imported with its
loopholes flagged. The symbol graph's order primitive survives
priced, not attacked: giving up definite order buys, in these
games, precisely what giving up local realism bought in P-17 -
the same sqrt-2 geometry, one affine map apart. Results:
scripts/experiments/p30_results.json.

## P-31 — 2026-08-28 — the second bridge (the distinction is the claim)
question: A-18 - P-29 proved the mediant skeleton transfers
between tongues and bands because they share a premise. The
complementary registered composite: the kneading tree of the
Bernoulli two-map system is a DIFFERENT skeleton - its structure
(finite multivalued orbits of the overlap boundary) sits at the
algebraic landmark ladders (multinacci t_n, doubling s_n) and
provably NOWHERE the Farey tree would put it: not at the simple
rationals of the interval, not at the Fibonacci convergents of t_2
itself, and not at the mediant - with every divergence CERTIFIED
by exact denominator growth, not by timeout.
method: derivation layer scripts/experiments/p31_derive.py runs
first and pins scripts/experiments/p31_registration.json: the
multinacci and doubling ladders by exact Fraction bisection to
1e-40 with their interleaving (t_4 < s_3 < t_3 < s_2 < t_2), the
exact Q(beta) kit (Fraction-coefficient polynomials mod the
defining polynomial, sign decisions by bracket refinement,
boundary membership decided algebraically), the golden anchor (the
overlap-boundary orbit at t_2 closes on {0, 2-phi, phi-1, 1},
size 4, hand-derived including the closed-edge subtlety), the
rational divergence certificate (finite orbit implies bounded
denominators; growth past 1e6 certifies divergence; tail-monotone
at t = 3/5), and the separation of predictions (mediant(1/2, 3/5)
= 4/7 vs s_2, gap 1.588e-3). Experiment
scripts/experiments/p31_bridge2.py, orbit cap 20000, exact
arithmetic throughout.
expects: (a) the overlap-boundary orbit CLOSES at every multinacci
rung n = 2, 3, 4, 5, with the golden size exactly 4 and all sizes
recorded (the kneading ladder's analog of the P-28 orbit table);
(b) the orbit also closes at the doubling landmarks s_2 and s_3;
(c) the orbit DIVERGES with the denominator certificate (> 1e6)
at every registered rational: 3/5, 5/9, 4/7 (the mediant), and
the Fibonacci convergents 8/13 and 13/21 of t_2 itself; (d) the
skeleton distinction assembled: structure at s_2 = 0.569840
(finite), certified nothing at 4/7 = 0.571429 (the mediant,
1.588e-3 away) - the kneading tree refuses the mediant; (e) sizes
and certificates reported for the whole table, no timeouts used
as evidence anywhere (closure = exact set closure; divergence =
denominator certificate; the cap is only an implementation guard).
changes-my-mind: a multinacci rung failing to close kills the
landmark import and the line halts for audit; a REGISTERED
RATIONAL CLOSING (finite orbit at 3/5, 4/7, 5/9, 8/13 or 13/21)
would put kneading structure exactly where the Farey tree predicts
it - the distinction claim dies and a transfer claim would need
its own fresh registration; the doubling rungs failing to close
fires clause (b) and is recorded as address-curve organization
(informative, diagnosed, not rescued - the multinacci clauses and
the rational certificates stand independently).
not-claimed-in-advance: any of Bandt's theorems (his results are
context, not premises); irreducibility of the defining polynomials
(defining degree is used, minimal degree is not certified);
absolute continuity or singularity of any Bernoulli convolution;
the measure-zero window statement in full generality (only the
registered rationals are certified); orbit structure for starting
points other than the overlap boundary; any transfer TO the Farey
systems (P-29 owns that side).

## R-28 — 2026-08-28 — resolves P-31 (all clauses, first run)
All five clauses held with no amendments, 0.1 s wall clock, exact
arithmetic end to end: (a) the overlap-boundary orbit closes at
every multinacci rung with sizes 4, 8, 10, 12 (n = 2..5; the
golden 4 as hand-derived, including the closed-edge subtlety);
(b) it also closes at both doubling landmarks, sizes 6 (s_2, the
supergolden parameter) and 8 (s_3); (c) it DIVERGES with the
denominator certificate at every registered rational - 3/5
(1.59e6), 5/9 (1.95e6), 4/7 (1.05e6), and t_2's own Fibonacci
convergents 8/13 (2.10e6) and 13/21 (4.83e6) - no timeout used as
evidence anywhere; (d) the skeleton distinction assembled: finite
structure at s_2 = 0.569840 and certified nothing at the mediant
4/7 = 0.571429, 1.588e-3 away. The kneading tree refuses the
mediant: where P-29's systems put their largest window at
denominator addition, the Bernoulli system puts its closures at
algebraic landmarks and provably nothing at the interval's simple
rationals - even the best Farey approximants of the golden
landmark itself diverge while the landmark closes. The registered
kill (a rational closing) stayed quiet. Orbit-size ladder
(4, 8, 10, 12 / 6, 8) recorded unscored. Third premises-bearing
claim filed (second-bridge-skeleton-distinction, premise
farey-bridge-mediant-mechanism): the two bridges together now
state, with computed evidence on both sides, that WHICH tree
organizes a system is a consequence of the system's premise - the
mediant follows from two-frequency competition (P-29's control),
the kneading landmarks from expansion redundancy at algebraic
parameters (this line's certificates). Results:
scripts/experiments/p31_results.json.

## P-32 — 2026-08-28 — the drive-geometry parity factorial
question: A-2 - the untested reconciliation: LC-3 proposed that
E1's no-parity result and the Josephson literature's even/odd
half-integer-step claim differ because of the DRIVE TYPE. Run the
2 x 2 factorial on one codebase - drive (per-site pinning vs
uniform bias + AC) x geometry (one pi seam vs alternating 0-pi
bonds), N = 4..9 - and let the registered frustration arithmetic
(EQ1: f(N) = (floor(N/2)/2) mod 1 plus the odd-N defect; classes
{4,8} clean, {5,9} defect, {6} half, {7} both) compete with plain
even/odd parity as the organizing variable of the half-integer
step.
method: derivation layer scripts/experiments/p32_derive.py runs
first and pins scripts/experiments/p32_registration.json: the
frustration classes (arithmetic), the instrument identities
(rho(I+1) = rho(I)+1 and the sign symmetry at 1e-12), the
ground-state anchors (seam strain 1/(2N) for every N; clean ALT
cancellation at N = 4; the N = 6 residual winding 1/2), the
twelve P-9 pinned widths as reproduction bands, and the declared
validation cell (N = 4 seam+bias half-step: stable, and zero).
Experiment scripts/experiments/p32_factorial.py (pmap over cells):
pinning cells K = 1.0, J = 0.6, rho = 1/2 plateau in Omega,
attractor-controlled initial conditions; bias cells K = 0,
J = 0.6, A = 0.9, nu = 1/8, steps at rho = nu (integer) and
rho = nu/2 (half) in I; widths by coarse scan (step 1e-3) + edge
bisection; width floor 1e-5; effective width resolution 3e-3
(TOL-edge systematic).
expects: (a) reproduction - the seam+pinning widths land within
5e-3 of all twelve P-9 pins, no parity alternation; (b) THE
QUESTION - the ALT+bias half-step widths are organized by f: the
f = 1/2 group {6, 7} separates from the f = 0 group {4, 5, 8, 9}
by a gap >= 3e-3 with the frustrated group ABOVE (half-integer
steps born from the half-turn frustration, the Frolov mechanism);
in particular {6} (even) sides with {7} (odd) - plain even/odd
FAILS to organize a ring; (c) seam+bias - no parity alternation
in the half-step widths (successive differences do not alternate
beyond 3e-3; the validation cell suggests they sit at zero);
(d) the drive factor - the f-gap under ALT+pinning (1/2-plateau
widths) is smaller than 3e-3 while the bias gap in (b) exceeds
it: the drive type is what activates the frustration classes;
(e) positive control - the integer step rho = nu has width above
the floor in every bias cell (control, seam, ALT; all N).
changes-my-mind: (a) any reproduction miss or parity alternation
- halt and audit (P-9's protocol would be in question); (b) no
f-gap - the derived arithmetic does not organize the dynamics and
the reconciliation stays open, recorded; the even/odd split
organizing INSTEAD of f (with {6} siding with {4, 8}) - the
imported parity claim transfers as stated and the ring-closure
refinement is dynamically irrelevant, recorded; every ALT+bias
half-width at the floor - the imported effect does not transfer
to this drive/geometry family at these parameters, recorded as
the honest transfer failure; (d) reversed (pinning gap >= bias
gap) - the geometry alone carries the classes and LC-3's
drive-type reading is revised in the R-entry.
not-claimed-in-advance: the open-array geometries of the
Josephson papers (our ring closure is declared as the source of
the EQ1 refinement); voltage-step physics beyond the rotation-
number analogy; the unexplained P-9 non-monotonicity at K = 1.4
(not this line's target); parameter dependence beyond the single
registered (J, A, nu, K) point; any claim at N outside 4..9.

## R-29 — 2026-08-28 — resolves P-32 (clauses b and d FIRED; diagnosed, not rescued)
Held: (a) the P-9 reproduction landed on all twelve pins with
r(N) = 0.300, 0.397, 0.473, 0.459, 0.446, 0.444 and no parity
alternation; (c) the seam+bias half-widths show no alternation;
(e) the integer step exists in every bias cell.
FIRED, both with clean diagnoses:
(b) every ALT+bias half-step "width" measured exactly 0.00080,
identical across N and geometry - which is the TOLERANCE SMEAR of
an unlocked staircase, 2 TOL / (d rho / d I) with the off-plateau
slope measured at 1.0000 in every probed cell (diagnostic in this
entry's evidence chain). The instrument's width floor (1e-5) was
mis-derived: the correct null width is the smear 8.0e-4, and
against THAT null there is NO half-integer locking at the
registered operating point (A = 0.9, nu = 1/8) in ANY geometry.
The imported effect did not transfer at this single operating
point; whether it transfers anywhere in this family is not
answered by P-32 and is re-registered (P-33) with the corrected
null and a declared operating-point grid.
(d) the metric fired for the opposite reason than guarded
against: the PINNING side has a large f-organization - under
ALT+pinning the frustrated classes {6, 7} have 1/2-plateau widths
0.089 NARROWER than the clean/defect classes, thirty times the
resolution - the registered expectation (classes silent under
pinning) was simply wrong. The frustration arithmetic organizes
the pinned ring strongly; direction: frustration NARROWS the
plateau. This appeared through a registered metric but its
direction was not registered in advance, so it is recorded here
as a diagnosed observation and promoted to a registered clause at
a FRESH coupling in P-33.
Results: scripts/experiments/p32_results.json.

## P-33 — 2026-08-28 — the factorial re-registered (corrected null, declared grid)
question: with the instrument corrected (the null width is the
derived tolerance smear w0 = 2 TOL / slope, measured per cell by
the registered finite-difference formula off-plateau; locking
present iff width > 2 w0), does the half-integer step appear
ANYWHERE on a declared bias operating grid, and does its
organization follow the EQ1 frustration classes - and does the
newly observed pinning-side f-organization persist at a fresh
coupling?
method: same codebase and cells as P-32 with: (1) bias cells run
over the declared grid A in {0.5, 0.9, 1.3, 1.7} x nu in
{1/8, 1/6}, geometries {control, seam, alt}, N = 4..9, half-step
target rho = nu/2; per cell the null w0 from the off-plateau
slope at I = nu/2 + 0.01; the cell's sup-width over the grid
recorded; (2) integer-step positive control at each grid point on
the control geometry; (3) pinning cells at the FRESH coupling
K = 1.2 (untouched by P-32/P-9), ALT geometry, N = 4..9,
attractor-controlled initial conditions.
expects: (a) two-outcome clause, both outcomes explicit: EITHER
the half-step appears (sup-width > 2 w0) in at least one ALT cell
and the f-classes organize the sup-widths (frustrated group
{6, 7} separated from {4, 5, 8, 9} by >= 3e-3, direction
recorded) - the transfer succeeds and the organizing variable is
identified - OR no cell on the whole grid exceeds 2 w0 and the
transfer failure of the imported effect to this uniform-bias
circle-map family is CONFIRMED across the declared grid (a
recorded negative import, LC-23's ring-closure caveat standing as
the suspected reason); (b) the pinning f-organization persists at
K = 1.2: f-gap_pin <= -3e-3 (frustrated narrower), the direction
observed in R-29; (c) integer-step positive control present at
every grid point.
changes-my-mind: (a) f-organization appearing with plain even/odd
organizing INSTEAD (the {6} cell siding with {4, 8} against
{5, 7, 9} in sup-widths) revives the imported parity claim
as-stated and kills the ring-closure refinement; (b) failing
(gap_pin > -3e-3 at K = 1.2) makes R-29's pinning observation a
K = 1.0 accident - recorded, and the promotion is withdrawn;
(c) failing voids the grid's operating points.
not-claimed-in-advance: as P-32, plus: no claim that the declared
grid is exhaustive (a negative outcome is scoped to the grid);
the mechanism of the pinning-side narrowing (reported, not
modeled).

## R-30 — 2026-08-28 — resolves P-33 (clause c FIRED; the stop rule closes the bias side)
Held: (a) the two-outcome clause resolved to TRANSFER FAILURE
CONFIRMED ACROSS THE DECLARED GRID - zero of 288 bias cells
exceeds twice its corrected null anywhere on A in {0.5, 0.9, 1.3,
1.7} x nu in {1/8, 1/6}; (b) the pinning f-organization PERSISTS
at the fresh coupling: at K = 1.2 the ALT 1/2-plateau widths are
0.1667, 0.1537, 0.0370, 0.0159, 0.1666, 0.1522 for N = 4..9 -
f-gap -0.1508, fifty times resolution - and in fact ALL FOUR EQ1
classes separate in order: clean {4, 8} > defect {5, 9} > half
{6} > both {7}. Frustration narrows the pinned plateau,
class by class.
FIRED: (c) the integer-step positive control failed at EVERY grid
point - and the diagnosis is an identity, not an operating-point
problem: the site-mean advance TELESCOPES. The coupling terms
cancel in antisymmetric pairs around the ring (each bond
contributes sin(...) to one site and its negation to the other),
so the site-mean rotation number satisfies rho = I identically -
verified at 6.8e-16 across geometries and drives - and NO Shapiro
step of any order can exist in this observable, for any geometry,
by algebra. P-32's clause (e) "positive control" had been fooled
by the same tolerance smear. This is the SECOND firing on the
positive-control clause family; per the stop rule the bias side
closes here with the finding recorded rather than a third
registration: the Josephson voltage lives ACROSS junctions
(difference variables), not in the mean phase drift, and a
faithful Shapiro analog would need both the difference observable
and per-junction nonlinearity in the driven loop - which is
exactly the sharpened form of LC-3's drive-type reading. E1's
pinned ring has the nonlinearity without the drive; this bias
ring had the drive without an effective nonlinearity in its
observable; the Josephson arrays have both. The reconciliation
A-2 asked for is thereby recorded: the literature's parity effect
could never have appeared in either of our families, and the
thing that DOES organize our rings is the EQ1 frustration
arithmetic on the pinned side - the line's positive product
(claim frustration-classes-organize-the-pinned-ring).
Results: scripts/experiments/p33_results.json.

## P-34 — 2026-08-28 — the horizon-coincidence census
question: A-8 - the famous horizon-scale coincidences (a0 ~
c H0/2pi; the CKN/Sorkin/Zeldovich dark-energy magnitude; the
why-now ratio; Weinberg's pion relation; the neutrino-dark-energy
scale) each carry a literature of proposed mechanisms. Priced
against a single derived codebook - monomials in {hbar, c, G, H0}
on a declared exponent lattice with a declared prefactor set -
how many bits does each coincidence actually earn, once the
codebook's derived coverage density and the census's own size are
charged?
method: derivation layer scripts/experiments/p34_derive.py runs
first and pins scripts/experiments/p34_registration.json, with
the AGENTS.md item-8 instrument nulls stated: (a) detector null =
the coverage function p(t) by exact interval union (p(0.05 dex) =
0.176, p(0.1) = 0.275, p(0.3) = 0.374 - factor-2 matches are
cheap BY DERIVATION); (b) conservation identity = the
mu-degeneracy (rank-3 dimension matrix; every coincidence is a
(k, prefactor) pair with mu = H0 t_P = 1.18e-61, so slots cannot
be double-counted); (c) domain = the k-lattice {p/q, q <= 3,
|k| <= 2}, the 20 prefactors in [1/4pi^2, 4pi^2], the 10.155-dex
cell with adjacent clouds verified disjoint. Calibration on the
Gibbons-Hawking theorem row (reproduced at < 1e-9 dex, excluded
from counting). Experiment scripts/experiments/p34_census.py: for
each of the five pinned census entries (LC-24), the nearest
codebook expression and mismatch t in dex; surprisal =
-log2 p(t); net bits = surprisal - log2(5) (the census's own
look-elsewhere); the slot-collision count for the k = 2 density
slot from LC-24's citations; the H0 sensitivity pair.
expects: (a) the census table computes with every entry matched
to a codebook expression at some t (coverage guarantees nothing;
the values are the finding); (b) THE VERDICT - no census entry
nets more than 3 bits after coverage and census-size charges;
(c) the k = 2 density slot carries >= 4 named mechanisms (CKN,
Sorkin, Zeldovich, holographic - LC-24): mechanisms are many,
slots are few, recorded as arithmetic; (d) stability: no entry's
net bits moves by more than 1 bit between H0 = 67.4 and 73.0;
(e) the calibration row stays < 1e-9 dex under both H0 values.
changes-my-mind: any entry netting > 3 bits is flagged as
deserving its own mechanism line (the census's positive-detection
arm - registered two-sidedly, not as a foregone null); the
coverage function failing its own re-derivation in the verify
layer voids the instrument.
not-claimed-in-advance: any mechanism verdict (Milgrom, Verlinde,
CKN, Sorkin - their statuses live in LC-6/LC-9/c33/c31, not
here); coincidences involving particle-scale constants beyond the
declared census (Dirac large numbers need extra base quantities
and are out of codebook, noted); the RAR's tightness as data (a
separate, real regularity); any cosmology.

## R-31 — 2026-08-28 — resolves P-34 (clause d FIRED: an underived band, attributed)
Held: (a) the census computed - every entry lands on a codebook
expression: a0 at t = 0.061 dex (k = 1, prefactor 1/2pi - the
Milgrom expression itself), rho_Lambda at 0.012 dex (k = 2,
1/4pi), the why-now ratio at 0.036 dex (prefactor 2), m_pi at
0.067 dex (k = 1/3, prefactor 2 - Weinberg's relation with its
factor two), the neutrino scale at 0.019 dex (k = 1/2, 4pi);
(b) THE VERDICT - no entry nets more than 3 bits: the maximum is
rho_Lambda at +2.13, the why-now ratio +0.59, the neutrino scale
+1.49, and a0 and m_pi price at -0.03 and -0.11 - ZERO net bits:
against the derived codebook (coverage p(0.1 dex) = 0.275) and
the census's own size, the two most famous horizon coincidences
are worth nothing at all, and the best is worth two bits; (c) the
k = 2 density slot carries four named mechanisms (CKN, Sorkin,
Zeldovich, holographic DE) - mechanisms are many, slots are few;
(e) calibration held under both H0.
FIRED: (d) the a0 entry's net moved 1.06 bits between H0 = 67.4
and 73.0, past the registered 1.0-bit band. Attribution: my band
was set without deriving the instrument's own sensitivity - the
pinned coverage table gives d(surprisal)/dt ~ 40 bits/dex near
small t, and the H0 tension is 0.035 dex, so up to ~1.4 bits of
motion was derivable IN ADVANCE from numbers already in the
registration. An AGENTS item-8(a) miss, one layer up: the
detector null was derived but its derivative was not. The
substance is unaffected (a0 nets -0.03 to +1.03 bits across the
H0 pair, under the 3-bit flag either way); the sensitivity is
reported with its derived bound rather than scored, and no
re-registration is spent. Continuation of D-3's recorded path:
the census PRICES the 2 pi rather than deriving it, and the
price is zero net bits - which is itself the answer to how much
a derivation of the constant would be worth. Results:
scripts/experiments/p34_results.json.

## R-32 — 2026-08-29 — resolves P-2 (mixed; two value-bands fired, attributed)
Held: (a) disjoint totals, no negative widths, symmetry spot at
6e-17; (d) THE DIMENSION - removing tongues wider than r and
fitting log mu(r) over r in [3e-4, 3e-2] gives D = 0.879 for the
critical unlocked set, inside the registered [0.84, 0.90] and
0.009 from Jensen-Bak-Bohr's 0.870 - our P-29 tangency instrument
reproduces the classical fractal dimension. The substantive
sub-conditions of (b) and (c) also held: the subcritical locked
total converges (q<=32 to q<=40 delta 3e-9) with complement
0.80786 - positive measure, the KAM side - and the critical
complement decreases strictly across Q = 8..40
(0.424, 0.350, 0.310, 0.285, 0.268).
FIRED: the VALUE windows of (b) ([0.15, 0.60]) and (c) (< 0.12 at
q <= 40). Attribution: both were guessed, not derived - and the
derivable estimate was in the same script: the finite-Q
complement at criticality is dominated by unresolved q > Q
tongues at scale ~ sum phi(q) c/q^3, the same order as measured
(heuristic tail figure 0.19 vs measured 0.27; the c_max
proxy is itself not a true bound, which is the second lesson). A
value window at fixed Q was never the right observable; the
Q-scaling and mu(r) were. No post-hoc windows are derived to
rescore the same deterministic data; the firings stand as
instrument-band errors, third of their kind this week - the
AGENTS item-8 checklist now needs its corollary applied in
practice: EVERY numeric band, not only detector nulls, must trace
to a derivation or a pinned source.
Resolution of P-2 as registered: the non-smoothness at K = 1 is
real and measured (a fractal, measure-zero-trending complement
with D = 0.879 at criticality against a converged positive
complement 0.808 subcritically); the rigorous half is Swiatek's
theorem, imported in LC-25, not reproved; and the two-anchor
framing remains interpretive exactly as the 2026-08-20
registration predicted - no claim is filed on it. The oldest
dangling registration closes. Results:
scripts/experiments/p2_results.json.

## P-35 — 2026-08-29 — the reopened P-4: holonomy budget on a free ring
question: R-3's reopen recipe made concrete - on a FREE ring of N
inertial phase oscillators with one pi bond (loop intact), a
massless dead-load contact at the antipode (constant point force f,
soft-ramped; a velocity belt cannot reach the fold on a free ring
and stick-slip was the source of R-3's S2/S6 artifacts), low
damping, N in {64, 96, 128}: does the holonomy affect the
sector-slip onset BEYOND its derived static budget? The budget is
the quasi-static fold of the point-loaded ring, solved exactly in
the derive layer (scripts/experiments/p35_derive.py): fold ratio
twisted/control 0.96629 / 0.97782 / 0.98350 at N = 64 / 96 / 128,
an O(1/N) shift with derived sign and scaling - the quantity the
clamped model of P-4 destroyed. Kinematics the observables must
reach (derived): half-integer covariant winding sectors W = n - 1/2
and the half-integer spectral address of e^{i theta} (EQ1, EQ5);
ring reflection makes the two twisted sectors exactly degenerate,
so any measured sector split is a self-calibrating instrument
floor (EQ4).
method: protocol, cells, and clause bands in
notes/p35_free_ring.md, all fixed before any registered cell ran;
every band traces to the derive layer or to the measured
degeneracy floor (no guessed windows).
expects: (a) sector arithmetic exact at every sample (half-integer
twisted, integer control, integer slips); (b) onset ratio
f*(twisted)/f*(control) within fold_ratio(N) +- band(N),
band = 2 x grid / fold + split + 1e-4 (0.0075 at N = 64 with
split at one grid step) - i.e. NO dynamical selection beyond the
static budget; (c) sector split <= one grid step everywhere (the
instrument null); (d) the ratio stays in band under gamma x
{0.5, 2}; (e) the spectral address sits at n - 1/2 vs n at every
pre-onset sample. Absolute onset vs the fold is reported
unregistered (no derived transient band; P-2's lesson).
changes-my-mind: (b) violated with the same sign at all three N,
surviving both gamma variants and the independent
reimplementation in the verify falsifier - that would mean the
bundle class does dynamical selection, which is what P-4's
mind-change clause always meant.
not-claimed-in-advance: stick-slip friction, bowed strings, real
Josephson arrays; the slip-cascade regime beyond onset; any
statement about the clamped geometry (settled in R-3).
