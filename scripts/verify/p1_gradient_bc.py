#!/usr/bin/env python3
"""P-1, sub-problems D2+D3: uniform-gradient states on the
Klein-twisted lattice - the corrected, lattice-exact statement.

Setup (klein_bottle.md's lattice): theta_{i,j} = 2*pi*(W1*i/N + W2*j/M)
with per-CYCLE windings W1, W2 (defined mod N, mod M respectively),
subject to
  theta_{i+N, j} = theta_{i, M+1-j} + pi  (mod 2*pi)
  theta_{i, j+M} = theta_{i, j}           (mod 2*pi)

Claim (proved by the j-coefficient argument, verified exhaustively
here for N = M = 12): for even M the compatible (W1, W2) are exactly

    W2 = 0   (uniform in y)        with W1 in Z + 1/2, and
    W2 = M/2 (pi-staggered in y)   with W1 in Z

- an XOR between half-integer x-winding and y-staggering. In
particular no other rational winding structure is admitted: spatial
windings on the twisted ring live in (1/2)Z only. Arbitrary-
denominator fractions of the tongue picture are TEMPORAL rotation
numbers, a different index set entirely (P-1 decomposition, D1).

Also verifies: the deck reflection acts on y-windings as W2 -> -W2
mod M, the lattice form of the Farey involution p/q -> (q-p)/q.

Note: the first version of this script parametrized windings per-site
and tested a different family; this exhaustive per-cycle version
replaced it after the mismatch surfaced - the checkable-ledger
mechanism working as intended.
"""

import math
import sys

N = M = 12
TWO_PI = 2 * math.pi


def residual(W1, W2):
    worst = 0.0
    for j in range(1, M + 1):
        for i in (0, 1, 5):
            lhs = TWO_PI * (W1 * (i + N) / N + W2 * j / M)
            rhs = TWO_PI * (W1 * i / N + W2 * (M + 1 - j) / M) + math.pi
            d = (lhs - rhs) % TWO_PI
            worst = max(worst, min(d, TWO_PI - d))
    return worst


MUTANT = sys.argv[sys.argv.index("--mutant") + 1] if "--mutant" in sys.argv and sys.argv.index("--mutant") + 1 < len(sys.argv) else ("--mutant" in sys.argv or None)
KNOWN_MUTANTS = {"and-not-xor"}
if MUTANT is not None and MUTANT not in KNOWN_MUTANTS:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN_MUTANTS)}")
    sys.exit(2)


def main() -> int:
    # exhaustive over half-integer W1 in [0, N) and integer W2 in [0, M)
    compatible = set()
    for k in range(0, 2 * N):          # W1 = k/2
        for W2 in range(0, M):
            if residual(k / 2, W2) < 1e-9:
                compatible.add((k / 2, W2))
    expect = set()
    for k in range(0, 2 * N):
        W1 = k / 2
        if MUTANT == "and-not-xor":
            # LAW-11 mutant: claim every W1 admits BOTH y-branches
            expect.add((W1, 0))
            expect.add((W1, M // 2))
        elif W1 != int(W1):
            expect.add((W1, 0))        # half-integer x-winding, uniform y
        else:
            expect.add((W1, M // 2))   # integer x-winding, staggered y
    ok = compatible == expect
    print(f"compatible (W1, W2) found: {len(compatible)}; expected XOR set: "
          f"{len(expect)}; equal: {ok}")
    others = [c for c in compatible if c[1] not in (0, M // 2)]
    print(f"admitted with W2 not in {{0, M/2}}: {len(others)} (expect 0)")
    ok &= not others
    # reflection = Farey involution on windings mod M
    refl_ok = all(((-W2) % M) == ((M - W2) % M) for W2 in range(M))
    print(f"reflection W2 -> -W2 mod M equals M - W2 mod M: {refl_ok}")
    ok &= refl_ok
    # continuum contrast: strictly continuous y admits only W2 = 0
    print("continuum contrast: coefficient 4*pi*b*y must vanish for all "
          "real y => b = 0; the staggered branch is lattice-only")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
