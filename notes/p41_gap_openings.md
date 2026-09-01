<!-- evidence: scripts/experiments/p40_derive.py, scripts/experiments/p40_registration.json, scripts/experiments/p40_gaps.py, scripts/experiments/p40_results.json, scripts/experiments/p41_gaps.py, scripts/experiments/p41_results.json -->
# P-40/P-41 working document: gap openings at the approximants (A-23)

Third item of the earned frontier. Dry Ten Martini (Band-Beckus-
Loewy 2024, imported LC-30) says every labeled gap of a Sturmian
Hamiltonian is open at every nonzero coupling; A-20's graph edge
could only run the trace-map engine. This line computes the
approximant shadow: at q = F_m in {34, 55, 89, 144}, both
couplings, every labeled gap is open, with exact labels.

## The detector story (P-40 -> P-41)

P-40 registered a scan detector (60q points + bisection) validated
at q <= 21. At q = 89 and 144 it FIRED: narrow bands fall between
scan samples, deleting both their edges (176/286/270 found where
178/288/288 exist). R-39 records the diagnosis - the R-36 lesson
in a spectral costume: resolution budgets must be derived at the
registered cells, not the validation cells. P-41 re-registered
with the eigen-route (edges ARE eigenvalues of the periodic and
antiperiodic operators - a route that cannot miss a band), keeping
the discriminant as a per-edge cross-check (Delta = +-2 at every
eigenvalue, 3.3e-11 worst). All eight cells then passed, including
the three the scan could not measure.

## Numbers

Min gap widths 4.5e-3 (q=34), 1.7e-3 (55), 6.2e-4 (89), 2.3e-4
(144) - roughly halving per Fibonacci step (unregistered trend),
all far above the validated 1e-6 floor. Labels s F_(m-1) = k
(mod F_m) bijective with |s| <= q/2 at every q, exact integers.
Trace-map recursion and the rotation-substitution tie at machine
precision (the layer's first pass had the letter map complemented
- the tie check caught it at O(1)).

## Instrument lineage

The falsifier re-derives everything with its own cyclic-Jacobi
eigensolver (the pinned kernel uses Householder + QL - different
algorithm family), own extended-gcd labels, and keeps the P-40
firing alive as the scan-blind mutant: asserting the scan finds
all edges at q = 89 fails exactly as the registered run did.
