# Notes gate (LAW-20, written BEFORE the gate exists): prose carries no load unless it declares its executable evidence.
FIXTURE undeclared-note
  FILE notes/x.md
    # A note
    The plateau width is 0.0740 at K = 1.
  END
RULE notes.1 "a note with no evidence or commentary declaration is rejected": GIVEN undeclared-note WHEN notes RUNS THEN REJECT MENTIONING "no declaration"
FIXTURE commentary-note
  FILE notes/x.md
    <!-- commentary -->
    # A note
    Thoughts with no load.
  END
RULE notes.2 "a note declared commentary is accepted": GIVEN commentary-note WHEN notes RUNS THEN ACCEPT
FIXTURE evidence-note
  FILE notes/x.md
    <!-- evidence: scripts/experiments/run.py, scripts/experiments/run_results.json -->
    # A note
    The width is 0.0740 (run_results.json).
  END
  FILE scripts/experiments/run.py
    print(1)
  END
  FILE scripts/experiments/run_results.json
    {"width": 0.074}
  END
RULE notes.3 "a note declaring existing executable evidence is accepted": GIVEN evidence-note WHEN notes RUNS THEN ACCEPT
FIXTURE evidence-missing
  FILE notes/x.md
    <!-- evidence: scripts/experiments/gone.py -->
    # A note
    Numbers from a script that does not exist.
  END
RULE notes.4 "declared evidence that does not exist is rejected": GIVEN evidence-missing WHEN notes RUNS THEN REJECT MENTIONING "does not exist"
FIXTURE evidence-not-executable
  FILE notes/x.md
    <!-- evidence: notes/other.md -->
    # A note
    Cites another note as its evidence.
  END
  FILE notes/other.md
    <!-- commentary -->
    # other
  END
RULE notes.5 "evidence must be executable or its output (py/js/json/ipynb/yml), not prose": GIVEN evidence-not-executable WHEN notes RUNS THEN REJECT MENTIONING "not executable"
FIXTURE commentary-claims-proof
  FILE notes/x.md
    <!-- commentary -->
    # A note
    This is proven by the argument above.
  END
RULE notes.6 "a commentary note may not use settled-status words (proven, verified, refuted) as verdicts": GIVEN commentary-claims-proof WHEN notes RUNS THEN REJECT MENTIONING "commentary uses"
