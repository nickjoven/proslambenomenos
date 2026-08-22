# Working in this repository with more than one actor

1. **One checkout per actor.** The primary checkout stays on `main` and
   is read-only for everyone. Every task - agent or human - works in a
   git worktree: `make wt TASK=name` (creates `../wt-name` on branch
   `name` from `main`), `make wt-done TASK=name` when merged. The Agent
   tool's `isolation: "worktree"` does the same thing.
2. **Never, in a tree you do not own:** `git checkout`, `git switch`,
   `git stash`, `git reset --hard` (LAW-2), or edits of any kind.
3. **Gate-covered files are integrator-only**: `scripts/check_*.py`,
   `scripts/run_all.py`, `scripts/*.js`, `scripts/verify/*`,
   `tests/test_checks.py`, `catalog/_common.py`. A task that needs a gate
   change reports it; the integrator writes the LAWCHANGES entry last,
   after rebase, with the hashes as they will be on `main`.
4. **IDs are allocated at assignment.** A task prompt that may produce a
   litcheck, prediction, or law entry is told its number (LC-n, P-n).
   The append-only ledgers merge by union (`.gitattributes`), so two
   appends never conflict textually; numbering is the only shared state.
5. **Namespaced outputs.** Results go to
   `scripts/experiments/<task>_results.json`; scratch to a per-task
   directory. Never write another task's file. Catalog entries that
   read results pin them by sha256.
6. **Landing is serial.** The integrator rebases each branch onto
   current `main`, runs all gates, opens the PR, merges (rebase-only),
   and packs the handoff. `main` is PR-only with CI on the PR head.
7. **Report, don't conclude.** Commit messages describe; the message
   gate rejects conclusive vocabulary without a `[claim id]` tag.
