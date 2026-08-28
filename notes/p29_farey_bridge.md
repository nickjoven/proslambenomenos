<!-- evidence: scripts/experiments/p29_derive.py, scripts/experiments/p29_registration.json, scripts/experiments/p29_bridge.py, scripts/experiments/p29_results.json, scripts/verify/p29_farey_bridge.py -->
# P-29: the Farey bridge

## What was asked

A-13: Arnold tongues and Hofstadter bands are both organized by
the rationals — folklore since Hofstadter's own paper. The
composite claim under registration: they share the MEDIANT
skeleton as mechanism, because they share a premise
(first-harmonic two-frequency competition) — with a control,
derived in advance, that breaks the bridge on exactly one side.

## The design

- Number theory first, exact: in every Farey interval the mediant
  is the unique minimal-denominator interior fraction (exhaustive
  to q = 40, 10 registered intervals).
- Two instruments, each with its own anchors: tongue widths by
  tangency bisection (the exact rho = 0 width K/pi at 1e-10; the
  K^q resonance ratios 3.998/7.992 vs 4/8 measured at small K),
  Harper bandwidths by the two-corner pipeline (S(1/2) = 4 sqrt 2
  at 1e-12).
- The control is DERIVED, not chosen: pure-second-harmonic
  forcing is exactly conjugate (phi = 2 theta) to the standard
  map at (2 Omega, 2K) — verified at 1e-8 — which pins, before
  the run, that the competitor 3/8 must dethrone the mediant 2/5
  in [1/3, 1/2] on the tongue side, while the butterfly side
  (untouched by the forcing) must not move.

## The result (R-26)

| clause | outcome |
|---|---|
| mediant widest tongue, all 10 intervals, every competitor | holds |
| mediant largest bandwidth, all 10 intervals | holds |
| grading: Spearman(tongue, band) per interval | 0.891–1.000 (8 eligible) |
| control: 3/8 over 2/5 under 2nd harmonic (derived direction) | holds (7.93e-3 vs 4.66e-3) |
| control: butterfly unchanged | holds (1.8434 vs 1.2021) |

The composite mechanism claim stands on its named premise: remove
the first harmonic and the ordering follows the CONJUGATED
denominators, exactly as the conjugacy demands. This is the
repo's first premises-bearing claim (premises:
harper-golden-ladder, golden-ladder-gap-integers, both verified,
so no conditional cap).

## Honesty trail

- First run fired clause (e): tongue widths for 1/11, 1/12, 1/13
  read exactly 0.0 — the Omega bracket 0.6 K/q missed windows
  displaced by the rho = 0 tongue (K/2pi = 0.0796 wide; at
  Omega = 1/11 the eleventh-iterate deficit is 0.165). Replaced
  by the rigorous per-step bound |Omega - rho| <= K/(2 pi) +
  1e-3, unique crossing by monotonicity. No band touched. The
  EQ5 feasibility numerology ((K/2)^q) was wrong-but-harmless;
  the true small parameter is nearer K/(4 pi).
- The falsifier's staircase route needed three fixes of its own
  (transient discarded + step count a multiple of q so locks read
  p/q to machine precision; edge bisection to absolute bracket
  ends; seed by monotone bisection so 4.5e-5-wide windows are
  found). Two mutant designs were discarded before one stuck: a
  numerator shift lands on the symmetric twin (q-p)/q, which
  TIES by the p -> q-p symmetry of both instruments; a bare
  denominator shift lands on unreduced fractions and crashes
  rather than failing. The surviving mutant uses the second
  mediant (a+2c)/(b+2d): interior, ties-or-loses, honest kill.

## Relation to the Bandt question (LC-19)

The Bernoulli-convolution landscapes the reader raised are
organized by the kneading/substitution tree with Pisot/multinacci
landmarks — Farey, mediant, and Stern-Brocot occur zero times in
that paper. The projections stay inspiration, never evidence;
phi-as-first-multinacci and Bandt's golden-parameter phase
transition are imported as address-route data in the VOCABULARY
taxonomy; a second-bridge candidate (Farey tree vs kneading tree)
is queued as its own line with its own premise obligations.
