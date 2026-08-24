<!-- evidence: scripts/experiments/symb.py, scripts/experiments/p13_symbolic.py, scripts/experiments/p13_profiles.py, scripts/experiments/p13_acoustic_chain.py, scripts/experiments/p13_results.json, scripts/experiments/p13_jz_diagnosis.py, scripts/experiments/p13_jz_diagnosis.json, scripts/verify/p13_acoustic_metric.py -->
# P-13: the acoustic metric, and what it does not see, on a chain

Registered before computing (PREDICTIONS.md P-13); every "=" below
carries an EQ id checked by the stdlib symbolic layer
(`scripts/experiments/p13_symbolic.py`, output committed) — symbolic
differentiation plus identity-testing by evaluation, no dependencies.

## Setup

A chain of masses m(x), springs J(x) is a substrate with two
independent local data:

- the acoustic metric c(x) = sqrt(J/m) — the local slope of the
  "light cone" (EQ3: c = dw/dk at k -> 0, from the dispersion
  relation w = 2 sqrt(J/m) sin(k/2), EQ1/EQ2);
- the impedance Z(x) = sqrt(mJ) — invisible to the metric.

Profiles pinned in `p13_profiles.py`: control (flat), ramp (c halves,
Z doubles), lens (Gaussian dip in c), zramp (c halves, Z = 1
identically, EQ8), jc (junction: Z jumps x4, c equal), jz (junction:
c drops x4, Z equal).

## Results (p13_results.json; dt-halving convergence included)

**Arrival times read the metric and only the metric.** Peak-arrival
times at 12 checkpoints match the discrete eikonal sum of 1/c
(closed form for the ramp, EQ4; sum = integral to O(1/N), EQ5):
RMS relative deviation 0.31% (ramp), 0.32% (lens), 0.30% (zramp) —
registered tolerance was 2%. The ramp's Z varies by a factor 2 and
the zramp's Z is constant while c makes the same excursion: the
arrival curve cannot tell them apart, which is the point. A
block-shuffled substrate (same multiset of local delays, different
arrangement) scores 85x (ramp) / 16x (lens) worse.

**Reflection reads the impedance and (mostly) not the metric.**
Junction jc — metric identical on both sides, Z jumps x4 — reflects
0.362 of the energy; the impedance law ((Z1-Z2)/(Z1+Z2))^2 = 0.360
(EQ6, exact lattice solve conserving energy to 3e-16, EQ7). The
smooth zramp — c halves, Z constant — reflects 2e-4. Scattering with
no metric change; metric change with no scattering.

**Where the dichotomy honestly breaks: the band edge.** Junction jz
(Z matched, c drops x4) was registered to reflect < 0.01 from the
monochromatic lattice value R(k = 0.05) = 0.0014; it measured 0.036.
The post-hoc diagnosis (`p13_jz_diagnosis.py`, labelled, no free
parameters) decomposes the actual pulse into frequencies and
reflects each with the exact lattice solve: predicted R = 0.039 vs
measured 0.036 (7%). Cause: the slow side's band edge w_c =
2 sqrt(J2/m2) = 0.5 — 2.9% of the pulse's flux lies above it and is
totally reflected no matter how well Z is matched. Impedance
matching silences reflection only inside the shared band, and the
band edge is set by the metric side of the substrate data. The
registered clause fails as registered; the corrected statement is
in the claim's scope line.

**The other registered miss, diagnosed.** The Airy front-width
exponent clause used the half-sine pulse, whose intrinsic width
(~28 time units) dominates its dispersive broadening; measured
exponent 0.027, band [0.23, 0.43] missed. A labelled step-drive
diagnostic on the same control chain gives 0.332 — the sharp-front
t^(1/3) is there; the registered observable was attached to the
wrong drive. Not rescued; recorded.

## Reading (commentary within an evidence note, no load)

This is the smallest executable instance of "a fundamental background
informs the geometry": consequential distances (arrival counts)
are set by how the oscillators couple, and the metric they define is
a *lossy summary* of the substrate — two chains with identical
geometry scatter differently (jc), and the summary's own band edge
leaks back into scattering (jz). Classical throughout: eikonal/WKB,
impedance matching, lattice band structure (Brillouin); the analogue-
gravity frame is Unruh, PRL 46, 1351 (1981) and Barcelo, Liberati,
Visser, Living Rev. Relativity 14, 3 (2011). Nothing here touches
Einstein equations, horizons, or real spacetime
(PREDICTIONS.md P-13 not-claimed-in-advance).
