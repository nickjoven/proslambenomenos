<!-- evidence: scripts/experiments/p20_derive.py, scripts/experiments/p20_registration.json, scripts/experiments/p20_eps_budget.py, scripts/experiments/p20_results.json, scripts/experiments/p19_results.json, scripts/experiments/p19_force_scan.json -->
# P-20 — the eps budget died; the frame-separability map mostly held

Registered before computing (PREDICTIONS.md P-20, derivation layer
p20_derive.py with pinned p20_registration.json); resolution R-15.
No claim is filed from this line — the registration made filing
conditional on the eps clauses holding, and they did not.

## What was asked

The alf-period-lattice claim carries a scope sentence asserting that
eps — the lattice offset, measured 0.034–0.055 T0 — is "slip-episode
duration plus reflection-filter group delay". P-20 turned that
sentence into a zero-parameter budget and tested it:

    eps_pred = (one-pole filter delays on the trigger path)
             + (delay-line rounding)
             + (measured mean slipping samples per lock cycle)

The fixed part was derived and pinned first: one-pole DC phase delay
a/(1-a) samples (CAS-checked and reproduced by running the actual
recursion), 3.000 samples for the base loop (bridge + nut poles),
3.000 samples per extra nut-side round trip (nut pole + contact
pole — EQ3 shows the stuck-bow reflection is carried entirely by the
contact-filtered injection term), plus per-cell rounding of the
delay-line lengths. Given the committed P-19 eps values, the budget
therefore REQUIRED mean slip terms of 12.61/8.71/12.63/14.99/13.03
samples in the five cells — pinned in the registration before any
slip flag was counted.

## What was measured

One slip episode per cycle (1.01 in every cell), lasting

| cell | S (samples) | beta·loop | required S |
|---|---|---|---|
| beta 0.10, m=1 | 50.9 | 44.8 | 12.6 |
| beta 0.13, m=1 | 62.0 | 58.2 | 8.7 |
| beta 0.16, m=1 | 75.4 | 71.7 | 12.6 |
| beta 0.13, m=2 | 61.9 | 58.2 | 15.0 |
| Kawano 50/325 | 73.7 | 68.9 | 13.0 |

The slip episode is the Helmholtz-style flyback: its duration sits a
few samples above the bridge-side transit beta·loop and scales with
beta, not with eps. It is 3–5x LONGER than the whole offset it was
supposed to be a term of. Every cell missed the 0.015 T0 band by
0.085–0.140 T0; the registered mind-change (any cell off by more
than 0.030 T0) fired. The force-trend clause agreed with the
autopsy: within the plateaus, S falls as force rises at beta 0.10
and 0.13 while eps_meas rises.

So the scope sentence's additive reading is dead, and R-15 records
the correction: eps cannot contain the slip-episode duration as a
term. What survives, unclaimed: the fixed filter+rounding part
(5.8–9.6 samples) is smaller than every measured eps (15.1–24.6
samples), so filter delay under-explains eps and the remainder is a
property of the locked orbit that this line did not decompose. The
lattice claim's measured content (locks, slope, spacing) is
untouched; only its parenthetical mechanism story for eps is
corrected.

## The separability map

Derived: at frame rate fps, one lattice interval differs from one
doubling interval by D = (beta − eps/T0)·fps/f0 frames; D ≥ 1 needs
beta ≥ f0/fps + eps/T0 = 0.107 at 3000 fps and the grid-median eps.
Registered partition (margin 0.02 in beta): overlap at beta 0.10,
zero overlap at 0.13, 0.16, 50/325.

Held at 0.10 (frames {29, 30} vs {30, 31} — overlap, as registered),
0.16 and 50/325 (frames {28, 29} vs {30, 31} — zero overlap). At
0.13 it failed: the lattice period lands at 29.004 frames, and 2 of
103 intervals quantize to 30 — support overlap at derived D = 1.469
frames, under the 1.5-frame mind-change line, which did not fire.
The honest boundary is therefore not D ≥ 1 alone: near-integer
frame counts can leak single intervals across. On the tested grid
at 3000 fps, certified separation starts at beta = 50/325; beta
0.13 separates in 101 of 103 intervals but is not certified.

## The Kawano anchor: provenance

The beta = 50/325 cell's operating numbers — lock 1.8887 T0
(104.25 Hz), force plateau [0.90, 1.15] with F = 1.05, and the
29-vs-30/31 frame histograms — come from the interactive session of
2026-08-25 and were computed BEFORE P-20 was registered. They enter
this line as known anchors only: the registration says so, the
derivation layer uses the lock value as a known eps anchor, and
nothing about that cell's lock or histogram split is claimed as a
P-20 outcome. The registered content at that cell was the
decomposition (which failed there like everywhere else) and the
map-side prediction of zero overlap (which held, reproducing the
session split from the registered protocol).

## What this does NOT reopen

P-19 and the alf-period-lattice claim's measured content stand:
locks at 1.9413/1.9036/1.8811/2.7950 T0, slope −1.004, spacing
0.891. The flyback finding (slip duration ≈ bridge-side transit)
and the corrected separability boundary are recorded as diagnosis
in R-15 and are available to a future registered line; they are not
claims.
