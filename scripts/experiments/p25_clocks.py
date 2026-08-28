#!/usr/bin/env python3
"""P-25 registered computation (with its derive block up front): the
matched clocks - continuous-time vs even-step walk d_s on fresh
sprinklings, with the agreement band derived from the exact
Poissonization identity. Reuses P-16's construction by source-level
import (p16_walk guards its main)."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
src = (HERE / "p16_walk.py").read_text().replace(
    'if __name__ == "__main__":', 'if False:')
ns = {"__name__": "p16_walk_mod", "__file__": str(HERE / "p16_walk.py")}
exec(compile(src, "p16_walk.py", "exec"), ns)
sprinkle, hasse_links = ns["sprinkle"], ns["hasse_links"]
walk_spectrum, ds_ct, ds_disc = ns["walk_spectrum"], ns["ds_ct"], ns["ds_disc"]

SEED0 = 251251
CELLS = [(64, 0), (64, 1), (128, 0), (128, 1)]
NSTEPS = [4, 6, 8, 12, 16, 24]


def derive_block():
    """EQ: the Poissonization identity per-eigenvalue, exact algebra."""
    lam = 0.37
    t = 9.0
    lhs = math.exp(-t * lam)
    rhs = math.exp(-t) * sum((t ** k) * ((1 - lam) ** k) / math.factorial(k)
                             for k in range(120))
    ok = abs(lhs - rhs) < 1e-14
    print(f"EQ Poissonization: e^(-t lambda) vs e^(-t) sum t^k (1-lambda)^k/k! "
          f"-> |diff| = {abs(lhs - rhs):.1e}  {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    if not derive_block():
        return 1
    out = {"clauses": {}, "detail": {}}
    ok_all = ok_tail = True
    for (N, r) in CELLS:
        pts = sprinkle(N, SEED0 + 977 * N + r)
        links = hasse_links(pts)
        lams, deg, iso = walk_spectrum(N, links)
        mus = [1 - x for x in lams]

        def pbar(m):
            return sum(mu ** m for mu in mus) / N

        rows = {}
        for n in NSTEPS:
            v_ct = ds_ct(float(n), lams)
            v_dc = ds_disc(lams, N, n)
            # derived smearing band: n |D2 ln Pbar| / 2 + 0.06, D2 the
            # second central difference in step count at n (even steps)
            lp = [math.log(pbar(n - 2)), math.log(pbar(n)), math.log(pbar(n + 2))]
            D2 = (lp[0] - 2 * lp[1] + lp[2]) / 4.0    # per unit step^2
            band = n * abs(D2) / 2.0 * 2.0 + 0.06     # x2: ds is a log-derivative
            diff = abs(v_ct - v_dc)
            good = diff < band
            ok_all = ok_all and diff < 2 * band
            if n >= 16:
                ok_tail = ok_tail and diff < 0.06
            if not good:
                ok_all = ok_all and False
            rows[str(n)] = {"ct": v_ct, "disc": v_dc, "diff": diff,
                            "band": band, "ok": bool(good)}
        out["detail"][f"N{N}_r{r}"] = {"links": len(links), "rows": rows}
        worst = max(rows.values(), key=lambda x: x["diff"] / x["band"])
        print(f"N={N} r={r}: worst diff/band = {worst['diff']:.3f}/{worst['band']:.3f}; "
              f"tail diffs {[f'{rows[str(n)]['diff']:.3f}' for n in (16, 24)]}")
    all_ok = all(v["ok"] for c in out["detail"].values() for v in c["rows"].values())
    out["clauses"]["bands"] = bool(all_ok)
    out["clauses"]["tail"] = bool(ok_tail)
    out["changes_my_mind_fired"] = bool(not (all_ok and ok_tail))
    (HERE / "p25_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"changes-my-mind fired: {out['changes_my_mind_fired']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
