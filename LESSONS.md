# LESSONS — the cold ledger of instrument lessons

Append-only. Each entry: an id, TRIGGERS (keywords a registration's
domain would match), the RULE (short, imperative), and CITATIONS
(where it was learned - the firing or audit that paid for it).
Consulted mechanically at registration time per AGENTS.md item 8d:
`python3 scripts/tools/lessons.py <keywords>`. This ledger exists so
AGENTS.md can stay small: invariants live hot, case knowledge lives
cold and is surfaced when its triggers match.

## L-1 — tolerance smear
TRIGGERS: locking, plateau, tolerance, width, staircase, detector
RULE: a tolerance-based detector reads 2*TOL/slope on featureless
background; every measured width must be compared against that
derived smear, never against a bare floor.
CITATIONS: R-29 (P-32: every bias-side width was the smear).

## L-2 — conservation identities first
TRIGGERS: observable, mean, sum, ring, telescoping, gauge, symmetry
RULE: before registering a positive control on an observable, check
its exact algebraic constraints (telescoping sums, Newton pairs,
gauge freedoms, reflection symmetries) - the constraint may make
the registered outcome trivial or impossible.
CITATIONS: R-30 (P-33: rho = I by telescoping); P-35 EQ3 (derived
up front, the lesson applied); R-33 (net-W blind to the paired
channel by the same reflection that makes sectors degenerate).

## L-3 — no guessed numeric bands
TRIGGERS: band, window, tolerance, clause, threshold, value
RULE: every numeric band in a clause traces to a derivation or a
pinned source; a value window at fixed resolution is never the
right observable when a scaling or convergence statement exists.
CITATIONS: R-32 (P-2: two guessed windows fired while the derivable
estimate sat in the same script); the corollary recorded there.

## L-4 — power budgets are bands too
TRIGGERS: power, sigma, sample size, M, detectable, ordering clause
RULE: a clause's statistical power calculation must trace to
registered quantities; leaning a 3-sigma design on an unregistered
overlay imports the overlay's error into the design.
CITATIONS: R-36 (P-37: the D = 0.28 wall pair, powered off the
deliberately unregistered Kramers overlay, fired at 1.9 sigma).

## L-5 — extrapolate along the ladder
TRIGGERS: Fibonacci, ladder, approximant, rung, q, scan, resolution
RULE: quantities on a convergent ladder scale geometrically
(Fibonacci: widths shrink ~ phi^-2 per rung; a 1/q scan gains only
phi^-1), so any detector budget validated at small q has a
COMPUTABLE failure rung - extrapolate the validation quantities by
the pinned per-rung factor before registering. R-25 pinned 0.324 =
phi^-2.34 four days before P-40 registered a budget that
contradicted it; the crossover computed to between q = 55 and 89
and the firing landed there.
CITATIONS: R-39 + the q = 13 audit note in
notes/p41_gap_openings.md (the min-band vs scan-spacing table);
R-25 (the pinned per-rung factor); P-28's registration (the
anti-pattern done right: promise scoped to the derivable rung).

## L-6 — certified-complete beats scanned
TRIGGERS: roots, edges, spectrum, scan, bisection, count
RULE: when the objects to be found are eigenvalues in disguise
(band edges, discriminant roots), use the eigen-route - a scan
misses features narrower than its spacing and deletes them in
PAIRS, silently; the count is then the only tell, so make the
count a registered integrity clause either way.
CITATIONS: R-39 (the 60q scan lost 2-18 edges at q >= 89); P-41
(the eigen-route measured all eight cells).

## L-7 — heavy-tailed estimators need a sampling condition
TRIGGERS: Jarzynski, exponential, estimator, rare event, average
RULE: an exponential-average estimator (e.g. <e^{-W/T}>) is
formally unbiased but practically dominated by rare tails; its
null cell must satisfy a derived sampling condition (e.g.
(sigma_W/T)^2 <= 0.5 at the registered M) with adequacy shown in
the layer, or the null will fail on statistics alone.
CITATIONS: P-37 layer (the first null cell read 0.855 +- 0.029 on
a true identity; the gentler cell passed).

## L-8 — mutants can be defeated by global structure
TRIGGERS: mutant, falsifier, discriminating, skip, global
RULE: a mutant that perturbs a LOCALLY-motivated quantity may be
rescued by a global identity (a gap line is global, so a skip-rung
Streda mutant still returns the right slope); verify each mutant
actually fails before pinning it, and record discarded
non-discriminating mutants with the reason.
CITATIONS: P-28 audit note (the 8/13 skip-rung mutant); the p29
skip-rung lesson recorded in its notes.

## L-9 — anchor the roles before trusting the value
TRIGGERS: convention, roles, inputs, outcomes, contraction, sign
RULE: when reimplementing a scenario from a paper, land on a
pinned anchor value FIRST (one known point reproduced) before
computing anything new - role inversions (inputs vs outcomes,
letter maps, normalization double-counts) produce plausible wrong
numbers that only an anchor catches.
CITATIONS: P-39 layer (game-role inversion caught against P-30's
(2+sqrt2)/4; the falsifier's double normalization caught the same
way); P-40 layer (the letter-map complement caught by the
trace-tie check).

## L-10 — a causal verb names its coupling term
TRIGGERS: momentum, drift, transfer, handed, hands, drag, torque,
feeds, pumps, exchange, flux, aftermath, reading, gloss
RULE: a verb that moves a quantity between two subsystems (hands,
transfers, drags, feeds, pumps, drains into) is a statement about
the COUPLING term of the exact identity, and is checked against
that term's integrated size before it is written - in the claim
statement, the registration, the R entry, the note and the OPEN log
alike. If the integral is bounded small, the loss is the
subsystem's own dissipation and the gain is the drive's; the verb
is wrong even when every number beside it is right. Unregistered
readings get the same check: name the identity, compute the term.
CITATIONS: R-44 (the "mean drag" that was a spin-up; the 182
"out-flow" that was pre-event pumping); P-46/R-45 (the correcting
line's own clause (2), "the ring hands its drift to the rotor",
against its own bound 4/Omega ~ 0.2 on 77 units of ring momentum -
under 0.3 percent transferred, the rest dissipated in the ring;
caught in the 2026-09-02 audit of PR 113, the lesson candidate
R-45 proposed and left unadded).

## L-11 — an absent check point fires
TRIGGERS: check point, sample, skip, missing, window, empty, holds
RULE: a registered check point that is absent from the run's data
is a FIRED clause, not a skipped one; a runner raises on a missing
point, and a verdict that is a boolean AND over "whatever was
found" is a loosened check that cannot fail on absence. Count the
compared points in the results against the registered list.
CITATIONS: P-46 runner (`if D in sm:` guarding the drift checks;
all four points were present so nothing fired, but the guard would
have passed a missing one as held); P-47 layer (a loosened-check
mutant that could not fail, caught there before registration).
