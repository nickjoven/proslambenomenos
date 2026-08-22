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

## Failure 1 - order in time (computed)

Kuramoto: theta' = omega + K sum sin(...). First order, gradient-like.
Linearised about a locked state it is the heat equation theta_t = K
nabla^2 theta: parabolic, infinite propagation speed. A localised
perturbation's width grows as t^(1/2); measured 0.500 on a 401-site
locked ring. ADM: the pair (gamma_ij, K_ij) obeys second-order
hyperbolic evolution; width grows as t^1; the same lattice with
inertia (m theta'' + ...) gives 0.989. No operation of differentiating
a first-order dissipative flow produces a second-order reversible one;
the order of the characteristic structure is an invariant of the
equation class (Hadamard; Courant-Hilbert II). The chain's "follows
from differentiating" has no derivation in the corpus and cannot have
one.

## Failure 2 - the lapse is constant where the chain lives (computed)

"Locked" means theta_i' = Omega for all i. The dictionary sets N = r;
but N's physical content is the position dependence of proper-time
rate, and in a locked state that dependence is identically zero
whatever r(x) does. Checked: a ring with coupling varying 0.2-1.0
along x (coherence gradient) relaxes to uniform frequency, residual
3.4e-5 -> 5.0e-6. The chain identifies the lapse in exactly the regime
where the lapse has no work to do. Side note: this is the same
identity as klein-twisted-mean-frequency-identity - the collective
clock is untouched by the coupling geometry.

## Failure 3 - the metric is a graph metric (computed)

gamma = delta + dtheta (x) dtheta is the induced metric of the
hypersurface z = theta(x) in flat R^(n+1): det gamma = 1 + |grad
theta|^2, and its curvature satisfies the Gauss equation of that
embedding; in 2D, K = det(Hess theta)/(1 + |grad theta|^2)^2, checked
against the Brioschi formula to 4e-4 on random theta. Such metrics
are codimension-one flat embeddings. A general 3-metric is locally
embeddable only in up to 6 flat dimensions (Janet 1926; Cartan 1927),
so the chain's gamma spans a thin subfamily; the Einstein equations
for arbitrary matter cannot be satisfied within it. Lovelock's
theorem, which the chain invokes, presupposes the metric is general.

## Failure 4 - the covariance hypothesis (cited, not computed)

Lovelock (J. Math. Phys. 12, 498 (1971)) characterises the unique
divergence-free symmetric second-order tensor under diffeomorphism
covariance in four dimensions. Diff(M) is infinite-dimensional;
SL(2,R) is three-dimensional and acts on the Farey/Stern-Brocot
structure, not on a 4-manifold. Transitivity of a finite-dimensional
group is not general covariance. P8's fourth hypothesis is not met,
independently of failures 1-3.

## What survives

Nothing of the chain. What is true nearby: Kuramoto lattices have a
continuum limit (a nonlinear diffusion equation), locked states have
a uniform clock, and correlation tensors of gradients are graph
metrics - each a classical fact, none a road to GR. The pattern is the
one X-8/X-9 name: a kinematic structure (a locked phase field) spoken
of in the vocabulary of a dynamical theory (Einstein's). Mood: the
four failures are independent; any one suffices; the refutation
script's mutant ('inertial') shows check 1 discriminates.
