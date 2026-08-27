#!/usr/bin/env python3
"""P-7 registered computation: the Fibonacci flux ladder (8,13) ..
(89,144) through the validated Bloch construction, scored against
p7_registration.json. Helper functions repeat p7_derive.py's logic
(module-level script, not importable without executing)."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p7_registration.json").read_text())
TOL = REG["jacobi_tol"]


def jacobi_eigs(A, tol=TOL, max_sweeps=40):
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < tol:
            break
        thr_skip = tol / (n * n)
        for p in range(n - 1):
            ap = a[p]
            for q_ in range(p + 1, n):
                if abs(ap[q_]) < thr_skip:
                    continue
                aq = a[q_]
                t = 0.5 * math.atan2(2 * ap[q_], aq[q_] - ap[p]) \
                    if ap[p] != aq[q_] else math.pi / 4
                c, s_ = math.cos(t), math.sin(t)
                for k in range(n):
                    x, y = ap[k], aq[k]
                    ap[k], aq[k] = c * x - s_ * y, s_ * x + c * y
                for k in range(n):
                    row = a[k]
                    x, y = row[p], row[q_]
                    row[p], row[q_] = c * x - s_ * y, s_ * x + c * y
    off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
    return sorted(a[i][i] for i in range(n)), off


def bloch(p, q, corner, k2):
    if q == 2:
        d = [2 * math.cos(2 * math.pi * p * n / q + k2) for n in (1, 2)]
        o = 1 + corner
        return [[d[0], o], [o, d[1]]]
    H = [[0.0] * q for _ in range(q)]
    for n in range(q):
        H[n][n] = 2 * math.cos(2 * math.pi * p * (n + 1) / q + k2)
    for n in range(q - 1):
        H[n][n + 1] = H[n + 1][n] = 1.0
    H[0][q - 1] = H[q - 1][0] = corner
    return H


def bandwidth(p, q):
    e1, r1 = jacobi_eigs(bloch(p, q, +1.0, 0.0))
    e2, r2 = jacobi_eigs(bloch(p, q, -1.0, math.pi / q))
    edges = sorted(e1 + e2)
    bands = [(edges[2 * i], edges[2 * i + 1]) for i in range(len(edges) // 2)]
    S = sum(b - a for a, b in bands)
    gaps = [bands[i + 1][0] - bands[i][1] for i in range(len(bands) - 1)]
    return S, gaps, max(r1, r2)


def main():
    B = REG["bands"]
    out = {"clauses": {}, "detail": {}}

    # (a) anchors reproduced
    S2, g2, r2 = bandwidth(1, 2)
    S3, g3, r3 = bandwidth(1, 3)
    ok_a = (abs(S2 - REG["anchors"]["2"]["S"]) < 1e-10
            and abs(S3 - REG["anchors"]["3"]["S"]) < 1e-10)
    out["clauses"]["a_anchors"] = bool(ok_a)
    out["detail"]["anchors"] = {"S2": S2, "S3": S3}

    # ladder
    ok_b = True
    ladder = {}
    for (p, q) in REG["ladder"]:
        S, gaps, resid = bandwidth(p, q)
        odd = q % 2 == 1
        if resid > B["jacobi_residual_max"]:
            ladder[str(q)] = {"S": S, "resid": resid, "voided": True}
            continue
        if odd:
            parity_ok = min(gaps) > B["closed_gap_eps"]
        else:
            mid = (q - 1) // 2          # q even -> q-1 gaps, single central
            central = gaps[mid]
            others_min = min(g for i, g in enumerate(gaps) if i != mid)
            parity_ok = central < B["closed_gap_eps"] and others_min > B["closed_gap_eps"]
        ladder[str(q)] = {"S": S, "qS": q * S, "min_gap": min(gaps),
                          "resid": resid, "parity_ok": bool(parity_ok)}
        ok_b = ok_b and parity_ok
        print(f"q={q}: S = {S:.6f}, qS = {q * S:.4f}, min gap {min(gaps):.2e}, "
              f"residual {resid:.1e}, parity {'ok' if parity_ok else 'FAIL'}")
    out["clauses"]["b_parity"] = bool(ok_b)
    out["detail"]["ladder"] = ladder

    # (c) plateau on the terminal pair
    qS89 = ladder["89"]["qS"]
    qS144 = ladder["144"]["qS"]
    pair_mean = 0.5 * (qS89 + qS144)
    ok_c = abs(pair_mean - REG["thouless"]) < B["plateau_abs"]
    out["clauses"]["c_plateau"] = bool(ok_c)
    out["detail"]["plateau"] = {"pair_mean": pair_mean, "thouless": REG["thouless"],
                                "dev": pair_mean - REG["thouless"]}

    # (d) the ln phi clock
    slope = math.log(ladder["89"]["S"] / ladder["144"]["S"])
    ok_d = abs(slope - REG["ln_phi"]) < B["slope_abs"]
    out["clauses"]["d_lnphi_clock"] = bool(ok_d)
    out["detail"]["clock"] = {"slope": slope, "ln_phi": REG["ln_phi"],
                              "dev": slope - REG["ln_phi"]}

    changes = (abs(pair_mean - REG["thouless"]) > B["plateau_kill"]
               or abs(slope - REG["ln_phi"]) > B["slope_kill"]
               or not ok_b)
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p7_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"plateau pair mean {pair_mean:.4f} vs {REG['thouless']:.4f}; "
          f"clock slope {slope:.5f} vs ln phi {REG['ln_phi']:.5f}")
    print(f"changes-my-mind fired: {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
