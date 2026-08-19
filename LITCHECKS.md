# Literature-check ledger (append-only)

Each entry: what was checked, when, how (search angles), and the verdict
with citations. A claim may carry `novelty: checked-novel` only by
referencing an entry here; `classical`/`folklore` carry their citation
inline. An entry is a record of a search, not a proof of absence.

## LC-1 — Klein-bottle orientation-bundle Laplacian spectrum (2026-08-19)

Claim checked: complete eigenmode classification under
f(x+L₁, y) = −f(x, L₂−y): (half-integer x ⊗ cos y) ⊕ (integer x ⊗ sin y),
constant excluded. **Verdict: KNOWN in substance / folklore.** The general
twisted-spectra machinery covers it as a minimal special case
(Miatello–Rossetti, Ann. Global Anal. Geom. 21 (2002) 341–376); the
anti-invariant torus-mode decomposition appears in Gordon–Rossetti
(arXiv:math/0111016); physics instances from Banach–Dowker, J. Phys. A 12
(1979); recent compactification papers state the integer⊗half-integer /
no-zero-mode quantization (arXiv:2510.05270 App. A). No single source
found displaying the packaged eigenbasis as a named theorem (~65%
confidence on that absence). Angles searched: flat-manifold twisted
spectra, Hodge isospectrality, Courant-sharp eigenfunction papers,
twisted-field QFT/Casimir, Klein-bottle compactification/pin structures,
string Klein-bottle amplitudes. Method: web search, 19 tool calls,
independent agent.

## LC-2 — Farey antipodal orbit counts, denominators coprime to 6 (2026-08-19)

Claim checked: orbit plateaus 1, 3, 6, 11, 17, 25 (endpoints included)
under p/q → (q−p)/q; increments φ(q)/2. **Verdict: ROUTINE.** Decomposes
into the classical Farey symmetry x → 1−x (Hardy & Wright ch. III),
evenness of φ, and ½Σφ(q) over restricted denominators; the
restricted-denominator Farey literature contains strictly stronger
counting results (Boca–Cobeli–Zaharescu arXiv:math/0201046; Haynes JNT
2003; arXiv:0907.0163, arXiv:0907.2171). OEIS: exact sequence absent
(reflecting triviality); near-coincidences A003022, A001859 both diverge
later. The "(q−1)/2" increment reading holds only at primes (φ(q)/2 in
general; first divergence q = 25). "Skips 15" carries no significance —
partial sums with increments ≥ 2 skip most integers. Method: web + OEIS
search + independent brute-force recomputation, separate agent.
