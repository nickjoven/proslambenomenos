# Falsifier runner (LAW-16): a mutant counts only if it RAN and FAILED.
FIXTURE ran-and-failed
  RESULT rc=1 STDOUT "checks...\nFAIL"
RULE falsifier.1 "rc 1 with a FAIL line and no traceback is a failing mutant": GIVEN ran-and-failed WHEN falsifier RUNS THEN ACCEPT
FIXTURE not-confirmed
  RESULT rc=1 STDOUT "REFUTATION NOT CONFIRMED"
RULE falsifier.2 "the refutation sentinel NOT CONFIRMED is accepted as a failure line": GIVEN not-confirmed WHEN falsifier RUNS THEN ACCEPT
FIXTURE crashed
  RESULT rc=1 STDOUT "" STDERR "Traceback (most recent call last): boom"
RULE falsifier.3 "a crash is not a failing mutant": GIVEN crashed WHEN falsifier RUNS THEN REJECT MENTIONING "crashed"
FIXTURE usage-error
  RESULT rc=2 STDOUT "usage error: unknown mutant"
RULE falsifier.4 "rc 2 (usage error, missing file) is not a failing mutant": GIVEN usage-error WHEN falsifier RUNS THEN REJECT MENTIONING "rc 2"
FIXTURE silent-exit
  RESULT rc=1 STDOUT "done"
RULE falsifier.5 "rc 1 without a FAIL line is not a failing mutant": GIVEN silent-exit WHEN falsifier RUNS THEN REJECT MENTIONING "no FAIL line"
FIXTURE passed
  RESULT rc=0 STDOUT "PASS"
RULE falsifier.6 "a passing mutant is rejected": GIVEN passed WHEN falsifier RUNS THEN REJECT MENTIONING "rc 0"
