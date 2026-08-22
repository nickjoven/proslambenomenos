# P-8: the Gabor limit for mode-locking measurements

Registered (PR #40, first commit) before computing; run 2026-08-23 in
worktree wt-p8-gabor-locking. Script scripts/experiments/
p8_gabor_locking.py; results p8_results.json (pinned by catalog c27).

## Method
Sine circle map; the repo's own model-free width measurement
(compendium C8/C9, notes/p1): grid scan of |rho_T - p/q| < 2e-5 over
T iterations after a T/4 transient, then bisection of both edges.
T in {600, 1200, 2400, 4800, 9600}, all multiples of 6 so that a
locked 1/2 or 1/3 orbit gives rho_T = p/q exactly (otherwise the
interior test itself fails at O(1/T) > tol). Fit w(T) - w(9600) =
c T^-a on the three smallest T.

## Results
| plateau | K | w(600) | w(9600) | from above | a | centre shift |
|---|---|---|---|---|---|---|
| 1/2 | 0.5 | 0.019520 | 0.019499 | yes | 1.82 | 0 |
| 1/3 | 0.5 | 0.004219 | 0.004237 | NO at T=600, yes from 1200 | 2.00 | +0.0055 |
| 1/2 | 1.0 | 0.073974 | 0.073966 | yes | 2.07 | 0 |
| 1/3 | 1.0 | 0.030567 | 0.030560 | yes | 2.06 | +0.0186 |

## Against P-8
Exponent a ~ 2 in all four - the passage-time mechanism (pi/sqrt(mu)
> T misjudges a drifting orbit as locked), not 1/T resolution. The
mind-change (a ~ 1, or from-below robustly) did not fire.
Convergence from above holds in 3 of 4; the exception is the
narrowest plateau at the shortest T, which comes in BELOW the limit:
near an edge the approach to the locked orbit is also slow (critical
slowing down, the same pi/sqrt(mu) scale), so a T/4 transient can
leave a genuinely locked orbit outside tolerance - an underestimate
with the same T^-2 scaling and the opposite sign. The two edge
mechanisms compete; which wins depends on the initial phase. At
T = 9600 both are below 1e-4 for every plateau measured.
Secondary expectation held: the q = 3 tongue centre sits above 1/3
by 0.0055 (K = 0.5) and 0.0186 (K = 1.0), ratio 3.4 against the 4
of a pure K^2 law - O(K^2) to the accuracy of two points. A
bisection started at p/q therefore overstates q >= 3 widths by a
T-independent factor; the compendium's brackets avoid this, the T1
notebook records it.

## Consequence for the repo's own numbers
Every plateau width reported in notes/p1 and the compendium was
measured at T = 6000 (plateauWidth) or 900 (rho grids): the 1/2
widths are good to ~1e-5 and ~2e-5 respectively; the E1 shrinkage
ratios (x3.5, x8.7) are unaffected at the precision quoted. Not
claimed: anything about model-based estimators.
