<!-- commentary -->
# Does a0 track H(z)? The discriminating test

Status: synthesis note. Nothing here is derived; the rival hypotheses
are all in the literature, and the contribution — if any — is the
side-by-side statement of what data would decide among them.
Claims: a0-milgrom-coincidence (coincidence-unruled),
a0-tracks-hubble-conjecture (asserted).

## The three hypotheses

At z = 0, a0_obs ~ 1.2e-10 m/s^2 and c*H0/(2*pi) = 1.04e-10 m/s^2
(ratio 1.15) — the Milgrom coincidence, unexplained since 1983. If it
is not a coincidence, a0 should evolve. Under flat LCDM
(H0 = 67.4, Omega_m = 0.315):

| z | H(z)/H0 | a0 ~ cH(z)/2pi | a0 constant | a0 ~ (1+z)^0.75 (Xu) |
|---|---|---|---|---|
| 0.5 | 1.32 | 1.32x | 1x | 1.36x |
| 1.0 | 1.79 | 1.79x | 1x | 1.68x |
| 2.0 | 3.03 | 3.03x | 1x | 2.28x |
| 3.0 | 4.57 | 4.57x | 1x | 2.83x |
| 5.0 | 8.29 | 8.29x | 1x | 3.83x |

The cH(z) and Xu scalings agree to ~15% at z <= 1.5 and separate
cleanly only at z >= 3 — so distinguishing those two needs the high-z
regime, while ruling constant a0 in or out is already a z ~ 2 question.

## The observable

The baryonic Tully-Fisher zero point: in the deep-MOND regime
V_flat^4 = G*Mb*a0, so a factor-3 shift in a0 by z = 2 moves the BTFR
normalization by ~0.5 dex in log Mb at fixed V_flat. Constant a0
predicts no evolution.

Current state (as of early 2026): RC100 (Nestor Shachar et al. 2023)
shows declining dark-matter fractions with z — qualitatively consistent
with rising a0 — but McGaugh et al. (2024) find no clear BTFR zero-point
evolution to z ~ 2.5. Neither settles it, because RC100 is massive
galaxies (V > 200 km/s), where the Newtonian regime dominates and an
a0 shift is least visible, and per-curve errors of 20-40% swamp the
~0.4 dex signal.

## What decides it

1. Rotation curves of LOW-mass disks (V_flat 50-120 km/s, the regime
   where a < a0) at z > 1.5; V_flat to ~10% needs R > 3000 spectral
   resolution and sub-kpc spatial resolution (lensed arcs or AO).
2. Baryonic masses to ~0.2 dex (NIRCam SED stellar masses + ALMA dust
   continuum or CO gas masses).
3. Sample size: with 0.3 dex intrinsic scatter, a 0.5 dex offset at
   3 sigma needs N ~ 4 per bin statistically, but the systematic floor
   (beam smearing, pressure support, inclination) pushes the practical
   requirement to N > 20 per redshift bin.
4. Baseline: z ~ 0 (SPARC) against z ~ 2 gives the factor-3 lever arm;
   adding z >= 3 separates cH(z) from the (1+z)^0.75 alternative.

## What this note does not claim

No derivation of a0 = cH/(2*pi) exists here (DECLINED.md D-3); the
2*pi is not explained; the coincidence's p-value is not computable
without an expression-ensemble choice this repo declines to smuggle in
(see QUEUE.md follow-through report). If the BTFR zero point stays
flat through z = 2 at the above precision, a0-tracks-hubble is wrong
and the claim file gets refutation evidence; that outcome would be a
complete, publishable resolution of the conjecture, and this note
commits to it in advance.

Sources: Milgrom 1983 (ApJ 270, 365); Nestor Shachar et al. 2023 (ApJ
944, 78); McGaugh et al. 2024 (ApJ 976, 13); Ubler et al. 2024 (A&A);
Xu 2022 (arXiv:2203.05606); v1 scripts a0_high_z.py / predict_highz.py
(repaired and re-run 2026-08-17, numbers above regenerated from them).
