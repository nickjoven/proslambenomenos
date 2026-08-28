<!-- evidence: scripts/experiments/p16_derive.py, scripts/experiments/p16_registration.json, scripts/experiments/p16_walk.py, scripts/experiments/p16_results.json, scripts/experiments/p25_clocks.py, scripts/experiments/p25_results.json, scripts/experiments/p16_plots.py, scripts/verify/p16_two_dimensions.py -->
# P-16/P-25: the two spectral dimensions of a causal set

Symbols: see the VOCABULARY.md symbol graph - d_s on a causal set is
DEFINITION-dependent across the literature and PROTOCOL-dependent
within the walk definition; this line adds both refusals with their
mechanisms.

Registered before computing (P-16; P-25); resolutions R-21
(mind-change FIRED on the instrument clause) and R-22 (FIRED on
both clauses - the line deliberately stops there). The three
physics clauses of P-16 held. Figure page p16_plots.html, published
as an artifact.

## What held

- The substrate nulls: link counts on the exact quadrature
  E[links] = N(N-1) int (1-a)(1-b)(1-ab)^{N-2} at every cell; mean
  Hasse degree growing ~ 2 ln N - the causet nonlocality driver.
- The EM signature, reproduced: walk window peaks 2.664 / 3.222 /
  3.687 at N = 64 / 128 / 256, growth 1.023 (floor 0.10). The walk
  spectral dimension increases with refinement, far above the
  Hausdorff 2, exactly as Eichhorn-Mizera report.
- The d'Alembertian side, from the SOURCE closed form
  g = -Z e^{Z/2} E2(Z/2) (ASS eq. 5): d_s runs 2 -> 2.260 (at
  s = 1.34) -> 2, N-independent, reproducing BBMM Fig. 2; the
  unregularised identity d_s = 4 rho s recovered at ratio 1.000;
  the exact-log-derivative instrument agrees with finite
  differences to 1.2e-7.
- The divergence, derived at EQ7 then measured: walk d_s <= 0.198
  at the lattice scale while the d'Alembertian sits at 2.03 at its
  smallest s. Opposite directions; opposite refinement trends; no
  winner crowned - the registered output IS the divergence.

## The audit catch (LC-15)

The derive layer caught that BBMM's PRINTED eq. (15) fails the
paper's own IR limit by exactly 4/sqrt(pi) - 2 = 0.256758: the
psi-sum identity sum b_n psi(n+1) = -2 forces g(0) = a + 1/c0,
confirmed by two independent implementations agreeing to 4e-4.
The source operator has the correct limits exactly and reproduces
their published curve, so their numerics evidently used the source
form; the printed formula carries a transcription defect. Caught
pre-registration, pinned in the falsifier as a live mutant.

## What fired, twice, and why that is the finding

R-21: the instrument-agreement clause compared the two walk clocks
at different diffusion scales (a design error of the P-22a class,
not caught pre-run). R-22: the properly matched re-registration
ALSO fired - the derived band carried the Poisson-smearing term but
omitted PARITY: Hasse graphs are triangle-free and near-bipartite
(mu-spectrum symmetric to 0.043), odd-step returns are suppressed
(odd/even 0.195 at five steps, 0.996 by twenty-three), so the
continuous-time clock (a Poisson mixture over all step parities)
and the even-step clock separate by a cell-dependent amount at
exactly the accessible scales. Two firings = stop: on sprinkled
causal sets at simulable N, the walk d_s is protocol-dependent
even within its own definition. That does not weaken P-16's
thesis; it is the thesis one level deeper - the short-scale
spectral dimension of a causal set is convention-laden, and the
literature's disagreement is the expected condition. BBMM's own
conclusion speculates about an interpolating description; that
question is framed by this computation and left open, as
registered.

Not claimed: which definition is right; d > 2; curved sprinklings;
the causal (meeting-probability) d_s; any interpolation claim.
