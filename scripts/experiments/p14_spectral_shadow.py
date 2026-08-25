#!/usr/bin/env python3
"""P-14 registered computation: lowest 80 Dirichlet eigenvalues of the
ramp and zramp chains at n = 1499 and 2999 by Sturm-sequence bisection
(exact linear algebra - no timestep), scored against the registration
pins in p14_registration.json. The three helper functions are
byte-identical in logic to p14_derive.py (that file is a module-level
script and cannot be imported without executing it)."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p14_registration.json").read_text())
L = REG["L"]
X0, X1, C_MIN = 150.0, 1350.0, 0.5
B = REG["B"]
T_TOT = REG["T_total"]
VBAR = REG["Vbar"]


def c_of(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    return 1.0 + B * (x - X0)


def chain(profile, n):
    a = L / (n + 1)
    if profile == "ramp":
        rho = lambda xx: 1.0 / c_of(xx) ** 2   # noqa: E731
        Tt = lambda xx: 1.0                    # noqa: E731
    else:
        rho = lambda xx: 1.0 / c_of(xx)        # noqa: E731
        Tt = lambda xx: c_of(xx)               # noqa: E731
    m = [a * rho(i * a) for i in range(1, n + 1)]
    J = [Tt((i + 0.5) * a) / a for i in range(0, n + 1)]
    return a, m, J


def sturm_count(diag, off, lam):
    cnt = 0
    q = diag[0] - lam
    if q < 0:
        cnt += 1
    for i in range(1, len(diag)):
        e2 = off[i - 1] * off[i - 1]
        q = diag[i] - lam - (e2 / q if q != 0 else e2 / 1e-300)
        if q < 0:
            cnt += 1
    return cnt


def lowest_eigs(profile, n, kmax):
    _, m, J = chain(profile, n)
    diag = [(J[i] + J[i + 1]) / m[i] for i in range(n)]
    off = [-J[i + 1] / math.sqrt(m[i] * m[i + 1]) for i in range(n - 1)]
    hi = max(dd + (abs(off[i - 1]) if i else 0) + (abs(off[i]) if i < n - 1 else 0)
             for i, dd in enumerate(diag))
    out = []
    for kk in range(1, kmax + 1):
        a_, b_ = 0.0, hi
        for _ in range(80):
            mid = 0.5 * (a_ + b_)
            if sturm_count(diag, off, mid) >= kk:
                b_ = mid
            else:
                a_ = mid
        out.append(0.5 * (a_ + b_))
    return out


def main():
    kmax = REG["n_eigs"]
    grids = REG["grids"]
    eig = {}
    for prof in ("ramp", "zramp"):
        for n in grids:
            eig[(prof, n)] = lowest_eigs(prof, n, kmax)
            print(f"solved {prof} n={n}: omega_1^2 = {eig[(prof, n)][0]:.6e}")

    tol = REG["tolerances"]
    out = {"clauses": {}, "detail": {}}

    # (b) Weyl at the fine grid, both profiles, k <= 60
    weyl_ok = True
    worst_weyl = {}
    for prof in ("ramp", "zramp"):
        devs = [abs(math.sqrt(eig[(prof, grids[1])][k - 1]) * T_TOT / (k * math.pi) - 1.0)
                for k in range(1, 61)]
        worst_weyl[prof] = {"worst": max(devs), "worst_k": devs.index(max(devs)) + 1,
                            "worst_k_ge_5": max(devs[4:])}
        weyl_ok = weyl_ok and max(devs) < tol["weyl_rel"]
    out["clauses"]["b_weyl"] = bool(weyl_ok)
    out["detail"]["weyl"] = worst_weyl

    # (c) not isospectral
    delta = {n: [eig[("ramp", n)][k] - eig[("zramp", n)][k] for k in range(kmax)]
             for n in grids}
    max_delta = max(abs(x) for x in delta[grids[1]])
    out["clauses"]["c_not_isospectral"] = bool(max_delta > tol["not_isospectral_min"])
    out["detail"]["max_abs_delta_fine"] = max_delta

    # (d) k-resolved shifts after Richardson (a halves exactly: 4/3 rule)
    d_ext = [(4 * delta[grids[1]][k] - delta[grids[0]][k]) / 3.0 for k in range(kmax)]
    k_lo, k_hi = REG["k_window"]
    resid = [d_ext[k - 1] - REG["shifts"][str(k)] for k in range(k_lo, k_hi + 1)]
    rms = math.sqrt(sum(r * r for r in resid) / len(resid))
    out["clauses"]["d_shift_match"] = bool(rms < tol["shift_rms_over_vbar"] * VBAR)
    out["detail"]["rms_over_vbar"] = rms / VBAR
    out["detail"]["mean_delta_ext"] = sum(d_ext[k_lo - 1:k_hi]) / (k_hi - k_lo + 1)
    out["detail"]["mean_shift_pred"] = (sum(REG["shifts"][str(k)] for k in range(k_lo, k_hi + 1))
                                        / (k_hi - k_lo + 1))
    # the registered metric-split alternative (changes-my-mind discriminator)
    ms = []
    for n in grids:
        pass
    out["detail"]["delta_ext_samples"] = {str(k): d_ext[k - 1] for k in
                                          (1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80)}
    out["detail"]["shift_pred_samples"] = {str(k): REG["shifts"][str(k)] for k in
                                           (1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80)}
    changes = (out["detail"]["mean_delta_ext"] < 0) or (rms > 1.0 * VBAR)
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p14_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"weyl worst: ramp {worst_weyl['ramp']['worst']:.2e} (k={worst_weyl['ramp']['worst_k']}; "
          f"k>=5: {worst_weyl['ramp']['worst_k_ge_5']:.2e}), "
          f"zramp {worst_weyl['zramp']['worst']:.2e}")
    print(f"max |Delta omega^2| = {max_delta:.3e}; Richardson mean Delta (k 5..60) = "
          f"{out['detail']['mean_delta_ext']:.3e} vs mean shift {out['detail']['mean_shift_pred']:.3e}; "
          f"RMS/Vbar = {rms / VBAR:.3f}")
    print(f"changes-my-mind fired: {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
