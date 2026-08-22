# P-6: stable twisted states on circulant graphs

Registered before computing (PREDICTIONS.md P-6, PR #38); run
2026-08-23 in worktree wt-p6. Script scripts/experiments/
p6_circulant_twisted.py; results p6_results.json; fast exhaustive
verify script p6_circulant_small.py (n <= 20, 0.1 s) with mutant.

## Method

C_n(S), identical oscillators; the q-twisted state is an equilibrium;
linear stability iff lambda_m = sum_{k in S} w_k cos(2 pi q k/n)(1 -
cos(2 pi m k/n)) > 0 for all m != 0 (the Jacobian is circulant). Every
reported maximiser is re-verified from the Jacobian's first row by
DFT, independently of the closed form. Exhaustive over all symmetric
S for n <= 28 (2^14 subsets at n = 28); greedy-by-cos plus 300 random
toggles per (n, q) for 28 < n <= 64. Density = 2|E|/(n(n-1)).

## Results

| range | max density | where |
|---|---|---|
| n <= 20 (exhaustive) | 12/19 = 0.6316 | n = 20, S = {1..6}, q = 1 |
| n <= 28 (exhaustive) | 2/3 = 0.6667 | n = 22, 25, 28; S = {1..k}, q = 1 |
| n <= 64 (search) | 0.6744 | n = 44, S = {1..7} u {15..22}, q = 2 |

All 60 reported states pass the independent Jacobian check. The
exhaustive maximisers are contiguous bands S = {1..k} with q = 1 -
the nearest-neighbour ring of Wiley-Strogatz-Girvan - with k/n just
below 1/3; the first two-band maximiser (q = 2) appears in the search
range at n = 44 and is the structure of the 2020 construction.

## Against P-6

Expectation held: no circulant in range exceeds 0.6809 (the maximum,
0.6744, is 0.0065 below it); the density maximum rises with n
(0.6316 -> 0.6667 -> 0.6744) and approaches the published value from
below, consistent with 0.6809 being a large-n limit of a two-band
family rather than a value attained at small n. The mind-change
condition (a verified stable state above 0.6819) did not fire. Scope:
the search above n = 28 is heuristic; it cannot exclude a better
circulant at 28 < n <= 64, only report none found. Not claimed:
anything about non-circulant graphs or the global threshold.

## What this is

A reproduction with an exhaustive small-n certificate, filed as the
verified claim circulant-twisted-max-density-small (n <= 20, where
the enumeration is complete and re-runs in 0.1 s). No contribution to
the open gap 0.681-0.75; the honest value is the certificate and the
tooling, which now handles the object the open problem is about.
