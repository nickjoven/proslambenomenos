# The vocabulary

The minimum set of terms in which every proven, verified, or
catalogued statement of this repository can be written, with the
demonstration that earns each term. The v1 framework's alphabet
{integer cycles, coupling, winding p/q, circle, mediant} assumed the
circle (harmonics E14), lacked amplitude, dissipation and scale, and
imported dimension; this list replaces it. A term is admitted only if
some runnable artifact needs it. A term that no artifact needs is
prose. Rule for extension: a new term enters with the catalog entry
or claim that requires it, not before.

## Primitives (cannot be defined from the others)

| term | meaning here | earned by |
|---|---|---|
| **order** | which event can influence which; causal precedence | X-10 (Malament: order fixes the conformal class) - cited, not computed |
| **count** | an integer or rational obtained by enumeration | c10 phi(q), c17 deficit turns, C1 depth-12 tree, P-6 certificate |
| **phase** | a point on U(1) = R/Z; a return, not a length | X-6/X-11; klein-twisted-gradient-xor (windings in Z + 1/2) |
| **amplitude** | the radial coordinate a phase-only model lacks; what a restoring force acts on | c21 (AM = FM only where the circle is Cartesian); X-7 (the amplitude-zero core) |
| **scale** | the conformal factor; the one thing order does not fix | c18 (curvature as the deviation of measured pi), X-10 (Sorkin's "number") |
| **dissipation** | irreversibility; what makes a record and an arrow | c26 (mud records direction), Proof Chain A refutation (gradient flow vs Hamiltonian) |

## Derived terms (defined from primitives; each with its demonstration)

| term | definition | demonstration |
|---|---|---|
| **period / return** | the smallest count of phase at which a state repeats | T0 notebook; c24 (rational returns, irrational never) |
| **rotation number** | phase advance per return, averaged over the whole orbit | C8; P-8 (finite-T bias ~ T^-2) |
| **holonomy** | phase accumulated around a closed loop; the only loop-invariant phase | c19 (latitude loop 2 pi (1 - cos theta)); the pi twist; P-4 R-3 (a clamp opens the loop and the holonomy vanishes) |
| **winding** | holonomy in units of full turns; a count | klein-twisted-gradient-xor; c20 (track period = circumference/n) |
| **sector / class** | a locally constant function of the medium (a bundle class, a parity, a Chern number) | C14 (four characters), half-shift-squares-by-x-parity, c25 (Dirac point at half flux) |
| **locking / plateau** | an interval of a parameter over which the rotation number is constant and rational | C8/C9/C10; c23 (Adler range); catalog c12/c13 |
| **drive** | an external periodic or constant input; what forces (classically) | E1's pinning; R-1 (no drive, no staircase: the mean-frequency identity) |
| **null system** | the simplest system in which the same computation gives the same answer | LAW-11 field; the refutation of twisted-sector-complex-structure |
| **invariant integral** | an integral of a medium-dependent integrand over a closed domain, valued in counts | c17 (Gauss-Bonnet), index theorems (cited) |
| **corner / weak discontinuity** | a propagating jump in a derivative, carried on characteristics, killed by dispersion or damping | X-12; c11 (chain dispersion); T5 notebook |
| **soliton** | a corner's stable descendant: nonlinearity balancing dispersion in an inertial medium | c29 (Toda chain: shape kept to 0.1%, v/c = sinh k/k; linear mutant disperses); notes/toda_solitons.md |
| **critical point** | the marginal parameter value between two behaviours, where scaling is universal | saddle-node-passage-time (pi/sqrt(mu)); c05 (Toomre Q = 1); P-8 exponent 2 |
| **universality** | a number fixed by the critical point, not by the medium | golden-mean-shenker-scaling; staircase-phi-squared-scaling |
| **rigidity / vacuity** | the two ends of "does the class reach the observable": fixed by it / untouched by it | P-3 and P-6 (rigidity); P-1, P-4, P-9 (vacuity) |
| **resolution** | the smallest change a finite window can report; Delta t * Delta f >= 1/4 pi | P-8; LC-4 (Gabor) |
| **record** | a dissipative imprint that fixes order after the fact | c26; the tread in mud; the ledgers of this repo |

## What the vocabulary cannot say (and must not pretend to)

- anything about **mass values** or **dimensionful constants** without a declared scale (harmonics E20, MANIFEST anchors);
- anything **non-local in the Bell sense** (LC-8: Gisin, Bell);
- anything that makes a **sector select a dynamics** (X-8/X-9: classes force which counts exist; only a drive or a threshold selects);
- anything **novel** until a litcheck says so (LAW-6, LC-1..8).

## Completeness test

Every statement in claims/*.yml with status proven or verified, and
every catalog docstring, should be expressible in the terms above.
Where one is not, either the vocabulary is missing a term (add it
with its demonstration) or the statement is carrying load it has not
earned (fix the statement). This file is the checklist; it is not a
gate, because a lexicon gate would be gamed by synonyms the same way
LAW-3's conclusive-vocabulary list was (F5).

## The symbol graph (verified interoperability)

Where two lines write the same symbol, this graph records whether the
repo has COMPUTED the equivalence, in which regime it holds, and
where it breaks. An edge "X <- Y" reads "X falls out of Y". Rule,
inherited from the vocabulary: an edge enters only with the runnable
artifact that verified it, and every edge carries the scale at which
it was verified - most edges here were EARNED by watching them fail
outside that scale first.

### Layer 0 — substrate parameters (chosen, never derived)

m(x), J(x) [chain masses, couplings] · K [ring stiffness] ·
eps [injection / lock rate] · D [noise strength] · N [system size] ·
delta [detuning] · k [Schmidt ratio]

### Layer 1 — falls out of the substrate

| symbol | falls out of | scale where verified | earned by |
|---|---|---|---|
| c = sqrt(J/m) | (m, J) | long wavelength, ka << 1 | P-13/R-8: arrivals read c at RMS <= 0.32% |
| Z = sqrt(mJ) | (m, J) | below the band edge | P-13/R-8: junction R = ((Z1-Z2)/(Z1+Z2))^2, 0.362 vs 0.360 |
| (m,J) <-> (c,Z) | bijection | leaks exactly at the band edge: the jz residual 0.036 is the pulse's evanescent flux (predicted 0.039) | P-13/R-8 |
| U(theta) = -(eps/2)cos 2theta | eps | overdamped, twice-frequency injection | P-22 EQ2 |
| Delta_E(N) | (K, N) via E(Delta), Delta* = pi(N-3)/(N-2) | w = 1 sector, N >= 5 (N = 4: barrier exactly 0) | P-24 EQ3/R-19 |

### Layer 2 — falls out of layer 1

| symbol | falls out of | scale where verified | earned by |
|---|---|---|---|
| tau = int dx/c | c | continuum travel time | P-13/P-14 (T pinned 2113.553, 2160.746) |
| V = (sqrt Z)''/sqrt Z = c'^2/4 - c c''/2 | Z, in the tau gauge | C2 PROFILES ONLY - at C1 the equivalence breaks (R-10 fired; P-18 repaired it at 0.004 Vbar) | P-14 EQ2, P-18 EQ1-3/R-13 |
| tongue half-width = eps | eps | first order, deterministic Adler | P-22/R-17(a) |
| memory barrier = eps | U, CAS max - min | same eps as the tongue: one symbol, two verified roles | P-24 EQ2 - the P-22/P-24 interop edge |

### Layer 3 — observables

| symbol | falls out of | scale where verified | earned by |
|---|---|---|---|
| omega_k ~ k pi/T | tau (the metric) alone | k in [5, 60]; k = 1-2 EXCLUDED (the V-shift is a percent-level relative effect there - R-10 clause b) | P-14/P-18 |
| shift_k = (2/T) int V sin^2 | V | first order in V, C2 profiles | P-18/R-13: RMS 0.004 Vbar, derived sign flip at k = 1 |
| beat = sqrt(delta^2 - eps^2) | the tongue | outside; estimator floor 2 pi/T (R-17's corrected boundary) | P-22/R-17 |
| tau_1 = 1/D | diffusion generator, eigenvalue 1 | all D, exact | P-24 EQ1/R-19(a) |
| tau_2 = T_MFPT(eps, D) | (U, D), exact quadrature | any D by quadrature; Kramers form at D << eps | P-22/R-17(d), P-24/R-19(b): Arrhenius slope 0.970 vs CAS barrier 1 |
| <cos 2theta> = I1(kappa)/I0(kappa), kappa = eps/2D | the stationary von Mises density | delta = 0, stationary averages | P-23/R-18 (0.24-1.23 SEM) |
| rate_3 = N Langer(H) e^(-Delta_E/D) | (Delta_E, Hessians, N) | Delta_E/D in [2.3, 7.1], verified 0.03-0.18 nat; NOT extensive (Delta_E saturates at 2K) | P-24/R-19(c) |
| d_s(t) = 2t <lambda>_P | the spectrum | window t < 0.5/lambda_1 (two-mode boundary 0.5433) | P-15/R-11 |
| d_hat | order + count via f(d) | sprinkled orders; CONVENTION TRAP: unordered f = 2x the usually quoted Gamma form | P-10/R-7 |
| S <= 2; S_QM <= 2 sqrt 2 | enumeration; the Landau identity | two settings, two outcomes | P-17/R-12 |
| p_Hardy max = phi^5 = (5 sqrt 5 - 11)/2 | y^2 - 3y + 1 = 0, y = k + 1/k | two qubits, projective; VANISHES at maximal entanglement | P-21/R-16, exact in Q(sqrt 5) |

### Cross-line edges (the same object verified in two homes)

- **eps**: tongue half-width (P-22) and Kramers barrier (P-24) - the
  same registration defines both from the same U; CAS-exact.
- **Vbar**: the impedance potential's mean shifts spectra (P-14/P-18)
  AND drifts the spectral-dimension trace as 2 Vbar t (P-15, measured
  1.008-1.015 of derived) - the instrument sees the potential.
- **I1/I0 continued fraction**: one instrument, two homes - P-15
  heat-kernel ratios and P-23 locked-phase equilibrium, each
  validated to 1e-12 against an independent route. The bridge
  DERIVATION (why one function serves both) is not yet registered:
  flagged, not claimed.
- **T_MFPT quadrature**: one construction verified against
  simulation in three lines (P-22 hops, P-23 budgets, P-24 rungs).
- **winding w**: the P-6 twisted-state count and P-24's rung-3
  charge are the same primitive; the ALF lock index m (P-19) is its
  branch-pending cousin.

### Verified refusals (equivalences the repo computed and REJECTED)

- c is NOT a complete substrate summary: scattering follows Z, not c
  (P-13); the spectrum hears the remainder (P-14/P-18).
- The metric does NOT fall out of the commutator in every
  representation: vertex-only caps distances at 2/sqrt 3 and sqrt 2;
  geodesic recovery is a property of the coupling (P-11).
- Delta_E does NOT scale extensively: no free topological memory in
  classical 1D (P-24 EQ5; a chat guess died there pre-registration).
- phi does NOT fall out of alpha^-1, g_e, the Omegas, the 2D
  Madelung constant, or the Kerr Davies point (LC-11, LC-12,
  notes/otto25_mechanization.md: excluded at 788 to 2e5 sigma, or
  net-zero information).

### The phi taxonomy (correcting an overstatement caught in review)

The golden numbers enter the ledger by exactly three routes, and the
refusals above concern only the third. The statements apply to the
whole class, not the single number: 1/phi = 1 + phi and every
(a phi + b)/(c phi + d) share the field Q(sqrt 5) and the
eventually-all-ones continued-fraction tail, so an admission or a
refusal of phi is one of the entire orbit.

1. AS THE ANSWER (algebra): Hardy's maximum p = phi^5 falls out of
   y^2 - 3y + 1 = 0 in y = k + 1/k (P-21/R-16, exact in Q(sqrt 5)).
   The one verified place where a physical quantity IS a golden
   number. (The Kepler-pyramid ratio pi phi^5 is exact geometry of
   the ideal shape - a math-let, not physics; the monument cannot
   decide, notes/otto25_mechanization.md.)
2. AS THE ADDRESS (Diophantine): the golden winding is the
   most-irrational rotation number, and criticality there is
   universal - imported as golden-mean-shenker-scaling (delta =
   2.83361, exponent ln delta/ln phi = 2.164). Here phi names WHERE
   and ln phi is the YARDSTICK (each Fibonacci approximant step
   contracts distances to phi by phi^2), but the universal constants
   at that address are NOT functions of phi: the claim that the
   staircase scales by phi^2 is in the refuted bin
   (staircase-phi-squared-scaling: 2.618 is not 2.834). Logarithms
   are therefore not refused - ln phi already serves as the ledger's
   golden-criticality unit, and the graph's observable layer runs on
   log-linear edges throughout (Arrhenius, nat bands, bit
   accounting). The entropy/growth edge is now EARNED:
   P-7/R-20 measured the critical Harper bandwidth contracting per
   Fibonacci-approximant step at ln(S(89)/S(144)) = 0.48075 against
   ln phi = 0.48121 - the ln phi clock, decomposed as clock (the
   F-ratio) times flatness (Thouless's imported plateau 32 G/pi,
   which the same ladder lands 0.0011 away). The remaining unearned
   relatives (cat-map Lyapunov 2 ln(1+phi), golden-shift entropy)
   stay in the unearned bin until their artifacts exist.
3. AS A FITTED CONSTANT: refused wherever computed - the block
   above.
- d_s is NOT one object on a causal set: the walk and d'Alembertian
  definitions diverge at short scale in direction and refinement
  trend (P-16/R-21), and the walk's own two clocks separate by
  derivable parity effects of the triangle-free Hasse graph
  (P-25/R-22) - definition- and protocol-dependence, both computed.
- The ALF period is NOT an integer subharmonic (P-19/R-14, landed
  via PR 61).
- Lambda's observed magnitude falls out of Sorkin's 1/sqrt(N)
  counting to 0.4 orders (c31, coincidence-unruled) - but the
  DYNAMICS that would make that edge live are refused: the ZAS/DNY
  Model 1 walk, with its exactly-derived amplitude
  sigma_OmegaLambda = 2 sqrt(165 pi) alpha (matter era) and
  (8/3) sqrt(210 pi) alpha (radiation era) falling out of the
  lightcone-volume closed forms (3 pi/55) t^4 and (8 pi/105) t^4,
  is priced out on DESI DR2 BAO at every registered amplitude
  (P-26/R-23: zero beats in 90000 - a mean-zero walk does not hold
  Omega_Lambda). The magnitude edge stays a coincidence entry; no
  dynamical edge is earned.
