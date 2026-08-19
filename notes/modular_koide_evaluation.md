# Modular / Koide stratum: direct-read evaluation

Method as in topology_evaluation.md: every verdict carried by an
inline computation (all numerics re-run 2026-08-19) or an explicit
gap. Docs read directly: w_plus_formalization.md,
L1_substrate_cusp_ground_state.md, koide_form_substrate_iteration_5.md,
hierarchy_gaussian_lattice.md, psl2z_subgroup_identification_phase_a.md,
gamma06_cosmological_modular_surface_audit.md,
cyclotomic_content_mass_ratios_audit.md,
padic_lfunction_mihailescu_pair_f64_audit.md.

## Verified correct (computation shown or re-run)

1. **Cusp classification of Γ₀(6).** The doc's definition "cusp 1/2 =
   {p/q reduced : gcd(q,6) = 2}" is right: for γ = [[a,b],[c,d]] ∈
   Γ₀(6), the image denominator satisfies q' ≡ dq (mod 6) with d
   invertible mod 6 (from ad ≡ 1 mod 6), so gcd(q,6) is a complete
   orbit invariant at level 6; four cusps {0, 1/2, 1/3, ∞} with widths
   6, 3, 2, 1 summing to the index 12. Re-verified: 200 random Γ₀(6)
   elements preserve gcd = 2 on the orbit of 1/2; width/index
   arithmetic checks.
2. **The V₄ decomposition in koide iteration 5.** Character table,
   Hadamard eigenbasis, and the Parseval sum are correct; the
   permutation table is the regular action of V₄. The reformulation
   "Koide Q = 2/3 ⟺ trivial-rep fraction |w_χ₀|²/|w|² = 3/8" is
   verified numerically (PDG masses: Q = 0.666661, fraction =
   0.375003) and is equivalent to Foot's classical observation
   (cos²θ = 1/2 between (√m) and (1,1,1); verified 0.500005) —
   R. Foot, hep-ph/9402242 (1994). Correct mathematics; known in the
   Koide literature in its 3-vector form.
3. **The psl2z cross-ratio j-invariants.** j(λ) = 256(λ²−λ+1)³ /
   (λ²(λ−1)²) at λ = 13/14, 12/13, 14/15 gives 47364.23, 40708.93,
   54531.66 — all three doc values reproduce to the printed
   precision. The machinery (PGL₂ cross-ratio invariance; j
   classifying 4-point configurations mod S₄ relabeling) is standard
   and correctly used. The program (select one orbit by a preserved
   subgroup) is Phase-A planning that never completed; w₊ itself was
   retracted to fitted.
4. **The p-adic audit's corrected facts.** The level-6 weight-4
   newform data (Atkin–Lehner (w₂, w₃) = (+1, +1), non-split
   multiplicative reduction) was corrected against LMFDB (6.4.a.a),
   with an in-place correction notice stating the original argument
   carried a sign error even where the corrected conclusion happened
   to survive. The retrieved facts are externally checkable; this doc
   is the stratum's best epistemic specimen (external substrate,
   honest correction).

## Refuted or unsupported

5. **hierarchy_gaussian_lattice n = 54.** Steps 3–4 argue "54 gauge
   cells, visited exactly once per iteration ⇒ n = 54 forced." No map
   is exhibited anywhere in the doc; the counting presumes a
   transitive 54-cycle that nothing constructs. The framework's
   operative iteration integer is 13, and ord₅₄(13) = ord₂₇(13) = 9
   (computed: 13⁹ ≡ 1, no smaller power; φ(54) = 18), so no
   13-generated orbit has size 54. The "complete pass" premise is
   unsupported and its natural candidate realization is false —
   entered in claims/ as refuted.

## Correct labels doing no work (the stratum's signature pattern)

6. **"MODAL ✓ / GENERATIVE ✓" verdicts** (gamma06, cyclotomic, and
   the padic audit's framing layer). These verdicts certify that a
   labeling is *possible*, not that a claim is true — and the labels,
   as labels, are mostly accurate: Z₁₄ ≅ Z₂×Z₇, Z₂₆ ≅ Z₂×Z₁₃, 6 = 2·3,
   the q=6 boundary and Γ₀(6) share the number 6. But "K* has 14th
   roots of unity content because its exponent is 14" and "√26 has
   Z₂₆ content" attach a group to an integer that appears in a
   formula — true of every integer, forceless for every claim. The
   distinction from §1 is exact: the cusp classification is a correct
   label that DOES work (it computes an orbit invariant); the
   cyclotomic tables are correct labels that do none. "Mihailescu
   primes" for {2, 3} is branding.
7. **L1_substrate_cusp_ground_state.** Composes "five Class 5
   results" of which C1 cites kam_bridge_synthesis.md for the
   constant λ_unlock — a document the v1 audit established was never
   committed (ghost citation). The modular vocabulary is the correct
   cusp classification of §1 used as decoration on an energy
   argument whose key constant has no source; the target value
   w₊ = 13/14 was fitted before the closure was written. Dead
   regardless of the ghost, per the campaign's Class-2 retraction;
   the ghost makes it unrevivable as written.

## Verdict table

| Doc | Core mathematical claim | Verdict | Backing |
|---|---|---|---|
| w_plus_formalization | cusp 1/2 of Γ₀(6) = {gcd(q,6)=2} | correct | invariance computation + 200-element check |
| w_plus_formalization | T1–T7 ⇒ w₊ = 13/14 given L1 | conditional on L1; moot (w₊ fitted) | campaign record |
| L1_substrate_cusp_ground_state | L1 closes via 5 components | unsupported — ghost citation for λ_unlock | v1 audit: kam_bridge_synthesis never committed |
| koide iteration 5 | V₄ decomposition; Koide ⟺ 3/8 | correct; classical (Foot 1994) | numeric verification |
| hierarchy_gaussian_lattice | n = 54 forced by complete pass | refuted | no map exhibited; ord₅₄(13) = 9 |
| psl2z phase A | orbit j-invariants of w₊ candidates | correct; program incomplete | j(λ) recomputation, 3/3 match |
| gamma06 audit | q=6 boundary ↔ Γ₀(6) | label only, no force | shared integer is the whole mapping |
| cyclotomic audit | mass ratios have cyclotomic content | labels correct, forceless | true of any integer in any formula |
| padic audit | f_{6,4} Atkin–Lehner/reduction data | correct after LMFDB correction | external database; honest correction notice |
