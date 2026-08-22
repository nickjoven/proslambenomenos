<!-- commentary -->
# Adversarial audit (context-free agent, 2026-08-19)

Performed by a fresh agent with no session context, instructed to
treat every repo statement as testimony and to attack. Bypasses were
constructed in scratch copies; the working repo was untouched.
Findings transcribed verbatim in substance; dispositions added below
each.

## Findings

**F1 | HIGH | bypass | Deleting an entire append-only ledger evades
the gate.** check_append_only.py:40-41 skips missing files, so
`git rm DECLINED.md` + commit reports clean, the file silently absent
from the "grew only" list. Verified by running the deletion commit in
a copy. Missed by the self-report, whose only append-only residual
was owner history-rewrite.
*Disposition: FIXED same pass — a ledger with git history that is
absent from the tree is now a violation.*

**F2 | HIGH | bypass | scripts/verify/*.py are cited as evidence but
not hash-covered by the law gate.** covered_files()
(check_lawchanges.py:31-38) excludes them; a stub printing PASS
replaced q1_saddle_node.py with law gate clean and verify gate
passing, while the claims citing it stayed proven. Missed by the
self-report, which rostered the scripts to run but not to be pinned.
*Disposition: FIXED — verify scripts join the covered set (LAW-3).*

**F3 | MED-HIGH | bypass | The pigeonhole cap is opt-in.** The cap
fires only when the author declares numeric_match
(check_claims.py:146-150); a crafted claim asserting the 6*pi^5
proton-electron coincidence as "an exact structural identity" derived
`imported`, uncapped — while README req. 2 advertises the cap as a
guarantee. *Disposition: MITIGATED — a statement scanner now forces
numeric_match on numeric-agreement vocabulary; residual: vocabulary
lists are tripwires, not walls, and the README now says so.*

**F4 | MED | bypass | machine:true minted a false claim proven.** A
"zeta zeros have real part 17" claim with machine:true and an
existing-but-irrelevant ref derived `proven`. The self-report (G5)
called the hole latent; it was active. *Disposition: FIXED — the flag
is disabled entirely until a machine-proof executor exists; setting
it is now an error (LAW-3). Honest removal beats honor-system.*

**F5 | MED | bypass | Conclusive-vocabulary synonym evasion.**
"establishes… settled and demonstrated rigorously", "definitively
resolve… guaranteed" pass untagged. *Disposition: MITIGATED — the
demonstrated synonyms join the lexicon; the tripwire-not-wall status
is already documented and remains true.*

**F6 | MED | overclaim | README advertised a coverage invariant the
corpus violates.** All claim-introducing commits predate the coverage
rule (b182d83); a full-range run shows 8 historical violations that
the HEAD-only default and push-range CI never surface.
*Disposition: FIXED honestly — the rule is now dated from its
enactment (grandfather boundary recorded in the gate and README), and
CI runs the full range from that boundary, so the invariant as now
stated is true and enforced.*

**F7 | LOW-MED | inconsistency | Fixture counts contradict across
artifacts (9 vs 14 vs actual 26).** A repeat of the G13
memory-reporting failure, in the very report that codified the fix.
*Disposition: FIXED — prose no longer states fixture counts; the
suite is the count.*

**F8 | LOW | README said seven declined routes; there are eight.**
*Disposition: FIXED — countless phrasing.*

**F9 | LOW | theater | Non-path evidence refs ("compendium C99")
are never resolved.* *Disposition: recorded residual — the G3 rule
covers path-shaped tokens only; free-text refs remain attestations.*

**F10 | LOW-MED | math-label | koide-foot-v4-equivalence smuggled the
empirical coincidence inside a proven claim.** The algebraic
equivalence is correct (re-derived by the auditor; Foot 1994
attribution verified); the PDG numeric agreement rode inside without
a cap. *Disposition: FIXED by decomposition — the equivalence claim
keeps proven with the numerics removed from its statement; the
empirical agreement is now its own claim, capped coincidence-unruled,
as the law requires.*

## Held up under attack (auditor's list)

Law gate (covered-file edits caught); intake gate (status flip
blocked; grading, premise cap, cycles verified); append-only line
removals caught with SHAs; compendium 18/18 from the tree with checks
testing the stated propositions, no tautologies; link-001 digests
still matching the tree. All independently re-derived mathematics
correct: orbit counts and increments, cusp widths/invariant, ord = 9
refutation, geodesic-flow counterexamples, a0 numbers, Shenker
exponent, Chebyshev identity and divergence sums to machine
precision.

## Meta

The self-audit found the reproducibility gaps; the context-free agent
found the preventive bypasses the shared context concealed, plus two
recurrences of memory-based counting. Detective gates held; the
exploitable surface was prevention — consistent with the trust
boundary the README states. Second-eyes verification is cheap
(one agent-run) and found what self-review could not: this audit
should recur before every link tag.
