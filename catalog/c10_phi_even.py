"""Euler's phi(q) is even for every q > 2, because p <-> q - p pairs the residues coprime to q without fixed points.
Source: Hardy & Wright ch. V. Mutant: claim evenness for all q >= 1 (phi(1) = phi(2) = 1)."""
import math, sys
from _common import mutant_flag, finish

phi = lambda q: sum(1 for p in range(1, q + 1) if math.gcd(p, q) == 1)
start = 1 if mutant_flag() else 3
bad = [q for q in range(start, 300) if phi(q) % 2]
fixed = [q for q in range(3, 300) if any(2 * p == q and math.gcd(p, q) == 1 for p in range(1, q))]
ok = not bad and not fixed
sys.exit(finish(ok, f"odd phi(q) for q >= {start}: {bad[:5]}; involution fixed points for q>2: {fixed}"))
