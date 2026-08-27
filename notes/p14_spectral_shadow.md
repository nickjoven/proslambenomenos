<!-- evidence: scripts/experiments/p14_derive.py, scripts/experiments/p14_registration.json, scripts/experiments/p14_spectral_shadow.py, scripts/experiments/p14_results.json, scripts/verify/p14_isometric_spectra.py -->
# P-14: the commutator kernel is spectrally audible - what held, what fired

Symbols: see the VOCABULARY.md symbol graph - V = (sqrt Z)''/sqrt Z falls out of Z in the tau gauge - C2 profiles only (this line found the boundary).

Registered before computing (PREDICTIONS.md P-14); resolution R-10,
whose mind-change condition FIRED on the k-resolved clause. This
note reports both halves with their labels.

## The construction

Two chains share P-13's metric profile c(x) and differ only in
impedance: ramp (Z = 1/c) and zramp (Z = 1). In travel-time
coordinates the metric is gauged away and the entire difference is
the Schrodinger potential V = (sqrt Z)''/sqrt Z - which the CAS
shows is the CONSTANT beta^2/4 = 4.340e-8 on the ramp (EQ2, worst
deviation 2.7e-23) and identically zero for zramp (EQ3). Eigensolves
are Sturm-sequence bisection on the symmetrized tridiagonal - exact
linear algebra validated to 1e-12 against the uniform chain's closed
form (EQ6), no timestep anywhere.

## What held (the claim)

**Commutator-isometric, not isospectral.** The weighted-seminorm
end-to-end distances agree between the two chains within 1.18e-4
(n = 1499), halving at n = 2999 - O(1/n) bookkeeping around
identical metric data - while the spectra differ at every low mode:
max |Delta omega_k^2| = 2.31e-7 with 1e-12 resolution. Both spectra
obey Weyl with the SAME leading term (|omega_k T/(k pi) - 1| <
2e-3 for 5 <= k <= 60): the metric is the leading spectral data,
and the impedance split is audible beneath it. Filed as
isometric-not-isospectral-chain.

## What fired (no claim)

The k-resolved zero-free-parameter prediction - Delta omega_k^2
equals the pinned first-order shift shift_k - failed with RMS
2.89 x Vbar; the registered mind-change threshold was 1.0 x Vbar.
It stays dead at these grids. Post-firing diagnosis, computed and
labelled post hoc:

- the window MEAN matches the impedance potential at 0.9%
  (3.443e-8 measured vs 3.414e-8 pinned) - an observation, not a
  claim;
- the metric-split alternative named in changes-my-mind is
  excluded: corr(residual, k^2) = 0.003;
- the residual is a bounded, sign-alternating oscillation
  consistent with lattice scattering off the profile's two
  derivative kinks at tau = 150 and 1813.6 - structure that
  first-order continuum theory does not model.

The honest retest is a C^2 ramp (no kinks), re-registered as its
own P-line; queued, not run (OPEN A-6).

## Reading (commentary within an evidence note, no load)

The Weyl clause's own failure at k = 1 (3.0e-3, exactly the V-shift
as a relative effect) is the neatest sentence in the run: at the
lowest mode, the "subleading" impedance data is a percent-level
part of the audible spectrum. The lossy shadow picture survives at
the level it was claimed (P-13, P-11, and here clauses a + c); its
quantitative first-order form owes a kink-free retest before it is
claimed at k-resolution. Classical anchors: one spectrum
under-determines a Sturm-Liouville operator (Borg, Acta Math. 78,
1 (1946); Gelfand-Levitan 1951); audibility questions: Kac (1966);
Gordon-Webb-Wolpert (1992).
