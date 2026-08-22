# Catalog gate: every entry passes plainly and fails under --mutant through the harness.
FIXTURE good-entry
  FILE catalog/c90_good.py
    """Two plus two is four. Source: arithmetic. Mutant: claims five."""
    import sys
    from _common import mutant_flag, finish
    sys.exit(finish(2 + 2 == (5 if mutant_flag() else 4), "2 + 2"))
  END
RULE catalog.1 "an entry that passes plainly and fails under the mutant is accepted": GIVEN good-entry WHEN catalog RUNS THEN ACCEPT
FIXTURE mutant-passes
  FILE catalog/c91_weak.py
    """Two plus two is four. Source: arithmetic. Mutant: does nothing."""
    import sys
    from _common import mutant_flag, finish
    sys.exit(finish(2 + 2 == 4, "2 + 2"))
  END
RULE catalog.2 "an entry whose mutant passes is rejected": GIVEN mutant-passes WHEN catalog RUNS THEN REJECT MENTIONING "mutant passed"
FIXTURE mutant-crashes
  FILE catalog/c92_crash.py
    """Two plus two is four. Source: arithmetic. Mutant: raises."""
    import sys
    from _common import mutant_flag, finish
    if mutant_flag():
        raise RuntimeError("boom")
    sys.exit(finish(2 + 2 == 4, "2 + 2"))
  END
RULE catalog.3 "an entry whose mutant crashes is rejected (LAW-16)": GIVEN mutant-crashes WHEN catalog RUNS THEN REJECT MENTIONING "mutant crashed"
FIXTURE no-docstring
  FILE catalog/c93_nodoc.py
    import sys
    from _common import mutant_flag, finish
    sys.exit(finish(not mutant_flag(), "x"))
  END
RULE catalog.4 "an entry without a docstring is rejected": GIVEN no-docstring WHEN catalog RUNS THEN REJECT MENTIONING "no docstring"
