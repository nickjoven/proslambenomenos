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
| **soliton** | a corner's stable descendant: nonlinearity balancing dispersion in an inertial medium | cited (Toda, KdV; LC-4 Holian-Flaschka-McLaughlin) - no artifact yet |
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
