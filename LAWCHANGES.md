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
