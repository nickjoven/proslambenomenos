# The math catalog

`catalog/c*.py` is the set of mathematical facts this repo's reasoning
leans on - classical results, textbook identities, and formulas
derived in the notes - each as a runnable check. The catalog gate
(`scripts/check_catalog.py`, in `run_all.py`, hence in CI) runs every
entry twice: plainly, where it must exit 0, and with `--mutant`, where
it must exit nonzero. An entry without a failing mutant is a
restatement, not a test (LAW-11), and the gate rejects it.

Conventions per entry: docstring line 1 is the fact; line 2 the
source; the mutant replaces the claimed discriminator with a specific
wrong alternative (a wrong exponent, a wrong constant, the refuted
formula). Entries are not hash-pinned by the law gate - they are
self-testing and adding one must not require a LAWCHANGES entry - but
the gate script itself is covered.

Difference from `scripts/verify/`: verify scripts are evidence for
claims in `claims/` and are hash-pinned; catalog entries are imported
facts used in prose and notes, with no claim attached. When a catalog
entry fails on a wording that is also in a note, the note is wrong
(c12's first version caught the run-5 "within ~15%" overstatement).

Run: `make catalog` or `python3 scripts/check_catalog.py`.
