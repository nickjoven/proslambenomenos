<!-- evidence: scripts/experiments/p15_derive.py, scripts/experiments/p15_registration.json, scripts/experiments/p15_specdim.py, scripts/experiments/p15_results.json, scripts/verify/p15_spectral_dimension.py -->
# P-15: the spectral-dimension instrument

Registered before computing (PREDICTIONS.md P-15); resolution R-11,
all clauses as registered. Spectral dimension d_s(t) =
-2 dlnP/dlnt is the counting observable behind the quantum-gravity
dimensional-flow literature (Ambjorn-Jurkiewicz-Loll PRL 95, 171301
(2005); Carlip CQG 34, 193001 (2017)) and, by Weyl, the spectrum's
leading metric data. The repo now carries it as an instrument with
exact anchors and a derived validity window.

## The instrument

- d_s computed as the EXACT log-derivative of exact eigen-sums - no
  curve fitting anywhere in the exact tier.
- Anchors (p15_derive.py, all EQ green): the line curve checked by
  two independent routes (eigen-sum vs Bessel continued fraction,
  agreement 1.1e-14); the 1/t lattice correction measured at 0.1255
  (~ 1/8); product additivity exact; the window rule t < 0.5/lambda_1
  with the exact two-mode decay past it (0.5436 vs closed form
  0.5433 at 3 t_mix).
- A Monte Carlo walker tier for objects with no computable spectrum
  (400k continuous-time walkers): 0.02-0.25 sigma from exact at the
  registered checks.
- The demo fact: the dense circulant C_4096({1..6}) PEAKS at d_s =
  2.95 at short diffusion time before crossing to its true 1D
  plateau - a six-neighbour ring looks three-dimensional to a short
  walk. Which dimension you see depends on the scale of the walk you
  couple to the object.

## The chain result: blind, then exactly sensitive

On the P-14 pair (identical metric, split spectra):

- leading order: max |Delta d_s| = 6.9e-5 over t in [100, 1000] -
  the instrument is blind to the impedance split (d_s is metric-
  level, Weyl-level data);
- second order: Delta d_s(t) / (2 Vbar t) = 1.008-1.015 across
  [300, 1000] - the derived trace drift, with Vbar = 3.416e-8 taken
  from P-14's registration, no parameters fit. The kink-localised
  oscillations that fired R-10's k-resolved clause cancel in the
  trace; the trace-level form of "the commutator kernel is
  spectrally audible" passed as registered.

## Reading (commentary within an evidence note, no load)

The lossiness dictionary now has all three faces computed on one
object family: fronts read the metric (P-13), the commutator
seminorm is the metric (P-11/P-14), and d_s - the spectrum's Weyl
face - is blind to exactly what they are blind to, then hears the
remainder as e^{-Vbar t}. Scope: finite graphs and chains, this
Laplacian and walk; the causal-set definitional disagreement
(Eichhorn-Mizera 2014 vs d'Alembertian-based flows) is P-16's
question, not settled here.
