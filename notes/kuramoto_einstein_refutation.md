# Refutation of Proof Chain A (Kuramoto -> Einstein)

First-class record, 2026-08-22. Source: harmonics
sync_cost/derivations/PROOF_A_gravity.md (status there: "Survives,
canonical proof chain") and adm_dictionary.md. Claim file:
einstein-from-kuramoto-chain-a (refuted). Script:
scripts/verify/kuramoto_einstein_refutation.py. Prose here carries no
load; each numbered item is a computation or a cited theorem.

## The chain's load-bearing steps

P7: at K = 1 (locked), metric = <d_i theta d_j theta>, lapse =
coherence r, shift = phase gradient, K_ij = <(d_i d_j theta)^2>; "the
first ADM equation is exact under locked-state conditions; the second
follows from differentiating and substituting the Kuramoto dynamics."
P8: Lovelock (1971) with four hypotheses, the fourth ("general
covariance") supplied by "SL(2,R) acts transitively."

## Failure 1 - gradient flow, not Hamiltonian (proof + computed signature)

With symmetric coupling and fixed natural frequencies, Kuramoto is a
gradient flow: theta' = -dV/dtheta with V = -sum omega_i theta_i -
K sum cos(theta_j - theta_i). V decreases along every trajectory (a
Lyapunov function) and the linearisation about any locked state is
self-adjoint with real spectrum. A time-reversible Hamiltonian
evolution of the ADM type cannot be a coarse-graining of a system
with a strict Lyapunov function. The computed signature: a localised
perturbation of a 401-site locked ring spreads with exponent 0.500
(diffusive); the same lattice with inertia gives 0.989. CORRECTION
OF RECORD (context-free audit, 2026-08-22): the first version of
this section claimed "the order of the characteristic structure is
an invariant of the equation class" as a general principle, which
is false under coarse-graining (Boltzmann/BGK -> Euler sound waves;
Schrodinger -> Madelung; the Kuramoto kinetic equation with a
frequency spread is Vlasov-like and supports Landau damping,
Strogatz, Mirollo, Matthews, PRL 68, 2730 (1992)). The exponent is a
necessary-condition check, not the proof; the Lyapunov argument is.
P7's own regime (r = 1, all locked) also collapses the frequency
spread that any kinetic rescue would need.

## Failure 2 - the lapse is constant where the chain lives (computed)

adm_dictionary.md line 153: "a clock at x ticks at rate r, and its
phase is psi." "Locked" means theta_i' = Omega for all i, so the
clock rate is uniform whatever r(x) does - and PROOF_A P7 (lines
110-111) sets r = 1 outright, so the chain's lapse is N = 1
identically with no computation needed. Checked on a locked ring
with heterogeneous natural frequencies at K = 3, where the local
coherence genuinely varies (0.805-1.000) while max |theta_i' - Omega|
= 2e-7 -> 4e-12. CORRECTION OF RECORD: the first version of this
check used identical frequencies with varying coupling, whose
attractor is the in-phase state (r = 1 everywhere) - a vacuous lapse
test, found by the audit.

## Failure 3 - the metric is a graph metric (computed)

adm_dictionary.md line 64 defines gamma_ij = delta_ij - d_i theta
d_j theta (positivity requires |grad theta| < 1, lines 41-49), with
the bracket average taken over a single smooth locked field, so the
tensor is rank-one as the source argues it (the positivity proof
uses the rank-one identity). That is the induced metric of the
spacelike graph z = theta(x) in Minkowski R^(n,1); its curvature
satisfies the corresponding Gauss equation - in 2D, K = -det(Hess
theta)/(1 - |grad theta|^2)^2 - checked against the Brioschi formula
to 3e-4 on random theta with |grad theta| < 1. Codimension-one flat
(pseudo-Euclidean) embeddings are a thin subfamily: one free
function against three for a general 3-metric modulo
diffeomorphisms (Janet 1926; Cartan 1927), so the chain's gamma
cannot be the spatial metric of arbitrary matter, and Lovelock's
uniqueness presupposes a general metric. Scope: this failure is
sufficient only under the rank-one reading; a genuine ensemble
average of several fields could produce any metric with eigenvalues
in (0, 1], which the source does not posit. CORRECTION OF RECORD:
the first version of the script checked delta + grad grad - the
wrong sign relative to the dictionary - and the Euclidean Gauss
formula; found by the audit, fixed to the dictionary's sign.

## Failure 4 - the covariance hypothesis (cited, not computed)

Lovelock (J. Math. Phys. 12, 498 (1971)) characterises the unique
divergence-free symmetric second-order tensor under diffeomorphism
covariance in four dimensions. Diff(M) is infinite-dimensional;
SL(2,R) is three-dimensional and acts on the Farey/Stern-Brocot
structure, not on a 4-manifold. Transitivity of a finite-dimensional
group is not general covariance. P8's fourth hypothesis is not met,
independently of failures 1-3.

## Audit of record (2026-08-22)

A context-free auditor attempting to overturn the refutation found
the verdict sound and three supports defective as first written
(the general principle in failure 1; the vacuous lapse test in
failure 2; the metric sign in failure 3) - all corrected above. The
auditor also noted the chain's "second-order in metric derivatives
because Kuramoto is first-order in theta" (PROOF_A line 139)
conflates field-derivative order with metric-derivative order and
space with time. Failure 4 stands as written.

## What survives

Nothing of the chain. What is true nearby: Kuramoto lattices have a
continuum limit (a nonlinear diffusion equation), locked states have
a uniform clock, and correlation tensors of gradients are graph
metrics - each a classical fact, none a road to GR. The pattern is the
one X-8/X-9 name: a kinematic structure (a locked phase field) spoken
of in the vocabulary of a dynamical theory (Einstein's). Mood: the
four failures are independent; any one suffices; the refutation
script's mutant ('inertial') shows check 1 discriminates.
