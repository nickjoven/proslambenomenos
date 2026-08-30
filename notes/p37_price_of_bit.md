<!-- evidence: scripts/experiments/p37_derive.py, scripts/experiments/p37_registration.json, scripts/experiments/p37_write.py, scripts/experiments/p37_results.json -->
# P-37 working document: the price of a bit (A-11)

The line P-24's note reserved: work-to-write against error rate
on rung 2, the locked double well whose forgetting P-24 derived
to the prefactor. Registration P-37; resolution R-36 (mixed).

## What the derive layer earned before registration

- Both registered clauses are THEOREMS about measured objects:
  W >= D[ln 2 - H(p)] (second law + coarse-graining) and
  W >= D[ln 2 - H(p)] + W_2^2/tau (thermodynamic optimal
  transport), with W_2 cut-scanned on the circle against the
  empirical commit sample. No guessed bands anywhere; the only
  judgment call (the Jarzynski null cell) carries its derived
  sampling condition (sig_W/D)^2 <= 0.5.
- The critical tilt h_c = 2 eps splits the protocol family into a
  thermal write (a = 1.2) and a deterministic write (a = 2.4).
- The layer's own first pass caught two instrument errors before
  registration: an undersampled Jarzynski null cell (the
  heavy-tailed estimator trap) and a reflecting-boundary bug in
  the tilted-MFPT quadrature (replaced by closed-form Kramers for
  the unregistered overlay).

## The surface (all 26 cells inside both bounds)

At a = 2.4, D = 0.22: work rises to 1.51 at tau = 16 (error
0.0088) then FALLS to 1.05 at tau = 55 while error RISES to
0.0150 - the wall: beyond the optimum, patience buys back work
but sells fidelity, at the rate set by the substrate's own
P-24-pinned hop rate. The registered 3 sigma ordering held at
D = 0.22 and fired at D = 0.28 (1.9 sigma, direction consistent);
the firing is attributed in R-36 to a power budget that leaned on
the deliberately unregistered Kramers overlay - the lesson, now
recorded: the R-32 corollary extends to POWER calculations, not
just clause bands. Also attributed: a readout-label inversion
(right-well population under the wrong-well name) found at first
run; H-symmetric clauses unaffected, wall pairs re-read from the
same seeded trajectories under the registered definition.

## Imports

LC-27: Proesmans-Ehrich-Bechhoefer 2020 (finite-time Landauer),
Van Vu-Saito PRX 2023 (transport unification) and PRX 2025
(time-cost-error), Sekimoto work convention, Jarzynski identity
(used as the 8b null, not a claim), and the 2026 quantum-cost
preprint as the reason quantum prices stay out of scope.
