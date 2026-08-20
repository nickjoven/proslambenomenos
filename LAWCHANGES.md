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

## LAW-2 — 2026-08-19 — G1–G3 closure + restoration after the reset incident
direction: strengthen
why: forensic gaps closed — the compendium harness enters the tree as
scripts/run_compendium_checks.js behind check_compendium.py (G1);
scripts/verify/*.py auto-rostered via check_verify_scripts.py (G2);
evidence refs naming repo paths must exist on disk (G3, in
check_claims.py). Coverage extended to scripts/*.js. Also restores
what a destructive red-test cleanup (git reset --hard in the working
repo) silently deleted before LAW-1's commit: the run_all roster of
the constitutional gates and the law/append-only fixtures — an
incident the law gate detects retroactively (5 violations against
LAW-1) and which this entry resolves. Red-test protocol changed:
scratch commits in worktrees, never reset --hard in the working tree.
hashes:
  615bffa803c6ee42aed4b12297ae23c0467d4feb5e8b76e283a77315d3451d61  scripts/check_append_only.py
  c635b4fe28608439ce9136b4dc180936da71133b28b3f8ff2d1e116131502b51  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  d063d8e2cbb5e0d0b0284cb0bd2be67cb5686795e9f5a074b4177d35a81d6580  scripts/check_lawchanges.py
  d5abdcfd24c0b207401a985e13838f2640f70e96b92efc1e3297d4db2bbe7cbf  scripts/check_messages.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  130da351d6753ec097afd996a3234223bacb26f22eac55a9b5e6e6c7b9d5060f  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  4bba2b0691d57c7ff938aedb9a8bc528c6eebb4e667e10f4260ea8e4169724fe  tests/test_checks.py
