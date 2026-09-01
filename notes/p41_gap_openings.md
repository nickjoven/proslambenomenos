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

## Audit note (2026-09-01): the q = 13 comparison

Owner-prompted comparison of R-39's firing against the ledger's
prior q = 13 record. The finding sharpens the attribution: the
P-40 scan budget did not merely lack a derivation - it
contradicted a pinned number. R-25 (P-28, four days earlier, same
Fibonacci ladder) pinned the per-rung width shrinkage at 0.324 =
phi^-2.34; P-40's own validation gaps (0.088 / 0.032 / 0.012 at
q = 8/13/21) display the same law. The narrowest BAND shrinks by
0.368-0.376 per rung (~ phi^-2) while the 60q scan's spacing
shrinks only as phi^-1 per rung - a geometric race with one
outcome. Recomputed with the P-41 instruments (min band width vs
scan spacing 5.5/60q, lambda = 1):

    q     min band    ratio    scan spacing
    8     9.82e-2     -        1.15e-2
    13    3.69e-2     0.376    7.05e-3
    21    1.36e-2     0.369    4.37e-3
    34    5.12e-3     0.376    2.70e-3
    55    1.88e-3     0.368    1.67e-3   (survives by 13%)
    89    7.06e-4     0.375    1.03e-3   SPACING EXCEEDS BAND
    144   2.60e-4     0.368    6.37e-4   SPACING EXCEEDS BAND

The crossover lands between q = 55 and q = 89 - exactly where the
firing happened - and P-40's clean cells were one rung from
failure. Three validation points and a division would have
derived the required density before registration.

The wider q = 13 pattern in the ledger: P-28 handled the same
problem correctly (its edge-gap clause promised resolution only
through q = 13 BECAUSE the derivation supported no more; reality
then outperformed the promise); the 8/13 skip-rung Streda mutant
was discarded as non-discriminating for a global-structure
reason; P-31's convergents 8/13 and 13/21 diverged in the
kneading tree as a computed refusal. Common thread: q ~ 13 is the
last rung where the golden ladder is cheap, and every instrument
judgment formed at q <= 21 is one to five rungs from wrong at a
rate the ledger can state in closed form. The standing rule now
lives in AGENTS.md item 8a: where a pinned or derivable scaling
law exists, validation quantities MUST be extrapolated to the
registered cells before the detector budget is set.
