<!-- evidence: scripts/experiments/p47_derive.py, scripts/experiments/p47_derive.json, scripts/experiments/p47_quench.py, scripts/experiments/p47_results.json, scripts/verify/p47_half_sector.py -->
# P-47 working document: the half-sector count through a quench

A-26 asked for Kibble-Zurek on the pi ring with the exact
half-sector count as the defect counter, and for the scaling with
quench rate registered against a derived window. The line delivers
the first half in full and declines the second on measurement.

## What is exact, and why the count needs no detector

The covariant winding W = sum wrap(D_j)/2 pi sits on its lattice at
every state because sum D_j = -sum A_j identically on a ring. No
threshold, no smear, no L-1 null to derive: a kink counter on a
substrate has to decide what a kink is, this counter has nothing
to decide. The twisted ring's lattice is the half-integers, so
W^2 >= 1/4 at every sample - the semifluxon floor in classical
dress.

At equilibrium the two rings read one density. Every bond weighs
exp(cos D/T), the pi bond included, so the summed wrapped strain
has one density rho_N(S) for both, and the closure picks S = 2 pi n
or 2 pi (n - 1/2). Everything about the twisted ring's counting
statistics is then the control's density read at shifted points:
the fast limit (both at N<u^2>/4 pi^2), the slow limit (0 against
1/4), and the whole curve between. The registered content is that
the FROZEN counts after a quench still share the density - the
freeze is local physics and the twist is a global label.

## What the derive layer changed

- The first anchor at T = 0.25 sampled every 10 units and read a
  degenerate twisted sample (all W = +-1/2, sample SE zero). The
  slip rate at T = 0.25 is ~ N e^{-8}, so consecutive samples were
  the same state. Anchors moved to T = 0.5 and 0.35 with gaps set
  from the slip rate; the error became model-based wherever a
  sample is degenerate. Below T ~ 0.3 equilibrium W cannot be
  sampled by dynamics on any affordable window - which is the
  freeze itself, seen from the other side.
- A dt/2 cell with 60 realizations read 1.03 against 0.45 and
  looked like a discretization effect at 3 sigma. The powered
  check (120 realizations each, dt and dt/4, same seed) read
  0.750 +- 0.086 against 0.833 +- 0.106. Statistics. Sixty samples
  of an integer-valued W^2 are not enough to see a factor of two;
  the registered cells use 200.
- The T = 0 settle changes W after fast quenches (48 of 60 at
  tau_Q = 0) and not after slow ones (0 of 60 at 80 and 320). The
  fast null is registered on the ramp-end count, the shared
  density on the final count.
- No exponent. The control's <W^2> at N = 32 fell 1.15 -> 0.37
  over tau_Q = 0 -> 320 with local exponents 0.23, 0.18, 0.47 and
  errors of 0.06 to 0.19. The freeze is activated (a bond must
  cross pi, barrier 2 J), not the spin-wave freeze of the textbook
  argument, and the ladder is four rungs. Reported, not
  registered. The Monaco-Mygind-Rivers annular junctions (LC-36)
  measured 0.27 +- 0.05 for a different quench; nothing here
  speaks to that number.

## The falsifier's route

Direct N-fold convolution of the bond density on a grid instead of
the characteristic-function integral; velocity-Verlet with the
noise kick at the half step; N = 16. Its first second mutant was a
loosened check (tolerance 0.1, floor 0) and could not fail on
correct data - an L-8 lesson taken literally: a mutant must assert
something false, so it became count-blind (read the unwrapped
strain sum, the topological constant -sum A/2 pi, zero variance at
every temperature), which the anchor kills.
