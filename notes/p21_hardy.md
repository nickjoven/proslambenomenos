<!-- evidence: scripts/experiments/p21_derive.py, scripts/experiments/p21_registration.json, scripts/experiments/p21_hardy.py, scripts/experiments/p21_results.json, scripts/verify/p21_hardy_maximum.py -->
# P-21: Hardy's maximum is the fifth power of the golden mean

Symbols: see the VOCABULARY.md symbol graph - phi^5 falls out of y^2 - 3y + 1 = 0 in y = k + 1/k - phi's one verified home as an ANSWER (the address/yardstick routes live in the VOCABULARY phi taxonomy).

Registered before computing (PREDICTIONS.md P-21); resolution R-16,
all clauses as registered; claim hardy-maximum-is-phi-fifth. This
closes A-9 - the one golden-mean physics number that survived the
Otto mechanization (notes/otto25_mechanization.md) - and the reason
it survived is the whole point of this note.

## The paradox

Two qubits, |psi> = c|00> + s|11>, local binary projective
measurements A0/A1 (Alice) and B0/B1 (Bob). Choose the measurements
so that three events never happen:

    Z1:  A0 = +  and  B0 = +
    Z2:  A1 = +  and  B0 = -
    Z3:  A0 = -  and  B1 = +

and watch the fourth: p_Hardy = P(A1 = +, B1 = +). A local
hidden-variable world that obeys Z1-Z3 cannot show the fourth event
at all: if A1 = + and B1 = +, then Z2 forces B0 = +, Z3 forces
A0 = +, and Z1 forbids the pair (exhaustive over all 16
deterministic assignments, EQ1 - no inequality needed, just the
four sentences). Quantum mechanics shows the event anyway.

## Where the golden mean enters - through a theorem

The three constraints eliminate three of the four measurement
angles (EQ2). The leftover freedom dies on an exact square,
not a derivative: D - (1+k^3)^2 = k^2 (a - k/a)^2 (EQ4). What
remains is one function of one variable, k = c/s:

    p_env(k) = k^2 (1-k)^2 / ((1+k^2)(1-k+k^2)^2)        (EQ5)

Stationarity is the quintic k^5 - 2k^4 - 2k + 1 = 0 (EQ6), which
factors as (k+1)(k^4 - 3k^3 + 3k^2 - 3k + 1) (EQ7); the quartic is
palindromic and collapses in y = k + 1/k to

    y^2 - 3y + 1 = 0,   y* = (3 + sqrt 5)/2 = Phi^2       (EQ8-9)

and in the y variable the whole envelope is p = (y-2)/(y(y-1)^2)
(EQ10), so at the optimum, with y* - 1 = Phi and y* - 2 = phi,

    p* = phi / Phi^4 = phi^5 = (5 sqrt 5 - 11)/2          (EQ11)

computed as an identity of rational pairs in Q(sqrt 5) - no
floating point. The optimal state is NOT maximally entangled: it
has c s = 1/y* = phi^2, Schmidt weights (1 -+ sqrt(6 sqrt5 - 13))/2
= 0.177352 / 0.822648 (EQ12), and at c = s the paradox vanishes
identically (EQ13) - maximal entanglement is where Hardy's argument
dies, one of the classic surprises of the subject.

The pedagogical point this repo exists to make: phi^5 here is a
THEOREM. The golden mean enters through the algebra - a palindromic
quartic whose y-collapse is the fibonacci polynomial y^2 - 3y + 1 -
not through a fit, a unit choice, or a numerological reading of a
measured constant. Contrast notes/otto25_mechanization.md, where
every golden-mean relation that touched a measured number sat
hundreds to hundreds of thousands of experimental sigma away, and
the two survivors (this one and the Kepler-pyramid in-sphere
theorem-let) survived precisely because they are theorems about
mathematical structures, with nothing to measure. Keeping those two
categories separate is what P-21's not-claimed-in-advance line
enforces.

## The blind route agreed to land where it landed

Route 2 knew none of the algebra: 200 seeded Nelder-Mead starts
(seed 20260826) over the raw 5-parameter space, maximizing
p_Hardy - lambda * (sum of squared constraint probabilities) on the
registered schedule 1e3..1e9, then the registered
constraint-eliminated polish. All 200 starts found the golden
basin; the polished maximum deviates from the pinned phi^5 by
2.4e-16, the Schmidt weights by 4.6e-10, and the maximally
entangled slice tops out at 1.2e-32 (p21_results.json). The
penalized stage sits ABOVE phi^5 by 3.3e-4 at constraint
probability 1.7e-7 - the textbook penalty-method infeasibility
offset (order C^2/4 lambda), which the polish removes; no feasible
point beat phi^5 anywhere in the run.

The falsifier keeps both surprises honest:
`--mutant maximally-entangled-best` asserts the c = s slice reaches
phi^5/2 (it reaches ~1e-32); `--mutant flat-landscape` asserts the
optimum is degenerate in the Schmidt angle (p moves by 1.3e-2 at
theta* +/- 0.1 against a 1e-6 bar).
