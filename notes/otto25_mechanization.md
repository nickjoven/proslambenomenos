<!-- evidence: scripts/experiments/otto25_mech.py, scripts/experiments/otto25_mech.json -->
# Mechanizing Otto 2025: every "=" executed, four bins

Symbols: see the VOCABULARY.md symbol graph - the verified-refusals block (phi vs alpha, g_e, Omegas, Madelung) is indexed in the symbol graph.

Target: H. H. Otto, "What Tells Geometrical Reciprocity about the
Universe and its Mass Constituents?" (2025, ResearchGate; the
companion of the 2018 JMP flat-lattice-multiverse paper audited
earlier via the Madelung/pigeonhole computation). The paper carries
roughly 170 numbered relations. Every one that asserts a numeric
equality was implemented and executed (107 checks); each lands in
one of four bins. This note is the audit record; no claim is filed
because nothing here was registered in advance - it is a
mechanization of someone else's ledger.

## The verdict in one paragraph

The paper is two books interleaved. Book one is TRUE and classical:
32 relations verify to 1e-9 or better, and every one of them is
standard algebra of the golden mean and its relatives - continued
fractions of metallic means, Vieta on Klein's icosahedral quartic,
geometric series, Lucas identities, and two genuinely pretty exact
facts (below). Book two attaches those true identities to physical
constants by proximity, and every attachment that touches a
measured constant with a real uncertainty is EXCLUDED by that
measurement at between 788 and 196,000 experimental standard
deviations. The bridge between the books is never a mechanism -
always adjacency.

## Bin 1 - EXACT (32): the paper's real mathematical content

- Metallic-mean algebra: phi^3 = sqrt(5) - 2 = [0;4,4,...],
  phi^5 = (sqrt(125) - 11)/2 = [0;11,11,...], phi^-5 = 11 + phi^5,
  5*phi = 3 + phi^5, sum phi^n = Phi, (sum m^-n)^-1 = m - 1,
  (m + 1/m)^2 = 4 + (m - 1/m)^2, 3 + phi = sqrt(13 + phi^5).
- Klein's icosahedral quartic x^4 - 228x^3 + 494x^2 + 228x + 1:
  the appendix radicals are roots (residuals < 1e-12), the root
  sum is 228 (Vieta), x2 = -1/x1, 494 = (13/6)*228.
- The golden quartic q(x) = x^4 - 2x^3 + (1 + phi^5)x^2 has
  q(phi) = q(1) = phi^5 AND q'(phi) = 0 exactly (the bracket
  2phi^2 - 3phi + 1 equals -phi^5, so it cancels; residual 2e-16).
- HARDY'S MAXIMUM: the maximum of P = p^2(1-p)/(1+p) sits at
  p = phi with value phi^5 = (5 sqrt 5 - 11)/2 exactly. This is
  Hardy 1993 / Mermin 1994 - real, peer-reviewed quantum
  foundations, and the ONE place in the paper where phi^5 attaches
  to physics through a theorem instead of proximity.
- THE KEPLER-PYRAMID THEOREM-LET: for a square pyramid whose
  face-to-base angle has cos = phi, the in-sphere radius is
  phi^(3/2) (half-base 1), the height is sqrt(Phi), and
  V_insphere / V_pyramid = pi * phi^(9/2) * phi^(1/2) = pi * phi^5
  EXACTLY (verified to 1e-15). A genuine exact geometric fact.
- The Lucas cluster: the "spiritual number 123" relations
  (sqrt(123 - 1/123) = 11 + phi^5 at 2e-9, its 5th/10th roots) are
  corrupted forms of the exact Lucas identity Phi^10 + phi^10 =
  L_10 = 123 - the paper substitutes 1/123 for phi^10 (5e-5 on the
  small term) and reads the 2e-9 residual as depth.

## Bin 2 - EXCLUDED by measurement (15): every physics attachment

alpha^-1 = 137.035999177(21): the six golden/pi formulas for it
miss by 1.4e4 to 2.0e5 sigma (best: sqrt(137^2 + pi^2) at 788
sigma). g_e = 2.00231930436182(52): the three "solely golden mean /
solely pi" formulas miss by 1.2e3 to 1.5e5 sigma. The El Naschie
mass constituents (Omega_M = phi^5/2, Omega_DE = 2phi - 1/2,
the 0.7331 variant) miss Planck 2018 by 6.6 to 8.4 sigma. A
relation wrong by 788 sigma is not "an approximation" - at these
experimental precisions the golden-mean representation of alpha
and g_e is refuted by the same standard that credits QED, which
matches g_e through 12 significant figures with a mechanism.

## Bin 3 - UNEXCLUDED (4): where the kill is structural, not numeric

- The three Omega RATIOS (Om_M/Om_DM ~ 2 phi^5 etc.) sit at ~1
  sigma of Planck - but the paper itself provides FIVE different
  golden values for Omega_DE spanning 7.3 experimental sigma
  (0.683 to 0.736): a framework that outputs five values for one
  observable predicts none of them.
- The Higgs relation m_H = (alpha_1/phi^2)(m_p + m_e) = 125.23 GeV
  sits 0.27 sigma from PDG 125.20 +/- 0.11. Two structural kills:
  (i) alpha_1 enters through its DEGREE value - in radians the
  same formula gives 2.186 GeV; a relation that depends on the
  historical convention of 360 parts per turn is numerology about
  our protractors, not about the Higgs field; (ii) the paper's own
  Table 5 lists FOURTEEN interchangeable "conditions" for alpha_1
  spanning 0.29% - a documented tuning ladder wider than the
  claimed agreement. The author asks "whether all that is pure
  coincidence"; Table 5 is the author answering himself.

## Bin 4 - the monument

The Great Pyramid's surveyed slope (146.59/115.165 = 1.27287) sits
between the Kepler-pyramid value sqrt(Phi) = 1.27202 and the
pi-theory value 4/pi = 1.27324, which differ from each other by
only 0.10% - inside the build tolerance. The monument cannot
decide between phi and pi, so it supports neither; the exact
theorem-let above is about the ideal shape, not the building.

## The control block

The same script closes with two classical identities run on the
same substrate - J(100) = sum pi(100^(1/n))/n counted both ways
(equal to machine precision) and ln zeta(2) = sum_p sum_m
1/(m p^(2m)) (7.6e-7, fully accounted by the derived prime-cutoff
tail). That is the difference on display: an identity that RUNS
either lands at machine precision or its residual has a derivation.
A "reciprocity relation" that lands at 1e-4 with no error model is
a sighting, not a statement.

## Non-killed paths out of this corpus

1. Hardy's phi^5 (the one theorem-grade attachment): promotable by
   direct optimization over two-qubit states and local
   measurements with the P-17 Bell machinery - queued as A-9.
2. The Kepler-pyramid theorem-let: catalog-fact material (exact,
   self-testing, mutant asserts the monument decides phi).
3. The metallic-means/Lucas algebra: true, classical, already in
   every number-theory text; no repo action.
4. Everything else: excluded, inconsistent, or unfalsifiable as
   scoped (the vacuum-condensate, consciousness, and superluminal
   chapters make no numeric claim at all).
