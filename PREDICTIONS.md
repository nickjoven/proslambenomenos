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
