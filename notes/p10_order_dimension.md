<!-- evidence: scripts/experiments/p10_mm_dimension.py, scripts/experiments/p10_results.json, scripts/experiments/p10_symbolic.py -->
# P-10: dimension from pure order (Myrheim-Meyer)

Symbols: see the VOCABULARY.md symbol graph - d_hat falls out of order + count; the unordered-vs-Gamma factor 2 is recorded as a convention trap.

Registered before computing (PREDICTIONS.md P-10, commit 3ce3997);
run 2026-08-24 in worktree wt-p10-order-dimension, seed 20260824.
Derivation and every checked equality: scripts/experiments/
p10_symbolic.py (27 EQ lines, all PASS, output committed as
p10_symbolic_out.txt); experiment p10_mm_dimension.py; results
p10_results.json; resolution R-7. Proposed falsifier
p10_verify_proposed.py (integrator to move into scripts/verify/ if
a claim is filed). Every displayed equation below carries the EQ id
of the line that checks it.

## The null, by direct integration

N points uniform in the causal interval I(p,q) of d-Minkowski, unit
proper time; x precedes y iff dt > |dx|. The related-pair fraction
f(d) = E[R]/C(N,2) depends on d alone:

    f(1) = 1   f(2) = 1/2   f(3) = 8/35   f(4) = 1/10
    (EQ 5-10; rational arithmetic where the integrand is polynomial,
    Simpson quadrature with refinement control elsewhere)

    f(d) = Gamma(d+1) Gamma(d/2) / (2 Gamma(3d/2))     (EQ 11-14)

Convention pinned by the integrals: the usually quoted
Gamma(d+1)Gamma(d/2)/(4 Gamma(3d/2)) is the ORDERED-pair
probability; the unordered related fraction is twice it (at d=2 the
lightcone-coordinate integral gives 1/4 ordered, 1/2 related, EQ
6-7). The estimator inverts f by bisection (monotone, EQ 15;
round-trips at d = 2, 3, 4, EQ 16-18). Dimension is read off the
order relation alone - Myrheim 1978, Meyer 1988, Sorkin's "order +
number = geometry"; novelty status: classical reproduction, no new
mathematics claimed.

## Variance, derived rather than assumed binomial

With g(x) = tau(p,x)^d + tau(x,q)^d (the fraction of the interval
related to x; volumes by EQ 1-4),

    Var(R) = C(N,2) f(1-f) + 6 C(N,3) (E[g^2] - f^2)
    E[g^2] = 5/18 (d=2, EQ 19), 0.0742857 (d=3, EQ 21),
             1/50 (d=4, EQ 20)

The shared-point covariance term dominates: sigma_f is 5.4x the
binomial value at N=2^7 and 43x at N=2^13 (BAND table in
p10_symbolic_out.txt). Registered bands: |mean_M d_hat - d| <=
|delta-method bias| + 4 sigma_d / sqrt(M).

## Results (p10_results.json; d_hat means over M sprinkles)

| d | N=2^7 | 2^9 | 2^11 | 2^13 | band 2^7 -> 2^13 |
|---|---|---|---|---|---|
| 2 | 2.020 | 1.994 | 2.006 | 1.999 | 0.052 -> 0.011 |
| 3 | 3.024 | 2.990 | 3.002 | 3.002 | 0.099 -> 0.021 |
| 4 | 4.079 | 3.984 | 3.999 | 3.993 | 0.153 -> 0.031 |

All 21 null cells in band; sample SD / derived sigma_d in
[0.72, 1.34] everywhere (registered window [0.4, 2.2]; the binomial
sigma would fail it at every N); SD shrinks ~ N^(-1/2); RMS mean
error 0.049 -> 0.004 from N=2^7 to N=2^13; acceptance rates match
the derived volume fractions 1/2, pi/12, pi/24 (EQ 1-3) within 4
binomial sigma at every cell.

## Mutants (order scrambled, point marginals kept)

Derived in advance (registered): permuting a lightcone coordinate
at d=2 is a distributional symmetry (iid product measure, EQ 22);
permuting the t coordinate at d=2 leaves f centred at 1/2 because
the time and space marginals of the diamond are the same triangle
density (EQ 23-25). Both d=2 mutants duly stayed in band at all N.
For d >= 3 the t-shuffle null is f_shuf(3) = 0.2141 -> d* = 3.080,
f_shuf(4) = 0.0824 -> d* = 4.230 (EQ 26-27).

Measured: d=4 shuffled-order outside every band (means 4.218-4.323,
tracking d* = 4.230); d=3 outside at six of seven N. The exception,
(d=3, N=2^8), mean 3.051 vs band 0.068, is a registration design
error recorded in R-7: the derived displacement 0.080 clears that
band by 0.9 sigma of the mutant mean, so the registered
"outside every d=3 band with N >= 2^8" ignored the mutant's own
sampling noise. Not rescued; the paired mutant-minus-null
difference there is 0.073, consistent with the derived 0.080.

## Scope

Flat Minkowski intervals only; fixed-N binomial sampling (not
Poisson-N); integer d = 2, 3, 4; nothing about curved spacetimes,
spectral dimension, or our universe. The d=2 estimator cannot be
falsified by marginal-preserving shuffles (mean-level symmetry,
above); its working falsifier lives at d >= 3.

## References

- J. Myrheim, "Statistical geometry", CERN preprint TH-2538 (1978).
- D. A. Meyer, "The dimension of causal sets", PhD thesis, MIT (1988).
- R. D. Sorkin, "Causal sets: discrete gravity" - the slogan
  "Order + Number = Geometry"; see also Brightwell-Gregory,
  Phys. Rev. Lett. 66, 260 (1991) for the neighbouring estimator.
