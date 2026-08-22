<!-- evidence: scripts/verify/iwasawa_one_stage.py, claims/sl2r-connected-subgroups.yml -->
# P-3: the Iwasawa one-stage claim, resolved

Governed by P-3 (PREDICTIONS.md). Source of the original: harmonics
sync_cost/derivations/planck_scale.md, "Result" (line 234): "Every
continuous H != {e} in SL(2,R) kills exactly one of the three
coupling stages (phase, amplitude, frequency), reducing the system to
N <= 2 effective stages", with the exhaustiveness paragraph (224-228)
"the three one-parameter classes exhaust all connected one-parameter
subgroups up to conjugacy; the only other possibility is a discrete
subgroup." Setting: G = SL(2,R) = K A N, K = SO(2), A positive
diagonals, N upper unipotents; "H kills a stage" means H is the
isotropy group of M = G/H and dim M = 3 - dim H. Dimension-3
conclusion (89-99, 237-240): with the physics premise that N <= 2
stages cannot self-sustain, H = {e} is forced, so dim M = 3.
Resolution by a context-free auditor 2026-08-22, reviewed; script
scripts/verify/iwasawa_one_stage.py.

## The original is false

Counterexample: the connected Borel subgroup AN = {[[p, q], [0, 1/p]]
: p > 0} is a connected, nontrivial, 2-dimensional Lie subgroup
containing A and N; G/AN = K = S^1 has dimension 1. It kills two
stages, not "exactly one", and N drops to 1, not 2. The dichotomy
"one-parameter, else discrete" omits dimensions 2 and 3. Secondary:
"exactly one stage" is meaningful only up to conjugacy - the
one-parameter subgroup exp(t [[1,1],[0,-1]]) equals none of K, A, N,
lies in AN, and is conjugate to A; and {+-I} is far from the only
discrete subgroup (SL(2,Z), cyclic groups, Fuchsian groups).

## The corrected theorem (proof in the auditor's report, reproduced)

Every connected Lie subgroup H of SL(2,R) is, up to conjugacy, exactly
one of: {e} (dim 0); K, A, or N (dim 1; three conjugacy classes,
distinguished by the sign of det of the generator X, with X^2 =
-det(X) I); AN (dim 2; every conjugate of A and of N lies in a
conjugate of AN, no conjugate of K does, since upper-triangular
matrices have real eigenvalues); G (dim 3). Hence dim G/H in
{3, 2, 1, 0} and dim G/H = 3 iff H is discrete.

Proof sketch. Connected subgroups <-> Lie subalgebras of sl(2,R). dim
1: Jordan form of a traceless real 2x2 matrix gives the three cases
by sign of det. dim 2: the centraliser of any nonzero X is RX (X^2
scalar), so a 2-dimensional subalgebra is non-abelian, hence has a
basis X, Y with [X, Y] = Y; ad_X has eigenvalues 0, +-2 mu with +-mu
the eigenvalues of X, and Y is an eigenvector with eigenvalue 1, so
mu is real and nonzero: X is hyperbolic, conjugate to D/2, and Y lies
in an ad_D eigenspace, i.e. Y in R N+ or R N-; conjugating by w =
[[0,-1],[1,0]] swaps them, so the subalgebra is conjugate to
span(D, N+) = Lie(AN). dim 3: all of sl(2,R). QED. Classical: this is
the standard classification of subalgebras of sl(2,R) (e.g. Lang,
SL2(R); Kirillov, Introduction to Lie Groups and Lie Algebras).

Corollary (the honest one-stage statement): every one-parameter
subgroup is conjugate to exactly one of K, A, N, and the stage it
kills is well defined up to conjugacy; every connected H != {e} kills
AT LEAST one stage - exactly one iff dim H = 1, two iff H ~ AN, three
iff H = G.

## The dimension-3 conclusion

Survives, and never needed the false statement: it uses only dim G/H
= 3 - dim H and dim H >= 1 for connected H != {e} - the trivial part.
The Borel case strengthens the reduction (N drops to 1), which is
more fatal under the source's premise, not less. What does not
survive as stated: "exactly one", the equality (vs conjugacy) reading
of the three stages, and the discrete-subgroup sentence. Untouched by
the mathematics: the physics premises (G = SL(2,R) as substrate; N <=
2 non-self-sustaining) - the theorem only converts "H != {e}
connected" into "dim M <= 2".

P-3's expectation holds; its mind-change condition does not fire.
R-2 recorded in PREDICTIONS.md. Harmonics ERRATA owed (E23).
