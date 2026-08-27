<!-- evidence: scripts/experiments/p18_derive.py, scripts/experiments/p18_registration.json, scripts/experiments/p18_smooth.py, scripts/experiments/p18_results.json, scripts/verify/p18_smooth_retest.py -->
# P-18: the C2 retest - the corners were the failure, the theory was not

Symbols: see the VOCABULARY.md symbol graph - shift_k falls out of V at first order on C2 profiles; omega_k falls out of the metric for k in [5, 60].

Registered before computing (PREDICTIONS.md P-18); resolution R-13,
all six clauses as registered, mind-change not fired. This closes
open item A-6 and completes the arc that R-10 left honest but
unfinished: P-14's per-mode clause fired its mind-change at RMS
2.89 x Vbar, and the post-firing diagnosis blamed the linear ramp's
two derivative discontinuities. A diagnosis is a claim. This was
its registered test.

## The construction

Same geometry as P-14 - c from 1.0 to 0.5 across [150, 1350] on
L = 1500 - but the ramp is the quintic smoothstep
s = 6u^5 - 15u^4 + 10u^3, which has s' = s'' = 0 at both ends. The
derivation layer (p18_derive.py, all "=" through the CAS) pins
before any eigensolve:

- the general closed form for Z = 1/c in travel-time coordinates:
  V = c'^2/4 - c c''/2 (EQ1), whose linear limit is P-14's b^2/4
  (EQ2);
- that the quintic's endpoint conditions make V globally continuous
  and ZERO at the ramp edges (EQ3) - no corners exist to blame;
- the smoothness certificate int V dtau = int c'^2/(4c) dx, exactly
  the boundary term [c'/2] that C1 corners fail to cancel (EQ5);
- T = 2160.746347, Vbar_s = 4.720552e-8, and 80 per-mode shifts by
  quadrature, including a SIGN FLIP at k = 1: shift_1 = -8.00e-8,
  structure the linear profile never had (EQ6);
- Fourier decay of the oscillatory part, the signature of a
  continuous V (EQ8).

## What the eigensolves returned

Sturm bisection, n = 1499 and 2999, Richardson in a^2, sramp minus
szramp; the P-14 linear pair rerun on the same grids as a positive
control. Results (p18_results.json):

- RMS over k = 5..60 of (Delta omega_k^2 - shift_k) = 0.004 x
  Vbar_s. The bar - the SAME one P-14's clause d registered and
  failed - was 0.3.
- The sign flip is in the data: Delta omega_1^2 = -1.04e-7 against
  the pinned -8.00e-8. The 2.4e-8 excess at k = 1 is grid-converged
  (identical at the verify script's n = 599/1199), i.e. a genuine
  second-order/lowest-mode effect, outside the registered window
  and outside the claim.
- Window mean 4.6709e-8 vs pinned 4.6620e-8 (0.19 percent apart).
- The control reproduces R-10's number: RMS 2.893 x Vbar_lin at
  n = 1499/2999 (R-10: 2.89), and 2.896 at the verify script's
  miniature grids - the failure ratio is grid-stable, consistent
  with a profile property, not a lattice artifact.
- Improvement factor: 756.

## Reading

The commutator-audibility chain of P-13/P-11/P-14 now stands on a
per-mode footing: the metric is gauged away in travel-time
coordinates, the impedance survives as a Schrodinger potential, and
on a substrate smooth enough for first-order theory the spectrum
returns that potential mode by mode with no free parameters -
including the sign structure of its Fourier data. What broke in
P-14 was the substrate's differentiability class, and that
diagnosis is now tested rather than told: remove the corners and
the original bar is passed with two orders of margin; keep them and
the failure reproduces on the same grids at the same magnitude.

Not claimed: any mechanism account of the corner residual itself
(beyond its absence here), higher orders in V, other boundary
conditions or profiles, dimensions above one.
