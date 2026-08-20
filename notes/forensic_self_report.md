# Forensic self-report: proslambenomenos under its own lens

Method: the same information-lift-with-correctness-scrutiny applied to
harmonics, now pointed at this repo. Every gate, claim, verification,
and note re-examined for: is it computationally sound (executed,
deterministic, re-runnable from the tree), and where are the gaps.
Live checks re-run 2026-08-19 where cited.

## A. Computationally sound — executed, deterministic, rostered

| Item | Evidence of soundness |
|---|---|
| Intake gate (argued/proven grades, pigeonhole, novelty, cycles, propagation) | 14 red/green fixtures, each rule shown to fail on a violating fixture; live-fired against its author's label errors |
| Message gate (conclusive vocab + touched-claims coverage) | 6 unit fixtures on the pure check_commit(); live red test (untagged claim edit → rc 2); has rejected the author's own commit message 4 times in production |
| Law gate + append-only gate | 3 unit fixtures on pure parsers; both red-tested LIVE (gate edit without ledger entry; committed line removal) with named violations, green on restore |
| Executed numerics behind claims | q1_saddle_node.py (rel err < 7e-4, exponent −0.5001), q_j_structure.py (7 modes, residuals < 1e-12), Γ₀(6) orbit check (200 elements), j-invariants (3/3 reproduce), multiplicative orders (ord₂₇(13) = ord₅₄(13) = 9), Koide numerics (Q = 0.666661, χ₀ fraction 0.375003), Weyl counts (ratio 0.99900 at R = 40, 1.00035 at R = 80) |
| Compendium checks C1–C18 | 18/18 executed headlessly pre-publish; expected values sourced from the extraction inventory's independent re-derivations, not from the page's own prose |

## B. Sound but NOT re-runnable from the tree — the biggest structural gap

**G1 (high). The compendium verification harness is not in the repo.**
The 18/18 headless result was produced by a Node harness that exists
only in the session history. Claim evidence cites "compendium C1/C7/
C9/C17" as reimplementation-grade computation, but nothing in the tree
can execute those checks; a fresh clone cannot reproduce the
compendium verification. Fix: commit the harness as
scripts/run_compendium_checks.js and roster it.

**G2 (high). scripts/verify/*.py are not rostered in run_all.**
q1_saddle_node and q_j_structure are cited as evidence and were run
once, by hand. Nothing re-runs them; they can rot silently while the
claims citing them stay green. Fix: roster them (they cost ~2 s).

**G3 (high, mechanical). Evidence refs are unresolved free text.**
check_claims never verifies that a path-shaped ref exists
(live-checked: no existence test in the gate). A claim could cite
scripts/verify/nonexistent.py and derive `proven`. Fix: any ref
matching a repo path pattern must exist on disk; red otherwise.

## C. Grade asymmetries and honor-system fields

**G4 (medium). Refutation evidence is ungraded.** `proven` demands a
machine-checked proof or independent reimplementation; `refuted`
accepts a prose ref with no corroboration requirement — an asymmetry
under which killing a claim is cheaper than establishing one. Current
instances: second-law-from-nonorientability rests on classical
theorems cited in prose (correct, but citation-grade — reversibility
of geodesic flow, Anosov entropy — nothing executed);
gaussian-lattice-54-cycle's refutation has one executed leg
(ord = 9) and one interpretive leg (that multiplication by 13 is the
claim's operative map — contextually supported by the v1 audit, but
the v1 doc exhibits no map at all, so "unsupported" and "refuted"
are separated only by that reading). Fix options: a refuted-argued
grade mirroring argued, or a corroboration requirement on
refutation evidence.

**G5 (medium). `machine: true` is self-attested.** The proof-grade
flag that upgrades prose to machine-checked is an honor-system
boolean; nothing executes the referenced artifact. Currently unused
by any real claim (all 13 proven claims qualify via reimplementation
evidence), so today it is a latent hole, not an active one. Fix:
`machine: true` must carry a runnable ref that a rostered check
executes.

## D. Minor gaps

| # | Gap | Severity | Note |
|---|---|---|---|
| G6 | Compendium randomized checks use unseeded Math.random | low | margins are exact-0 vs O(1), flake probability negligible; seeded PRNG is still more honest |
| G7 | Merge commits skip touched-claims coverage (diff-tree without -m) | low | repo is currently linear; document or handle -m |
| G8 | touched_claims() git path unit-untested (pure fn is tested; live path tested once, manually) | low | a temp-repo fixture would make the live red test repeatable |
| G9 | Premise cap reads recorded premise statuses: a wrong premise label yields one transient run where downstream looks clean while the premise is flagged | low | converges on the fix commit; never silently green overall |
| G10 | C15 pass threshold (5%) is loose vs measured convergence (0.1% at R = 40) | low | tighten to 0.5% |
| G11 | LITCHECKS confidences are agent-self-reported | recorded residual | closes only with human/second-method checks |
| G12 | link-001 digests pin the pre-argued-grade tree | not a gap | that is what a link is; next tag carries the strengthened law |

## E. What this report does not cover

The mathematical *content* of the claims was scrutinized in
topology_evaluation.md and modular_koide_evaluation.md and is not
re-litigated here; this report is about whether the apparatus that
carries those results is itself sound. The known law-level residuals
(owner history-rewrite pending a protected remote; approval-vs-
visibility of law changes; singleton pigeonhole) are recorded in
README and QUEUE and are not repeated as findings.

## Post-report incident (2026-08-19, same day): the report itself contained an unsound claim

Section A originally asserted the constitutional gates were rostered
and their fixtures present. Closing G1–G3 revealed this was false at
the time of writing: an earlier red-test cleanup had used `git reset
--hard` in the working repo, silently destroying the then-uncommitted
run_all roster edit and the law/append-only fixtures — and thereby
un-rostering the very gate that would have detected the loss. The
subsequent greens were `tail -1` over a reduced roster, and the report
asserted the roster from memory instead of re-checking. Three causes,
three corrections, now in force:

1. **Destructive cleanup in the working tree** → red-tests that need
   scratch commits run in git worktrees; `reset --hard` is banned in
   the working repo (LAW-2 records the protocol change).
2. **Output truncation** (`tail -1`) → final verification runs show
   the full per-gate roster, never a truncated tail.
3. **Memory-based reporting** → any rostering/count statement in a
   report is re-derived by grep at writing time.

Detection credit: the law gate, run directly, flagged 5 hash
violations against LAW-1 — the constitution caught its own
disablement retroactively, which is the designed behavior. Restored
and closed in LAW-2 alongside G1–G3.

## Disposition

G1–G3: CLOSED (LAW-2, same day) — the harness is
scripts/run_compendium_checks.js behind check_compendium.py, rostered;
scripts/verify/*.py auto-rostered via check_verify_scripts.py;
evidence refs naming repo paths must exist (fixture pair added).
G4–G5 remain queued as law amendments. G6–G10 hygiene. The incident
above is the report's own erratum and stands as finding G13.
