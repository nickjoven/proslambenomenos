<!-- evidence: scripts/experiments/p17_derive.py, scripts/experiments/p17_registration.json, scripts/experiments/p17_bell.py, scripts/experiments/p17_results.json, catalog/c32_bell_experiments.py, scripts/verify/p17_bell_ladder.py -->
# P-17: the Bell ladder - expansion is cheap, contraction is a theorem

Registered before computing (PREDICTIONS.md P-17); resolution R-12,
all clauses as registered; constants litchecked in LC-10. The 2022
Nobel experiments honour a theorem about mechanical models; the most
sophisticated honest mechanical model is the one that computes its
own ceiling exactly and prices every route past it.

## The ladder (every rung derived before any simulation)

    2         the local ceiling - exhaustive over all 16
              deterministic strategies; shared randomness buys
              nothing (linearity, EQ1-EQ2)
    2 sqrt 2  the quantum ceiling - Landau's identity S^2 = 4I -
              [A0,A1]x[B0,B1] entrywise to 8.9e-16; operator norm
              and singlet expectation both 2 sqrt 2 (EQ3)
    4         the algebraic ceiling - one blunt bit (send the
              setting) reaches it deterministically (EQ5)

The best honest machine: a shared rotor, E = 2 theta/pi - 1. Its
zigzag saturates S = 2 at the very angles where the cosine reaches
2 sqrt 2 (EQ4) - the visual gap between zigzag and cosine is the
prize. Simulated at 1e6 pairs per point: worst 1.03 sigma, CHSH
2.00050.

## The price list (each escape implemented and paid)

- **One clever bit** (Toner-Bacon 2003): shared lambda1, lambda2;
  c = sign(a.l1) sign(a.l2); Bob answers sign(b.(l1 + c l2)). The
  simulated curve IS -cos theta (worst 0.91 sigma). One bit of
  signalling buys the exact singlet.
- **A quarter of the detections**: Bob detects with probability
  |b.lambda|. Two sphere identities (E[(b.l) sign(a.l)] = cos/2,
  E|b.l| = 1/2, EQ6) make the post-selected correlation -cos theta
  EXACTLY at mean efficiency 3/4 - below the Garg-Mermin threshold
  2/(1+sqrt 2) = 0.8284, which is why the 2015 loophole-free
  experiments had to exceed it. Measured: eta_B = 0.500 at every
  angle, curve within 1.41 sigma.
- **Setting knowledge**: S = 4, deterministically.

## The extremes (the design principle followed to both ends)

Expansion's extreme is the PR box, and there the reductio fires:
communication complexity collapses - the n-bit inner product costs
ONE bit (van Dam; implemented exhaustively at n = 8, 65,536 input
pairs, EQ7). Contraction is the hard direction: the one principled
cut, information causality (Pawlowski et al. 2009), gives
f(E, k) = 2^k (1 - h((1+E^k)/2)) - bounded below 1 for every depth
exactly at E = 1/sqrt 2 (max 0.7982 at k = 1, falling to
1/(2 ln 2) = 0.7213), broken at finite depth for any E above it
(k = 8 suffices at E = 0.73), exploding as 2^k at the PR box
(EQ8). The boundary of the principle is the quantum ceiling: for
this slice, "why not 4" has a computable answer, and "why exactly
2 sqrt 2" is answered by IC only on the CHSH slice - the full
quantum boundary needs the NPA hierarchy and is not attempted.

## The history (c32)

AGR 1982: S = 2.697 +/- 0.015 - 46.5 sigma above the local ceiling,
95.35% of Tsirelson. FC 1972: 6.25 sigma. Sources in LC-10.

## Reading (commentary within an evidence note, no load)

The scope line that keeps this honest: classical wave mechanics can
build the cosine (nonseparable local modes; "classical
entanglement"), so the correlation FUNCTION is mechanically
constructible - what cannot be built locally is its ALLOCATION
across separated stations. Every mechanical model that claims
otherwise is paying one of the listed prices, and the list is
exhaustive for CHSH. In the repo's vocabulary: which correlations
exist is decided by the coupling class, and the three ceilings are
the counting invariants of three coupling classes.
