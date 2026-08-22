# Message gate: conclusive vocabulary needs a supporting [claim id]; touched claims need their tag.
FIXTURE plain
  COMMIT "routine refactor" STATUSES good=proven,weak=argued
RULE message.1 "a plain engineering message is accepted": GIVEN plain WHEN message RUNS THEN ACCEPT
FIXTURE conclusive-untagged
  COMMIT "proves the theorem" STATUSES good=proven,weak=argued
RULE message.2 "conclusive language without a claim tag is rejected": GIVEN conclusive-untagged WHEN message RUNS THEN REJECT MENTIONING "no [claim"
FIXTURE conclusive-argued
  COMMIT "proves it [claim weak]" STATUSES good=proven,weak=argued
RULE message.3 "conclusive language supported only by an argued claim is rejected": GIVEN conclusive-argued WHEN message RUNS THEN REJECT MENTIONING "weak"
FIXTURE conclusive-proven
  COMMIT "proves it [claim good]" STATUSES good=proven,weak=argued
RULE message.4 "conclusive language supported by a proven claim is accepted": GIVEN conclusive-proven WHEN message RUNS THEN ACCEPT
FIXTURE coverage-plus-support
  COMMIT "proves it [claim good] [claim weak]" TOUCHING good,weak STATUSES good=proven,weak=argued
RULE message.5 "a capped claim's coverage tag is allowed when a supporting tag exists (LAW-5)": GIVEN coverage-plus-support WHEN message RUNS THEN ACCEPT
FIXTURE touched-untagged
  COMMIT "tweak wording" TOUCHING good STATUSES good=proven,weak=argued
RULE message.6 "a touched claim without its tag is rejected": GIVEN touched-untagged WHEN message RUNS THEN REJECT MENTIONING "touches claims/good.yml"
FIXTURE touched-tagged
  COMMIT "tweak wording [claim good]" TOUCHING good STATUSES good=proven,weak=argued
RULE message.7 "a touched claim with its tag is accepted": GIVEN touched-tagged WHEN message RUNS THEN ACCEPT
FIXTURE hyphen-guard
  COMMIT "handle checked-novel novelty in the gate" STATUSES good=proven
RULE message.8 "the vocabulary term checked-novel is not conclusive language (LAW-7)": GIVEN hyphen-guard WHEN message RUNS THEN ACCEPT
FIXTURE bare-novel
  COMMIT "a novel identity" STATUSES good=proven
RULE message.9 "bare novel is still conclusive": GIVEN bare-novel WHEN message RUNS THEN REJECT MENTIONING "novel"
