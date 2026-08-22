# Pure parsers behind the append-only, law, and prediction gates.
FIXTURE insert-only-diff
  FILE diff.txt
    commit abcdef1234567
    --- a/DECLINED.md
    +++ b/DECLINED.md
    @@ -1,3 +1,3 @@
    +added line
     context
  END
RULE ledgers.1 "insertions and headers produce no removals": GIVEN insert-only-diff WHEN append-only-parser RUNS THEN EQUALS []
FIXTURE removal-diff
  FILE diff.txt
    commit abcdef1234567
    --- a/DECLINED.md
    +++ b/DECLINED.md
    @@ -1,3 +1,3 @@
    +added line
     context
    -a past ruling
  END
RULE ledgers.2 "a removed line is detected with its commit": GIVEN removal-diff WHEN append-only-parser RUNS THEN EQUALS [["abcdef123", "a past ruling"]]
FIXTURE two-law-entries
  FILE LAWCHANGES.md
    # L
    
    ## LAW-1 x
    direction: neutral
    hashes:
      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  scripts/check_claims.py
    
    ## LAW-2 y
    direction: strengthen
    hashes:
      bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb  scripts/check_claims.py
  END
RULE ledgers.3 "the last law entry's hashes win": GIVEN two-law-entries WHEN law-parser RUNS THEN EQUALS {"scripts/check_claims.py": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}
FIXTURE two-predictions
  FILE PREDICTIONS.md
    # P
    
    ## P-1 — 2026-08-20 — thing
    expects: X
    changes-my-mind: Y
    
    ## P-2 — 2026-08-20 — other
    expects: Z
  END
RULE ledgers.4 "a complete entry parses and a missing changes-my-mind is detected": GIVEN two-predictions WHEN prediction-parser RUNS THEN EQUALS {"P-1": {"expects": true, "changes": true}, "P-2": {"expects": true, "changes": false}}
FIXTURE numeric-claim
  FILE claim.yml
    numeric_match: {observable: x}
  END
RULE ledgers.5 "a numeric_match claim is in the preregistration scope": GIVEN numeric-claim WHEN prediction-scope RUNS THEN EQUALS true
FIXTURE checked-novel-claim
  FILE claim.yml
    novelty: {status: checked-novel}
  END
RULE ledgers.6 "a checked-novel claim is in scope": GIVEN checked-novel-claim WHEN prediction-scope RUNS THEN EQUALS true
FIXTURE classical-claim
  FILE claim.yml
    novelty: {status: classical}
  END
RULE ledgers.7 "a classical claim is out of scope": GIVEN classical-claim WHEN prediction-scope RUNS THEN EQUALS false
