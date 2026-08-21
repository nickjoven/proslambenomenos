#!/usr/bin/env python3
"""D4 hole (b): can the nontrivial spatial sectors - (half-integer
x-winding, uniform y) and (integer x-winding, staggered y), the two
XOR classes of the gradient theorem-let - be STABILIZED under the
pinned dynamics at stronger coupling, so their temporal locking can
be measured rather than found empty by default? Seeds each sector,
sweeps Omega at J in {1.2, 2.0}, K = 1.0; records retention of the
seeded (bx, by) class and the locked rationals per class. Writes
d4_sector_results.json."""

import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from d4_2d_pairs import run  # noqa: E402

TOL = 5e-4


def main():
    grid = 100
    out = []
    print(f"{'J':>4} {'seed':>10} | {'retained':>8} {'locked':>7} "
          f"{'locked&retained':>16} | q-parity of locked&retained")
    for J in (1.2, 2.0):
        for branch, want in (("uniform", (1, 0)), ("staggered", (0, 1))):
            retained = locked = both = 0
            qpar = {"odd": 0, "even": 0}
            for k in range(grid + 1):
                Om = k / grid
                rho, bx, by = run(Om, 1.0, J, branch)
                pq = None
                for q in range(1, 9):
                    p = round(rho * q)
                    if abs(rho - p / q) < TOL and math.gcd(p, q) == 1 and 0 <= p <= q:
                        pq = (p, q)
                        break
                ret = (bx, by) == want
                retained += ret
                locked += pq is not None
                if ret and pq:
                    both += 1
                    qpar["odd" if pq[1] % 2 else "even"] += 1
                out.append({"J": J, "branch": branch, "Omega": Om, "rho": rho,
                            "bx": bx, "by": by, "pq": pq})
            print(f"{J:>4} {branch:>10} | {retained:>8} {locked:>7} "
                  f"{both:>16} | odd {qpar['odd']}, even {qpar['even']}")
    Path(__file__).with_name("d4_sector_results.json").write_text(json.dumps(out))
    print("wrote d4_sector_results.json")


if __name__ == "__main__":
    main()
