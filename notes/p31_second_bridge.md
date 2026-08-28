<!-- evidence: scripts/experiments/p31_derive.py, scripts/experiments/p31_registration.json, scripts/experiments/p31_bridge2.py, scripts/experiments/p31_results.json, scripts/verify/p31_second_bridge.py -->
# P-31: the second bridge — the kneading tree refuses the mediant

## What was asked

A-18, born from the reader's Bandt question: P-29 proved the
mediant skeleton transfers between tongues and bands *because of a
shared premise*. Does the Bernoulli-convolution landscape — whose
projections visually resemble butterfly organization — run on the
same tree? The registered composite: no, and the distinction is
computable with certificates on both sides.

## The instrument

Exact Q(beta) arithmetic: field elements as Fraction-coefficient
polynomials mod the defining polynomial, sign decisions by
refining the root bracket (terminating for unequal elements),
boundary membership decided algebraically. The multivalued orbit
of the overlap boundary {1−t, t} under g0 = βx, g1 = βx+1−β
closes ⟺ the BFS set closes exactly. For rational t = p/q the
complementary certificate: a finite orbit has bounded
denominators, so growth past 1e6 *proves* divergence — no
timeouts as evidence, in either direction.

## The result (R-28, all clauses first run, 0.1 s)

| parameter | kind | verdict | size / certificate |
|---|---|---|---|
| t₂ (golden) | multinacci 2 | closes | 4 = {0, 2−φ, φ−1, 1} |
| t₃, t₄, t₅ | multinacci 3–5 | closes | 8, 10, 12 |
| s₂ (supergolden) | doubling 2 | closes | 6 |
| s₃ | doubling 3 | closes | 8 |
| 3/5, 5/9 | simple rationals | diverges | den 1.6e6, 2.0e6 |
| **4/7 (the mediant)** | Farey's prediction | **diverges** | den 1.0e6 |
| 8/13, 13/21 | t₂'s own convergents | diverges | den 2.1e6, 4.8e6 |

The sharpest cell: finite structure at s₂ = 0.569840, certified
nothing at 4/7 = 0.571429 — 1.588e-3 apart. Even the golden
landmark's best Fibonacci rationals diverge while the landmark
itself closes.

## The two bridges together

- P-29: mediant skeleton transfers (tongues ↔ bands) — because
  both systems carry first-harmonic two-frequency competition,
  and the derived control (kill the harmonic, dethrone the
  mediant) proved the premise carries the skeleton.
- P-31: the kneading skeleton does NOT transfer — structure at
  algebraic landmarks, certified nothing at rationals, because
  the premise here is expansion redundancy at algebraic
  parameters, not frequency competition.

Composite: **which tree organizes a system is a consequence of
the system's premise.** Visual resemblance between landscapes
(the reader's original screenshots) carries no evidential weight;
the premise does. This is the ledger's standing anti-numerology
argument, now stated as two verified premises-bearing claims.

## Honesty trail

- The hand-derivation of the golden orbit initially missed that
  1−t lies on the CLOSED left edge of g1's domain, so g1(1−t)=0
  joins the orbit (size 4, not 3). Caught during the derive
  layer, derived properly, and weaponized as the open-edge
  falsifier mutant.
- Orbit sizes (4, 8, 10, 12 / 6, 8) are recorded unscored — no
  pattern claim registered.
- Defining degrees are used without certifying minimality;
  Bandt's theorems are context, never premises.
