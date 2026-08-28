<!-- evidence: scripts/experiments/p27_derive.py, scripts/experiments/p27_registration.json, scripts/experiments/janse_table1.json, scripts/experiments/p27_score.py, scripts/experiments/p27_results.json, scripts/verify/p27_squeeze_windows.py -->
# P-27: the classical-gravity squeeze windows

## What was asked

A-15: Oppenheim's postquantum classical gravity is the rival
worldview with a computable exposure. If gravity is fundamentally
classical, coherence of massive superpositions must be paid for
with stochastic spacetime diffusion D2: interferometry bounds D2
from BELOW (coherence observed, so diffusion must exist), force-
noise experiments bound it from ABOVE (the diffusion would shake
test masses). What parameter space survives, computed rather than
narrated?

## The imports (LC-17) and what the audit found

- OSSW's three kernel-class squeezes pin the game. Mechanized:
  all three are dimensionally consistent (unit algebra AND the
  falsifier's independent random-rescaling route), with the
  decoherence rate in every lower bound's denominator - long
  coherence demands MORE diffusion.
- The three printed lower bounds reproduce exactly from their
  stated inputs. The three printed upper bounds do not: signed
  deltas +2.26 / -1.35 / +1.65 orders, and the averaging time in
  their eq. (42) is never given a value in the paper (Janse et al.
  attest 100 s). Order-of-magnitude prose, now mechanized.
- Janse Table I (46 rows, machine-parsed): internally consistent
  on S_a = S_F/m and FOM = N S_a^2 at every row; the Monteiro '20
  row's printed N is 8x its composition value; their eq. (5)
  lower bound 1e-35 is underivable from any stated input set
  (OSSW printed 1e-40; a Fein-2019 update gives 1.3e-38).

## The window table (R-24)

| class | rule | window (printed / recomputed) | verdict |
|---|---|---|---|
| ultra-local continuous | every rule | -17.0 to -41.6 | EXCLUDED, robust |
| ultra-local discrete | direct-on-Earth (Gisler) | +9.5 / +10.8 | survives, robust |
| ultra-local discrete | + Asenbaum (contested) | -0.6 / +0.7 | UNDECIDABLE at source precision |
| nonlocal continuous | direct-on-Earth | +11.5 to +16.5 | survives, robust |
| nonlocal continuous | + Asenbaum, Janse convention | +1.4 / -0.3 | UNDECIDABLE at source precision |

The registered sign-stability clause FIRED: all three contested
atom-interferometry verdicts flip sign between the sources'
printed bounds and the same bounds recomputed from their own
inputs. The dramatic reading of Janse's Figure 1 - that
Asenbaum-class data already closes the discrete window - is not
supported at the sources' own arithmetic precision, independently
of the deeper imported question (differential/relative
measurements may not bound D2 at all, their own caveat).

## What would decide it

- Discrete class: an UNCONTESTED absolute on-Earth measurement at
  FOM_D2 = N S_a = 1e-10 m^2 s^-3. Best current: Gisler's
  nanowire at 3e-1. Nine orders - not incremental.
- Or: a settled theoretical ruling on whether relative
  measurements (atom interferometry, LISA Pathfinder) bound D2 -
  at which point existing data either closes the discrete window
  or fails to, with nothing in between until the bound arithmetic
  itself is done beyond order of magnitude.
- Nonlocal continuous: 5-12 further orders beyond that, depending
  on whose lower-bound convention survives scrutiny.

## Scope honesty

We computed windows; we did not adjudicate worldviews. The
Newtonian-limit squeezes are taken as printed; the superposition-
volume conventions (V_lambda, R_lambda) are the recorded source of
the lower-bound discrepancy; Tilloy-Diosi and other hybrid models
are untouched; and the possibility that one experiment cannot
serve as both bounds (raised by Janse et al. themselves) is
imported, unresolved, and material to every contested cell.
