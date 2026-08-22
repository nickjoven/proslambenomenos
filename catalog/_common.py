"""Shared scaffolding for catalog entries. Each entry is one checkable
mathematical fact used in the repo's reasoning: a docstring whose first
line states the fact, a source line, a check() that returns True iff
the fact holds numerically, and a MUTANT branch that must make check()
return False (LAW-11 discipline: a check without a failing mutant is a
restatement, not a test)."""
import sys


def mutant_flag() -> bool:
    return "--mutant" in sys.argv


def finish(ok: bool, fact: str) -> int:
    tag = "MUTANT " if mutant_flag() else ""
    print(f"{tag}{'PASS' if ok else 'FAIL'}: {fact}")
    return 0 if ok else 1
