# LAWCHANGES — constitutional ledger (append-only)

The gates cannot be edited silently: every change to a covered file
(all scripts/check_*.py, run_all.py, tests/test_checks.py) requires a
new entry here — date, direction (strengthen | weaken | neutral), why,
and the post-change SHA-256 of every covered file. check_lawchanges.py
compares the tree to the LAST entry; check_append_only.py forbids
editing old entries. A weakening is legal; a silent one is not.

## LAW-1 — 2026-08-19 — constitution established
direction: strengthen
why: initial ledger; covers the intake gate (with the argued grade),
the message gate (with the touched-claims coverage rule), the fixture
suite, the runner, and the two new constitutional gates themselves.
hashes:
  615bffa803c6ee42aed4b12297ae23c0467d4feb5e8b76e283a77315d3451d61  scripts/check_append_only.py
  f96b3d3be34c4a8ece472037021f88efd28eacf5a87d5025b548555d0744d99a  scripts/check_claims.py
  b441ea6fbfb900ec24036673c654a74ef92e4d7cc6bf178e04f14835527e6ab0  scripts/check_lawchanges.py
  d5abdcfd24c0b207401a985e13838f2640f70e96b92efc1e3297d4db2bbe7cbf  scripts/check_messages.py
  a7e9bbc75ccdcfcb600a276237b7499798f5bc6141262ad46a2de935fc562d04  scripts/run_all.py
  fc575ac64752a991a0c18a9e01fdaefa26ea61dd6f9346d2e9b4b9e41e649b2d  tests/test_checks.py
