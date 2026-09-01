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

## LAW-3 — 2026-08-20 — adversarial-audit fixes F1–F6
direction: strengthen
why: context-free adversarial audit (notes/adversarial_audit_2026-08-19.md)
found four preventive bypasses and two overclaims. Fixed: deleted
ledgers now detected via git history (F1); scripts/verify/*.py join
the hash-covered set (F2); a statement scanner forces numeric_match
on agreement vocabulary, tripwire-grade (F3); the machine: flag is
disabled entirely until a machine-proof executor exists (F4/G5);
demonstrated synonyms join the conclusive lexicon (F5); the coverage
rule is dated from its enactment with CI checking the full governed
range via --all (F6). Koide claim decomposed per the law (F10);
prose counts made countless (F7/F8).
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  aea3324dc029969cb70bb7a0b48ca0173d8cb95dd8f173fbab31e113de7c13c1  scripts/check_messages.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  130da351d6753ec097afd996a3234223bacb26f22eac55a9b5e6e6c7b9d5060f  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  2f3899f75eaf856f0c371c8b763e0800a6cf00f5f2a48eb505f460671fcff94f  tests/test_checks.py

## LAW-4 — 2026-08-20 — repair the LAW-3 lexicon regex
direction: strengthen
why: the LAW-3 edit wrote doubled backslashes into the conclusive
lexicon, turning word boundaries into literals and silently disabling
the whole pattern — caught by the message-gate fixtures on the next
run (two fixture failures). Single-backslash boundaries restored;
pattern verified against fixtures. Also of record: the expanded
lexicon retroactively flagged the prior commit's title, which was
reworded by amendment (unpushed, untagged, so no history covenant was
broken); once a remote with protected history exists, amendments stop
being available and lexicon expansions must state their own effective
boundary.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  0acced4b658b5fe1fbeb4717ffdf9b4a0ff7c70ac5f2b5715ae27d00db4e3f6a  scripts/check_messages.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  130da351d6753ec097afd996a3234223bacb26f22eac55a9b5e6e6c7b9d5060f  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  2f3899f75eaf856f0c371c8b763e0800a6cf00f5f2a48eb505f460671fcff94f  tests/test_checks.py

## LAW-5 — 2026-08-20 — coverage tags and support tags disentangled
direction: neutral
why: rule conflict discovered by use — the coverage rule requires
tagging every touched claim, and the conclusive-language rule then
demanded every tag be supporting, so a commit touching a capped claim
could not use conclusive language even when a proven claim was also
tagged. Amended to: conclusive language requires at least one
supporting tag; coverage tags of capped or argued claims are
legitimate alongside. Unknown-tag detection now unconditional.
Fixture added for the mixed-tags case.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  44fc37dc5bb0ba7f70b2656fda26f004ec7993eb8253c21615fe55eecc76a144  scripts/check_messages.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  130da351d6753ec097afd996a3234223bacb26f22eac55a9b5e6e6c7b9d5060f  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  8b678a7e859617b0c466a7683efd750959c97d28c3c9b88d661749b7afbb8909  tests/test_checks.py

## LAW-6 — 2026-08-20 — preregistration becomes law
direction: strengthen
why: PREDICTIONS.md enacted (append-only, auto-covered by the
append-only gate) with check_predictions.py rostered: predictions
must precede the claims that cite them in commit ancestry, with the
protected remote supplying third-party attestation of the ordering;
post-enactment claims carrying numeric_match or checked-novel novelty
require one, as do post-enactment LITCHECKS entries. The ledger is
committed BEFORE the gate so the enactment commit is well-defined
and the gate's own commit is already governed. P-1..P-3 preregister
the three solve-candidates ahead of any derivation attempt.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  44fc37dc5bb0ba7f70b2656fda26f004ec7993eb8253c21615fe55eecc76a144  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  0680b9c18dc3818976e88e693d5ca910baeda9894fc4d4ef1e1678d4e5a33b3e  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  8c4511d8b609624ff413e0207ad5874121dce301f64f33e1d827c2638c0c1ce5  tests/test_checks.py

## LAW-7 — 2026-08-20 — the lexicon must not flag its own vocabulary
direction: neutral
why: first ceremony PR went red because \bnovel\b matches inside the
hyphenated field value "checked-novel" — the message gate flagging the
name of the novelty vocabulary itself. Hyphen guards added around
that token; fixtures cover both directions (checked-novel passes,
bare "novel" still blocks). Found by CI on the protected remote,
which is the enforcer doing precisely what it was installed to do.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  0680b9c18dc3818976e88e693d5ca910baeda9894fc4d4ef1e1678d4e5a33b3e  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  527b57b8752ce2131070c2a3dccdfe17e98a7a01a252ea3ed0ff5ecdbe480edf  tests/test_checks.py

## LAW-8 — 2026-08-20 — P-1 evidence generators enter the covered set
direction: strengthen
why: two new verification scripts join scripts/verify/ for the P-1
work (p1_depth6_pairs.py recomputing the depth-6 pair census;
p1_gradient_bc.py exhaustively checking the twisted-lattice gradient
XOR), and by LAW-3's rule every verify script is hash-pinned, so
their arrival requires this entry. Of record: the first version of
p1_gradient_bc.py tested a per-site winding family, disagreed with
the prose algebra, and was replaced by the per-cycle exhaustive
version - the disagreement corrected the prose, not the other way
around, and both versions remain in git history.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  0680b9c18dc3818976e88e693d5ca910baeda9894fc4d4ef1e1678d4e5a33b3e  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  667419f270af5760fc8771f45986257af72327326626076c1407c7f0ee21bd0c  scripts/verify/p1_gradient_bc.py
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  527b57b8752ce2131070c2a3dccdfe17e98a7a01a252ea3ed0ff5ecdbe480edf  tests/test_checks.py

## LAW-9 — 2026-08-21 — mean-frequency identity check enters the covered set
direction: strengthen
why: scripts/verify/p1_mean_frequency.py joins scripts/verify/ as the
fast evidence generator for claim klein-twisted-mean-frequency-identity
(the no-drive leg of the P-1 resolution); by LAW-3 every verify script
is hash-pinned. No gate logic changes. Of record: the identity the
script checks is textbook (LC-3) and is carried as a claim for the
chain of premises, not for credit.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  0680b9c18dc3818976e88e693d5ca910baeda9894fc4d4ef1e1678d4e5a33b3e  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  667419f270af5760fc8771f45986257af72327326626076c1407c7f0ee21bd0c  scripts/verify/p1_gradient_bc.py
  fa24ba6c1cb765e15ffdd8e485a6f5554f9bac2c316da0bc160722dc8b40d8c8  scripts/verify/p1_mean_frequency.py
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  527b57b8752ce2131070c2a3dccdfe17e98a7a01a252ea3ed0ff5ecdbe480edf  tests/test_checks.py

## LAW-10 — 2026-08-22 — refutation script for the half-shift sector error enters the covered set
direction: strengthen
why: scripts/verify/q_j_structure_sectors.py refutes
twisted-sector-complex-structure (a proven claim sealed in
link-001..004 whose verify script encoded the statement's own sector
misidentification) and verifies its replacement. By LAW-3 every
verify script is hash-pinned. Of record: the gate, the fixtures, and
the context-free adversarial audit all passed the wrong claim; what
caught it was deriving the null (the same arithmetic on a plain
antiperiodic circle). No gate logic changes; the lesson is filed in
topology_evaluation.md sec. 7a.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  1629443f3ffefce0aaf2ebeafa5f696fb5539b4658c323ef86963fd7b2b3e3b1  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  a6c0a5ece94b42524e6a328ba11528e145e0746ba567580e87e80042c5a9970d  scripts/check_verify_scripts.py
  0680b9c18dc3818976e88e693d5ca910baeda9894fc4d4ef1e1678d4e5a33b3e  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  667419f270af5760fc8771f45986257af72327326626076c1407c7f0ee21bd0c  scripts/verify/p1_gradient_bc.py
  fa24ba6c1cb765e15ffdd8e485a6f5554f9bac2c316da0bc160722dc8b40d8c8  scripts/verify/p1_mean_frequency.py
  4dc17a58fec3a3983b199a565b6f85b02c63a0d09961f554c36ab98e63403661  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  4d3b4216c23b82de6589c2b2185c46f3168c60f9526da841d409c6d72843a468  scripts/verify/q_j_structure_sectors.py
  527b57b8752ce2131070c2a3dccdfe17e98a7a01a252ea3ed0ff5ecdbe480edf  tests/test_checks.py

## LAW-11 — 2026-08-22 — null and falsifier required; falsifiers must fail
direction: strengthen
why: LC-5 / topology_evaluation.md sec. 7a: a proven claim passed the
gate, the fixtures, and the context-free audit because its verify
script restated the statement's sector labels instead of deriving
them (tautological verification). Mechanism: every proven claim
whose computation evidence cites a scripts/verify script must carry
(i) null_system: the simplest system in which the same computation
gives the same answer, naming what the claimed object does NOT
contribute; (ii) falsifier: a "<script> --mutant <name>" command that
mutates the claimed discriminator, which the verify gate runs and
REQUIRES to exit nonzero. A script for which no failing mutant can be
written is not a test. Fixtures added (red: missing fields; green:
present). Sweep of the four affected claims done in this entry:
saddle-node-passage-time (wrong-exponent), klein-twisted-gradient-xor
(and-not-xor), klein-twisted-mean-frequency-identity (phase-lag),
half-shift-squares-by-x-parity (bundle-decides). Of record: the first
phase-lag mutant used a half-turn same-sign lag, which is
indistinguishable from the antisymmetric form (pi = -pi), and the
gate rejected it as a passing falsifier - a too-weak mutant is the
known residual failure mode, and the rule caught its own first
instance. Field is named null_system because "null" is a YAML
keyword. Known gap, owed as LAW-12: the 18 compendium JS checks and
proven claims whose computation lives in compendium or
scripts/experiments are not yet under this rule.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  c2c271b6a2d03b966a44cbf3567c32f4fd7f9adcf61d95e7a32e391fe9a58587  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  1ab7498f5c873bda35296eecb5fe7ef01c200a0703887df0e9c8c08f9366f771  scripts/check_verify_scripts.py
  0680b9c18dc3818976e88e693d5ca910baeda9894fc4d4ef1e1678d4e5a33b3e  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  c42c77e5b668a5a8e0029d4d60d1ff7a8c6dddfcaeabfb33f6e546b3e9f3efd4  scripts/verify/p1_gradient_bc.py
  b6a275e86a0af49da1648700e3a041c083bac5014cb7697367d20201d8e3a431  scripts/verify/p1_mean_frequency.py
  a11f1ed7002239ac46d661b81428fc0ebbfd02f300c61fbaebcf70943aee388d  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  9573c69f65ee06679584e3fa67cb37bc4b2c7aba9e745eaa2d5da9ad01438646  scripts/verify/q_j_structure_sectors.py
  28dac92b5ffc812b5f8b6c60a268779f6d4a5b90a34b2c55e07772312a151bc4  tests/test_checks.py

## LAW-12 — 2026-08-22 — Kuramoto -> Einstein refutation script enters the covered set
direction: strengthen
why: scripts/verify/kuramoto_einstein_refutation.py is the
computational refutation of harmonics Proof Chain A, made a
first-class claim (einstein-from-kuramoto-chain-a, refuted) at the
owner's instruction. Carries a --mutant inertial mode so that check 1
is shown to discriminate parabolic from hyperbolic spreading. By
LAW-3 every verify script is hash-pinned. No gate logic changes. The
compendium/experiments falsifier gap named in LAW-11 remains owed.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  c2c271b6a2d03b966a44cbf3567c32f4fd7f9adcf61d95e7a32e391fe9a58587  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  1ab7498f5c873bda35296eecb5fe7ef01c200a0703887df0e9c8c08f9366f771  scripts/check_verify_scripts.py
  0680b9c18dc3818976e88e693d5ca910baeda9894fc4d4ef1e1678d4e5a33b3e  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  3a97e7a4513995b128f601764a4dd218320e5b0093c378a314dbd99965444133  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  c42c77e5b668a5a8e0029d4d60d1ff7a8c6dddfcaeabfb33f6e546b3e9f3efd4  scripts/verify/p1_gradient_bc.py
  b6a275e86a0af49da1648700e3a041c083bac5014cb7697367d20201d8e3a431  scripts/verify/p1_mean_frequency.py
  a11f1ed7002239ac46d661b81428fc0ebbfd02f300c61fbaebcf70943aee388d  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  9573c69f65ee06679584e3fa67cb37bc4b2c7aba9e745eaa2d5da9ad01438646  scripts/verify/q_j_structure_sectors.py
  28dac92b5ffc812b5f8b6c60a268779f6d4a5b90a34b2c55e07772312a151bc4  tests/test_checks.py

## LAW-13 — 2026-08-22 — the math catalog becomes a ninth gate
direction: strengthen
why: the night's reasoning used a dozen classical facts (Tusi couple,
cycloid cusp and tautochrone, the winding problem, Toomre's fluid
criterion, the Madelung quantum potential, the Gibbons-Hawking period,
Koenig's theorem and the CM torque, Koide Q and the 12/23 running
exponent, phi even, chain dispersion, the P-4 loading formula) as
prose. Each is now catalog/c*.py: exit 0 plainly, nonzero under
--mutant, run by scripts/check_catalog.py on every gate pass and
therefore in CI. Of record: the first run failed twice - c04's mutant
was written to pass (test bug, fixed) and c12 showed the run-5 note's
"within ~15%" to be an overstatement (27-37% near the Helmholtz
period; note corrected, fact scoped). Catalog entries are not
hash-pinned; the gate script is, via the check_*.py glob.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  361cee68968d5f14b4b2b5afc5d2918ddb59226bd5b8d4190f728b96642011f0  scripts/check_catalog.py
  c2c271b6a2d03b966a44cbf3567c32f4fd7f9adcf61d95e7a32e391fe9a58587  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  1ab7498f5c873bda35296eecb5fe7ef01c200a0703887df0e9c8c08f9366f771  scripts/check_verify_scripts.py
  28302350dc360f2408c0e97793fcb6a9b7bacd6b19f41383595139aa238daaac  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  3a97e7a4513995b128f601764a4dd218320e5b0093c378a314dbd99965444133  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  c42c77e5b668a5a8e0029d4d60d1ff7a8c6dddfcaeabfb33f6e546b3e9f3efd4  scripts/verify/p1_gradient_bc.py
  b6a275e86a0af49da1648700e3a041c083bac5014cb7697367d20201d8e3a431  scripts/verify/p1_mean_frequency.py
  a11f1ed7002239ac46d661b81428fc0ebbfd02f300c61fbaebcf70943aee388d  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  9573c69f65ee06679584e3fa67cb37bc4b2c7aba9e745eaa2d5da9ad01438646  scripts/verify/q_j_structure_sectors.py
  28dac92b5ffc812b5f8b6c60a268779f6d4a5b90a34b2c55e07772312a151bc4  tests/test_checks.py

## LAW-14 — 2026-08-22 — P-3 verify script enters the covered set
direction: strengthen
why: scripts/verify/iwasawa_one_stage.py is the computation leg of
sl2r-connected-subgroups and the refutation leg of
iwasawa-one-stage-original (P-3, R-2); written by a context-free
auditor, reviewed line by line, carries a --mutant that asserts the
refuted statement and fails. Hash-pinned per LAW-3. No gate changes.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  361cee68968d5f14b4b2b5afc5d2918ddb59226bd5b8d4190f728b96642011f0  scripts/check_catalog.py
  c2c271b6a2d03b966a44cbf3567c32f4fd7f9adcf61d95e7a32e391fe9a58587  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  1ab7498f5c873bda35296eecb5fe7ef01c200a0703887df0e9c8c08f9366f771  scripts/check_verify_scripts.py
  28302350dc360f2408c0e97793fcb6a9b7bacd6b19f41383595139aa238daaac  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  8041be6fba084ea49040746294644ab559d31901040f355820ea16feacfa6463  scripts/verify/iwasawa_one_stage.py
  3a97e7a4513995b128f601764a4dd218320e5b0093c378a314dbd99965444133  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  c42c77e5b668a5a8e0029d4d60d1ff7a8c6dddfcaeabfb33f6e546b3e9f3efd4  scripts/verify/p1_gradient_bc.py
  b6a275e86a0af49da1648700e3a041c083bac5014cb7697367d20201d8e3a431  scripts/verify/p1_mean_frequency.py
  a11f1ed7002239ac46d661b81428fc0ebbfd02f300c61fbaebcf70943aee388d  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  9573c69f65ee06679584e3fa67cb37bc4b2c7aba9e745eaa2d5da9ad01438646  scripts/verify/q_j_structure_sectors.py
  28dac92b5ffc812b5f8b6c60a268779f6d4a5b90a34b2c55e07772312a151bc4  tests/test_checks.py

## LAW-15 — 2026-08-22 — refutation script corrected after adversarial audit
direction: strengthen
why: a context-free audit of einstein-from-kuramoto-chain-a found
the verdict sound and three supports defective: check 3 used
delta + grad grad where the source defines delta - grad grad
(Minkowski-graph Gauss formula now used); check 2 used identical
frequencies, whose attractor is in-phase (r = 1 everywhere), so it
could not test a varying coherence (now heterogeneous frequencies,
coherence 0.805-1.000, residual 4e-12); check 1's stated principle
(characteristic order invariant under coarse-graining) was false and
is replaced by the gradient-flow/Lyapunov argument, the exponent
kept as a necessary-condition signature. Script re-pinned. Of
record: the gate could not have caught any of these - all three
were the evidence testing the wrong object while passing - which is
the failure mode LAW-11 addresses and which the audit practice
exists for.
hashes:
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  361cee68968d5f14b4b2b5afc5d2918ddb59226bd5b8d4190f728b96642011f0  scripts/check_catalog.py
  c2c271b6a2d03b966a44cbf3567c32f4fd7f9adcf61d95e7a32e391fe9a58587  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  9eb8db6c46e6ab1149c8db33087d5282f4cd70a97663654ddbc7ab285a038343  scripts/check_lawchanges.py
  3064529f88ec4d4ad95532e0724ad28e81a8cda66ddbde230792e0f613f40eea  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  1ab7498f5c873bda35296eecb5fe7ef01c200a0703887df0e9c8c08f9366f771  scripts/check_verify_scripts.py
  28302350dc360f2408c0e97793fcb6a9b7bacd6b19f41383595139aa238daaac  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  8041be6fba084ea49040746294644ab559d31901040f355820ea16feacfa6463  scripts/verify/iwasawa_one_stage.py
  f742e81930c1b1419825d28c0bb42e3ed940d119921ed035642d29ac66364b75  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  c42c77e5b668a5a8e0029d4d60d1ff7a8c6dddfcaeabfb33f6e546b3e9f3efd4  scripts/verify/p1_gradient_bc.py
  b6a275e86a0af49da1648700e3a041c083bac5014cb7697367d20201d8e3a431  scripts/verify/p1_mean_frequency.py
  a11f1ed7002239ac46d661b81428fc0ebbfd02f300c61fbaebcf70943aee388d  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  9573c69f65ee06679584e3fa67cb37bc4b2c7aba9e745eaa2d5da9ad01438646  scripts/verify/q_j_structure_sectors.py
  28dac92b5ffc812b5f8b6c60a268779f6d4a5b90a34b2c55e07772312a151bc4  tests/test_checks.py

## LAW-16 — 2026-08-22 — gate bypasses closed after adversarial audit
direction: strengthen
why: a context-free audit of LAW-11/13 found, with demonstrations:
(1) the falsifier runner regexed claims/*.yml and, on a single-quoted
or block-scalar value, ran a nonexistent file whose rc 2 counted as
"fails as required" - the repo's own green fixture used the evasion
form; (2) any crash, any file, or another claim's script satisfied
"nonzero exit"; (3) LAW-11 applied to proven only, while verified
settles premises with equal weight; (4) VERIFY_REF missed
scripts//verify/x.py while G3 resolved it; (5) the message gate's
diff-tree was blind to merge commits; (6) catalog/_common.py - the
harness that defines "self-testing" - and c12's data were unpinned;
a raising mutant branch counted as failing. Fixes: falsifiers are
read from parsed YAML; a falsifier counts only if it is one of the
claim's own cited verify scripts, runs, exits 1 (not 2), prints a
FAIL line, and leaves no traceback; verify scripts exit 2 on an
unknown mutant name; the rule covers proven and verified; evidence
paths are normalised; diff-tree runs with -m --first-parent; the
catalog harness requires the MUTANT FAIL sentinel and handles a
missing docstring as a failure; catalog/_common.py joins the covered
set; data-reading entries pin their inputs by sha256. Entries that
asserted several facts under one mutant were split (c08 -> c08/c14/
c15; c09 -> c09/c16); c04 asserts the 1/t law; c12 rescoped (25%,
16 rows); c13 records the mu_d dependence the formula cannot see.
Fixtures added for borrowed falsifier, verified-in-scope, and path
normalisation. Of record: the P-3 mutant was renamed borel-abelian
to satisfy the named-mutant rule.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  bf002174d2acae7f6ee1e20cb85c9c1079893d54a4761c593af09a960e774bb2  scripts/check_catalog.py
  25565a386761e84d5cea6f708c8d9dbf09f23525c4d204a9be6082df41b43b22  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  1a1610d4c0238d5e6c04b2e59fc68fb413aa52fb142fa3788a794b21f2518ee8  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  28302350dc360f2408c0e97793fcb6a9b7bacd6b19f41383595139aa238daaac  scripts/run_all.py
  dcf9e6438a304e9e1812dadb8745f40a9e27767e01601e3df23012240b6ba6d2  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  e58ecaca687124efa87ee52c64f449dbd20fbb2371eee445f6dcf0b8afd8ce8f  tests/test_checks.py

## LAW-17 — 2026-08-22 — the compendium under the falsifier rule (the LAW-12-owed gap)
direction: strengthen
why: a context-free audit of the 18 compendium checks found none
mathematically wrong and seven of 31 mutants surviving: C10's lock
assertion short-circuited on the statement's own threshold, C5
counted orbits by the statement's formula, C17 verified five
functions built to satisfy the claim, C12 and C9 asserted numbers
but not the law (divergence rate; absolute exponent), C14 labelled
the orientation character instead of computing it, C16 never tested
tau^2 = id, and the harness did not assert the check count. Fixes:
register(id, fn, mutants) with a KNOBS object every check reads; the
headless harness runs each named mutant and requires failure,
requires at least one mutant per check, seeds Math.random, and
requires the registered id set to equal the page's data-verify
buttons; C10 integrates to lock at an interior point, C5 pairs
fractions directly and asserts 15 is never attained, C17 unwraps
random BC-respecting fields and integrates the stability swap, C12
asserts the per-decade increment, C9 asserts the absolute K^q
scaling, C14 computes chi from det of the deck elements' linear
parts, C16 asserts tau^2 = id. 22 mutants, all fail. check_claims
now rejects a free-text "compendium C<n>" reference naming no
registered check. compendium/index.html itself stays unpinned, as
catalog entries do (LAW-13), because its checks are now self-testing
through the pinned harness; the tradeoff is recorded here.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  bf002174d2acae7f6ee1e20cb85c9c1079893d54a4761c593af09a960e774bb2  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  1a1610d4c0238d5e6c04b2e59fc68fb413aa52fb142fa3788a794b21f2518ee8  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  28302350dc360f2408c0e97793fcb6a9b7bacd6b19f41383595139aa238daaac  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  f3a31f6bd498b34969dc720fea7e7b00e547552338d6375be3c01f62a2b7213c  tests/test_checks.py

## LAW-18 — 2026-08-23 — the curriculum notebooks become a tenth gate
direction: strengthen
why: the temporal-first curriculum (T0-T6 + capstone) now exists as
eight stdlib-only Jupyter notebooks built by an agent from the notes
and the catalog, each module ending on a visibly failing mutant.
scripts/check_notebooks.py (covered by the check_*.py glob) runs
scripts/nb_run.py - every code cell in order, fresh namespace,
nonzero on any exception - on every gate pass. A notebook that does
not run is prose; the curriculum is evidence-grade only while it
executes. The notebooks and nb_run.py are not hash-pinned (same
tradeoff as catalog entries, LAW-13); the gate script is. Of record
from the build: the P-4 note's "4.3 values are grid coincidences"
was wrong (corrected in the note); for q >= 3 the sine-map tongue
centre shifts by O(K^2), so widths bisected from p/q overstate by
~4x (the compendium's C9 brackets already avoid this; the T1 notebook
records it).
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  bf002174d2acae7f6ee1e20cb85c9c1079893d54a4761c593af09a960e774bb2  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  1a1610d4c0238d5e6c04b2e59fc68fb413aa52fb142fa3788a794b21f2518ee8  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  b9295a59107726bc6be52dbc876b4843a08e083f0835c51032d96ea5e5262ebb  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  f3a31f6bd498b34969dc720fea7e7b00e547552338d6375be3c01f62a2b7213c  tests/test_checks.py

## LAW-19 — 2026-08-23 — P-6 exhaustive certificate enters the covered set
direction: strengthen
why: scripts/verify/p6_circulant_small.py is the computation leg of
circulant-twisted-max-density-small (verified; P-6, R-4): an
exhaustive enumeration over all symmetric connection sets of C_n(S),
n <= 20, with the maximiser re-checked from the Jacobian, 0.1 s, and
a named mutant (claims-two-thirds) that fails. Hash-pinned per
LAW-3. First task run under AGENTS.md in its own worktree; the
registration (PR #38) precedes the computation in the history.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  bf002174d2acae7f6ee1e20cb85c9c1079893d54a4761c593af09a960e774bb2  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  1a1610d4c0238d5e6c04b2e59fc68fb413aa52fb142fa3788a794b21f2518ee8  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  b9295a59107726bc6be52dbc876b4843a08e083f0835c51032d96ea5e5262ebb  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  f3a31f6bd498b34969dc720fea7e7b00e547552338d6375be3c01f62a2b7213c  tests/test_checks.py

## LAW-20 — 2026-08-23 — every gate rule is a spec line; every note declares its load
direction: strengthen
why: (1) the ad-hoc fixture file is replaced by tests/spec/*.spec, a
controlled grammar with one rule per line (GIVEN fixture WHEN gate
RUNS THEN ACCEPT | REJECT MENTIONING token | EQUALS json) executed by
tests/run_spec.py; all 41 prior fixtures migrate as 49 rules and the
specs are hash-pinned as the law's tests. A rule naming a gate that
does not exist fails, so gates are written test-first: the notes
spec (6 rules) was committed red before scripts/check_notes.py
existed, then implemented to green - the commit order is the record.
(2) The notes gate: every notes/*.md opens with <!-- commentary -->
(no load; may not issue proven/verified/refuted verdicts) or
<!-- evidence: paths --> naming existing executable artifacts
(.py/.js/.json/.ipynb/.yml, or compendium/notebooks html); prose is
not evidence. All 16 notes declared: 6 commentary, 10 evidence.
check_catalog.py and check_notes.py honour PROS_ROOT so the spec gate
can run them on fixture trees. Gates are now eleven.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-21 — 2026-08-24 — the P-13 falsifier: verification by live miniature reimplementation
direction: strengthen
why: adds scripts/verify/p13_acoustic_metric.py, the falsifier for the
two P-13 claims. The intake gate's derivation rules forced its shape:
"verified" requires reimplementation, so the script integrates its own
500-site chains live (different size, pulse, profiles, and a different
arrival observable from the experiment - front threshold crossing
rather than peak time, because the peak of a reshaping envelope drifts
and lobe-hops on short baselines; no access to p13_results.json),
re-runs the symbolic layer EQ1-EQ8, and re-derives both scattering
coefficients against the impedance law. Two mutants: shuffled-profile
(scores live arrivals against a block-shuffled substrate's eikonal;
the arrangement of local delays is what the arrival curve reads) and
c-ratio-reflection (predicts scattering from the metric ratio; wrong
in both directions). No gate semantics change; the hash table below
re-pins all covered files with the new verify script included.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec
## LAW-22 — 2026-08-24 — the P-11 falsifier pinned
direction: strengthen
why: adds scripts/verify/p11_spectral_metric.py, the falsifier for
connes-distance-representation-dichotomy. Independent
reimplementation: rebuilds the Gram matrix, the exact witnesses
(2/sqrt(3) neighbour, sqrt(2) far), the diagonal and minor caps, and
the circulant in-degree aggregation from scratch, reading nothing
from the results file. Mutants: hop-metric (asserts the vertex-only
metric grows with hop; saturation kills it) and tent-everywhere
(asserts the hop tent stays feasible on the dense circulant; the
sqrt(in-degree) norm kills it). No gate semantics change; the table
below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec
## LAW-23 — 2026-08-24 — the P-10 falsifier pinned
direction: strengthen
why: adds scripts/verify/p10_order_dimension.py, the falsifier for
order-and-count-read-dimension (written in the p10 worktree as a
proposed script per AGENTS.md rule 3, reviewed and promoted by the
integrator). Independent reimplementation: re-derives the d = 2
related fraction by exact rational integration, checks the Gamma
form at d = 1..4, and runs its own fixed-seed d = 4 sprinkle
(N = 1024, M = 10) with an acceptance-rate check against pi/24 -
no access to p10_results.json. Mutant shuffled-order permutes the
time coordinate; the derived scrambled null d* = 4.230 pushes the
mean past the 0.15 gate. The d = 2 shuffle symmetry (f stays 1/2
exactly) is recorded in the claim as a falsifier limit. No gate
semantics change; the table below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec
## LAW-24 — 2026-08-24 — the P-14 falsifier pinned
direction: strengthen
why: adds scripts/verify/p14_isometric_spectra.py, the falsifier for
isometric-not-isospectral-chain. Independent reimplementation: both
chains rebuilt at a grid the experiment never used (n = 749), the
Sturm eigensolver re-validated inline against the uniform chain's
closed form, seminorm isometry and the spectral split re-derived
live with no access to the results file. Mutants: isospectral
(asserts the spectra coincide; the resolved split kills it) and
z-blind-seminorm (asserts the commutator distance sees the
impedance; the O(1/n) split kills it). The registered k-resolved
clause fired its mind-change condition and is NOT covered by the
claim or this falsifier (R-10). No gate semantics change; the table
below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec
## LAW-25 — 2026-08-24 — the P-15 falsifier pinned
direction: strengthen
why: adds scripts/verify/p15_spectral_dimension.py, the falsifier for
spectral-dimension-instrument. Independent reimplementation: the line
anchor re-derived by the Bessel continued-fraction route, the dense-
circulant crossover and the two-mode window decay by fresh eigen-sums,
and the chain trace drift at a grid the experiment never used
(n = 749), reading nothing from the results file. Mutants:
past-window (reports d_s beyond the mixing time as a dimension; the
two-mode decay kills it) and squared-generator (walks under L^2,
whose line dimension is 1/2; the line anchor kills it - the first
draft's deg-minus-adjacency mutant was discarded because on a cycle
it reconstructs the Laplacian exactly). No gate semantics change;
the table below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec
## LAW-26 — 2026-08-24 — the P-17 falsifier pinned
direction: strengthen
why: adds scripts/verify/p17_bell_ladder.py, the falsifier for
bell-ladder-priced. Independent reimplementation: the local ceiling
re-enumerated, the quantum ceiling re-derived by direct power
iteration on the CHSH operator, the information-causality ladder
recomputed from its closed form, and all three machines re-run as
fresh short seeded simulations, reading nothing from the results
file. Mutants: local-exceeds-two (asserts a deterministic local
strategy beats 2; the exhaustive enumeration kills it) and
ic-allows-pr (asserts information causality tolerates the PR box;
f(1, 12) = 4096 kills it). No gate semantics change; the table
below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-27 — 2026-08-25 — the P-18 falsifier pinned
direction: strengthen
why: adds scripts/verify/p18_smooth_retest.py, the falsifier for
c2-profile-recovers-first-order-shifts. Independent
reimplementation: the first-order shifts re-derived by the script's
own quadrature from V = c'^2/4 - c c''/2, all four chains rebuilt
at grid sizes the experiment never used (n = 599, 1199, Richardson),
reading nothing from the results file; the linear control's failure
must reproduce live. Mutants: c1-corners-benign (asserts the linear
pair also passes the 0.1 x Vbar bar; it fails it at 2.9) and
wrong-sign-potential (predicts with V = c'^2/4 + c c''/2; the RMS
bar and the k = 1 residual kill it). No gate semantics change; the
table below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-28 — 2026-08-26 — the P-21 falsifier pinned
direction: strengthen
why: adds scripts/verify/p21_hardy_maximum.py, the falsifier for
hardy-maximum-is-phi-fifth. Independent reimplementation: the
Hardy constraint elimination and the reduced closed form re-derived
against directly computed amplitudes, the maximum reproduced in its
own exact Q(sqrt5) field arithmetic, and a fresh 40-start seeded
search (seed 20260827, different from the experiment's) rerun and
polished live, reading nothing from the registration or results
files. Mutants: maximally-entangled-best (asserts the c = s slice
reaches phi^5/2; it tops out at ~1e-32) and flat-landscape (asserts
the maximum is degenerate in the Schmidt angle; p_env moves by
1.3e-2 at theta* +/- 0.1 against a 1e-6 bar). No gate semantics
change; the table below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-29 — 2026-08-26 — the P-22/P-23 falsifier pinned
direction: strengthen
why: adds scripts/verify/p22_locking_skeleton.py, the shared
falsifier for two-photon-locking-z2-skeleton and
locking-protects-mod-pi-observable. Independent reimplementation:
own Euler-Maruyama integrator with fresh seeds, own log-domain
mobility quadrature, own Bessel continued fraction; the beat band
carries the winding-quantization term 2 pi/T that R-17 showed the
registration missed. Mutants: single-phase-lock (asserts one locked
phase per period; the pi-separated bistable pair kills it),
tongue-squared (asserts an eps^2 lock range; the locked (0.3, 0.5)
cell kills it), bessel-blind (asserts the mod-pi equilibrium is
D-independent; the Bessel ratio's motion 0.6356 -> 0.8308 kills
it). No gate semantics change; the table below re-pins all covered
files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  2218e889bc78f33c27e7452b071e6db1e8795eca60698c8d3d5a98177644f287  scripts/verify/p22_locking_skeleton.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-30 — 2026-08-26 — the P-24 falsifier pinned
direction: strengthen
why: adds scripts/verify/p24_memory_hierarchy.py, the falsifier for
memory-hierarchy-of-substrates. Independent reimplementation: own
Langevin integrator on a fresh (N, D) cell the experiment never ran,
own closed-form barrier and saddle stationarity check, own Hessians
and Jacobi eigensolver for the Langer prefactor, fresh rung-1
ensemble. Mutants: extensive-protection (asserts Delta_E(64) >=
8 Delta_E(8); the closed form gives 3.85 and saturates at 2K) and
barrier-free (asserts the escape rate is D-independent; it moves
0.87 nat between D = 0.2 and 0.3 against a derived 0.77). No gate
semantics change; the table below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  2218e889bc78f33c27e7452b071e6db1e8795eca60698c8d3d5a98177644f287  scripts/verify/p22_locking_skeleton.py
  95295290411be46b98100bb238f9924259fefb60179e4e52168a88894eace4bb  scripts/verify/p24_memory_hierarchy.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-31 — 2026-08-27 — the P-7 falsifier pinned
direction: strengthen
why: adds scripts/verify/p7_golden_flux.py, the falsifier for
harper-golden-ladder. Independent reimplementation: own Bloch
matrices, own Jacobi eigensolver, own Catalan series, on the short
ladder to q = 21 with the same anchor closed forms. Mutants:
bandwidth-constant (asserts S(21) > 0.8 S(5); it contracts about
fourfold) and silver-clock (asserts the ladder clock is
ln(1 + sqrt 2) = 0.8814; the measured clock is golden, 0.4982 on
the short ladder). No gate semantics change; the table below
re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  2218e889bc78f33c27e7452b071e6db1e8795eca60698c8d3d5a98177644f287  scripts/verify/p22_locking_skeleton.py
  95295290411be46b98100bb238f9924259fefb60179e4e52168a88894eace4bb  scripts/verify/p24_memory_hierarchy.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-32 — 2026-08-27 — the P-19 falsifier pinned (renumbered at rebase; main took LAW-28..31)
direction: strengthen
why: adds scripts/verify/p19_alf_lattice.py, the falsifier for
alf-period-lattice (the PR 60 content rebuilt as P-19). Independent
miniature at half the sample rate with a different observable
(bridge-waveform autocorrelation) and per-beta force selected only
by lock quality over a band containing 2.0; mutants exact-doubling
and beta-independent, both red. Entry written by the integrator
after rebase per the .gitattributes rule; the number moved from the
branch's provisional LAW-28 because main allocated 28-31 while the
PR floated. No gate semantics change; the table below re-pins all
covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  2218e889bc78f33c27e7452b071e6db1e8795eca60698c8d3d5a98177644f287  scripts/verify/p22_locking_skeleton.py
  95295290411be46b98100bb238f9924259fefb60179e4e52168a88894eace4bb  scripts/verify/p24_memory_hierarchy.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-33 — 2026-08-27 — the P-16 falsifier pinned
direction: strengthen
why: adds scripts/verify/p16_two_dimensions.py, the falsifier for
causal-set-spectral-dimensions-diverge. Independent live
reimplementation: fresh sprinkling with its own bitset links, own
Jacobi eigensolver, own E1 and source-operator closed form, own
link quadrature. Mutants: walk-reduces (asserts the walk shows
dimensional reduction; the sprinkling's superdiffusive peak kills
it) and printed-formula-fine (asserts BBMM's printed eq. 15 has no
IR defect; the derived-and-measured 4/sqrt(pi) - 2 kills it - the
LC-15 audit finding lives in the falsifier). No gate semantics
change; the table below re-pins all covered files.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  ab28484233b07d3741fa29753e4cc14a9095532b2f0aa7f5e9dfc0ce738fa212  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  1d57e73be3a958caa2398f84964580f40472d5978a6de39f5dfdc4c15a6118ce  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  2218e889bc78f33c27e7452b071e6db1e8795eca60698c8d3d5a98177644f287  scripts/verify/p22_locking_skeleton.py
  95295290411be46b98100bb238f9924259fefb60179e4e52168a88894eace4bb  scripts/verify/p24_memory_hierarchy.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-34 — 2026-08-27 — kernels/ under the law gate
direction: strengthen
why: the re-implemented simulation kernels move into a governed
kernels/ layer (eig, sde, quad, specfun, causet, minimize,
instruments, figpage, project, pmap - extracted from landed
artifacts under a two-artifact admission rule, each with derive-layer
--selftest anchors), and the three newest falsifiers
(p16_two_dimensions.py, p24_memory_hierarchy.py,
p22_locking_skeleton.py) now import them: kernels imported by
falsifiers must be pinned, or the evidence layer could change
silently one import away. check_lawchanges.py's covered-file
discovery therefore gains kernels/*.py (the one gate-semantics
change of this thread, in this entry's own hash). The ported
falsifiers produce byte-identical PASS lines and all seven mutants
still run-and-fail; the three newest plot scripts (p7/p16/p24)
regenerate their committed HTML byte-for-byte from the same kernels.
Older experiment files deliberately keep their inline copies -
declared residual duplication, to be retired only behind their own
verify contracts. The table below re-pins all covered files
including the new kernels/.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-35 — 2026-08-28 — the P-26 falsifier pinned
direction: strengthen
why: scripts/verify/p26_everpresent_scorecard.py is new gate-covered
evidence (the everpresent-Lambda scorecard's live reimplementation:
its own Simpson integrator, explicit block chi2, grid fit, marcher,
analytic-volume amplitude route, two discriminating mutants - the
eds-threshold mutant being R-23's recorded design error kept as a
weapon). New covered files require a fresh pin of the full covered
set; nothing else changes and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-36 — 2026-08-28 — the P-27 falsifier pinned
direction: strengthen
why: scripts/verify/p27_squeeze_windows.py is new gate-covered
evidence (the squeeze-window live reimplementation: an independent
random-rescaling route to dimensional consistency, its own bound
arithmetic, the three registered sign flips reproduced; mutants
lambda-flip and flip-blind). New covered files require a fresh pin
of the full covered set; nothing else changes and no gate
semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-37 — 2026-08-28 — the P-28 falsifier pinned
direction: strengthen
why: scripts/verify/p28_gap_integers.py is new gate-covered
evidence (the gap-integer live reimplementation: characteristic-
polynomial bisection spectra, brute-force Diophantine labels, its
own Streda band count; mutants shifted-window and parity-blind,
with the non-discriminating skip-rung mutant discarded and the
reason recorded in the notes). New covered files require a fresh
pin of the full covered set; nothing else changes and no gate
semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-38 — 2026-08-28 — the P-29 falsifier pinned
direction: strengthen
why: scripts/verify/p29_farey_bridge.py is new gate-covered
evidence (the Farey-bridge live reimplementation: rotation-number
staircase tongue widths, char-poly bandwidths, its own mediant
arithmetic; mutants harmonic-blind - the premise kill switch - and
mediant-shift, the second mediant, after two discarded designs
whose failure reasons are recorded in the notes). New covered
files require a fresh pin of the full covered set; nothing else
changes and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-39 — 2026-08-28 — the P-30 falsifier pinned
direction: strengthen
why: scripts/verify/p30_order_ladder.py is new gate-covered
evidence (the order-ladder live reimplementation: a wider
four-letter-message causal enumeration, its own trace evaluation
of the OCB process, density-matrix switch evolution; mutants
two-way and loop-blind). New covered files require a fresh pin of
the full covered set; nothing else changes and no gate semantics
move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-40 — 2026-08-28 — the P-31 falsifier pinned
direction: strengthen
why: scripts/verify/p31_second_bridge.py is new gate-covered
evidence (the second-bridge live reimplementation: 60-digit
Decimal orbit closure, its own Fraction divergence BFS; mutants
mediant-lands and open-edge). New covered files require a fresh
pin of the full covered set; nothing else changes and no gate
semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-41 — 2026-08-28 — the P-32/P-33 falsifier pinned
direction: strengthen
why: scripts/verify/p32_parity_factorial.py is new gate-covered
evidence (its own ring integrator and plateau search; the
telescoping identity at 1e-14; the K = 1.2 class hierarchy; the
P-9 pin; mutants telescope-blind and class-blind). New covered
files require a fresh pin of the full covered set; nothing else
changes and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-42 — 2026-08-28 — the P-34 falsifier pinned
direction: strengthen
why: scripts/verify/p34_horizon_census.py is new gate-covered
evidence (direct Planck-unit route, its own interval-union
coverage, the census spot set; mutants census-of-one - the
look-elsewhere charge is load-bearing - and mu-wrong). New covered
files require a fresh pin of the full covered set; nothing else
changes and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-43 — 2026-08-29 — the P-36 falsifier pinned
direction: strengthen
why: scripts/verify/p36_free_ring.py is new gate-covered evidence
(its own fold solver and velocity-Verlet integrator; checks the
closed form 2N/(N-1), the fold ratio, both slip channels, the
half-integer lattice, and the threshold separation; mutants
channel-blind - the load-bearing dichotomy - and naive-budget,
the derivation error corrected before registration). New covered
files require a fresh pin of the full covered set; nothing else
changes and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  07915db9ebdc1a7264d2fdb8d8778d0505f65cea98a6af0f4673d54de7a61bcd  scripts/verify/p36_free_ring.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-44 — 2026-08-30 — the P-37 falsifier pinned
direction: strengthen
why: scripts/verify/p37_price_of_bit.py is new gate-covered
evidence (its own Langevin integrator with rejection-sampled
equilibrium starts, its own floor arithmetic, a stricter fixed-cut
W_2; mutants half-work - the Jarzynski identity is load-bearing -
and entropy-blind - the H(p) refund is load-bearing). New covered
files require a fresh pin of the full covered set; nothing else
changes and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  07915db9ebdc1a7264d2fdb8d8778d0505f65cea98a6af0f4673d54de7a61bcd  scripts/verify/p36_free_ring.py
  7aff5efba156c54133fb0218c9d8bed61e89d404701d73a8fd3a2f33b388c30a  scripts/verify/p37_price_of_bit.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-45 — 2026-09-01 — the P-38 falsifier pinned
direction: strengthen
why: scripts/verify/p38_switch_bridge.py is new gate-covered
evidence (the X-basis branch-expansion route: revealed-sign
bookkeeping on the GHZ branches, conditioned Bell-pair Y
parities, a fresh enumeration encoding; mutants ceiling-blind -
the exhaustion is load-bearing - and wiring-blind - the
coherence is load-bearing). New covered files require a fresh
pin of the full covered set; nothing else changes and no gate
semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  07915db9ebdc1a7264d2fdb8d8778d0505f65cea98a6af0f4673d54de7a61bcd  scripts/verify/p36_free_ring.py
  7aff5efba156c54133fb0218c9d8bed61e89d404701d73a8fd3a2f33b388c30a  scripts/verify/p37_price_of_bit.py
  beaa8b467ab3b3cf6b150dcee9369e9f4a86be13d8778bb56736ac5506a14054  scripts/verify/p38_switch_bridge.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-46 — 2026-09-01 — the P-39 falsifier pinned
direction: strengthen
why: scripts/verify/p39_alpha_family.py is new gate-covered
evidence (Pauli-orthogonality route with no matrices, its own
causal enumeration encoding, the analytic optimal angle; mutants
symmetric-blind - the alpha-dependence of the optimal process is
load-bearing - and square-blind - the quantum-causal separation
is load-bearing). New covered files require a fresh pin of the
full covered set; nothing else changes and no gate semantics
move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  07915db9ebdc1a7264d2fdb8d8778d0505f65cea98a6af0f4673d54de7a61bcd  scripts/verify/p36_free_ring.py
  7aff5efba156c54133fb0218c9d8bed61e89d404701d73a8fd3a2f33b388c30a  scripts/verify/p37_price_of_bit.py
  beaa8b467ab3b3cf6b150dcee9369e9f4a86be13d8778bb56736ac5506a14054  scripts/verify/p38_switch_bridge.py
  98db9a8461680d0bc552c00844c04ca8081f87ff01d4a4f8a113a4bbd73685e1  scripts/verify/p39_alpha_family.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-47 — 2026-09-01 — the P-41 falsifier pinned
direction: strengthen
why: scripts/verify/p41_gap_openings.py is new gate-covered
evidence (its own cyclic-Jacobi eigensolver against the kernel's
Householder+QL, extended-gcd label arithmetic, the trace
recursion; mutants label-blind - the modular arithmetic is
load-bearing - and scan-blind - P-40's fired detector kept as the
counterexample). New covered files require a fresh pin of the
full covered set; nothing else changes and no gate semantics
move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  07915db9ebdc1a7264d2fdb8d8778d0505f65cea98a6af0f4673d54de7a61bcd  scripts/verify/p36_free_ring.py
  7aff5efba156c54133fb0218c9d8bed61e89d404701d73a8fd3a2f33b388c30a  scripts/verify/p37_price_of_bit.py
  beaa8b467ab3b3cf6b150dcee9369e9f4a86be13d8778bb56736ac5506a14054  scripts/verify/p38_switch_bridge.py
  98db9a8461680d0bc552c00844c04ca8081f87ff01d4a4f8a113a4bbd73685e1  scripts/verify/p39_alpha_family.py
  84f8fd170e131a9741e116672d401db6a328bf52e624bd0f50cb978a66a42435  scripts/verify/p41_gap_openings.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-48 — 2026-09-01 — the P-42 falsifier pinned
direction: strengthen
why: scripts/verify/p42_same_data.py is new gate-covered evidence
(stabilizer-group arithmetic for the GHZ side, the X-basis branch
route for the switch side, GF(2) elimination, the ring section by
direct construction; mutants coin-blind - exact fairness of the
free coins is load-bearing - and section-blind - the
global-section contrast is load-bearing). New covered files
require a fresh pin of the full covered set; nothing else changes
and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  07915db9ebdc1a7264d2fdb8d8778d0505f65cea98a6af0f4673d54de7a61bcd  scripts/verify/p36_free_ring.py
  7aff5efba156c54133fb0218c9d8bed61e89d404701d73a8fd3a2f33b388c30a  scripts/verify/p37_price_of_bit.py
  beaa8b467ab3b3cf6b150dcee9369e9f4a86be13d8778bb56736ac5506a14054  scripts/verify/p38_switch_bridge.py
  98db9a8461680d0bc552c00844c04ca8081f87ff01d4a4f8a113a4bbd73685e1  scripts/verify/p39_alpha_family.py
  84f8fd170e131a9741e116672d401db6a328bf52e624bd0f50cb978a66a42435  scripts/verify/p41_gap_openings.py
  ff7d158cc90ea0cabcc6fbfc5f2529eff1078750ff8bd53e7d4db037b10d6ae8  scripts/verify/p42_same_data.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec

## LAW-49 — 2026-09-01 — the P-43 falsifier pinned
direction: strengthen
why: scripts/verify/p43_shadow_body.py is new gate-covered
evidence (own tuple-table strategy encodings, reversed-pivot
Fraction elimination, exact shadow extremes, the constructive
circle settings; mutants body-blind - the invariant mismatch is
load-bearing - and shadow-blind - the on-circle tangency is
load-bearing). New covered files require a fresh pin of the full
covered set; nothing else changes and no gate semantics move.
hashes:
  1b8ab111bb43eb17a25a822468e8f978c4883f67b9ea3b15bc5b85d0b499f7b4  catalog/_common.py
  fb7ed34eb62f641c0a93a98fe0e8a484b61cab8c38a0a76e8c61ea6246468ba9  kernels/__init__.py
  02f3a2118b28aeaea0ead99be1cfde6ecd1f6ebdbf08e61cb6c6dc342db02a36  kernels/causet.py
  a5834396362f91141d9604bb5908fdcb8c4908a004cea8aa7ac5115a6ecd14bd  kernels/eig.py
  54ee1d5ed95507b48e52be766d9292b43a0440a171d3aea9e36a62b6fbf6a283  kernels/figpage.py
  c524fe17170bee951b78465c602e2dfd47eb958aa724d726bb610e77bb751187  kernels/instruments.py
  88ba79a2a596a40c6cf3a946af64fa1dfc5dcc298637e5f22c71c7d6ca5913b2  kernels/minimize.py
  9179669510f8103bdeaaf754d5aac7351467dbd66e5973ddc158b35f10b10a57  kernels/pmap.py
  2239753e4186ef144a9c7f0aa65c289f6981354d85fdfb92e4b026f4e4595ac6  kernels/project.py
  4085e67db5bf48b827e3cb8bb3e1a4534d903eb8d85ffe2d1d9b56accb640ef7  kernels/quad.py
  5c8e97f26ed9c52efc2fe7ff6a342b2e50f25a5d0fb80c66d7b6575f5e19742f  kernels/sde.py
  510830e21491c9064e1b20400eb5507c55e9c4a7f4a34e977a31f7801d76766f  kernels/specfun.py
  f66449b5076b3d3a49c80551f0881d8bf26f2ac4022f143e7a00be88ab0114e5  scripts/check_append_only.py
  7e0dc75ccf248f9c85f66b4be979ac44136c15890c152abb59a1edeb7292ca53  scripts/check_catalog.py
  de456c53a7ca5d62c0e80184fe6e20fe8115f85e130de3a2a50212be3da4ab39  scripts/check_claims.py
  c607f72b887665dee08c7609bc2e6b7172d0fab39edd3386b3e0e1a93d11c3fb  scripts/check_compendium.py
  6defe31675919f175c5f0bcbcb6e0459fd10a1a6aab7b9bc51ae44dda8b104d3  scripts/check_lawchanges.py
  bdefe7404cf4d08b7fb019d2ce607933e594fff6e13cb7666cfe92d6cbae42a8  scripts/check_messages.py
  9b0e2fcc9228dfd2c1ee4c011247205d58ca895c932e1f11496c86b596b9bb35  scripts/check_notebooks.py
  252c2d52ca0539114caf42bbf79722ec304656bd86805be4a286dab73c311106  scripts/check_notes.py
  0ddaeb011ba633cf3f4433b049c919393759ade85fe023374e33834048fd59f9  scripts/check_predictions.py
  d234ef54cbcca21383fc960d8ecf1d55e835ebbedfec464515739e2ae1edc34c  scripts/check_verify_scripts.py
  a6fe7f804b4fcf673137804fd0f6f5b124d29d030e5dd1f7b48bebd9206098d4  scripts/run_all.py
  78e4dc2720ffd206c7ef827cc7856c892ba9c3b11ccec07ac4c99e3b2d865052  scripts/run_compendium_checks.js
  de67901cdc5fbdf8b29eed5e880e8736f3270f8ae6f3f01b579d41caf7c7255c  scripts/verify/iwasawa_one_stage.py
  664b6917eb806d0bf4894d0a089b5107de4a95684b35827e2473c1b46f65879f  scripts/verify/kuramoto_einstein_refutation.py
  c7d77ffd0006a7dc7ec562f29b416934557aec30e7d3eabbf96a349837785b4a  scripts/verify/p10_order_dimension.py
  cdeacdee9a97a20e209a01f712a5fe1c43fb9c11b65f9b3434f98fd65e37252b  scripts/verify/p11_spectral_metric.py
  792ce4623ab937012b43d33575fd36057b0c20cf8cc4ce8395cf94d960dbe52d  scripts/verify/p13_acoustic_metric.py
  99ae99cd74ff87f88105d05f3f131fa48eb35ffcd150ce07c08964e7e77624c2  scripts/verify/p14_isometric_spectra.py
  68716f23dafe0b72ef9d117f010e8b44276ca1d3226df2586442001c7343df3e  scripts/verify/p15_spectral_dimension.py
  365c09a7ded171876208761cce634b98e17a68fadde27e95bf3414d61f580f15  scripts/verify/p16_two_dimensions.py
  24ec0a6651f1ead949398d03a20be4cb17cc6a9a5f90241fe5f0cbf95a703d82  scripts/verify/p17_bell_ladder.py
  3a8ec4fca6a063b9a38756d45b97ae5a0cb104d1d3aca073250154fe49362aa1  scripts/verify/p18_smooth_retest.py
  9cd306e59bf3066cb5f52545b14a1343ff24416b17e92351de112e8c85932791  scripts/verify/p19_alf_lattice.py
  19f02072bb299e8a590cc43b3c85a6c91dbe1ef20fe79da2a9aa813fd689bbd1  scripts/verify/p1_depth6_pairs.py
  295765a5ab72dc9c4684762d91d41d7ef643785a99eb4bb7e0f5000dd0a0ff30  scripts/verify/p1_gradient_bc.py
  9dd948075e8a0a5da9db0438be3b9ed9bb6d7b8f4e7092f282402318efc14e8a  scripts/verify/p1_mean_frequency.py
  9549e2345684c7a7d0d4a911e11893e712a57a0e46117e085b2955c741ad56d4  scripts/verify/p21_hardy_maximum.py
  a86504461802d59c6e81bdfc12655a0c08556498dce1ac3b37366b99898f4589  scripts/verify/p22_locking_skeleton.py
  f2e1f75ac953c10ad4b06ed5a3ab608421a9a720b2379c4d7bff7f67d7f13b96  scripts/verify/p24_memory_hierarchy.py
  a62a3dc991e3f15a876d26476d1f0e4f40be293fccc4d90658dee4648b2defc0  scripts/verify/p26_everpresent_scorecard.py
  6de941993aff6b2ce579349b13fdeec04eee1fe5bc21ceeece090bb68d1805b6  scripts/verify/p27_squeeze_windows.py
  56618ebf0b1d4cfcbaafeaf0d82a6a9b03817eee7f3d10f31fd923f752c5d511  scripts/verify/p28_gap_integers.py
  b091e22acf60b3995c2b09de1fbd5e78c9310a4918a40cf29db94626a515b75a  scripts/verify/p29_farey_bridge.py
  6abf4ad07bb3c57dd88c9d8b220fa1ffd7fa5500e6faa2d5be6d1e6ab66f83dd  scripts/verify/p30_order_ladder.py
  3259f4e44ab56e5532d6f3de1429eaa0873061a0d330d141025f2e86df8a3916  scripts/verify/p31_second_bridge.py
  b3fabf7e05c432d8efda4d3879fdd91f4ae96511ea43364c7d3c4edf09a78de4  scripts/verify/p32_parity_factorial.py
  3e0a90ddcb720317d4e16def0b3cf2d8a51cd2f55d0be6d7a1c9de921d774987  scripts/verify/p34_horizon_census.py
  07915db9ebdc1a7264d2fdb8d8778d0505f65cea98a6af0f4673d54de7a61bcd  scripts/verify/p36_free_ring.py
  7aff5efba156c54133fb0218c9d8bed61e89d404701d73a8fd3a2f33b388c30a  scripts/verify/p37_price_of_bit.py
  beaa8b467ab3b3cf6b150dcee9369e9f4a86be13d8778bb56736ac5506a14054  scripts/verify/p38_switch_bridge.py
  98db9a8461680d0bc552c00844c04ca8081f87ff01d4a4f8a113a4bbd73685e1  scripts/verify/p39_alpha_family.py
  84f8fd170e131a9741e116672d401db6a328bf52e624bd0f50cb978a66a42435  scripts/verify/p41_gap_openings.py
  ff7d158cc90ea0cabcc6fbfc5f2529eff1078750ff8bd53e7d4db037b10d6ae8  scripts/verify/p42_same_data.py
  36b6b2d4a1a3dff82b291ba06dba557936cd16f0452d377d511f25a5783ba7af  scripts/verify/p43_shadow_body.py
  4355a643f81ab69f9d7f92331355fe37964c445e64873a49b5461c1eefe391e6  scripts/verify/p6_circulant_small.py
  b60ad77d615e353171739472bafbda552f4d1f60f34dd504812c7383a60f7df5  scripts/verify/p7_golden_flux.py
  97bde79c88fc71a1f10af692c7acc4f980a7e97a6f9b1887bf55c5900485a1e5  scripts/verify/q1_saddle_node.py
  9817e5aa93f80e96db3d9429fc778498fd3249f72c1fa17332d21006ff59820f  scripts/verify/q_j_structure.py
  243240999a02eb20701c5b20cca171aca2c45ee6b9dc6fcfd253bd799d62ad07  scripts/verify/q_j_structure_sectors.py
  49a15d0ed708463af8fa998c2e41544c2f2488c9681711eada58aee3c1bbd29e  tests/run_spec.py
  68ca44f2f153f84714c977ae0bf25f81f6fdcb5f01d069208a5777597ec1f937  tests/spec/catalog.spec
  5d476e65468c813857cd33d2e16580b786a0156e1c2abf64997092b66743c2f3  tests/spec/falsifier.spec
  c342759d5f6356fc14ef6097c0bf2379f11be1e1c19de3761161d9b75295744b  tests/spec/intake.spec
  5d870c2fe6dd7d5b7ed807cc8780fcacded655414851fb0f3b6c55fb0b6321b6  tests/spec/ledgers.spec
  ae60038700e7505b580ce7915375e32e9816b0079232f8a406435f0a013d9d10  tests/spec/message.spec
  af180d006a2b25e6c9722190de07ba8b58ffa0f05c4ad34b36eff9557a677692  tests/spec/notes.spec
