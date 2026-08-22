# proslambenomenos

*Proslambanomenos*: in Greek music theory, the added lowest note — the
tone beneath the Greater Perfect System that anchors the scale while
belonging to no tetrachord. This repo begins with mathematics, at the
bottom, and rises only as far as evidence carries.

Successor to the harmonics corpus (`~/code/harmonics`, retained as
archive and adversarial test bed). Everything here enters through the
intake gate; nothing is grandfathered.

## Strategy

**Two tracks.**

*Track 1 — the a₀ spine.* The one community-legitimate physics question
the old corpus touched: does the MOND acceleration scale track cH(z), or
sit constant? Held here exactly as the intake law prices it — a
conjecture with a stated falsifier, the 2π declined and cited to Milgrom
(DECLINED.md D-3). First deliverable: the discriminating-test note
(which surveys, which mass range, what sample sizes separate cH(z)/2π
from constant a₀ from (1+z)^¾). Contribution class: synthesis with a
real audience, not new physics — and labeled so.

*Track 2 — the drip.* The formerly numbered derivations, reworked from
the lowest number up, one claim per release. Each release is the
derivation's honest mathematical content only: correct, verifiable,
in-literature welcome ("classical with citation" is a first-class
label, not a demotion). The physics identifications that rode on each
derivation stay where the disposition put them — declined, conjectured,
or queued as solve-candidates — and never re-enter by adjacency. The
drip queue with per-item reductions lives in QUEUE.md; the compendium
page grows one section per drip, each with a Verify button that can
fail.

**Why a drip.** The old corpus outran its verification because claims
entered in arcs — dozens of interdependent docs landing together, each
lending unearned plausibility to its neighbors. A drip inverts that:
one claim, one gate pass, one runnable verification, no load-bearing
welds between releases. The corpus cannot grow faster than its
checking, structurally.

**What carries over from v1.** The audits (the reason anything here can
be trusted), the compendium (the surviving math, runnable), DECLINED.md
(closed routes with reopen conditions), LITCHECKS.md (the
literature-check ledger), and the two solve-candidates (the XOR
spectrum-to-tree translation; the two-anchor minimum). What does not
carry over: any status, any framework vocabulary, any claim that has
not individually re-entered through the gate.

**ket: decoupled.** This repo runs on git plus the Python gates alone —
no CAS layer, no sealing. At this scale git is the content-addressed
store, and coupling the substrate in would recreate v1's
apparatus-gravity (corpus serving tooling serving corpus). ket iterates
separately, on its own roadmap (hardening branch, the read-as-formation
memory experiment, the probe-ledger direction for latent
representations). If this repo one day needs ket, that need enters as
a recorded decision, not a default.

## The intake law

**Statuses are computed, never declared.** A claim file records
evidence artifacts; `scripts/check_claims.py` derives the status from
fixed rules. A recorded status that disagrees with the computed one is
a blocking error. There is no promotion, no demotion, no closure
ceremony — to change a status you change the evidence, and the tool
re-derives.

Derived vocabulary (in order of precedence):

| status | derived when |
|---|---|
| `refuted` | any refutation evidence exists (wins over everything) |
| `conditional` | any premise resolves to a non-settled claim (caps all below) |
| `coincidence-unruled` | claim asserts numeric agreement with an observable and its permutation-null p ≥ 0.05 or is missing (caps all below) |
| `proven` | proof evidence that is machine-checked OR corroborated by independent reimplementation/external computation, premises settled |
| `argued` | proof evidence, prose-grade only — attested, not enforced; NOT settled for propagation |
| `verified` | computational evidence with `method: reimplementation` or `external` |
| `reproduced` | computational evidence, `method: rerun` only (same-algorithm rerun is not independent verification) |
| `imported` | external citation evidence only |
| `asserted` | no evidence |

## Birth requirements (the checks v1 lacked, required from commit 1)

1. **Novelty is a field, not a vibe.** `novelty.status ∈ {unchecked,
   classical, folklore, checked-novel}`. `classical`/`folklore` require a
   citation; `checked-novel` requires a `LITCHECKS.md` entry. While
   `unchecked`, novelty vocabulary is banned in the claim statement.
2. **Pigeonhole gate.** Any claim asserting numeric agreement with a
   measured observable must carry `numeric_match.pigeonhole_p` from a
   permutation null; p ≥ 0.05 or absent ⇒ status capped at
   `coincidence-unruled`. A statement scanner forces the block when
   agreement vocabulary appears — a tripwire, not a wall: paraphrase
   can evade it, and the residual is recorded (adversarial audit F3).
3. **Verification method is recorded.** Script evidence declares
   `method: rerun | reimplementation | external`; rerun-only derives the
   weaker `reproduced`, not `verified`.
4. **The message layer is audited.** `scripts/check_messages.py` blocks
   commit messages that use conclusive claim vocabulary without
   referencing an existing claim id whose computed status supports it —
   and any commit touching `claims/*.yml` must tag every touched claim
   id, so the narrative layer cannot silently modify the evidence
   layer. The coverage rule holds from its enactment (b182d83); CI
   checks the full range from that boundary (--all).
5. **The law cannot change silently.** Every scripts/check_*.py,
   run_all.py, and the fixture suite is hash-covered by LAWCHANGES.md
   (append-only): any edit without a dated, directed
   (strengthen/weaken/neutral), justified entry goes red. Amendments
   are legal; silent ones are not.
6. **Rulings cannot be unmade quietly.** DECLINED.md, LITCHECKS.md,
   LAWCHANGES.md (and PREDICTIONS.md when created) are append-only
   against git history: any commit removing a line goes red. Residual:
   local history can still be rewritten by the owner — closed fully
   only by a remote with protected history (trust rung 3).
7. **Work is preregistered.** PREDICTIONS.md (append-only) records,
   BEFORE an attempt runs, the expected outcome and what would change
   the author's mind; the gate enforces that a cited prediction's
   registration is an ancestor of the claim citing it, and the
   protected remote makes the ordering third-party-attested.
   Post-enactment claims with numeric agreements or novelty checks
   require one. The three solve-candidates are preregistered as
   P-1..P-3 before any derivation attempt.
8. **Routes are separable from problems.** Withdrawing a derivation
   (DECLINED.md) never closes the underlying problem, and a plausible
   route never settles one. The decomposition — "X is derivable" versus
   "X holds" — is mandatory.

## Layout

- `claims/*.yml` — one claim per file (schema in `check_claims.py`)
- `QUEUE.md` — the drip queue: each old derivation's honest reduction
- `DECLINED.md` — withdrawn routes, with reopen conditions (append-only)
- `LITCHECKS.md` — literature-check ledger (append-only)
- `compendium/index.html` — the public face: every claim, runnable
- `scripts/` — the gates; `tests/` — red/green fixtures for every rule

## Trust boundary

A green gate is consistency accounting, not truth: statuses are derived
from *recorded* evidence, undeclared premises are invisible, and the
checker cannot read mathematics. Reds are theorems; greens are not.

## Handoffs and owner actions

- `make handoff` — generate HANDOFF.md from repo state + OPEN.yml and
  pack it as a catbus packet in `~/code/handoffs` (linked to the
  previous packet). `make handoff-preview` prints it without packing.
- `make owner-commands` — print the owner-action commands from
  OPEN.yml as bare lines, one per action, for copying.
- OPEN.yml is the single source of truth for open items; edit it, not
  the chat, when an item opens or closes.

## Specs and the notes gate (LAW-20)

Every gate rule is a line in `tests/spec/*.spec`, in a controlled
grammar (`RULE gate.n "label": GIVEN fixture WHEN gate RUNS THEN
ACCEPT | REJECT MENTIONING "token" | EQUALS json`). `make spec` runs
them; a rule naming a gate that does not exist fails, which is how a
new gate is written test-first. Every `notes/*.md` opens with
`<!-- commentary -->` (no load, no verdicts) or `<!-- evidence: paths
-->` naming the executable artifacts that carry its numbers.
