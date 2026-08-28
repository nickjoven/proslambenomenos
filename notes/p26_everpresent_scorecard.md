<!-- evidence: scripts/experiments/p26_derive.py, scripts/experiments/p26_registration.json, scripts/experiments/desi_dr2_table4.json, scripts/experiments/p26_score.py, scripts/experiments/p26_results.json, scripts/verify/p26_everpresent_scorecard.py -->
# P-26: the everpresent-Lambda scorecard on DESI DR2 BAO

## What was asked

A-14 (the 2026-08-27 paradigm scan's entry point): c31 records that
Sorkin's causal-set count-fluctuation argument lands 0.4 orders of
magnitude from the observed Lambda, and DESI DR2 now prefers
evolving dark energy over LCDM. Do the concrete everpresent-Lambda
DYNAMICS survive the one likelihood this repo can recompute — the
DR2 BAO Table 4 compression — when scored in the bit currency?

## The derivation layer (all pre-registration)

- The past-lightcone 4-volume in exact matter domination is
  V = (3 pi/55) t^4 and in exact radiation domination
  V = (8 pi/105) t^4 — Beta-function integrals, reproduced by the
  production incremental accumulator on its own grid.
- The DNY Model 1 update makes S = Lambda V a Brownian walk in
  V-time, so sigma_Lambda = 8 pi alpha/sqrt(V), and the fluctuation
  RELATIVE TO CRITICAL is era-fixed and alpha-linear:
  2 sqrt(165 pi) alpha = 45.54 alpha (matter),
  (8/3) sqrt(210 pi) alpha = 68.49 alpha (radiation).
  That is the quantitative meaning of "everpresent": a constant
  fraction of the total density at every epoch — which is exactly
  what makes the model both attractive (the c31 magnitude) and
  fragile (nothing suppresses the fluctuation early).
- Bits = dchi2/(2 ln 2). DNY's own published SNe record prices to
  net -10.0 bits (16 winners of 90000 seeds, dchi2 3.4). The 2-dof
  sigma<->dchi2 map reproduces DESI's published -12.5 from their
  3.1-sigma statement to 0.005 — the conversion is validated
  against the source before it is used.

## The scorecard (R-23)

| model | on DR2 BAO alone | bits |
|---|---|---|
| flat LCDM | chi2 10.55/11 dof; Omega_m 0.2970, h r_d 101.56 Mpc (published: 0.2975 +- 0.0086, 101.54 +- 0.73) | reference |
| w0waCDM | dchi2 = 4.74 (source's own characterization: 1.7 sigma ~ 4.84); prior-railed at wa | +3.42 bought, 3.70 MDL price: net -0.28 |
| everpresent Model 1 | 0 of 90000 realizations beat LCDM; best survivor +22.8 on the wrong side; median survivor 1555 (Einstein-de Sitter: 1457) | net -14.9 to -39.5 every cell |

Survival to a = 1: 0.994 (alpha 0.005), 0.194 (0.01), 0.000 (0.02,
all three Omega_m), 0.000 (0.04). The squeeze that produces the
zero: the walk's mean is zero, so the small-alpha limit is
Einstein-de Sitter (no dark energy, chi2 1457); the radiation-era
amplitude 68.5 alpha kills large alpha before today; and in
between, mimicking Lambda requires an excursion of about three of
the walk's own sigmas held steady across all of z < 2.33, which no
realization among 90000 managed even approximately.

DR2 BAO is the decisive upgrade over the data DNY tested: their
SNe scatter allowed 16 lucky seeds in 90000; the sub-percent BAO
distance ladder allows none.

## Honesty trail

- First full run: clause (c) read 0.00000 because the validation
  mode's recorded E^2 omitted rho_Lambda — the wiring check caught
  its own omission and voided the run, which is what it is for.
- The zero-initialized lightcone volume killed 99.3 percent of
  alpha = 0.005 realizations at birth (sigma ~ 1/sqrt(V_acc)
  diverges); DNY specify V_0 at the start; the fix initializes the
  eta-moments to their exact radiation-era closed forms, which
  reassemble to (8 pi/105) t^4.
- The first beat threshold was an alpha = 0 realization — which is
  Einstein-de Sitter, not LCDM, since the walk is the model's only
  dark energy (chi2 1457.2). Replaced by the LCDM best fit pushed
  through the same native-grid pipeline (grid bias +0.020,
  cancelled). Kept as the eds-threshold falsifier mutant: the bug
  became the mutant.
- A covariance-blind mutant was tried and discarded as
  non-discriminating: zeroing the printed correlations moves chi2
  by 0.92 and Omega_m by 0.002. Table 4 is error-dominated per
  block — worth knowing, useless as a falsifier.
- Survival fractions are discretization-pinned (256-step verify
  marcher: 0.235; 512-step production: 0.194): finer marching can
  only find more deaths, so these are upper bounds on continuum
  survival. The zero-beat verdict does not inherit this caveat.

## What this does and does not settle

Does: the ZAS/DNY Model 1 dynamics, at any registered amplitude,
cannot be rescued by DESI DR2 BAO — the dataset most often cited
as friendly to fluctuating dark energy. The bit ledger makes the
seed-selection cost explicit instead of narrative.

Does not: the c31 order-of-magnitude coincidence (untouched and
still recorded as such); DNY Models 2/3; CMB and SNe likelihoods
(imported, LC-16); any statement about w0waCDM as physics — on
BAO alone it nets -0.28 bits, and the headline preferences live in
the CMB-lensing and SNe combinations that Wang-Mota contest.
