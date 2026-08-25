#!/usr/bin/env python3
"""P-18 registered computation: lowest 80 Dirichlet eigenvalues of the
C2 (quintic smoothstep) sramp/szramp pair AND the P-14 linear
ramp/zramp pair (positive control), at n = 1499 and 2999, by
Sturm-sequence bisection, scored against p18_registration.json.
The helper functions repeat p18_derive.py's logic (that file is a
module-level script and cannot be imported without executing it)."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p18_registration.json").read_text())
L = REG["L"]
X0, X1, C_MIN = REG["X0"], REG["X1"], REG["C_MIN"]
DX = X1 - X0
T_TOT = REG["T_total"]
VBAR_S = REG["Vbar_s"]
B_LIN = REG["linear"]["B"]
VBAR_LIN = REG["linear"]["Vbar"]
T_LIN = 2113.5532333438687          # P-14 pin (p14_registration.json)


def c_smooth(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    u = (x - X0) / DX
    return 1.0 - 0.5 * (u * u * u * (10.0 + u * (-15.0 + 6.0 * u)))


def c_linear(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    return 1.0 + B_LIN * (x - X0)


def chain(c_of, kind, n):
    a = L / (n + 1)
    if kind == "ramp":                       # Z = 1/c
        rho = lambda xx: 1.0 / c_of(xx) ** 2   # noqa: E731
        Tt = lambda xx: 1.0                    # noqa: E731
    else:                                    # Z = 1
        rho = lambda xx: 1.0 / c_of(xx)        # noqa: E731
        Tt = lambda xx: c_of(xx)               # noqa: E731
    m = [a * rho(i * a) for i in range(1, n + 1)]
    J = [Tt((i + 0.5) * a) / a for i in range(0, n + 1)]
    return m, J


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


def lowest_eigs(c_of, kind, n, kmax):
    m, J = chain(c_of, kind, n)
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


def richardson_delta(c_of, grids, kmax):
    eig = {}
    for kind in ("ramp", "zramp"):
        for n in grids:
            eig[(kind, n)] = lowest_eigs(c_of, kind, n, kmax)
            print(f"  solved {kind} n={n}: omega_1^2 = {eig[(kind, n)][0]:.6e}")
    delta = {n: [eig[("ramp", n)][k] - eig[("zramp", n)][k] for k in range(kmax)]
             for n in grids}
    d_ext = [(4 * delta[grids[1]][k] - delta[grids[0]][k]) / 3.0 for k in range(kmax)]
    return eig, d_ext


def main():
    kmax = REG["n_eigs"]
    grids = REG["grids"]
    tol = REG["tolerances"]
    k_lo, k_hi = REG["k_window"]
    out = {"clauses": {}, "detail": {}}

    print("C2 smoothstep pair:")
    eig_s, dext_s = richardson_delta(c_smooth, grids, kmax)
    print("linear control pair:")
    eig_l, dext_l = richardson_delta(c_linear, grids, kmax)

    # (a) Weyl over k in [5, 60], fine grid, both C2 profiles
    weyl = {}
    weyl_ok = True
    for kind in ("ramp", "zramp"):
        devs = [abs(math.sqrt(eig_s[(kind, grids[1])][k - 1]) * T_TOT / (k * math.pi) - 1.0)
                for k in range(k_lo, 61)]
        weyl[kind] = max(devs)
        weyl_ok = weyl_ok and max(devs) < tol["weyl_rel"]
    out["clauses"]["a_weyl"] = bool(weyl_ok)
    out["detail"]["weyl_worst_k5_60"] = weyl

    # (b) not isospectral
    max_delta = max(abs(x) for x in dext_s)
    out["clauses"]["b_not_isospectral"] = bool(max_delta > tol["not_isospectral_min"])
    out["detail"]["max_abs_delta_ext"] = max_delta

    # (c) per-mode match, RMS over the window against the pinned shifts
    resid = [dext_s[k - 1] - REG["shifts"][str(k)] for k in range(k_lo, k_hi + 1)]
    rms_s = math.sqrt(sum(r * r for r in resid) / len(resid))
    out["clauses"]["c_shift_match"] = bool(rms_s < tol["shift_rms_over_vbar"] * VBAR_S)
    out["detail"]["rms_over_vbar_s"] = rms_s / VBAR_S

    # (d) the derived sign flip at k = 1
    out["clauses"]["d_sign_flip"] = bool(dext_s[0] < -4e-8)
    out["detail"]["delta_ext_1"] = dext_s[0]
    out["detail"]["shift_1_pinned"] = REG["shifts"]["1"]

    # (e) window mean within 3 percent
    mean_meas = sum(dext_s[k_lo - 1:k_hi]) / (k_hi - k_lo + 1)
    mean_pred = sum(REG["shifts"][str(k)] for k in range(k_lo, k_hi + 1)) / (k_hi - k_lo + 1)
    out["clauses"]["e_mean"] = bool(abs(mean_meas - mean_pred) < tol["mean_rel"] * mean_pred)
    out["detail"]["mean_meas"] = mean_meas
    out["detail"]["mean_pred"] = mean_pred

    # (f) positive control: the linear pair reproduces P-14's failure
    p14_shifts = json.loads((HERE / "p14_registration.json").read_text())["shifts"]
    resid_l = [dext_l[k - 1] - p14_shifts[str(k)] for k in range(k_lo, k_hi + 1)]
    rms_l = math.sqrt(sum(r * r for r in resid_l) / len(resid_l))
    improvement = (rms_l / VBAR_LIN) / (rms_s / VBAR_S)
    out["clauses"]["f_control"] = bool(rms_l > tol["control_rms_over_vbar_min"] * VBAR_LIN
                                       and improvement > tol["improvement_factor_min"])
    out["detail"]["control_rms_over_vbar_lin"] = rms_l / VBAR_LIN
    out["detail"]["improvement_factor"] = improvement

    out["detail"]["delta_ext_samples"] = {str(k): dext_s[k - 1] for k in
                                          (1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80)}
    out["detail"]["shift_pred_samples"] = {str(k): REG["shifts"][str(k)] for k in
                                           (1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80)}

    changes = (rms_s > 1.0 * VBAR_S) or (rms_l < 1.5 * VBAR_LIN) or (dext_s[0] > 0)
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p18_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"C2 RMS/Vbar_s = {rms_s / VBAR_S:.3f}; control RMS/Vbar_lin = {rms_l / VBAR_LIN:.3f}; "
          f"improvement x{improvement:.1f}")
    print(f"Delta_1 = {dext_s[0]:.3e} vs pinned {REG['shifts']['1']:.3e}; "
          f"window mean {mean_meas:.6e} vs {mean_pred:.6e}")
    print(f"changes-my-mind fired: {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
