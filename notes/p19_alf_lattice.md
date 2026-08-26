<!-- evidence: scripts/experiments/p19_alf_waveguide.py, scripts/experiments/p19_results.json, scripts/verify/p19_alf_lattice.py -->
# P-19 — ALF locked periods lie on a two-generator timing lattice

## Statement

On a bowed string driven above the Schelleng maximum force, the
locked "anomalous low frequency" periods are not integer subharmonic
periods n·T0. They lie on the lattice

    P(m, beta) = T0 * (1 + m*(1 - beta)) + eps,   m = 1, 2, ...

one full-loop transit plus m round trips of the nut-side segment
behind the sticking bow, with eps a small positive systematic
(slip-episode duration + reflection-filter group delay, ~0.03-0.07 T0
in the model, weakly force-dependent). Two discriminators separate
the lattice from the exact-subharmonic reading:

1. **The beta slope.** dP/dbeta = -1 (in T0 units, m = 1); eps
   cancels in the slope. Measured: -1.004 (experiment, three bow
   positions), -0.926 (independent miniature, different rate and
   observable). Exact subharmonics predict slope 0.
2. **The m-spacing.** P(m+1) - P(m) = (1 - beta)*T0 at fixed beta.
   Measured 0.891 vs 0.87 at beta = 0.13. Integer subharmonics
   predict spacing 1.

Corollary: the "octave-down" ALF at beta = 0.10 sits at 1.94 T0, about
50 cents sharp of the true octave, and its pitch moves with bow
position.

## Numbers (experiment, fs = 88200, v_bow = 0.05 m/s)

| beta | F (N) | m | lock (T0) | lattice | n |
|---|---|---|---|---|---|
| 0.10 | 1.50 | 1 | 1.9413 ± 0.0011 | 1.900 | 100/100 |
| 0.13 | 1.10 | 1 | 1.9036 ± 0.0010 | 1.870 | 103/103 |
| 0.16 | 0.95 | 1 | 1.8811 ± 0.0011 | 1.840 | 104/104 |
| 0.13 | 1.70 | 2 | 2.7950 ± 0.0003 | 2.740 | 69/69 |

Independent miniature (fs = 44100, autocorrelation observable,
physical filter time constants held fixed): 1.9377 / 1.9109 / 1.8799,
slope -0.926, residuals 0.036-0.041 — agreement with the experiment
within 0.007 T0.

## Model and provenance

Travelling-wave (MSW) string with exact per-sample stick-slip against
a near-Coulomb falling curve (v0 = 0.01 m/s), on the steel G string of
arXiv:2502.11902 (196.9 Hz, 325 mm, 0.8 mm, 7700 kg/m^3). Four
ingredients were each necessary for the locks to exist (ablation
record in the source repo): DC-lossless end reflections (-g·onepole;
the clamped-end drag ramp is the pump), a damped torsional pair
(clamped at DC), one-pole contact-width smoothing of the force
injection (a point contact re-sharpens the slip spike and keeps a
hard period-1 orbit alive far above the ceiling), and the near-Coulomb
curve (lock quality at slow bow speeds tracks v0/v_bow; the Coulomb
limit is scale-invariant under (v, F) -> (l·v, l·F), which is also why
the lock windows sit at fixed F/v).

Origin: harmonics working session 2026-08-24/25 (commits e045ab8,
e7e1383, ff25d3f, 105cd3c in ~/harmonics — archive repo, adversarial
test bed). This note and both scripts are fresh implementations; the
verify script reads nothing from the experiment.

## Prior art (per LC-4, plus what a new litcheck must pin)

KNOWN: ALF conditions — bow force above Schelleng's f_max with slow
bow (Guettler, CASJ 2(6), 8 (1994); Guettler PhD KTH 2002; Guettler &
Schoonderwaldt ISMA 2007; Kimura, J. New Music Res. 28, 178 (1999);
Hanson, Halgedahl & Schneider, CASJ 2(6), 1 (1994)). Guettler's wave
analysis describes ALF qualitatively as the string wave "taking one
or more extra rounds before causing a slip", and reports ALF pitch
families (third, octave, octave-plus-fifth) with transverse and
torsional trigger families. Schelleng, JASA 53, 26 (1973). Corner
rounding: Cremer, Acustica 30, 119 (1974). MSW simulation: McIntyre,
Schumacher & Woodhouse, JASA 74, 1325 (1983). The driving paper:
arXiv:2502.11902 (FEM + high-speed imaging; reads the subharmonic as
exact halving, at 0.33 ms timing resolution, which cannot separate
1.94 from 2.00 at 196.9 Hz).

NOT FOUND by LC-4: any topology/holonomy framing of ALF onset; any
published "N sites to hold a corner" statement. **A new litcheck must
check specifically** whether Guettler 1994/2002 states the quantitative
period formula T0 + m(1-beta)T0 and/or the dP/dbeta = -1 discriminator;
"one or more extra rounds" makes the formula plausibly implicit there.
Until that check runs, novelty is UNCHECKED and the honest expectation
is "classical with citation" for the lattice itself, with the slope
discriminator and the lab protocol as the contribution.

## Lab falsifier (the real-string test)

A cello or violin G string, scale length L: bow at two marked
positions (beta ~ 0.10 and ~ 0.16, +/-2 mm), slow heavy stroke into
the ALF regime, audio-record; extract the ALF period by
autocorrelation over >= 20 cycles. Lattice: period ratio
P(0.10)/P(0.16) = 1.90/1.84 = 1.033 (about 55 cents of pitch), same
direction on every string and instrument. Exact halving: ratio 1.000.
The 3% period difference needs timing resolution ~1 ms over a 10 ms
period — trivial for audio, invisible at the paper's 3000 fps.
Confounds to control: torsional-trigger ALF (Guettler's second
family) produces a different ladder — classify runs by slip waveform
before pooling; keep v_bow and F inside the m=1 window found by ear.

## What does NOT come along

The gated-cylinder/winding-number geometric framing, the
medium-vs-direct discriminator program, and every cosmological
analogy (GW echo combs, BAO) from the source sessions stay out. They
re-enter, if ever, as their own claims with their own evidence.
LC-8's finding stands: no published cosmological staircase; the
staircase's homes are the circle map, Shapiro steps, CDWs,
Frenkel-Kontorova — and, per this claim, the over-pressed bowed
string.
