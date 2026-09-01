<!-- evidence: scripts/experiments/p38_derive.py, scripts/experiments/p38_registration.json, scripts/experiments/p38_bridge.py, scripts/experiments/p38_results.json -->
# P-38 working document: the Hardy-order bridge (A-21)

First item of the earned frontier (owner directive 2026-09-01:
earned parts to their ends before cleanup). Source: van der Lugt
& Ormrod, Quantum 8, 1543 (2024) - the possibilistic proof of
indefinite causal order in the quantum switch. What is earned
here vs imported is stated exactly in LC-28; the short form: the
DATA (our simulation) and the CEILING (our exhaustion) are
earned; the reduction theorem making the ceiling binding on
definite-causal-order models is imported.

## The scenario, in the repo's terms

Three X-controlled switches, controls GHZ-entangled, targets |0>.
Inside each: x = 1 means Z-measure and re-prepare |1>; x = 0
means identity. A Y measurement on each outgoing control. The
four registered patterns give GHZ-type parity implications - the
XXX parity 0 and three Y-pattern parities 1.

## What the two computational routes established

Dense route (experiment): 64-dim stdlib simulation. Forbidden
parity mass is EXACTLY 0.0 - the events cancel at amplitude
level, so the possibilistic reading needs no tolerance at all.
Allowed outcomes are uniform (1/32 and 1/8). No-signalling holds
in the data at 2.8e-17. The definite-wiring control world (every
switch frozen to its |+> wiring) satisfies the XXX condition and
violates each Y-pattern condition with mass exactly 1/2.

Branch route (falsifier): the GHZ control state has four X-basis
branches (even minus count). An x = (1,1) switch publishes its
branch sign in a1 (the re-prepared |1> makes a1 = 1 possible only
in the agent-2-first wiring); an x = (0,0) switch leaves its
control coherent for the Y measurement. Pattern 111 reduces to
"the minus count is even" - parity 0 on every branch; each Y
pattern reduces to a revealed sign conditioning the other two
controls into (|++> + |-->)/sqrt2 or (|+-> + |-+>)/sqrt2, whose
Y (x) Y parity is fixed at the registered value. Same clauses,
different mathematics.

Classical side, both encodings: 4096 deterministic local-order
strategies exhausted; satisfaction histogram {1: 2048, 3: 2048}
(odd counts only - XOR the four conditions and the variables
cancel, leaving 0 = 1: at least one fails, and flipping any
single output flips exactly two conditions, preserving parity of
the satisfied count). Mermin functional: classical max 2, switch
4, algebraic max 4.

## Why this line matters to the graph

P-21 earned Hardy's maximum (phi^-5) - possibilistic logic on
nonlocality. P-30 earned the causal-game ladder. This line runs
Hardy's TEMPLATE on P-30's SUBJECT: the two earned clusters of
the inviolables graph (the phi-Hardy-Fibonacci quarter and the
Bell-order quarter) are now joined by an earned edge, per the
directive that the earned parts be taken to their ends.
