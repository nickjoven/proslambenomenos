# harmonics-v2

Rebuild from the beginning. The v1 corpus (`~/code/harmonics`) is retained
as an archive and adversarial test bed; nothing enters v2 without passing
the intake gate. v2 starts empty except for the mathematics that survived
v1's audits.

## The intake law

**Statuses are computed, never declared.** A claim file records evidence
artifacts; `scripts/check_claims.py` derives the status from fixed rules.
A recorded status that disagrees with the computed one is a blocking
error. There is no promotion, no demotion, no closure ceremony — to
change a status you change the evidence, and the tool re-derives.

Derived vocabulary (in order of precedence):

| status | derived when |
|---|---|
| `refuted` | any refutation evidence exists (wins over everything) |
| `conditional` | any premise resolves to a non-settled claim (caps all below) |
| `coincidence-unruled` | claim asserts numeric agreement with an observable and its permutation-null p ≥ 0.05 or is missing (caps all below) |
| `proven` | proof evidence, premises settled |
| `verified` | computational evidence with `method: reimplementation` or `external` |
| `reproduced` | computational evidence, `method: rerun` only (same-algorithm rerun is not independent verification) |
| `imported` | external citation evidence only |
| `asserted` | no evidence |

## Birth requirements (the checks v1 lacked, required from commit 1)

1. **Novelty is a field, not a vibe.** `novelty.status ∈ {unchecked,
   classical, folklore, checked-novel}`. `classical`/`folklore` require a
   citation; `checked-novel` requires a `LITCHECKS.md` entry (date,
   method, sources searched). While `unchecked`, novelty vocabulary is
   banned in the claim statement.
2. **Pigeonhole gate.** Any claim asserting numeric agreement with a
   measured observable must carry `numeric_match.pigeonhole_p` from a
   permutation null; p ≥ 0.05 or absent ⇒ status capped at
   `coincidence-unruled`. (v1's own commit 5f41c24 carried p = 0.13 and
   closed the claim anyway. Never again, mechanically.)
3. **Verification method is recorded.** Script evidence declares
   `method: rerun | reimplementation | external`; rerun-only derives the
   weaker `reproduced`, not `verified`.
4. **The message layer is audited.** `scripts/check_messages.py` blocks
   commit messages that use conclusive claim vocabulary ("proves",
   "exactly", "confirms", "closes", "novel", "zero free parameters")
   without referencing an existing claim id whose computed status
   supports the language. v1's history reads as discovery at every claim
   moment because nothing ever read the messages.

## Layout

- `claims/*.yml` — one claim per file (schema in `check_claims.py` docstring)
- `LITCHECKS.md` — literature-check ledger (append-only)
- `scripts/check_claims.py` — the intake gate (blocking)
- `scripts/check_messages.py` — commit-message claim-language gate
- `scripts/run_all.py` — run everything; exit nonzero on any failure
- `tests/test_checks.py` — red/green fixtures for every rule above

## Trust boundary

A green gate is consistency accounting, not truth: statuses are derived
from *recorded* evidence, undeclared premises are invisible, and the
checker cannot read mathematics. Reds are theorems; greens are not.
