# Intake gate: statuses are derived, never declared. One rule per line.
FIXTURE label-without-evidence
  FILE claims/a.yml
    id: a
    statement: x
    status: proven
  END
RULE intake.1 "a declared status with no evidence computes to asserted": GIVEN label-without-evidence WHEN intake RUNS THEN REJECT MENTIONING "recorded != computed (asserted)"

FIXTURE pigeonhole-weak
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}]
    numeric_match: {observable: o, pigeonhole_p: 0.13}
    status: proven
  END
RULE intake.2 "pigeonhole p >= 0.05 caps at coincidence-unruled": GIVEN pigeonhole-weak WHEN intake RUNS THEN REJECT MENTIONING "coincidence-unruled"

FIXTURE pigeonhole-strong
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}, {kind: computation, ref: c, method: reimplementation}]
    numeric_match: {observable: o, pigeonhole_p: 0.001}
    status: proven
  END
RULE intake.3 "pigeonhole p < 0.05 does not cap": GIVEN pigeonhole-strong WHEN intake RUNS THEN ACCEPT

FIXTURE prose-proof
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: prose argument}]
    status: proven
  END
RULE intake.4 "a prose proof alone is argued": GIVEN prose-proof WHEN intake RUNS THEN REJECT MENTIONING "recorded != computed (argued)"

FIXTURE proof-plus-rerun
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: prose}, {kind: computation, ref: r, method: rerun}]
    status: proven
  END
RULE intake.5 "a proof plus a same-algorithm rerun is argued": GIVEN proof-plus-rerun WHEN intake RUNS THEN REJECT MENTIONING "recorded != computed (argued)"

FIXTURE machine-flag
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: lean, machine: true}]
    status: proven
  END
RULE intake.6 "the machine flag is disabled until an executor exists (LAW-3)": GIVEN machine-flag WHEN intake RUNS THEN REJECT MENTIONING "disabled"

FIXTURE agreement-vocab
  FILE claims/a.yml
    id: a
    statement: the ratio agrees with the observed value to 0.1%
    evidence: [{kind: citation, ref: r}]
    status: imported
  END
RULE intake.7 "numeric-agreement vocabulary requires a numeric_match block (F3)": GIVEN agreement-vocab WHEN intake RUNS THEN REJECT MENTIONING "pigeonhole cap is not optional"

FIXTURE proof-plus-reimplementation
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: prose}, {kind: computation, ref: r, method: reimplementation}]
    status: proven
  END
RULE intake.8 "a proof plus an independent reimplementation is proven": GIVEN proof-plus-reimplementation WHEN intake RUNS THEN ACCEPT

FIXTURE argued-premise
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: prose}]
    status: argued
  END
  FILE claims/b.yml
    id: b
    statement: y
    premises: [a]
    evidence: [{kind: proof, ref: p}, {kind: computation, ref: r, method: reimplementation}]
    status: proven
  END
RULE intake.9 "an argued premise caps a downstream proven claim at conditional": GIVEN argued-premise WHEN intake RUNS THEN REJECT MENTIONING "recorded != computed (conditional)"

FIXTURE rerun-only
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: computation, ref: r, method: rerun}]
    status: verified
  END
RULE intake.10 "a rerun-only computation is reproduced, not verified": GIVEN rerun-only WHEN intake RUNS THEN REJECT MENTIONING "recorded != computed (reproduced)"

FIXTURE asserted-premise
  FILE claims/a.yml
    id: a
    statement: x
    status: asserted
  END
  FILE claims/b.yml
    id: b
    statement: y
    premises: [a]
    evidence: [{kind: proof, ref: r}]
    status: proven
  END
RULE intake.11 "an unsettled premise caps at conditional": GIVEN asserted-premise WHEN intake RUNS THEN REJECT MENTIONING "recorded != computed (conditional)"

FIXTURE novel-unchecked
  FILE claims/a.yml
    id: a
    statement: a novel identity
    evidence: [{kind: proof, ref: r}]
    status: proven
  END
RULE intake.12 "novelty vocabulary is banned while novelty is unchecked": GIVEN novel-unchecked WHEN intake RUNS THEN REJECT MENTIONING "novelty vocabulary"

FIXTURE bogus-litcheck
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}]
    novelty: {status: checked-novel, litcheck: LC-999}
    status: proven
  END
RULE intake.13 "checked-novel requires a real LITCHECKS entry": GIVEN bogus-litcheck WHEN intake RUNS THEN REJECT MENTIONING "LITCHECKS"

FIXTURE refutation-wins
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}, {kind: refutation, ref: r2}]
    status: proven
  END
RULE intake.14 "refutation evidence outranks proof": GIVEN refutation-wins WHEN intake RUNS THEN REJECT MENTIONING "recorded != computed (refuted)"

FIXTURE premise-cycle
  FILE claims/a.yml
    id: a
    statement: x
    premises: [b]
    status: asserted
  END
  FILE claims/b.yml
    id: b
    statement: y
    premises: [a]
    status: asserted
  END
RULE intake.15 "premise cycles are detected": GIVEN premise-cycle WHEN intake RUNS THEN REJECT MENTIONING "cycle"

FIXTURE missing-path
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: computation, ref: 'scripts/verify/nonexistent_xyz.py - check', method: reimplementation}]
    status: verified
  END
RULE intake.16 "evidence citing a missing repo path is rejected (G3)": GIVEN missing-path WHEN intake RUNS THEN REJECT MENTIONING "does not exist"

FIXTURE no-falsifier
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}, {kind: computation, ref: 'scripts/verify/q1_saddle_node.py - check', method: reimplementation}]
    status: proven
  END
RULE intake.17 "proven with verify-script evidence requires null_system and falsifier (LAW-11)": GIVEN no-falsifier WHEN intake RUNS THEN REJECT MENTIONING "falsifier" AND "null_system"

FIXTURE borrowed-falsifier
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}, {kind: computation, ref: 'scripts/verify/q1_saddle_node.py - check', method: reimplementation}]
    null_system: 'n'
    falsifier: 'scripts/verify/p1_gradient_bc.py --mutant and-not-xor'
    status: proven
  END
RULE intake.18 "a falsifier must be one of the claim's own cited scripts (LAW-16)": GIVEN borrowed-falsifier WHEN intake RUNS THEN REJECT MENTIONING "borrowed"

FIXTURE verified-no-falsifier
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: computation, ref: 'scripts/verify/q1_saddle_node.py - check', method: reimplementation}]
    status: verified
  END
RULE intake.19 "verified claims are in the falsifier rule's scope (LAW-16)": GIVEN verified-no-falsifier WHEN intake RUNS THEN REJECT MENTIONING "falsifier"

FIXTURE double-slash-path
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}, {kind: computation, ref: 'scripts//verify/q1_saddle_node.py - check', method: reimplementation}]
    status: proven
  END
RULE intake.20 "path normalisation: scripts//verify does not dodge the rule (LAW-16)": GIVEN double-slash-path WHEN intake RUNS THEN REJECT MENTIONING "falsifier"

FIXTURE complete-falsifier
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: proof, ref: r}, {kind: computation, ref: 'scripts/verify/q1_saddle_node.py - check', method: reimplementation}]
    null_system: 'the same computation on a trivial system'
    falsifier: 'scripts/verify/q1_saddle_node.py --mutant wrong-exponent'
    status: proven
  END
RULE intake.21 "proven with null_system and a named --mutant falsifier is accepted": GIVEN complete-falsifier WHEN intake RUNS THEN ACCEPT

FIXTURE phantom-compendium
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: computation, ref: 'compendium C99 - census', method: reimplementation}]
    status: verified
  END
RULE intake.22 "a free-text compendium reference must name a registered check (LAW-17)": GIVEN phantom-compendium WHEN intake RUNS THEN REJECT MENTIONING "not a registered check"

FIXTURE real-experiment-path
  FILE claims/a.yml
    id: a
    statement: x
    evidence: [{kind: computation, ref: 'scripts/experiments/d4_2d_pairs.py - check', method: reimplementation}]
    status: verified
  END
RULE intake.23 "evidence citing an existing non-verify repo path is accepted": GIVEN real-experiment-path WHEN intake RUNS THEN ACCEPT
