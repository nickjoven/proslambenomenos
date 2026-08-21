#!/usr/bin/env python3
"""P-1 checkable: the audit's 1,764-pairs-both-ways figure, recomputed
from the definition rather than quoted.

Convention that reproduces it: mediant insertion between endpoints 0/1
and 1/1 for 6 rounds gives 63 interior fractions; among them the
denominator-parity classes split 42 odd / 21 even, and the numerator
classes split 42/21 as well, so ORDERED pairs with differing parity
number 2 * 42 * 21 = 1764 under BOTH rules - while the allowed SETS
differ (the discriminating fact behind P-1's under-determination
expectation). Exit 0 iff all counts reproduce and the sets differ.
"""

import sys


def depth6():
    level = [(0, 1), (1, 1)]
    for _ in range(6):
        nxt = [level[0]]
        for a, b in zip(level, level[1:]):
            nxt.append((a[0] + b[0], a[1] + b[1]))
            nxt.append(b)
        level = nxt
    return [f for f in level if f not in ((0, 1), (1, 1))]


def main() -> int:
    fr = depth6()
    n = len(fr)
    q_odd = [f for f in fr if f[1] % 2]
    p_odd = [f for f in fr if f[0] % 2]
    q_pairs = {(a, b) for a in fr for b in fr if (a[1] + b[1]) % 2}
    p_pairs = {(a, b) for a in fr for b in fr if (a[0] + b[0]) % 2}
    ok = (n == 63 and len(q_odd) == 42 and len(p_odd) == 42
          and len(q_pairs) == 1764 and len(p_pairs) == 1764
          and q_pairs != p_pairs)
    print(f"interior fractions after 6 rounds: {n} (expect 63)")
    print(f"q-parity split: {len(q_odd)} odd / {n - len(q_odd)} even "
          f"(expect 42/21); p-parity split: {len(p_odd)}/{n - len(p_odd)}")
    print(f"ordered XOR pairs: q-rule {len(q_pairs)}, p-rule {len(p_pairs)} "
          f"(expect 1764 both)")
    print(f"rule sets identical: {q_pairs == p_pairs} (expect False; "
          f"symmetric difference {len(q_pairs ^ p_pairs)})")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
