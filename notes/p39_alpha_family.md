<!-- evidence: scripts/experiments/p39_derive.py, scripts/experiments/p39_registration.json, scripts/experiments/p39_family.py, scripts/experiments/p39_results.json -->
# P-39 working document: the alpha-family (A-22)

Second item of the earned frontier. Liu-Chiribella's ICO Tsirelson
bound for the biased OCB correlation, reproduced two-sided with our
own instruments; the upper-bound proof imported (LC-29), both
curves and the achieving family earned.

## What was earned

- Causal curve: C(alpha) = max(1 + alpha/2, 1/2 + alpha), by
  exhausting all 8192 deterministic one-way-signalling strategies
  in Fraction arithmetic (the same count as P-30). The causal
  (P_A, P_B) polytope has 9 vertices; the two useful extremes
  (1, 1/2) and (1/2, 1) sit ON the Tsirelson circle - the square
  is inscribed, so the circle's whole margin is quantum.
- Quantum curve: the theta-rotated family W(theta) = (1/4)[1 +
  cos(theta) ZZ + sin(theta) ZXZ] - P-30's OCB process is
  theta = pi/4 - is a valid process for EVERY theta (unit
  coefficient vector => spectrum {0 x8, 1/2 x8}; the no-loop
  trace-and-replace identity holds), and with the OCB local
  strategies its success probabilities are (1 + sin theta)/2 and
  (1 + cos theta)/2. Maximizing at tan theta* = 1/alpha lands on
  B(alpha) = (1 + alpha + sqrt(1 + alpha^2))/2 to 2.1e-12 at
  worst across the grid.
- Geometry: advantage zero at alpha = 0 (tangency), positive
  everywhere on the grid, maximal at the unbiased game with value
  (sqrt2 - 1)/2.

## Instrument errors on record

The layer's first pass mis-assigned the OCB game roles (the
guesses are the MEASUREMENT OUTCOMES x, y; the inputs are a, b,
b') and returned value 1.0 at alpha = 1 - caught at once against
P-30's pinned (2+sqrt2)/4. The falsifier's first pass
double-applied the projector normalization (the Pauli-basis
factors already carry it) - caught against the same anchor. Both
fixes are one-liners; both anchors did their job.

## Falsifier route

Pauli orthogonality: every operator a dictionary of Pauli strings,
Tr[P_i P_j] = 16 delta_ij, no matrices anywhere; plus a fresh
enumeration encoding. Mutants: symmetric-blind (the alpha-blind
error - asserting P-30's symmetric process optimal at alpha = 2;
the rotated family beats it) and square-blind (asserting a causal
strategy attains the bound at alpha = 1; the exhaustion caps at
3/2).
