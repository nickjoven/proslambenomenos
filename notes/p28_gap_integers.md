<!-- evidence: scripts/experiments/p28_derive.py, scripts/experiments/p28_registration.json, scripts/experiments/p28_labels.py, scripts/experiments/p28_results.json, scripts/verify/p28_gap_integers.py -->
# P-28: the gap integers of the golden ladder

## What was asked

A-12: P-7 computed the golden butterfly's spectra to q = 144 and
deliberately left Chern content not-claimed. Convert that scope
into an earned claim: do the computed gaps carry their
Diophantine/Streda labels?

## The number theory (all pre-registration, all exact)

- Every gap r at flux p/q has a unique label (s, t), r = sq + tp,
  |t| <= q/2 — except, for even q, the single ambiguous case
  r = q/2 where t = +-q/2 both solve. That is exactly the gap
  P-7's parity rule closes: **the gap the labeling cannot name is
  the gap the spectrum does not open.** Two independent
  formalisms pointing at the same object.
- The Fibonacci congruence F_{n-1} F_j = (-1)^{j+1} F_{n-j}
  (mod F_n) forces THE MAP: the gap at r = F_j carries
  |t| = F_{n-j}, mirrors sign-flipped. Fibonacci positions carry
  Fibonacci Chern numbers — not numerology, a two-line congruence.
- Corollaries: the principal pair t = +1 at r = F_{n-1}, t = -1
  at r = F_{n-2}; and the edge gap r = 1 carries the LARGE
  Fibonacci label |t| = F_{n-2}.

## The spectra (R-25, all clauses first run)

- Principal pair: widest two gaps at every rung, t = +-1; the
  t = +1 width saturates at 1.6851 — an O(1) gap heading into the
  irrational limit.
- The edge gap: resolved through q = 144, carrying t = -1, +2,
  -3, +5, -8, +13, -21, +34, -55 — the full alternating Fibonacci
  sequence — with widths 1.27 down to 8.2e-5. Per-rung ratio
  0.324: width ~ q^{-2.34} (unscored). The registration only
  required resolution through q = 13; the power-law scaling of
  the critical point carried it to 144. Exponential gap closing
  would have killed it by q = 21 — the edge gap's persistence is
  itself a visible signature of criticality.
- Streda mechanized: 18/18 Farey-neighbor gap pairs overlap in
  energy and band-counting returns integer slopes exactly
  (Fractions, no tolerance).
- Hierarchy: tier medians at q = 89: 1.685 / 0.332 / 0.147 for
  |t| = 1/2/3.

## Two audit notes

- Satija's review says "for rational flux p/q there are q gaps";
  the ladder has q-1 gap indices, and for even q the central one
  both closes and is label-ambiguous (LC-18).
- A skip-rung Streda mutant (8/13 paired with 34/55,
  non-unimodular) was tried and DISCARDED as non-discriminating,
  for a reason worth keeping: the gap line N = s + t alpha is
  GLOBAL, so any two fluxes sharing a gap's (s, t) give slope
  exactly t. Unimodularity buys adjacent-rung gap continuity (the
  windows overlap), not slope exactness. The registration's EQ4
  framing slightly over-credited unimodularity; the computed
  content (overlap + integer counting) is unaffected.

## Interop

- First experiment-side consumer of kernels.eig.eigh (anchored
  against the P-7 Jacobi route at 3.6e-15; full ladder runs in
  0.5 s).
- Feeds A-13 (the Farey bridge): the mediant/unimodular structure
  used here for window overlap is the same skeleton the tongues
  side carries (LC-7 Stern-Brocot).
