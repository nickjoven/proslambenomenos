<!-- evidence: scripts/experiments/p32_derive.py, scripts/experiments/p32_registration.json, scripts/experiments/p32_factorial.py, scripts/experiments/p32_results.json, scripts/experiments/p33_regrid.py, scripts/experiments/p33_results.json, scripts/verify/p32_parity_factorial.py -->
# P-32/P-33: the drive-geometry parity factorial

## What was asked

A-2's debt: LC-3 hypothesized that E1's no-parity result and the
Josephson literature's even/odd half-integer-step claim differ
because of the drive type. Test it with a 2×2 factorial on one
codebase: drive (per-site pinning vs uniform bias + AC) ×
geometry (one π seam vs alternating 0-π bonds), N = 4..9.

## The derived refinement (before anything ran)

A ring is not an open array: with alternating offsets the net
frustration is f(N) = (⌊N/2⌋/2) mod 1 and odd N forces an
alternation defect. The imported even/odd claim CANNOT be the
whole story on a ring — evens split into {4,8} (clean) and {6}
(half-frustrated), odds into {5,9} (defect) and {7} (both).

## What happened (the honest arc)

1. **P-32 ran; two clauses fired.** Every bias-side "width" came
   out exactly 0.00080 — the tolerance smear of an unlocked
   staircase (2·TOL/slope, slope measured 1.0000). The width
   floor was mis-derived; there was no half-integer locking at
   the registered operating point. And the pinning side surprised
   in the opposite direction: frustration organizes it strongly.
2. **P-33 re-registered** with the corrected per-cell null and a
   declared (A, ν) grid. Outcome: zero of 288 bias cells locks
   anywhere on the grid — and the positive control fired too,
   which produced the diagnosis that closes the line:
3. **The telescoping identity.** The coupling terms cancel in
   antisymmetric pairs around the ring, so the site-mean rotation
   number is ρ = I *identically* (verified at 9e-17). No Shapiro
   step of any order can appear in this observable, for any
   geometry — by algebra. Second firing on the positive-control
   family → the stop rule closes the bias side.

## The findings

- **Positive (the claim):** the four derived frustration classes
  order the pinned ALT ring's 1/2-plateau widths at K = 1.2:
  clean 0.1667/0.1666 > defect 0.1537/0.1522 > half 0.0370 >
  both 0.0159. Frustration narrows the plateau, class by class;
  plain parity fails ({6} sides with {7}).
- **Negative (the reconciliation, sharpened):** the Josephson
  parity effect needs BOTH per-junction nonlinearity in the
  driven loop AND a difference-variable observable. E1's pinned
  ring has the nonlinearity without the drive; our bias ring had
  the drive but its site-mean observable telescopes to triviality;
  the Josephson arrays have both. The literature's effect could
  never have appeared in either of our families — LC-3's
  drive-type reading survives in this sharpened form.

## Process notes

- The P-9 reproduction landed on all twelve pins
  (r(N) = 0.300...0.444, no alternation), revalidating R-6's
  attractor-controlled protocol.
- Two instrument lessons banked: (i) a locking detector's null is
  the tolerance smear 2·TOL/slope, not an arbitrary floor;
  (ii) check conservation identities of the OBSERVABLE before
  registering positive controls on it — ρ_mean was conserved-
  trivial by construction and two clauses had to fire before the
  algebra was seen.
