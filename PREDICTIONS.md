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

## R-33 — 2026-08-29 — resolves P-35 (mixed; instrument, diagnosed not rescued)
Held: (a) sector arithmetic - covariant winding on the half-integer
lattice at 6.8e-13 (control, loaded) and 1e-16 (twisted) at every
sample; (c) sector degeneracy - the two twisted onsets split by
3.6e-5, three orders under the one-grid-step floor. Twisted onsets
landed at fold - 0.005 (one grid step below the derived fold), both
sectors, N = 64.
FIRED: (b) was UNMEASURABLE as registered - the control ring showed
no net-winding change at any grid level while its raw contact
strain diverged to 4.7e4: the control's supercritical motion is a
symmetric PAIRED slip (+2 pi and -2 pi through the two contact
bonds; the loaded node tears out and spins at ~ f/gamma), invisible
to a net-W detector BY SYMMETRY. (e) fired in all cells including
control (8 of 28 pre-onset address samples off): the spectral
address is a sector observable of the UNLOADED ring only - under
load the phase profile accumulates O(N) radians (8.3 rad at
half-fold, DFT peak already at -1/8) and the derive layer had
established the address only at equilibrium.
Attribution: two detector responses underived at registration -
the net-W response of the control's post-fold channel (8a) and the
loaded-ring address response (8a). Both are one-afternoon
derivations that existed the whole time; both are now in
scripts/experiments/p36_channel.py. What the diagnosis yielded is
better than what fired: the control fold has the closed form
2N/(N-1) (contact pair saturating together, solver agrees to the
bisection floor), the twisted loop constraint forces TOP-only
saturation (bottom sin -0.933/-0.956/-0.967 at N = 64/96/128), so
the holonomy SELECTS THE SLIP CHANNEL - paired and W-neutral
without the pi bond, single and W-changing with it. P-4's "which
orbits close on the base vs the double cover" returns as a derived,
registerable observable. Re-registered as P-36 with a channel-blind
detector replaced and the address clause demoted.
Results: scripts/experiments/p35_results.json (quick cells, N = 64).

## P-36 — 2026-08-29 — holonomy selects the slip channel (P-35 re-registered)
question: P-35's protocol (free pi ring, soft-ramped dead load at
the antipode, ground-state init, N in {64, 96, 128}, gamma 0.02
with {0.01, 0.04} variants at 64) with the detector the derive
addendum shows BOTH channels reach: a bond-slip event = any bond's
raw covariant strain leaving its initial value by more than 1.5 pi
(pre-fold bound: |e_j| < pi on the quasi-static branch; event
amplitude 2 pi; the margin is stated in EQ10). Channel classified
after a 120-unit settle: net W changed vs unchanged.
expects: (a) sector arithmetic as P-35(a) - held there,
re-registered unchanged; (b) onset ratio f*(twisted)/f*(control)
within fold_ratio(N) +- band(N), band = 2 x 0.005/fold + split +
1e-4, fold_ratio = 0.96629 / 0.97782 / 0.98350 at N = 64/96/128
(control fold now the closed form 2N/(N-1)); (c) sector split <=
one grid step; (d) the ratio stays in band at gamma = 0.01 and
0.04; (e) CHANNEL: the control's first event leaves net W
unchanged (paired), the twisted ring's first event changes W by
exactly +-1 (single) - derived in EQ8/EQ9 from which constraint
binds at the fold. Absolute onset vs fold stays unregistered.
changes-my-mind: (b) violated with the same sign at all three N,
surviving both gamma variants and the independent reimplementation
in the verify falsifier - the bundle class doing dynamical
selection beyond its strain budget. A violation of (e) - a
W-neutral first event on a twisted ring or a net first event on
control - would mean the channel derivation missed a competing
branch and fires the clause, not the mind-change.
not-claimed-in-advance: as P-35, plus supercritical cascade
statistics beyond the first event and its channel.

## R-34 — 2026-08-29 — resolves P-36 (as expected)
All five clauses held at every registered cell (three N, three
configurations, both gamma variants, the dt/2 validation):
(a) winding on its lattice at 1.3e-15 worst; (b) onset ratios
0.96620 / 0.98024 / 0.98594 at N = 64 / 96 / 128 against derived
fold ratios 0.96629 / 0.97782 / 0.98350, inside bands of ~0.005;
(c) sector splits 3.6e-5 / 2.4e-5 / 1.8e-5, three orders under
the floor; (d) gamma 0.01 ratio unchanged, gamma 0.04 at 0.96867,
in band; (e) the channel in every cell - control's first event
paired and winding-neutral (two contact bonds, dW = 0), each
twisted sector's first event a single slip with mirror dW = +1 /
-1. The mind-change condition did not fire: the bundle class does
NOT do dynamical selection beyond its derived static budget - but
the budget itself is real, O(1/N), and the holonomy picks which
channel breaks first. P-4's registered question, four ledger
entries later, has its answer: the threshold moves by exactly the
strain the pi bond pre-loads (the clamp had silently erased it),
and the "orbits on the base vs the double cover" half of the
question is the paired/single channel dichotomy, derived and
observed. Unregistered observation: onsets sit one grid step
below the fold at gamma <= 0.02 and on it at gamma = 0.04 - the
inertial transient nudges the marginal level over; the absolute
onset was left unregistered for exactly this reason.
Claim filed: holonomy-selects-the-slip-channel (verified;
falsifier scripts/verify/p36_free_ring.py, mutants channel-blind
and naive-budget). Results:
scripts/experiments/p36_results.json.

## R-35 — 2026-08-29 — resolves P-5 (as expected; bookkeeping closure)
outcome: as expected. LC-6 (2026-08-22) is the resolution's
substance and has been all along: the published literature contains
Milgrom's 1999 heuristic identification (a0 as the acceleration
where the Unruh temperature meets the de Sitter temperature), not a
derivation - no interpolating function, no BTFR normalisation, no
surviving relativistic completion follows from it. The claim
a0-tracks-hubble-conjecture stayed coincidence-unruled and gained
its literature pointer, exactly as registered. The mind-change
condition (a parameter-free derivation) did not fire; P-34/R-31
later priced the same coincidence at -0.03 net bits. This R entry
was simply never written - the omission was found by the
2026-08-29 fresh-context corpus audit (A-19 item 3) and is closed
here with no new computation and no change of any status.

## P-37 — 2026-08-30 — the price of a bit (A-11, the line P-24 reserved)
question: on rung 2 - the locked double well U = -(eps/2) cos 2
theta, eps = 1, overdamped with kT = D, the substrate whose
forgetting P-24 derived to the prefactor - what does writing one
bit cost, and does the measured (work, error) surface respect the
two rigorous floors while showing the repo-native WALL: the
substrate's own hop rate forbids slow writing? Protocol: V = U -
h(t) cos theta, h ramped 0 -> a -> 0 linearly over tau (closed
loop, Delta F = 0), Sekimoto work, error p = wrong-well occupancy
at commit t = tau, start in equilibrium (the unknown bit).
method: derive layer scripts/experiments/p37_derive.py, run and
committed BEFORE this entry (pins in p37_registration.json): the
floor W >= D[ln 2 - H(p)] (second law + coarse-graining
monotonicity, exact curve); the speed limit W >= D[ln 2 - H(p)] +
W_2^2/tau (thermodynamic optimal transport, mobility 1), with W_2
computed on the circle by the cut-scanned quantile method against
the EMPIRICAL commit sample - both bounds are theorems about
measured objects; the critical tilt h_c = 2 eps (wrong well
vanishes: V''(pi) = 2 eps - h), a grid {1.2, 2.4} straddling it;
the two-state frozen-Kramers overlay p_kin (magnitudes
UNREGISTERED, P-2's lesson - only the ordering is registered);
Jarzynski null-cell design condition (sig_W/D)^2 <= 0.5 at
M = 2000, adequacy shown in the layer (1.005 +- 0.029 and 0.990
+- 0.020); domain: dt = 0.002, tau grids {1..32}/{1..12} capped
at T_MFPT/5, M = 1500, seeds 20260830 + cell index; the four
wall cells (below) at M = 6000, deliberately at T/3 and T/2.
expects: (a) nulls - Jarzynski |<e^{-W/D}> - 1| <= 3 SE at the
two null cells; the dt/2 validation cell within 3 sqrt(2) SE;
(b) floor at EVERY cell: W_mean >= D[ln 2 - H(p_hat)] - 3 SE_W;
(c) floor plus speed limit at every cell: W_mean >= D[ln 2 -
H(p_hat)] + W_2^2(empirical)/tau - 3 SE_W; (d) THE WALL, scoped
to a = 2.4 with pre-registered pairs: p_hat(55) > p_hat(16) at
D = 0.22 and p_hat(32) > p_hat(12) at D = 0.28, each by >= 3
sigma combined at M = 6000 - error is non-monotone in tau because
the substrate forgets while you write (overlay gaps 0.0102 and
0.0149); (e) import - the fresh MFPT quadrature within the
printed precision (0.05) of both P-24 pins (verified in the
layer, registered as standing).
changes-my-mind: (b) or (c) violated beyond its band at any cell,
surviving the dt/2 protocol and the falsifier's independent
reimplementation. The bounds are theorems; a surviving violation
means the instrument's work-error bookkeeping is mis-derived, and
that failure would be the finding.
not-claimed-in-advance: optimal protocols; tightness or
saturation of either bound; quantum costs (the bounds coincide
but the prices differ - see LC-27); rungs 1 and 3; engineered
feedback or measurement-based erasure.

## R-36 — 2026-08-30 — resolves P-37 (mixed; one wall pair fired, attributed)
Held: (a) both Jarzynski nulls (0.9880 +- 0.0107, 0.9990 +-
0.0189) and the dt/2 cell (0.0487 vs 0.0469, band 0.0177);
(b) the Landauer-with-errors floor at all 26 cells; (c) the floor
PLUS the transport speed limit at all 26 cells - the measured
surface sits a factor 2.5-6 above the combined bound (this linear
ramp is far from optimal, as expected and not claimed); (e) the
P-24 pin import (0.0499 and 6.5e-5, both under the 0.05 printed
precision). The wall: at D = 0.22 the registered pair held -
error 0.0088 at tau = 16 vs 0.0150 at tau = 55, gap 0.0062
against 3 sigma = 0.0059 - writing slower COSTS FIDELITY because
the substrate forgets while you write; and the work meanwhile
FELL from 1.51 to 1.05: the tradeoff is real and priced.
FIRED: the D = 0.28 wall pair - gap 0.0053 at 1.9 sigma,
direction consistent, under the registered 3 sigma. Attribution:
the pair's power was budgeted from the Kramers overlay whose
magnitudes the registration itself refused to register; the
overlay's prefactor under-predicts the best-cell error at
eps/D = 3.6, and half the expected gap vanished. A design-power
error - the unregistered magnitude leaked into the DESIGN through
the M = 6000 choice; the R-32 corollary needs extending from
clause bands to power calculations. Not rescued: the clause
stands fired; the D = 0.28 direction is reported as consistent
and unregistered.
Also recorded: a readout-label bug found at the first run - the
right-well population was reported under the wrong-well name.
The floor clauses are insensitive (H(p) is symmetric), the wall
clause was re-read from the SAME seeded trajectories with the
registered definition, and the fix is a one-line readout change
committed with this entry. The mind-change condition did not
fire: both bounds held everywhere, surviving dt/2 and the
falsifier's independent reimplementation.
Claim filed: writing-a-bit-pays-its-floors (verified; falsifier
scripts/verify/p37_price_of_bit.py, mutants half-work and
entropy-blind). Results: scripts/experiments/p37_results.json.

## P-38 — 2026-09-01 — the Hardy-order bridge (A-21, the earned frontier)
question: van der Lugt & Ormrod (Quantum 8, 1543 (2024)) give a
POSSIBILISTIC, GHZ-style proof that the quantum switch's causal
order is indefinite - Hardy's logical template applied to causal
order. The earned re-derivation: does our own simulation of their
three-switch GHZ scenario (controls GHZ-entangled, switches
X-controlled, agents measure-and-reprepare on x = 1, a Y
measurement on the outgoing control) reproduce the four parity
implications possibilistically - forbidden events at zero, not
merely small - and does exhaustive enumeration of deterministic
local-order strategies certify the classical ceiling their
imported reduction theorem needs?
method: derive layer scripts/experiments/p38_derive.py, run and
committed BEFORE this entry (pins in p38_registration.json): own
64-dim stdlib simulation; all 4096 deterministic per-switch
response strategies enumerated; the Mermin functional on the four
patterns; item-8 nulls (normalization, a no-signalling marginal
check making relativistic causality a verified property of the
data, and the definite-wiring control showing the coherence is
load-bearing). The reduction from definite causal order +
relativistic causality + free choice to the enumerated class is
IMPORTED (their Theorem 1; LC-28), not reproved.
expects: (a) the four parity conditions hold with total forbidden
probability mass <= 1e-14 per pattern and each pattern
normalized to 1 +- 1e-12; (b) the allowed outcomes are UNIFORM:
32 outcomes at 1/32 (XXX pattern), 8 at 1/8 (each Y pattern),
every allowed probability within 1e-12 of its value; (c) the
exhaustive ceiling: no strategy satisfies 4 conditions, the
maximum is 3, and the satisfaction histogram is {1: 2048,
3: 2048} - odd counts only, the parity signature; (d) Mermin
functional: classical max = 2 (exhaustive), switch value = 4 =
the algebraic maximum - "maximal indefiniteness" in
ladder-priced form; (e) nulls: no-signalling marginal invariance
<= 1e-12; the definite-FE world satisfies the XXX condition and
puts violation mass 1/2 +- 1e-12 on each Y-pattern condition.
changes-my-mind: any clause failing under the falsifier's
independent reimplementation (X-basis branch expansion, its own
enumeration encoding) - a surviving nonzero forbidden mass would
mean the possibilistic reading of the switch is wrong as
computed, and would be reported as our error or the paper's,
whichever the diagnosis supports.
not-claimed-in-advance: experimental realizations; the
gravitational-switch discussion in the same paper; the reduction
theorem itself (imported); fixed-order inequalities (the scan's
refused candidate stays deferred); any statement about
single-switch scenarios (their Appendix D shows one switch does
not suffice - imported context, not rederived).

## R-37 — 2026-09-01 — resolves P-38 (as expected)
All five clauses held; numbers pasted by script from
p38_results.json. (a) forbidden parity mass 0.0 - the true zero
of the amplitude structure, not a small float - at every pattern,
totals at 1e-16 of unity; (b) allowed outcomes uniform: 32 x 1/32
(XXX), 8 x 1/8 (each Y pattern); (c) the exhaustion: 4096
deterministic local-order strategies, maximum 3 of 4 conditions,
histogram {1: 2048, 3: 2048} - only odd satisfaction counts
occur, the parity signature; (d) Mermin functional: classical
max 2, switch value 4 = the algebraic ceiling - van der Lugt &
Ormrod's "maximal" statement lands in the ladder-priced form the
repo already speaks; (e) no-signalling marginal invariance at
2.8e-17 and the definite-wiring control satisfying the XXX
condition while dumping violation mass exactly 1/2 on each
Y-pattern condition - the coherence is load-bearing, the
bookkeeping alone reproduces nothing. The falsifier's independent
route (X-basis branch expansion: the x = (1,1) switch reveals its
branch sign in a1; the revealed sign conditions the remaining
controls into a Bell pair whose Y-parity is fixed) reproduces
every clause with different mathematics. The mind-change did not
fire. The Hardy-order bridge is EARNED: Hardy's possibilistic
template, which this ledger first met as P-21's phi^-5 maximum,
now runs on causal order itself - the graph's two earned clusters
are joined by computation, not citation. Claim filed:
switch-parity-ceiling. Results:
scripts/experiments/p38_results.json.

## P-39 — 2026-09-01 — the alpha-family (A-22, the earned frontier)
question: Liu & Chiribella (Nat. Commun. 16, 3314 (2025)) proved
the ICO Tsirelson bound for the biased OCB correlation I_alpha =
P(a1=b|c=0) + alpha P(a2=x1|c=1): B(alpha) = (1 + alpha +
sqrt(1+alpha^2))/2, geometrically a circle of radius 1/2 around
(1/2, 1/2) with the causal square inscribed. A-20 imported the
alpha = 1 point as a graph edge. The earned extension: does P-30's
instrument family - exhaustive causal enumeration and the OCB
process machinery - reproduce BOTH sides across the family: the
causal value C(alpha) = max(1 + alpha/2, 1/2 + alpha) by exact
exhaustion, and the bound B(alpha) as ACHIEVED by a process family
we construct ourselves, the theta-rotated W(theta) = (1/4)[1 +
cos(theta) sz^A2 sz^B1 + sin(theta) sz^A1 sx^B1 sz^B2]?
method: derive layer scripts/experiments/p39_derive.py, run and
committed BEFORE this entry (pins in p39_registration.json): 8192
deterministic one-way-signalling strategies in Fraction
arithmetic; W(theta) validity via P-30's checks (spectrum, trace,
the no-causal-loop trace-and-replace identity); full-contraction
probabilities in OCB's eq. 20-23 conventions with the game roles
determined by computation (a role mis-assignment in the layer's
first pass produced value 1.0 at alpha = 1 and was caught against
P-30's pinned (2+sqrt2)/4 - recorded, the layer doing its job).
The upper-bound proof is IMPORTED (LC-29), the achieving family
and both curves are earned.
expects: (a) enumerated C(alpha) equals the closed form EXACTLY
(rationals) on the grid alpha in {0, 1/4, 1/2, 3/4, 1, 3/2, 2,
4}; the extreme points (1, 1/2) and (1/2, 1) occur; the
(P_A, P_B) point set has exactly 9 elements; (b) W(theta*) at
every grid alpha: spectrum {0 x8, 1/2 x8} at 1e-9, Tr = 4 at
1e-10, the no-loop identity at 1e-10; (c) the achieved value sits
on the imported bound at 1e-11 at every grid alpha; (d) geometry:
the four causal extreme points on the circle at 1e-12; advantage
B - C equal to 0 at alpha = 0, positive at every grid alpha > 0,
grid-maximal at alpha = 1 with value (sqrt2 - 1)/2 at 1e-12.
changes-my-mind: any clause failing under the falsifier's
independent Pauli-basis route (no matrices - trace orthogonality
bookkeeping) and its own enumeration encoding.
not-claimed-in-advance: the upper-bound proof (imported); GYNI /
LGYNI (numerical SDP values, the scan's caveat); multipartite
generalizations; optimality of the OCB local strategies among all
local operations (that is part of the imported theorem).

## R-38 — 2026-09-01 — resolves P-39 (as expected)
All four clauses held; numbers from p39_results.json. (a) the
8192-strategy exhaustion lands on C(alpha) = max(1 + alpha/2,
1/2 + alpha) EXACTLY at all eight grid rationals; the causal
(P_A, P_B) set has exactly 9 points including the extremes
(1, 1/2) and (1/2, 1); (b) every W(theta*) is a valid process
(spectrum {0 x8, 1/2 x8}, Tr = 4, the no-causal-loop identity) -
the rotation never leaves the process cone; (c) the achieved
values sit on the imported bound with worst gap 2.1e-12 across
the grid: the theta-rotated OCB family TRACES the Tsirelson
circle, so achievability is earned for the whole family, not
imported at one point; (d) the causal extremes lie on the circle
at machine zero (the square is inscribed), the advantage is 0 at
alpha = 0 exactly, positive at every grid alpha > 0, and
grid-maximal at alpha = 1 with value (sqrt2 - 1)/2 at 1e-16 -
the unbiased game is where indefinite causal order buys the most,
and the bias kills the advantage smoothly toward both ends. The
falsifier reproduces everything through the Pauli-orthogonality
route (no matrices) and its own enumeration encoding. One
instrument error is on record from the layer: the first pass
mis-assigned the game roles (guesses vs inputs) and produced
value 1.0 at alpha = 1 - caught immediately against P-30's pinned
(2+sqrt2)/4. The mind-change did not fire. The A-20 theorem edge
upgrades to EARNED across the family. Claim filed:
biased-ocb-on-the-circle. Results:
scripts/experiments/p39_results.json.
## P-40 — 2026-09-01 — gap openings at the approximants (A-23, the earned frontier)
question: Band, Beckus & Loewy (arXiv:2402.16703) proved Dry Ten
Martini for Sturmian Hamiltonians: every labeled gap is open at
every nonzero coupling. A-20 imported this with only the
trace-map engine as its runnable check. The earned upgrade: at
the periodic approximants of the Fibonacci Hamiltonian (period
q = F_m, exact rational rotation words), do our own instruments
show every one of the q - 1 labeled gaps OPEN, with the label
arithmetic exact and the instrument tied to the theorem's engine?
method: derive layer scripts/experiments/p40_derive.py, run and
committed BEFORE this entry (pins in p40_registration.json):
discriminant Delta(E) by transfer product, band edges as the 2q
simple roots of Delta^2 - 4 (scan + bisection at 1e-13; a closed
gap would produce a double root and break the simple-root count,
so the count is the closed-gap detector - 8a); exact letter
counts; exact modular-inverse labels; the trace-map recursion
verified on substitution words at machine precision and the
rotation word tied to the substitution word by trace equality
(a letter-map complement error in the layer's first pass broke
the tie at O(1) and was caught - recorded). Validation at q in
{8, 13, 21}: min gap widths 0.012-0.13, three-plus orders above
the registered floor (8c: floor validated, not guessed).
expects: at every registered cell - q in {34, 55, 89, 144},
lambda in {1.0, 2.0}: (a) instrument integrity: exactly 2q simple
edges, q disjoint bands with |Delta| <= 2 at midpoints and > 2 in
gap midpoints; (b) ALL q - 1 gaps open with width > 1e-6 (the
validated floor, seven orders above resolution); (c) the label
map k -> s with s F_{m-1} = k (mod F_m), |s| <= q/2, is an exact
bijection; (d) the trace-map recursion and the rotation-tie hold
at 1e-9 at the registered (lambda, E) samples.
changes-my-mind: a registered cell with a genuinely closed or
below-floor labeled gap, surviving the falsifier's independent
route (band edges as periodic/antiperiodic eigenvalues via the
pinned cyclic-Jacobi kernel, no discriminant scan) - that would
contradict the imported theorem's approximant shadow and be
reported as our instrument error or a real tension, whichever
the diagnosis supports.
not-claimed-in-advance: the quasiperiodic limit itself and
arbitrary coupling (the theorem, imported LC-30); gap-width
scaling laws in q or lambda (reported unregistered); other
Sturmian frequencies.

## R-39 — 2026-09-01 — resolves P-40 (mixed; the detector fired, diagnosed)
Held: (b) every measurable cell has all q - 1 labeled gaps open
with margin (min widths 4.5e-3 / 1.7e-3 / 6.2e-4 at q = 34 / 55 /
89, floors cleared by 600x at worst); (c) the label bijections
exact at all four q; (d) the trace-map recursion and rotation-tie
at machine precision.
FIRED: (a) at three of eight cells - q89/lam1.0 found 176 of 178
edges, q144 found 286 and 270 of 288. Diagnosis: the scan
detector undersamples - a NARROW BAND falling between two scan
points leaves Delta dipping through the |2| line and back with no
sign change at the samples, deleting BOTH its edges. The scan
density (60 q points) was validated at q <= 21 where the
narrowest band is wide, and never derived from the narrowest band
it must resolve at the registered q - the R-36 lesson (power and
resolution budgets must trace to derived or validated quantities
at the REGISTERED cells, not the validation cells) repeated in a
spectral costume. Not rescued: the three cells stand unmeasured
under this instrument. Re-registered as P-41 with a
certified-complete detector: band edges as the eigenvalues of the
periodic and antiperiodic q x q operators - a route that cannot
miss a band because every edge IS an eigenvalue - with the
discriminant retained as a cross-check at midpoints only.
Results: scripts/experiments/p40_results.json.

## P-41 — 2026-09-01 — gap openings at the approximants (P-40 re-registered)
question: P-40's question with the detector the diagnosis
demands: at q = F_m in {34, 55, 89, 144}, lambda in {1.0, 2.0},
are all q - 1 labeled gaps open?
method: band edges = eigenvalues of the periodic (corner +1) and
antiperiodic (corner -1) tridiagonal operators via the pinned
kernels eigensolver; bands = consecutive pairs of the sorted
union (standard interlacing); the discriminant now serves as
CROSS-CHECK only (|Delta| <= 2 at band midpoints, >= 2 at gap
midpoints, and every periodic eigenvalue has Delta = +2, every
antiperiodic Delta = -2, at 1e-6). Everything else carries over
from P-40's layer unchanged: the floor 1e-6, the exact labels,
the trace-map tie.
expects: (a) integrity: 2q edges from the eigen-route at every
cell, bands disjoint, the discriminant cross-checks pass; (b) all
q - 1 gaps open above the floor at every cell; (c) label
bijections exact; (d) trace clauses as P-40(d).
changes-my-mind: as P-40, with the falsifier's independent route
now an OWN Sturm-sequence bisection eigensolver (not the pinned
kernel, not a scan).
not-claimed-in-advance: as P-40.

## R-40 — 2026-09-01 — resolves P-41 (as expected)
All four clauses held at all eight cells; numbers from
p41_results.json. (a) the eigen-route found every edge - 2q at
every cell, including the three cells the P-40 scan could not
measure - with the discriminant cross-checks at 3.3e-11 worst
(every periodic eigenvalue sits on Delta = +2, every antiperiodic
on Delta = -2, and the midpoint conditions hold); (b) ALL labeled
gaps open at every cell: min widths 4.5e-3 / 1.7e-3 / 6.2e-4 /
2.3e-4 at q = 34 / 55 / 89 / 144, the smallest still 230x above
the validated floor; (c) label bijections exact at all four q;
(d) trace-map recursion and rotation-tie at machine precision.
The mind-change did not fire. The Dry Ten Martini import now has
an earned approximant shadow: at every computed approximant and
both couplings, every gap the labeling theorem allows is open -
computed, not cited. The narrowing trend (min width roughly
halving per Fibonacci step) is reported unregistered. Claim
filed: approximant-gaps-all-open. Results:
scripts/experiments/p41_results.json.

## P-42 — 2026-09-01 — the switch's data is GHZ's data; its half is not the ring's half
question: two identity questions from the theoretical press,
lessons L-9 consulted. (1) Is P-38's switch empirical model,
restricted to the registered contexts, EXACTLY the GHZ model
tensored with deterministic copies and independent fair coins? If
so, indefinite causal order contributes no correlations in this
scenario - the entire content is which hidden-variable class the
data excludes, and resource-language conflates data with causal
hypothesis. (2) Do the switch's parity 1/2 and the pi ring's
winding 1/2 differ by the Abramsky-Brandenburger criterion -
global-section existence - making their identification a REFUSAL?
method: derive layer scripts/experiments/p42_derive.py, run and
committed BEFORE this entry (pins in p42_registration.json): own
3-qubit GHZ computation at the four paradox contexts; P-38's
switch joints marginalized; exact factorization test on the full
outcome space; the AvN system's GF(2) ranks in integer
arithmetic; the ring's ground-state section recomputed. The AvN
-> nonvanishing-cohomology implication is IMPORTED (LC-31,
Abramsky-Brandenburger-Barbosa), not reproved.
expects: (a) switch marginals equal the GHZ model with worst
difference <= 1e-14 per outcome per context; (b) the remainder
factorizes EXACTLY: equal completion counts per GHZ triple and
conditional uniformity with worst nonuniformity <= 1e-14 (the
counts themselves pinned: 8 completions at XXX, 2 at each Y
pattern); (c) AvN: coefficient rank 3, augmented rank 4 over
GF(2) - inconsistent, exact integers; (d) the ring section:
uniform covariant strain with spread <= 1e-12 and winding within
1e-12 of -1/2 - a global section exists, so the ring's half
carries ZERO contextual obstruction while the switch's carries a
nonzero one (by (c) + the import); the identification of the two
halves is REFUSED.
changes-my-mind: (a) or (b) failing beyond band under the
falsifier's independent routes (stabilizer-identity GHZ; the
X-basis branch route for the switch) - a real difference between
the models would be reported as the discovery it would be.
not-claimed-in-advance: resource-theoretic statements beyond this
scenario (other switch protocols may generate non-GHZ
correlations); the cohomology computation itself (imported
implication); any claim about experimental switches.

## R-41 — 2026-09-01 — resolves P-42 (as expected)
All four clauses held. (a) The switch triple-marginals equal the
GHZ empirical model with worst difference 1.4e-16 - the two data
sets are THE SAME at machine zero. (b) The remainder factorizes
without residue: completion counts (8, 2, 2, 2) as pinned,
conditional nonuniformity 0.0 - the switch scenario's data is GHZ
tensored with deterministic copies and exactly fair coins.
(c) AvN over GF(2): coefficient rank 3, augmented rank 4 -
inconsistent, so (imported AB-Barbosa) the contextual obstruction
is nonzero. (d) The ring's half is one globally consistent
configuration (strain spread 2.2e-15, winding -1/2 at 1e-13) -
zero obstruction. The mind-change did not fire. READINGS: (1) in
this scenario indefinite causal order contributes no correlations
whatsoever; every bit of novelty lives in WHICH hidden-variable
class the same GHZ data excludes - definite orders here, local
states there - and resource language that does not say so
conflates data with causal hypothesis; (2) the graph's two halves
are hereby REFUSED as one object: the switch's half is a
no-global-section obstruction, the ring's half is a global
section's topological label. Same numeral, different mathematics.
Falsifier routes: stabilizer identities (the four signed contexts
live in the GHZ group of size 8) and the X-basis branch expansion.
Claim filed: switch-data-is-ghz-data. Results:
scripts/experiments/p42_results.json.
## P-43 — 2026-09-01 — the shadow is the same square; the bodies are not
question: Liu-Chiribella remark their causal-vs-ICO picture
'coincides' with the CHSH picture. Is the coincidence an affine
isomorphism of the underlying polytopes, or only of a
two-dimensional shadow? Item 2 of the theoretical press; lessons
L-8 consulted.
method: derive layer scripts/experiments/p43_derive.py, run and
committed BEFORE this entry (pins in p43_registration.json): both
polytopes' vertex sets from exhaustive deterministic strategies
(0/1-valued conditional distributions are extreme, so vertices =
deduped strategies); affine dimensions by incremental Fraction
elimination; the two shadows and their extreme points in exact
rationals; the CHSH quantum circle achieved CONSTRUCTIVELY
(closed-form singlet settings landing on (cos phi, sin phi) at
machine epsilon - an earlier 4-angle hill-climb stalled at
cos(pi/12) and was replaced by the construction, recorded); disc
completeness IMPORTED (LC-32), mirroring P-39's split.
expects: (a) local CHSH polytope: 16 vertices, affine dimension 8
(exact); (b) causal OCB polytope: 2368 vertices, affine dimension
24 (exact - the registration's pins); (c) REFUSAL: the pairs
differ in both invariants, so no affine isomorphism exists - the
coincidence is a shadow, not a body; (d) the shadow identity is
EXACT: causal extremes {(1,1/2),(1/2,1),(0,1/2),(1/2,0)} on the
radius-1/2 circle, CHSH extremes {(+-1,0),(0,+-1)} on the unit
circle, and T(u,v) = ((u+1)/2,(v+1)/2) carries one set onto the
other as rationals; the constructive settings land on the circle
at 1e-12 across the phi grid.
changes-my-mind: (a) or (b) pins failing under the falsifier's
independent elimination and encodings - a matching (dim, V) pair
would reopen the isomorphism question and be handed to a deeper
invariant, reported as such.
not-claimed-in-advance: facet structure and deeper combinatorial
invariants (vertex counts and dimensions suffice for the refusal;
nothing further is computed); the completeness of either quantum
disc (imported); multipartite scenarios.

## R-42 — 2026-09-01 — resolves P-43 (as expected)
All four clauses held. (a) Local CHSH polytope: 16 vertices,
affine dimension 8, exact. (b) Causal OCB polytope: 2368
vertices, affine dimension 24, exact - the pins land. (c) The
REFUSAL: (16, 8) vs (2368, 24) - no affine isomorphism exists
between the bodies; Liu-Chiribella's 'coincidence' with the CHSH
picture is a genuine identity of the two-dimensional SHADOW and
nothing more. (d) The shadow identity is exact: four extreme
points on each circle, carried onto each other by
T(u,v) = ((u+1)/2, (v+1)/2) as rationals, and the CHSH circle
achieved constructively (closed-form singlet settings on
(cos phi, sin phi) at 1.1e-16; the abandoned hill-climb that
stalled at cos(pi/12) is recorded in the layer - a flat 4-angle
landscape defeating per-coordinate steps, replaced by
construction rather than by a better search). The mind-change did
not fire. Reading: the square-in-circle picture is a low-
dimensional UNIVERSAL of two very different convex bodies - the
right conflation-guard is now computed: same shadow, different
objects, like the halves of R-41. Claim filed: shadow-not-body.
Results: scripts/experiments/p43_results.json.

## P-44 — 2026-09-01 — the Jin engine corroborated (scope: instrument, not proof)
question: Jin's claimed proof of Crouzeix's conjecture
(preprints.org 202607.1919.v4) rests on new intermediate objects
- the mass-2 numerical-range double layer, a matrix Caratheodory
completion with its defect confined to the adjoint algebra, an
exact sampling cancellation, and an ordered-Gramian chain
I <= P~ <= 2I forcing ||T|| <= 2. A fresh-context survey agent
hand-verified the argument and built a stdlib verification layer
(committed as p44_spotcheck.py / p44_ellipse.py, provenance
noted). The registered question: do those NEW objects verify
numerically under seeded, legitimate, exhaustively-checked
instances, with the inequality exactly tight at the known
extremizer? SCOPE: this corroborates the manuscript's engine; it
does NOT verify the proof. The proof's status is imported (LC-33:
the manuscript; the independent Lorist-Schwenninger proof;
expert endorsements; the audited Lean covering the mass-2
endpoint). Lessons L-7, L-8, L-9 consulted.
method: derive layer = the survey scripts rerun and pinned
(mass defects 5e-15 / 7e-15; ellipse membership discrimination
7e-13 vs 6e-2; cancellation 1e-11; 400-instance hunt clean; ramp
tight from the correct side). Registered runner
scripts/experiments/p44_gramian.py with seed 20260901. The
ellipse carries the membership clause because the DISK silently
trivializes the adjoint-algebra defect (the survey's own trap,
recorded).
expects: (a) mass defects <= 1e-13 on disk and ellipse, density
samples PSD at -1e-12; (b) Caratheodory (eigmin ReH >= -1e-9) and
membership discrimination: right-basis offdiagonal <= 1e-9,
wrong-basis >= 1e-2, on the ellipse; (c) the Gramian chain over
400 fresh legitimate instances (n in 2..5, condition to 1e3):
eigmin(2G-P)/|G| >= -1e-9, eigmin(P-G)/|G| >= -1e-9, k=1 slack
>= -1e-9, and ||T|| <= 2; (d) extremal tightness on the
near-Jordan ramp: ||T|| >= 1.999 at eps = 0.01 with the 2G-P
slack positive, strictly decreasing along the ramp, and <= 1e-6
at the end - saturation from the correct side; (e) the
Psi-cancellation at 1e-9 and the sampled Gram PSD at -1e-7
(ellipse).
changes-my-mind: a single legitimate instance violating (c)
beyond band, surviving the falsifier's independent small-n route
- that would refute Theorem 2 + Proposition 1 jointly and be
reported upstream as such; conversely nothing here can PROVE the
manuscript, and the claim's scope says so.
not-claimed-in-advance: the proof's correctness (imported
status); the completely-bounded Crouzeix conjecture (open, noted
in LC-33); the mass-m generalization beyond spot dimension; any
Lean statement (the audit repo's scope).

## R-43 — 2026-09-01 — resolves P-44 (as expected; one runner error fixed against the pinned instrument)
All five clauses held. (a) Mass two on both domains (disk 4.9e-15,
ellipse 1.0e-14; density samples PSD). (b) Caratheodory holds
(eigmin ReH >= 0.947) and the adjoint-algebra membership
discriminates at TEN ORDERS on the ellipse (right basis 1.4e-12,
wrong basis 6.0e-2) - the domain where the defect is nonscalar,
per the survey's own recorded trap. (c) The Gramian chain
I <= P~ <= 2I and the k = 1 term clean over 400 seeded legitimate
instances (worst slacks 3.4e-13 / 2.1e-24 / -1.3e-16 within
band), ||T|| max 1.039. (d) Extremal tightness: on the pinned
near-Jordan family, ||T|| = 1.9996 at eps = 0.01 with the 2G-P
slack positive, strictly decreasing (9.7e-3 -> 4.0e-8), and
saturating from the correct side. (e) Psi-cancellation at 1.0e-11
and the sampled Gram PSD. One implementation error is on record:
the runner's first draft substituted its own Jordan family
([[0,1],[0,eps]], radius 1/2 + O(eps)) for the derive layer's
pinned one ([[eps,1],[0,-eps]], radius 1/2 + O(eps^2)) and fired
clause (d) at ||T|| = 1.980 - an L-9 lesson repeated inside the
very line that consulted it; restored to the registered
instrument, one-line fix, dynamics of nothing changed. The
falsifier reruns the chain with closed-form 2x2 eigenvalues, a
literal fixed instance, its own scalar-mass quadrature, and two
deterministic mutants. The mind-change did not fire - and by
scope, nothing here proves the manuscript: the corroboration is
of the ENGINE. Claim filed: jin-engine-corroborated. Results:
scripts/experiments/p44_results.json.

## P-45 — 2026-09-01 — ring energy continuity: the slip footprint as a derived current
question: the P-35/P-36 inertial pi ring (theta_dd_j = -gamma v_j
+ sin D_j - sin D_{j-1} + f delta_{jb}, D_j = theta_{j+1} -
theta_j - A_j, the p36_ring.py instrument unchanged) carries an
exact local energy-continuity identity in the lattice
heat-transport convention (LC-34: Lepri-Livi-Politi 2003 eqs. 11
and 17 with V = 1 - cos D, F = -sin D): with site energy
h_j = v_j^2/2 + (u_{j-1} + u_j)/2, u_j = 1 - cos D_j, and bond
current J_j = -(1/2) sin(D_j) (v_j + v_{j+1}),
  dh_j/dt + (J_j - J_{j-1}) = -gamma v_j^2 + f v_j delta_{jb},
local change plus current divergence equals local dissipation
plus local injection, and summed over the ring the current
telescopes to dE/dt = f v_b - gamma sum v^2. This is the L-2 move
for the slip aftermath: the "footprint" of a slip stops being a
description of where excess energy sits and becomes the
integrated divergence of a derived current - a bookkeeping
observable with an exact null. Registered question: does the
identity hold at the floating-point floor over random states of
both rings, does A enter only through D (no seam term at the pi
bond), and does the P-36 integrator's discrete balance converge
at first order on the registered grid and through the slip?
method: derive layer scripts/experiments/p45_derive.py with
p45_derive.json, everything measured before this entry was
written. (i) Residual bound: the residual at a random state is
evaluated by the chain rule from the EOM (no dt anywhere,
species-two zero) in ~30 rounded double operations on terms whose
absolute sum T_j is computed alongside; the registered bound is
32 eps T_j (eps = 2^-52), the floating-point floor scaled by the
state's own term magnitudes, so it tracks the velocity scale
automatically; the layer reads worst ratios 0.037 (site), 0.034
(seam), 0.023 (global) at both vmax = 2 and vmax = 100 over 80k
states. (ii) Mutants verified failing before pinning (L-8):
current-blind (J = -sin(D_j) v_j, no average) fails per site at
O(1) (3.5) on both rings but is INVISIBLE to the global balance
(its residual telescopes away too: 3.6e-15), which is why the
site-resolved clause is the load-bearing one; sink-blind (drop
gamma v^2) fails per site at gamma v^2 (0.08) and globally at
O(1) (2.16); gauge-blind (u from theta_{j+1} - theta_j, A
dropped) is identical to the clean identity on the control ring
(1.3e-15) and fails only at the two seam sites of the twisted
ring at O(1) (3.6) - the deterministic seam-only signature of
"A enters only through D". (iii) Discrete balance: under
Euler-Cromer in the P-36 update order, injection is the exact
work of the load over the step (f dt v'_b), dissipation
gamma dt v'^2, current post-step; the defect D(dt) = sup over
unit samples of |E(t) - E(0) - W_inj + W_diss| is first order,
D = C dt + O(dt^2), ratio r = D(dt)/D(dt/2) = 2 + O(dt). Per L-3
the registered observable is the convergence, not a value at a
resolution: monotone decrease along dt, dt/2, dt/4 with both
ratios inside the ORDER-DISCRIMINATION band [2^0.5, 2^1.5] - the
geometric midpoints between a first-order scheme's 2 and its
neighbours 1 (no convergence) and 4 (second order); order is
discrete, so the midpoint band is the derived classifier.
Validation cells pinned: smooth (control N = 64 at fold - 0.10,
dt = 0.02 ladder) r1 = 2.0001, r2 = 2.0001 global and local;
rotor (control N = 16 at fold + 0.02, dt = 0.001 ladder,
event at 206 in all three) r1 = 2.0093, r2 = 2.0051 global,
2.0016, 2.0017 local. Contraction of |r - 2| itself is at noise
level in the rotor cell (1.6e-3 vs 1.7e-3) and is therefore
REPORTED, not registered - the clause that would have fired on
instrument grounds was removed by the derive layer, which is what
the layer is for. (iv) Step size for the slip (8c): the torn-out
node spins at ~ f/gamma ~ 100, so the slip ladder starts at
dt0 = 0.001 (0.098 rad per step at that speed), four rungs below
P-36's 0.02, which advanced the rotor by ~2 rad per step. (v)
Slip cell chosen at f = fold + 0.005, the first P-36 grid level
ABOVE the derived twist0 fold: no equilibrium exists there, so
the event's existence is dt-independent (P-36's onset one grid
step below the fold was an inertial-transient effect and could
vanish under refinement). Lessons consulted: L-2 (the whole
point), L-3 (the ratio band pinned/derived, not guessed), L-8
(mutants verified), L-4/L-5 surfaced and not applicable (no
statistical power clause; no ladder in q). Registered runner
scripts/experiments/p45_continuity.py, seed 20260902.
expects: (a) over one million random states at N = 64 (control
and twisted rings, 400k each at vmax = 2 and 100k each at
vmax = 100; f = the slip-cell load, gamma = 0.02), every site
residual of the identity is within the bound 32 eps T_j (worst
ratio <= 1); (b) the global balance dE/dt = f v_b - gamma sum v^2,
computed from E directly (a different code path from the site
sum), and the telescoping sum of the current divergence are each
within their bounds 32 eps T at every state (worst ratios <= 1);
(c) twist invariance: on the twisted ensembles the two seam sites
the pi bond touches sit at the same bound as every other site
(worst seam ratio <= 1); (d) on the P-36 grid pre-onset -
{control, twist0, twist1} x N in {64, 96, 128}, f = fold - 0.10,
ramp 200, hold 100 - the global and the site-resolved sup-defects
both decrease monotonically along the dt = 0.02 / 0.01 / 0.005
ladder with both successive ratios in [2^0.5, 2^1.5] (first
order, discriminated from orders 0 and 2); (e) at the slip cell
(twist0, N = 64, f = fold + 0.005, ramp 200, run to the P-36 event
plus 40 units) the event occurs at every rung of the dt = 0.001 /
0.0005 / 0.00025 ladder and the global and site-resolved
sup-defects converge as in (d) THROUGH the slip - so the
site-resolved decomposition (stored, in-flowed, dissipated,
injected) is a resolved observable at the loaded site and its
neighbours. Reported unregistered: the aftermath footprint at
event + 40 (peak excess site energy, the 10-percent radius, the
excess profile by offset from the load) and the loaded site's
four-way decomposition; the ratios' deviations from 2 against the
pinned validation values.
changes-my-mind: (a) or (b) violated at any state, surviving the
falsifier's independent implementation - the identity as written
would be wrong (an algebra error in the derive layer, recorded as
such and re-derived). (c) violated with (a) held - A would enter
somewhere other than through D, a seam term the derivation
missed. (d) or (e) firing with (a)-(c) held is an INSTRUMENT
statement about the Euler-Cromer bookkeeping or the step size,
not about the identity; it costs a re-registration per AGENTS 8,
not a mind-change.
not-claimed-in-advance: any statement about the slip aftermath's
SHAPE (the footprint radius, the excess profile, the fraction of
injected energy that leaves the loaded site) - those are read off
and reported, with wavebench recording of aftermaths against this
current queued as the follow-up; thermal transport, Fourier's law
or conductivity of the ring (LC-34's context, not its claim);
anything about the overdamped P-37 substrate (Sekimoto's
convention covers it and is already cited at LC-27); Kibble-Zurek
counting on the pi ring (queued separately).

## R-44 — 2026-09-01 — resolves P-45 (as expected)
All five clauses held. (a) One million random states (400k control
and 400k twisted at vmax = 2, 100k each at vmax = 100): worst
per-site residual 0.042 of the bound 32 eps T_j (absolute 2.2e-15
at vmax = 2, 1.7e-13 at vmax = 100 - the bound tracked the scale,
as designed). (b) Global balance from E directly at 0.024 of its
bound; telescoping sum at 0.0086 of its bound. (c) The twisted
ring's seam sites at 0.033 of the bound - no seam term, A enters
only through D. (d) All nine grid cells (three configurations x
N = 64, 96, 128, pre-onset at fold - 0.10): global and per-site
sup-defects 1.2e-2 to 2.3e-2 at dt = 0.02, halving at each rung
with every ratio between 2.0000 and 2.0002, inside the order-one
band and on top of the pinned smooth validation value 2.0001.
(e) The slip cell (twist0, N = 64, fold + 0.005): the P-36 event
at t = 217.0 at all three rungs of the dt = 0.001 ladder; global
sup-defect 4.46e-2 / 2.21e-2 / 1.10e-2 (ratios 2.0144, 2.0072),
per-site 7.11e-2 / 3.53e-2 / 1.76e-2 (ratios 2.0151, 2.0081) -
first order THROUGH the tear-out, and here the deviation from 2
does contract (reported: the rotor validation cell's non-
contraction was the small-N case at a coarser effective
resolution, the registered cell's ratios sit 4x further from 2
and halve cleanly). The decomposition is therefore a resolved
observable, and it reads, at event + 40 on the loaded site:
injected 2827.6, dissipated on the site 1075.5, out-flowed into
the ring through the two adjacent bonds 182.1, stored (kinetic,
the rotor) 1569.9; ring-wide, E rose by 1585.8 = 2827.6 injected
minus 1241.8 dissipated - the 182 that left the loaded site was
dissipated in the ring (166.3) and stored there (15.8). The
figures agree across the three rungs to four digits. Unregistered
footprint at event + 40 (peak excess site energy relative to the
last pre-event sample): peak 1566 at the loaded site, 10-percent
radius ZERO; every other site sits at -0.4 to -1.1 - the ring
LOST energy through the slip relative to its pre-event state,
which is the rigid drift at f/(N gamma) = 1.54 (kinetic 1.18 per
site) decelerating once the loaded node took the load alone plus
the released pre-fold strain. So the aftermath footprint of this
slip, in the derived current, is: nothing spreads. The rotor
spins at ~56 at event + 40, from the stored 1566 = v^2/2 (not
f/gamma = 98: the adjacent bonds carry a mean drag, which is the
182 out-flow), 6.4 percent of the injected
power leaks into the ring and is dissipated within it, and the
excess-energy footprint is one site wide because the drive at
~56 sits nearly thirty times above the lattice band edge 2. That is a
reading, not a claim; a claim about aftermath shape needs its
own registration (A-25 queued: wavebench recordings of slip
aftermaths against this current). No instrument error on record
in the registered line; the falsifier's first draft charged its
rounding budget against too small a term sum (ratio 1.36 on a
clean identity) and was corrected before pinning (notes). Claim
filed: ring-energy-continuity (falsifier
scripts/verify/p45_continuity.py, mutants current-blind,
sink-blind, gauge-blind - the first is invisible to the global
balance, the third to the control ring). Results:
scripts/experiments/p45_results.json.

## P-46 — 2026-09-02 — the slip aftermath is off-band: momentum exact, drift handed over, footprint evanescent
question: A-25 executed as a registered line. R-44 left the slip
aftermath as an unregistered reading and got two things wrong in
it: the rotor at ~56 was called "held by a mean drag" (it was
0.55 of terminal at event + 40 because 1 - e^{-0.8} = 0.55: a
spin-up on the damping time, not a drag), and the 182 called
out-flow after the slip was accumulated over the whole run, mostly
BEFORE the event, when the loaded site fed the ring's rigid drift
(the derive layer's N = 32 cells read pre-event out-flow 98 / 196
/ 312 at gamma 0.1 / 0.04 / 0.02 and post-event in-flow of 0.2 to
0.5). The registered question: what is the aftermath's shape in
the P-45 current? Three derived pieces. (i) MOMENTUM: summing the
EOM over the ring telescopes the bond forces away, dP/dt = f -
gamma P with P = sum v, exactly, slip or no slip; under
Euler-Cromer the discrete recursion P' = P + dt(f - gamma P) is
exact too; and the ring's share P_ring = sum_{j != b} v_j obeys
exactly dP_ring/dt = -gamma P_ring - (sin D_b - sin D_{b-1}), the
rotor's torque on the ring being the two-bond force. So the
pre-event rigid drift f/(N gamma) (1.54 / 0.77 / 0.31 at gamma
0.02 / 0.04 / 0.1, N = 64) is HANDED to the rotor: the ring's
drift decays at rate gamma up to the integrated rotor torque.
(ii) EVANESCENCE: once the rotor's Omega ~ f/gamma (98 / 49 / 20)
sits above the band edge 2, the bond force sin D_b - amplitude
exactly 1 at the bond's own phase - drives site b+1 as the end of
a semi-infinite damped chain of stiffness c = cos D ~ 1: with
z = Omega^2 - i gamma Omega the evanescent root w (|w| < 1) solves
w + 1/w = 2 - z/c, so |w| ~ c/Omega^2 per site, staggered, and the
end site's velocity amplitude is A_1 = |Omega/(c(1 - w) - z)|
~ 1/Omega. The footprint above the band is a geometric tail with
ratio 1.03e-4 / 4.13e-4 / 2.59e-3 per site at the three gammas
(exact discrete-map values at dt = 0.001, see method). Read by
lock-in against the bond phase, A_d = 2|(1/T) int v_{b+d} e^{-i
(theta_b - theta_{b+1})} dt|. (iii) DC TORQUE: NOT registered -
see method for why.
method: derive layer scripts/experiments/p46_derive.py with
p46_derive.json, all before this entry. THE ANCHOR (L-9): the
lock-in pipeline was pointed first at a linear semi-infinite chain
driven by a unit sinusoid at its end, integrated with the same
Euler-Cromer, and had to land on the closed forms. It caught, in
order: the missing factor 2 (a real sinusoid demodulates to half
amplitude: A_1 read -0.500 relative); the continuous-time
response formula being off by ~(dt Omega)^2, the size of the
gamma = 0.02 band, replaced by the EXACT Euler-Cromer discrete
response (z_d = -[(q-1)^2/(q dt^2) + gamma(q-1)/(q dt)], q =
e^{i Omega dt}, velocity factor |q-1|/dt); and, on the nonlinear
cells, a 1.5-percent detuning when the rotor's phase alone was
the reference - the ring's residual drift shifts the force's
phase, so the reference is the bond phase. Anchors now: A_1
within 2.1e-4 and 1.2e-4 of the closed form at Omega = 20 and 49,
the per-site ratios within 4e-6 and 2e-7, the offset-3 ratios
within 2e-5. THE NULLS (8a, L-1): the lock-in reads two floors
from the run itself - the in-band wave the slip launches
(amplitude a measured at offsets >= 2) leaks at most
2a/(T(Omega - 2)), and the demodulated product's 2-Omega term
leaks A_d/(Omega T) over a window not tied to whole periods (the
anchors' residuals ARE this floor: 2e-4 and 1e-4 relative at
Omega T = 2000 and 4900). The floors decide the registered
offsets (8c): at gamma = 0.02 the wave floor sits at 12x the
offset-2 signal for any window inside the run, so offset 1 only;
offsets 1 and 2 at gamma 0.04 (floor 0.14 of A_2 in [300, 400])
and 0.1 (0.06 in [100, 200]); offset 3 nowhere (floor >= 22x).
THE CLAUSE THE LAYER REMOVED: the DC rotor torque, T-bar =
K gamma/Omega^3 by the leading-order lag argument, was to be
registered with K pinned at N = 32. Step-quantized cycle windows
leaked A_T dt/T_w, which at Omega^3/gamma scaling read K ~ 50 to
850; interpolating the rotor-turn crossings brought the floors to
4e-3 and 0.55, and the two clean readings then DISAGREED: K =
-0.917 at gamma 0.1 (Omega 19) and +1.899 at gamma 0.04 (Omega
48), opposite signs, both above their floors. The leading-order
argument does not capture the coefficient; the torque is REPORTED
against the scale that would hold the ring's drift at 1 percent
(0.01 gamma P_ring(event)), not registered. THE DRIFT BAND: the
deviation of P_ring from P_ring(10) e^{-gamma(Delta - 10)} is
exactly the integrated rotor torque; over the evanescent phase
the torque is an oscillation of amplitude <= 2 at Omega, whose
integral against e^{-gamma(t-s)} is bounded by 4/Omega; Delta = 10
is the reference because the rotor crosses the band edge inside
the first unit and reaches Omega ~ 13 to 22 by Delta = 10 (the
launch phase, Delta < 10, is excluded and not claimed). Validation
at N = 32 read deviations <= 1.3e-3 against bounds 0.19 to 0.30.
Lessons consulted: L-1, L-2, L-3, L-8, L-9. Registered runner
scripts/experiments/p46_aftermath.py; the wavebench recording of
the gamma = 0.02 aftermath (site-energy excess, current, velocity
for Delta in [0, 120]) is written by the same run.
expects: cells twist0, N = 64, f = fold + 0.005, ramp 200, dt =
0.001, gamma in {0.02, 0.04, 0.1}, run to the P-36 event plus 400
/ 400 / 200. (a) Both exact identities at the floor at every step
of all three trajectories: the total-momentum recursion and the
ring-share recursion with the two-bond torque, residual ratios
<= 1 against 32 eps times the summands' magnitudes. (b) Drift
transfer: at Delta in {1/gamma, 2/gamma, 3/gamma} and a late
point (300 / 300 / 200), |P_ring(Delta) - P_ring(10)
e^{-gamma(Delta - 10)}| <= 4/Omega-bar(10). (c) Evanescence: in
the windows [300, 400] / [300, 400] / [100, 200], A_1 lies in the
band spanned by the exact discrete response over the window's
Omega range and stiffness range, widened by the two floors, at all
three gammas; A_2 lies in A_1 times the |w| band, widened by the
floors, at gamma 0.04 and 0.1. Reported unregistered: the
cycle-windowed DC torque and its K; A_3; the rotor's spin-up
fraction at Delta = 40, 100, 200 against 1 - e^{-gamma Delta}; the
loaded site's energy split pre/post event; the wavebench frames.
changes-my-mind: (b) violated at the late point with (a) held -
the ring would keep a share of its drift, i.e. the rotor transmits
a mean torque the linear-response picture excludes; (c) violated
at offset 2 with offset 1 held - the tail is not the evanescent
root, the footprint has structure the linear chain does not; (a)
violated - an algebra error, recorded and re-derived. (c) violated
at offset 1 alone is a lock-in instrument statement (8a) and costs
a re-registration.
not-claimed-in-advance: the launch phase (Delta < 10, the rotor
crossing the band) and the released strain wave's shape - recorded
on the wavebench page, not measured; the DC torque coefficient;
N-dependence of any of it (one N); the control ring's paired slip
(two rotors; not run); anything about real Josephson arrays.

## R-45 — 2026-09-02 — resolves P-46 (as expected)
All three clauses held at all three cells (events at 217.0 / 221.0
/ 243.0 for gamma 0.02 / 0.04 / 0.1). (a) Both momentum identities
at the floor at every step of every trajectory: the total recursion
at 0.016 of its bound, the ring-share recursion with the two-bond
torque at 0.020 - the slip leaves no trace in P at any step. (b)
Drift transfer: with the ring's share 63.20 / 29.15 / 6.11 at
Delta = 10, the deviations from P_ring(10) e^{-gamma(Delta - 10)}
at 1/gamma, 2/gamma, 3/gamma and the late point were 6.6e-3,
3.9e-3, 1.7e-3, 7.1e-4 (gamma 0.02); 1.5e-3, 1.9e-2, 7.4e-4,
3.0e-5 (0.04); 0, 2.6e-2, 1.6e-3, 1.5e-4 (0.1), against bounds
0.189 / 0.219 / 0.295 - the ring hands its drift to the rotor at
rate gamma to a part in 10^4 of the drift it had, and at the late
point holds 0.19 / 0.0002 / 0.0002 against the 0.77 / 0.44 / 0.17
that one percent of its event share would be. (c) Evanescence:
A_1 = 1.0178e-2 / 2.0331e-2 / 5.0970e-2 against the exact discrete
response bands [1.0170, 1.0191]e-2 / 2.0334e-2 / 5.0942e-2 with
floors 1.4e-5 / 5.2e-6 / 3.2e-5 - inside at all three; A_2 =
8.860e-6 against 8.406e-6 +- 1.1e-6 (gamma 0.04, ratio 4.358e-4
vs |w| 4.135e-4) and 1.2876e-4 against 1.3227e-4 +- 6.1e-6 (gamma
0.1, ratio 2.526e-3 vs 2.595e-3) - inside, the deviations 5 and 3
percent sitting within the in-band wave floors 13 and 5 percent.
The footprint above the band is the evanescent tail at the derived
per-site ratio; at gamma = 0.02 that ratio is 1.03e-4 and the
offset-2 signal 1.0e-6 sat under a wave floor of 1.3e-5 for any
window in the run, as the layer said it would - offset 1 there
reads 1.0178e-2 inside a band 0.2 percent wide. Unregistered
readings: the rotor's spin-up fraction 0.569 / 0.870 / 0.982 at
Delta = 40 / 100 / 200 (gamma 0.02) against 1 - e^{-gamma Delta} =
0.551 / 0.865 / 0.982 - the R-44 "mean drag" was this curve; the
loaded site's energy split at gamma 0.02: pre-event out-flow 183.2
(the ring's drift being pumped; R-44's 182), post-event in-flow
0.4, post-event injected 68193 and dissipated on the site 63362,
the remainder the rotor's kinetic energy; the cycle-windowed DC
torque, K = -0.738 +- 0.004 at gamma 0.1 (313 turns) and 0.139 +-
0.519 at 0.04 (782 turns), the coefficient still unpinned and
still opposite in sign to the validation cell at one gamma - and
in absolute terms 5.8e-4 and 2.7e-6 of the torque that would hold
one percent of the drift; A_3 at 18x and 321x under its floor.
The wavebench page scripts/experiments/p46_waves.html records 240
frames of the gamma = 0.02 aftermath (site-energy excess, current,
velocity, Delta in [0, 120]): the released strain wave circling
the loop, the rotor's one-site footprint, the ring's drift
draining. Claim filed: slip-aftermath-is-off-band (falsifier
scripts/verify/p46_aftermath.py, mutants bond-blind, rate-blind,
band-blind; the response there by direct tridiagonal solve, not
the root). Results: scripts/experiments/p46_results.json.

## P-47 — 2026-09-02 — quench counts on the pi ring share one density: exact half-sector statistics
question: A-26 executed as a registered line. Quench the P-35/P-36
free ring (N inertial phase oscillators, sine bonds J = 1, one pi
bond on the twisted ring, no load) through a Langevin bath whose
temperature ramps linearly from T_i = 2 to 0 over tau_Q, and count
the covariant winding W = sum_j wrap(D_j)/2 pi at the end. Three
things are exact before any run. THE COUNT: sum_j D_j = -sum_j A_j
identically on a ring, so sum_j wrap(D_j) = -sum A - 2 pi (number
of wraps) and W sits on the integer lattice (control) or the
half-integer lattice (twisted) at EVERY state, thermal or frozen -
a defect count with no threshold and no smear (L-1 has nothing to
bite on: the count is arithmetic). THE SHARED DENSITY: at
temperature T every bond carries exp(cos D/T), the pi bond
included (its energy is 1 - cos of the covariant strain), so with
S = sum_j wrap(D_j) the ring's closure reads ONE density rho_N(S)
- the N-fold convolution of the single-bond wrapped density - at
S = 2 pi n (control) or 2 pi (n - 1/2) (twisted). The twist shifts
the lattice and touches nothing else: (E_c, E_tw) = (<W^2>_control,
<W^2>_twisted) lie on a one-parameter curve traced by T, the fast
limit has both at N <u^2>_{T_i}/4 pi^2, the slow limit has
E_c -> 0 and E_tw -> 1/4. THE FLOOR: W^2 >= 1/4 at every twisted
sample, exactly - the half quantum the pi ring cannot shed, the
semifluxon's classical shadow. The registered prediction is the
shared density applied to the FROZEN counts: both rings quenched
at the same tau_Q freeze at the same effective temperature (the
twist is invisible to the local physics that sets the freeze), so
the twisted ring's counting statistics are predicted from the
control's with no free parameter, at every quench rate. What is
NOT predicted: how the control's count falls with tau_Q. The
winding changes only by a bond wrapping through pi, an activated
event with barrier 2 J, so the freeze is set by the phase-slip
rate rather than by the spin-wave correlation length the textbook
Kibble-Zurek argument uses; the derive layer's ladder at N = 32
read the control's <W^2> at 1.15 / 1.23 / 0.90 / 0.70 / 0.37 for
tau_Q = 0 / 5 / 20 / 80 / 320 with errors of 0.06 to 0.19 - a slow
fall with local exponents 0.23, 0.18, 0.47, nothing a power law
would be pinned to at this statistics (L-3, L-5). The scaling is
REPORTED; the ordering fast-above-slow is the only rate clause.
method: derive layer scripts/experiments/p47_derive.py with
p47_derive.json. rho_N by the characteristic-function integral
(stdlib quadrature); the curve for N = 32 and 64; the fast null
N <u^2>_{T_i}/4 pi^2 = 1.904 / 3.808 at T_i = 2 equals the curve's
value at T_i to four digits (the closure correction is
O(e^{-N/xi}), invisible). THE ANCHOR (L-9): equilibrium sampling by
the Langevin ring at T = 0.5 and 0.35 (gaps 20 and 60 units,
chosen from the activated slip rate ~ N e^{-2/T} so consecutive
samples decorrelate; below T ~ 0.3 equilibrium sampling by
dynamics is out of reach, which is the freeze physics itself) lands
on rho_N's lattice moments: z = 0.79 / -0.25 (T 0.5, control /
twisted) and 0.07 / 1.01 (T 0.35), with the inner-lattice
probabilities matching to 0.01. A first anchor at T = 0.25 with
10-unit gaps read a degenerate twisted sample (every W = +-1/2, a
sample SE of zero) and was diagnosed as correlated sampling, not
physics - recorded, and the error is now model-based (from the
predicted lattice distribution) wherever the sample is degenerate.
THE PROTOCOL: burn-in 20 units at T_i, ramp over tau_Q, settle 20
units at T = 0, read W; the count at the ramp's end is kept
alongside because the T = 0 descent still changes W after fast
quenches (48 of 60 realizations at tau_Q = 0, 2 of 60 at 20, none
at 80 and 320) - the fast null is therefore registered on the
RAMP-END count at tau_Q = 0 (the equilibrium count at T_i), while
the shared-density clause is registered on the FINAL count at
every rung (validation z = -1.10 / -0.97 / -1.10 / -1.06 / -0.78).
THE INTEGRATOR: Euler-Cromer with Maruyama noise (v' = v + dt a +
sqrt(2 gamma T dt) xi), gamma = 1, dt = 0.05; a first dt/2 cell
with 60 realizations read 1.03 against 0.45 and looked like a
discretization effect; the powered check (120 realizations each,
dt = 0.05 vs 0.0125, same seed) reads 0.750 +- 0.086 against
0.833 +- 0.106, z = -0.61 - statistics, not dt. Lessons consulted:
L-1, L-3, L-4 (every band here is a model SE or a binomial SE
from the registered M), L-5, L-8, L-9. Registered runner
scripts/experiments/p47_quench.py, seed 20260903.
expects: N = 64, gamma = 1, T_i = 2, dt = 0.05, tau_Q in {0, 5,
20, 80, 320}, M = 200 realizations per ring per rung. (a) Every
sample of every run on its lattice at 1e-12 (control integer,
twisted half-integer). (b) The fast null: at tau_Q = 0 the
ramp-end <W^2> of both rings equals N <u^2>_{T_i}/4 pi^2 = 3.808
within 3 SE. (c) The shared density at every rung: with T_eff
inverted from the control's final <W^2> on the N = 64 curve, the
twisted ring's final <W^2> lies within 3 combined SE (the model SE
of the predicted twisted distribution, plus the control's SE
propagated through the curve) of the prediction, AND its
probability of |W| = 1/2 lies within 3 combined binomial SE of the
predicted one. (d) The floor: min W^2 = 1/4 over every twisted
sample at every rung. (e) Ordering: the control's final <W^2> at
tau_Q = 0 exceeds its value at tau_Q = 320 by more than 3 combined
SE. Reported unregistered: the control's local exponents along the
ladder; T_eff per rung; the settle-changed counts; the full
histograms.
changes-my-mind: (c) violated at any rung with (a), (b) and (d)
held - the frozen twisted statistics would NOT be the control's
density on the shifted lattice, i.e. the twist would enter the
freeze, which the local-physics argument excludes; that is the
mind-change. (b) violated - the bath is not at T_i after the
burn-in (instrument). (a) or (d) violated - an arithmetic
impossibility; the code is wrong. (e) violated - the quench rate
does not reach the count at all in this range (reported as such;
not a mind-change about the shared density).
not-claimed-in-advance: any Kibble-Zurek exponent or scaling law
(reported, not registered: the freeze here is activated, the
ladder is short, the statistics are 200 per cell); N-dependence
(one N registered; the N = 32 layer is validation); the loaded
ring; the overdamped limit; real annular Josephson junctions and
their fluxon-trapping experiments (LC-36 context only).

## R-46 — 2026-09-02 — resolves P-47 (as expected)
All five clauses held at all five rungs, 200 realizations per ring
per rung, N = 64. (a) Every one of the 2000 samples on its lattice
at 9.1e-15 worst. (b) The fast null on the ramp-end count at
tau_Q = 0: control 3.785 +- 0.361, twisted 3.930 +- 0.342 against
3.808 (z = -0.06, 0.36). (c) The shared density at every rung -
the twisted ring's final <W^2> against the value predicted from
the control's through the N = 64 curve: 1.880 vs 1.940 (z -0.23),
1.730 vs 1.660 (0.31), 1.490 vs 1.520 (-0.14), 1.060 vs 1.105
(-0.31), 0.860 vs 0.800 (0.52) at tau_Q = 0 / 5 / 20 / 80 / 320;
and its probability of |W| = 1/2 against the predicted one: 0.520
vs 0.537, 0.540 vs 0.575, 0.575 vs 0.597, 0.675 vs 0.679, 0.735 vs
0.764 (z -0.43, -0.85, -0.53, -0.09, -0.72; binomial SE 0.04). Ten
comparisons, worst 0.85 sigma: the frozen counts of the twisted
ring ARE the control's density on the half-integer lattice, at
every quench rate, with the effective temperature inverted from
the control alone (0.726 / 0.631 / 0.586 / 0.459 / 0.364). (d) The
floor: min W^2 = 1/4 over every twisted sample at every rung. (e)
Ordering: the control's final count 1.940 at tau_Q = 0 against
0.800 at 320, z = 5.8. Unregistered readings: the T = 0 settle
changed the count in 168 / 104 / 19 / 0 / 0 control realizations
along the ladder (the fast quench's count is set by the descent,
the slow quench's by the ramp); the control's local exponents
0.06 / 0.23 / 0.23 across the three ladder steps - the two slow
steps agree with each other and sit near the 0.25 the annular
junction experiments of LC-36 predict for their quench, which is
noted as a number and not as a result: two steps, one N, an
activated freeze, 200 samples. The full histograms are in the
results file; at tau_Q = 320 the control holds W = 0 in 90 of 200
and the twisted ring holds |W| = 1/2 in 147 of 200. Claim filed:
quench-counts-share-one-density (falsifier
scripts/verify/p47_half_sector.py by direct convolution and
velocity-Verlet, mutants shift-blind and count-blind). Results:
scripts/experiments/p47_results.json.

## R-45a — 2026-09-02 — audit corrections on record (R-43, R-44, R-45; the P-44 and P-46 claim texts)
Three corrections from the 2026-09-02 adversarial audit of PRs 110,
112 and 113 (every falsifier and mutant rerun at its expected exit
code; no registered clause fires, no status moves). The entries
stand; these sit beside them, append-only.
(1) R-45 and the P-46 claim's clause (2): "the ring hands its
pre-event rigid drift f/(N gamma) to the rotor" is wrong as
physics. By the line's own identity dP_ring/dt = -gamma P_ring - T
and its registered bound, the integrated torque obeys
|int T e^{-gamma(t-s)} ds| <= 4/Omega(10) = 0.189 / 0.219 / 0.295
against P_ring(event) = 77.26 / 43.69 / 16.75 at gamma 0.02 / 0.04
/ 0.1 (p46_results.json): at most 0.2 to 1.8 percent of the ring's
momentum can reach the rotor through the torque. The ring's drift
is dissipated by the ring's own damping at rate gamma; the rotor is
spun up by the load directly. What moves from ring to rotor is the
load's momentum flux, not the ring's momentum. The claim text is
amended in this commit; clause (b) and its numbers stand. The
mechanism the numbers hide, on record for the first time (own rerun
of the registered integrator, N = 64, gamma = 0.1, Delta in
[50, 60]): the slip carries the pi twist from the ring's bonds onto
the rotor's bond pair (D_b + D_{b-1} = -0.098 at t = 0, +3.067
after the event, mod 2 pi), so the two rotor-adjacent sites are
driven nearly in anti-phase (v_{b+1} + v_{b-1} peak-to-peak 0.045
against 0.126 for v_{b+1} alone) - which is why P_ring is clean at
unit samples. The derive table's stiffness anchor cos(pi/(N-2))
assumed the ring keeps the twist; the registered bands use the
measured c, so no verdict moves. L-10.
(2) R-44's unregistered footprint reading, "10-percent radius ZERO
... nothing spreads": the radius is thresholded at 0.1 x peak with
the peak the rotor's own kinetic energy (1566.3), while the ring's
sites carry site energies of order 1 (excess by offset -1.00,
-0.78, -1.04, -1.07, -1.03 at offsets 1 to 5, p45_results.json).
In the rotor regime the metric cannot read anything but zero;
"nothing spreads" was the metric, not the aftermath. With R-45's
two corrections, three misreadings stood in R-44's readings. L-12.
(3) R-43, the P-44 claim's null_system and LAW-50: "two
deterministic mutants (sup-blind, mass-blind)". They are one test:
sup-blind (f x 1.5, tau 0.5) and mass-blind (tau 0.75, f x 1) give
tau^2 |lambda|^2 = 0.5625 |lambda|^2 in both, and the chain and its
k = 1 term depend on lambda only through tau lambda; the two runs
print the identical chain -1.25e-4 / 7.30e-8 / 1.64e-11. |T|
(2.99940 against 1.99960) is not checked in mutant mode. The
falsifier still runs and fails as LAW-16 requires; its
discriminating power is one perturbation, not two. The claim text
is amended; a distinct second mutant is a gate change, queued.
L-13.
On record from the same audit, not corrections: P-46 clause (b)
holds by 10 to 1000x under a bound that follows from |T| <= 2
unless the rotor stalls, and at gamma 0.1 its 1/gamma check point
is the Delta = 10 reference itself (deviation identically 0); the
A_1 bands (0.02 to 0.2 percent wide) are the Euler-Cromer discrete
map's, and the tail law is carried by offset 2 at 3 to 5 percent
deviation under 5 to 13 percent floors. P-45's falsifier: its
ladder check is one-sided (ratios >= 2^0.5; its own velocity-Verlet
reads 4.0 globally), it has no slip coverage, and its twisted cell
at F = 1.97 (N = 48, twisted fold 1.9497) slips at t = 29 of 60
with the rotor at 47 and 0.94 rad per step - taken up by LAW-54 in
this line.

## P-48 — 2026-09-02 — the stiffness is a clock; the tail law to within a fifth of the band edge
question: the owner asked for a bond-stiffness column kappa as the
honest refinement axis of the ring (P-46's "evanescent above the
band edge 2" is a lattice statement; N is length, not resolution,
because the spacing is fixed at 1). The model with stiffness kappa,
theta_dd_j = -gamma v_j + kappa (sin D_j - sin D_{j-1}) + f delta_jb,
turned out in the derive layer to carry no new parameter: with
u = v/sqrt kappa and tau = sqrt kappa t it IS the unit-stiffness
ring at damping gamma/sqrt kappa and load f/kappa, exactly, and
exactly for the Euler-Cromer map too when dt scales to sqrt kappa dt
(the ramp keeps its step count). kappa is a time unit. The band top
2 sqrt kappa and the rotor speed f/gamma scale together, so "above
the band" is the DAMPING statement f/(gamma sqrt kappa) > 2, which
at kappa = 1 is f/gamma > 2; P-46's cells sat at 98 / 49 / 20 by
choice. The ladder kappa stood in for is therefore a gamma ladder at
kappa = 1 and fixed reduced load: gamma in {0.2, 0.35, 0.45, 0.5,
0.6, 0.8}, terminal Omega = f/gamma from 9.8 down to 2.5 (the band
top is 2). Registered questions: (i) is the scaling an identity of
the map at the floor, and through the slip; (ii) does the P-46
evanescent-tail law A_2/A_1 = |w|, w the root of w + 1/w = 2 - z/c
(exact discrete form), hold down the ladder toward the band edge?
method: derive layer scripts/experiments/p48_derive.py with
p48_derive.json, everything measured before this entry was
written; lessons consulted L-3, L-5, L-8, L-11, L-12, L-13 (and
L-9 by the anchor below). THE IDENTITY: one Euler-Cromer step of
the kappa model against one step of the scaled unit model on the
scaled state, at 5000 random states x two velocity scales,
residuals against 32 eps times the summands: 0.04 to 0.06 of the
bound at kappa 0.5 and 2; and exactly ZERO at kappa 1/4 and 4 -
sqrt kappa dyadic makes the two computations bit-identical
(recorded because it is a fact about the arithmetic, and because it
means a dyadic kappa cannot test the identity at the floor, only
below it). Whole trajectories through the slip at kappa 0.5 and 2
(N = 64, gamma = 0.1, 300 to 400 thousand steps): identical event
steps (294000, 221000), phase deviation 1.3e-10 and 2.2e-10 on
rotor phases of order 1e4, i.e. the accumulated rounding (the
derived bound 32 eps x steps x max|theta| is 1e-5). Mutants
kappa-blind (gamma/kappa) and load-blind (f/sqrt kappa) fail the
one-step identity at 7e9 and 4e13 of the bound (L-8). THE LADDER
AND ITS INSTRUMENT: the P-46 instrument unchanged (bond-phase
lock-in, the in-band wave floor 2a/(T(Omega - 2)), the 2-Omega self
floor A_d/(Omega T), the exact discrete root at the window's
measured stiffness range [cmin, cmax]) read the tail ratio INSIDE
its band at gamma 0.1 and 0.2 (0.97 and 1.04 of |w|, floors 5
percent) and then 26, 28, 33, 23, 19 percent ABOVE the band top at
gamma 0.35 to 0.8, against floors of 11 to 24 percent - while the
L-9 linear-chain anchor at Omega 3.9 and 5.6 landed on the closed
form to 4e-3 (its self floor), so the pipeline is clean and the
departure is the ring's. Two candidates were run down. (1) The m =
0 parametric resonance of the rotating junction with the band
(LC-37: omega = Omega/2 in band for Omega < 4, i.e. gamma > 0.49):
the Omega/2 content at offsets 2 to 6 sits at 2e-3 against a far-
field RMS of 3e-2, and that far field grows smoothly through Omega
= 4 (8e-4, 3e-3, 2.3e-2, 3.1e-2, 3.3e-2 at gamma 0.1 to 0.5) - it is
the slip's long-wavelength relaxation, overdamped at these gammas
(omega_1 = 2 sin(pi/64) = 0.098 < gamma/2, decay omega_1^2/gamma =
0.02 per unit at gamma 0.5), not a resonance. Refused. (2) The
REFERENCE. The bond phase theta_b - theta_{b+1} carries the
neighbour's own displacement; with that slow relaxation alive in
the window (rms 0.04 to 0.07 in velocity, of order 0.5 rad in
displacement), demodulating against the ROTOR's phase alone puts
the offset-2 ratio inside the band at every ladder cell (gamma 0.35
to 0.8: 3.15e-2 / 5.98e-2 / 7.47e-2 / 1.04e-1 / 2.18e-1 against bands
[3.29, 3.38]e-2 / [5.42, 5.87]e-2 / [6.80, 7.47]e-2 / [1.03, 1.16]e-1
/ [1.96, 2.59]e-1 with floors 12 / 15 / 13 / 11 / 24 percent), while
the same reference smears A_1 by the neighbour's slow phase wander
(A_1 rotor/bond = 0.998, 0.858, 0.704, 0.750, 0.750, 0.688 - the
smear of a phasor wandering ~0.5 rad). The first-order mixing term
of a reference carrying an Omega-component of index X = A_1/Omega,
(X/2) v_slow, covers 8, 8, 8, 7, 5 percent of A_2 - a third of the
bond-reference excess - and the excess is NOT monotone along the
ladder (4, 24, 23, 27, 16, 4 percent). So the reference comparison
is REPORTED with the mechanism as a candidate, not registered (L-3:
no band for what is not derived), and the registered tail law
carries the rotor-phase reference, whose Omega-component is the
rotor's own velocity ripple (2/Omega^2 in phase, negligible) and
whose smear is common to A_1 and A_2 and cancels in the ratio.
Small-cell check (the falsifier's N = 16, gamma 0.5): the two
references agree to 0.6 percent, both in band - the slip's k = 1
mode is underdamped there (omega_1 = 0.39 > gamma/2) and gone by
the window; the mixing is a long-ring effect. NULLS (8a): the
floors are computed per run; the rotor's Omega is measured (it
reads 0.999, 0.996, 0.994, 0.988, 0.954 of f/gamma along the
ladder - the back-action that in band, at gamma 1, becomes 0.868).
Registered runner scripts/experiments/p48_kappa.py, seed 20260903.
expects: (a) the one-step map identity at kappa in {0.5, 2, 3},
vmax in {2, 100}, 20000 states each: every residual within 32 eps
of its summands (worst ratio <= 1); (a2) at kappa in {1/4, 4} the
trajectories through the slip (N = 64, gamma = 0.1, reduced load
fold + 0.005, ramp 200, event + 100) are bit-identical to the
scaled unit run (deviation exactly 0, same event step); (b) at
kappa in {0.5, 2, 3} the event steps are identical and the phase
deviation over the run is within 32 eps x steps x max|theta|; (c)
at kappa = 1, gamma in {0.2, 0.35, 0.45, 0.5, 0.6, 0.8}, windows
[60,120] / [40,100] / [30,90] / [30,80] / [30,80] / [20,70] after
the event, the offset-2 ratio A_2/A_1 demodulated against the
rotor's phase lies in [|w(cmin)|, |w(cmax)|] widened by (wave floor
+ 2-Omega self floor at offset 2)/A_1, with the event occurring at
every cell. Reported unregistered: the bond-phase reference's A_1
and A_2 beside the rotor's at every cell, the first-order mixing
estimate, the Omega/2 content, the rotor's slowing, the event times
(243 to 777: the saddle-node bottleneck lengthening with gamma), the
in-band cell gamma = 1 (Omega 1.71, the propagating root).
changes-my-mind: (a) or (b) violated - the scaling is not an
identity of the map, an algebra error recorded and re-derived; (a2)
violated with (a) held - a rounding-order difference the layer did
not see, an instrument note; (c) violated at any cell with (a)-(b)
held - the driven-chain tail law fails inside the band's fifth, and
the near-band footprint has structure beyond the linear root (the
reported bond-reference excess would then be physics, not
instrument); (c) violated only at gamma 0.8 (Omega 2.35, floor 24
percent) is an instrument statement about the floor near the edge
and costs a re-registration.
not-claimed-in-advance: the mechanism of the bond-reference excess
(a candidate, reported); any parametric resonance (looked for,
absent above the floors, LC-37); the in-band regime Omega < 2
(instrument not built: the wave floor is negative there); the
continuum limit (there is none that keeps the slip: kappa is a
clock and the sine bond has no small-strain limit at fixed
winding); N-dependence beyond the two ring sizes named; anything
about real arrays.

## R-47 — 2026-09-02 — resolves P-48 (as expected)
All four clauses held. (a) The one-step map identity at kappa 0.5 /
2 / 3, vmax 2 and 100, 20000 states each: worst residuals 0.044 /
0.062, 0.044 / 0.062, 0.054 / 0.062 of the 32 eps bound (v / theta).
(a2) Dyadic kappa 1/4 and 4: the trajectories through the slip are
bit-identical to the scaled unit run - deviation exactly 0 in theta
and v/sqrt kappa at every sample, events at steps 409000 and 212000
on both sides. (b) Kappa 0.5 / 2 / 3: identical event steps (294000
/ 221000 / 215000), phase deviations 1.3e-10 / 2.2e-10 / 8.1e-10
against the derived bounds 2.7e-6 / 8.4e-6 / 1.2e-5 - the identity
holds through the tear-out to the accumulated rounding on a rotor
phase of order 1e4. (c) The tail law under the rotor-phase
reference at every ladder cell: gamma 0.2 / 0.35 / 0.45 / 0.5 / 0.6 /
0.8, events at 295 / 380 / 439 / 469 / 530 / 653, measured Omega
9.840 / 5.616 / 4.358 / 3.914 / 3.240 / 2.348, A_2/A_1 = 1.0593e-2 /
3.1457e-2 / 5.9770e-2 / 7.4670e-2 / 1.0413e-1 / 2.1772e-1, each inside
[|w(cmin)|, |w(cmax)|] widened by its floors (the bands and floors
in p48_results.json; at gamma 0.8 the band is [1.96, 2.59]e-1 with a
24 percent floor, the widest of the ladder). The evanescent-tail law
of P-46 holds from Omega = 20 down to Omega = 2.35, a fifth above the
band top, at the ring's own damping. Reported unregistered, beside
the registered reference: the bond-phase lock-in of P-46 reads A_2/
A_1 above the band top by +4.0 / +24.4 / +22.9 / +26.8 / +16.1 /
+4.3 percent along the ladder (non-monotone), and A_1 below its band
by 0.08 / 1.4 / 2.4 / 3.5 / 3.3 / 5.7 percent; the rotor-phase
reference smears A_1 by the neighbour's slow displacement to 0.998 /
0.858 / 0.704 / 0.750 / 0.750 / 0.688 of the bond reading; the first-
order mixing term of the bond reference covers 2.4 / 7.9 / 8.4 / 7.7 /
6.5 / 5.3 percent of A_2 - a third of the excess where it peaks. No
mechanism is claimed for the excess; A-29 queued. The rotor slows to
0.999 / 0.996 / 0.994 / 0.988 / 0.954 of f/gamma along the ladder and
to 0.868 in band (gamma 1, Omega 1.709, reported: the ratio 3.93e-1
there sits outside the propagating-root band with the wave floor
invalid below the band edge - the in-band instrument is not built).
The Omega/2 content at offset 4 reads 1.3 / 1.1 / 0.9 / 1.1 / 0.4 / 0.2
of the wave floor: no subharmonic. The event times lengthen with
gamma as the saddle-node bottleneck (243 at gamma 0.1 to 777 at 1).
No instrument error in the registered line; the derive layer's two
refused candidates are in P-48. Claim filed: stiffness-is-a-clock
(falsifier scripts/verify/p48_kappa.py, mutants kappa-blind and
load-blind; the reference-blind mutant tried and not pinned).
Results: scripts/experiments/p48_results.json.

## R-47a — 2026-09-03 — correction to R-47: clause (c) held by leakage; the near-band tail law is the late window's
The A-29 derive layer (scripts/experiments/p49_derive.py, the ring
rerun at gamma 0.2 / 0.35 / 0.5 / 0.8 with the full time series at
sites b to b+3 over the P-48 windows) took the two lock-in readings
apart exactly. Each site's velocity is split by least squares into
its fundamental locked to the drive phase (the bond phase, since the
force on b+1 is -sin D_b), its running mean over one rotor period,
and the rest; each reference then demodulates each component, and
the complex pieces sum to the reading. Two facts follow. (1) The
bond-phase reading IS the drive-locked fundamental (the remainder is
orthogonal to the same carrier by construction), so R-47's "bond-
reference excess" was never a reference effect: the drive-locked
amplitude at offset 2 exceeds the linear root band by +24.4 / +26.9 /
+5.7 percent at gamma 0.35 / 0.5 / 0.8 (+4.0 at 0.2). (2) The rotor-
phase reading is that fundamental times the smear of the neighbour's
slow phase wander - 0.733 at gamma 0.5 against 0.731 predicted from
the measured x_1 rms of 0.77 rad, identical at sites 1 and 2 - PLUS
the slow and harmonic components of the site's motion leaking
through the reference's modulation, which at site 2 (where the
fundamental is ten times smaller) pull the reading down by 20
percent (0.01462 read against 0.01813 smeared fundamental). The
rotor-reference ratio sat inside the band at every near-band cell
because that correlated leakage happened to offset the excess
within floors 11 to 24 percent wide. Clause (c) of P-48 held, its
numbers stand, and it is not evidence for the tail law near the
band; the claim's scope is amended in this commit and the
"registered physics" sentence of R-47 is withdrawn to a reading.
What replaces it: a LATE window. With the slip's long-wavelength
relaxation decayed (Delta in [300, 380]; x_1 rms 0.049 / 0.023
against 0.77 / 0.57 in the P-48 windows), the drive-locked ratio
reads 7.4476e-2 against a band top of 7.4547e-2 at gamma 0.5 (-0.1
percent) and 3.3809e-2 against 3.3804e-2 at gamma 0.35 (+0.0
percent), both references agreeing to 0.05 percent, and A_1 inside
its band (2.7122e-1 in [2.7055, 2.7223]e-1; 1.8357e-1 in [1.8357,
1.8374]e-1). The evanescent-tail law holds at Omega 3.9 and 5.6 to a
tenth of a percent once the ring is quiet; while the slip's slow
mode is alive it is exceeded by up to 27 percent at offset 2, an
effect of the ring's state, not of the instrument. Its dependence on
the slow mode's amplitude and the in-band instrument (the same late
window, where the launched transient is gone and the wave floor is
not needed) are P-49. Lessons: L-9 (the anchor was clean; the
disagreement was the ring's), L-12 (a reading inside a floor wider
than the effect is not a reading), L-13 (two estimators disagreeing
is a decomposition owed, not a choice).

## P-49 — 2026-09-03 — the late window: the tail law near and in the band, the transient excess, and the smear identity
question: A-29, after R-47a. P-48's near-band readings sat inside
the slip's long-wavelength relaxation - at N = 64 the k = 1 mode
(omega_1 = 0.098) is overdamped for gamma > 0.2 and decays at
omega_1^2/gamma, 0.02 per unit at gamma 0.5 - and the component
accounting of R-47a showed the drive-locked offset-2 amplitude
exceeding the linear root by up to 27 percent while that mode is
alive, and the rotor-phase reference's agreement to be leakage-
assisted. Three registered questions: (i) in a LATE window, after
the relaxation has decayed, does the driven-chain tail law hold at
the drive-locked amplitudes near the band (Omega 5.6, 3.9) and in
it (Omega 2.35, 1.69), with derived floors and no wave floor (the
launched transient is gone, so the window separates the driven tail
from it by decay, not by frequency); (ii) does the transient excess
decay monotonically with the slow mode's amplitude to within the
floor; (iii) is the rotor-phase lock-in of a site's drive-locked
fundamental exactly that fundamental times the characteristic
function |<e^{-i x_1}>| of the neighbour's displacement, up to the
reading's own leakage phasors (an instrument identity).
method: derive layer scripts/experiments/p49_derive.py (two
passes) with p49_derive.json, everything measured before this
entry. Lessons consulted L-3, L-8, L-9, L-12, L-13, L-14 (written
from R-47a). THE READOUT: the ring is run at N = 64 with the full
time series at sites b to b+3 over the window; each site's velocity
is split by least squares into its fundamental locked to the bond
phase (the drive's own phase), the running mean over one rotor
period, and the rest; the registered amplitudes A_d are the
fundamentals. THE BANDS (L-3): the exact discrete root |w| over the
window's stiffness range [cmin, cmax], the lower end reduced by the
describing-function factor 2 J_1(delta)/delta of the drive-frequency
strain amplitude delta = A_1 |1 - w|/Omega (LC-38; 0.9999 / 0.9993 /
0.9922 / 0.9782 at gamma 0.35 / 0.5 / 0.8 / 1); the floor is the
2-Omega self floor only, (A_2 + ratio A_1)/(Omega T A_1). THE SMEAR
IDENTITY: |A_1(rotor)/A_1(bond) - |<e^{-i x_1}>|| <= (|slow| + |rest|
phasors of the rotor reading)/A_1(bond) + the self floor, a triangle
inequality on the decomposition. Layer readings, late window
[300, 380]: ratio A_2/A_1 = 3.3809e-2 / 7.4476e-2 / 2.5560e-1 /
4.4803e-1 against bands [3.3777, 3.3804]e-2 / [7.4209, 7.4547]e-2 /
[2.3865, 2.5847]e-1 / [3.6940, 4.4704]e-1 with floors 1.5e-4 / 4.8e-4
/ 2.7e-3 / 6.6e-3 - inside at all four (+0.02, -0.10, -1.11, +0.22
percent of the top); A_1 = 1.8357e-1 / 2.7122e-1 inside [1.8369,
1.8370]e-1 / [2.7188, 2.7197]e-1 with self floors above the band, and
below its band by 2.6 and 6.6 percent at gamma 0.8 and 1 (in band
the neighbour's strain amplitude is 0.25 and 0.42 rad and the rotor
slows to 0.954 and 0.868 of f/gamma; A_1 there is reported, not
claimed); smear measured 1.0000 / 1.0003 / 1.0025 / 1.0068 against
predicted 0.9997 / 0.9988 / 0.9891 / 0.9666 within tolerances
0.0032 / 0.0067 / 0.0331 / 0.0936. The decay ladder at gamma 0.5,
windows of 50 units starting at Delta 30 / 80 / 130 / 180 / 230 /
300: x_1 rms 0.772 / 0.277 / 0.112 / 0.062 / 0.051 / 0.049 (the
last is the site's own drive-frequency motion, A_1/Omega); excess
over the band top +26.85 / +4.13 / +2.11 / +0.91 / +0.20 / -0.08
percent against floors ~1 percent; A_1 -4.19 / -1.27 / -0.64 /
-0.45 / -0.34 / -0.26 percent; smear 0.7500 / 0.9689 / 0.9971 /
1.0001 / 1.0003 / 1.0005 against 0.7305 / 0.9620 / 0.9937 / 0.9981 /
0.9987 / 0.9988 within tolerances 0.037 / 0.016 / 0.010 / 0.010 /
0.009 / 0.009. Mutants (L-8, L-13): smear-blind (asserts no smear)
fails the identity at the first decay window (0.7500 read against
1.0 asserted, tolerance 0.037); band-blind (asserts the in-band
tail ratio is 1/Omega) fails the late in-band cell (0.448 read
against 0.590 asserted). Anchor (L-9): the P-48 linear-chain anchor
at Omega 3.9 and 5.6 stands; the P-49 falsifier's own N = 16 ring
reads the late-window ratio inside the band in band and above it,
and its N = 48 ring reads the smear 0.784 against 0.780 predicted.
NULLS (8a): the wave floor is not used - the window is placed where
the launched transient has decayed by more than e^{-6} at every
gamma (gamma Delta/2 >= 52 for the underdamped modes, omega_1^2
Delta/gamma >= 5.8 for the overdamped k = 1 mode at gamma 0.5) and
the residual slow content is read from the run (period-mean rms
6e-4 to 1.5e-2 in velocity against A_2 of 6e-3 to 2.6e-1). Registered
runner scripts/experiments/p49_near_band.py.
expects: cells twisted sector 0, N = 64, f = fold + 0.005, ramp 200,
dt = 0.001. (a) Late window [300, 380] at gamma 0.35 / 0.5 / 0.8 /
1.0: the drive-locked A_2/A_1 lies in [|w(c_min 2J_1(delta)/delta)|,
|w(c_max)|] widened by the self floor, at all four. (b) At gamma 0.35
and 0.5 the drive-locked A_1 lies in its band widened by its self
floor. (c) The decay ladder at gamma 0.5: the excess over the band
top is non-increasing along the six windows, x_1 rms is
non-increasing, and the last window's ratio is inside its band and
floor. (d) The smear identity holds at every cell of (a) and every
window of (c). Reported unregistered: A_1 in band (gamma 0.8, 1.0);
A_3/A_2 everywhere (late: 3.34e-2 / 7.44e-2 / 2.61e-1 / 4.30e-1
against |w| bands - inside at gamma 0.5 and 0.8, 1 and 4 percent
under at 0.35 and 1, its floors not derived); the functional form
of the excess in the slow amplitude (near-linear for A_1, faster for
A_2 - two points above the floor, not a law).
changes-my-mind: (a) violated at gamma 0.35 or 0.5 - the tail law
fails near the band even with the ring quiet, and R-47a's reading
was wrong about what the excess is tied to; (a) violated in band
only - the propagating root or the describing-function band is the
wrong instrument there (a re-registration); (c) violated - the
excess is not the slow mode's; (d) violated - the rotor-phase
reading is not the smeared fundamental and the R-47a accounting has
an error, re-derived and recorded.
not-claimed-in-advance: the mechanism of the transient excess (a
nonlinear coupling of the slow strain to the drive-frequency
response, candidate only); A_1 in band; offset 3; the in-band
rotor slowing as a law; any statement for gamma < 0.35 near the
band or for N other than 64 (the falsifier's 16 and 48 are its own).

## R-48 — 2026-09-03 — resolves P-49 (as expected)
All four clauses held. (a) Late window [300, 380] at gamma 0.35 /
0.5 / 0.8 / 1.0 (events 380 / 469 / 653 / 777; Omega 5.617 / 3.917 /
2.351 / 1.694): the drive-locked A_2/A_1 = 3.3809e-2 / 7.4476e-2 /
2.5560e-1 / 4.4803e-1 inside [3.3777, 3.3804]e-2 / [7.4209, 7.4547]
e-2 / [2.3865, 2.5847]e-1 / [3.6940, 4.4704]e-1 with self floors
1.5e-4 / 4.8e-4 / 2.7e-3 / 6.6e-3 (+0.02 / -0.10 / -1.11 / +0.22
percent of the top): the driven-chain tail law holds at the drive-
locked amplitudes from a fifth above the band edge to inside the
band, once the ring is quiet, with no wave floor. (b) A_1 = 1.8357e-1
/ 2.7122e-1 inside its band with self floor at gamma 0.35 / 0.5
(-0.07 / -0.27 percent of the top). (c) The decay ladder at gamma
0.5: x_1 rms 0.772 / 0.277 / 0.112 / 0.062 / 0.051 / 0.049,
excess over the band top +26.85 / +4.13 / +2.11 / +0.91 / +0.20 /
-0.08 percent, both non-increasing, the last window inside its band
and floor (1.02 percent): the transient excess is the slow mode's
and is gone with it. (d) The smear identity at all ten cells:
measured 1.0000 / 1.0003 / 1.0025 / 1.0068 against predicted 0.9997
/ 0.9988 / 0.9891 / 0.9666 (tolerances 0.0032 / 0.0067 / 0.0331 /
0.0936) in the late windows and 0.7500 / 0.9689 / 0.9971 / 1.0001 /
1.0003 / 1.0005 against 0.7305 / 0.9620 / 0.9937 / 0.9981 / 0.9987 /
0.9988 (tolerances 0.037 / 0.016 / 0.010 / 0.010 / 0.009 / 0.009)
along the ladder - the rotor-phase lock-in is the drive-locked
fundamental times the characteristic function of the neighbour's
displacement, within the reading's own leakage. Reported
unregistered: A_1 in band, 2.62 and 6.64 percent below its band at
gamma 0.8 and 1.0 (neighbour strain 0.25 and 0.42 rad; the rotor at
0.954 and 0.868 of f/gamma); A_1's transient deficit -4.19 / -1.27 /
-0.64 / -0.45 / -0.34 / -0.26 percent along the ladder, near-linear
in x_1 rms where above the floor; A_3/A_2 late 3.34e-2 / 7.44e-2 /
2.61e-1 / 4.30e-1. No instrument error in the registered line; the
line's instrument (the late window, the drive-locked decomposition,
the describing-function band, the smear identity) replaces P-46's
bond-phase lock-in with its wave floor for any window in which the
slip's relaxation is alive. Claim filed: late-window-tail-law
(falsifier scripts/verify/p49_near_band.py, mutants smear-blind and
band-blind). Results: scripts/experiments/p49_results.json.
