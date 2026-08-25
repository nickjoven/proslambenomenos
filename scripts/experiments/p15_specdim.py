#!/usr/bin/env python3
"""P-15 registered computation: the spectral-dimension instrument.

Three tiers, scored against p15_registration.json:
  (a) a fresh exact implementation (this file, written independently
      of p15_derive.py) must reproduce every pinned anchor to 1e-9;
  (b) a continuous-time random-walk Monte Carlo tier - the route that
      later runs on objects with no computable spectrum - must land
      within 4 derived sigma of the exact P(t) on C_4096({1..6});
  (c,d) the P-14 chains (spectra via the Sturm solver imported from
      p14_spectral_shadow, lowest 250 modes, truncation bounded):
      leading-order blindness |Delta d_s| < 1e-3 in-window, and the
      derived second-order trace drift Delta d_s ~ 2 Vbar t within a
      factor of 2 for t in [300, 1000].
"""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from p14_spectral_shadow import chain, lowest_eigs  # noqa: E402  (guarded module)

REG = json.loads((HERE / "p15_registration.json").read_text())
VBAR = 3.416182e-08          # P-14 registration (p14_registration.json Vbar)


# ---------------- the instrument (fresh implementation) ----------------
def circulant_spectrum(n, S):
    return [sum(2.0 * (1.0 - math.cos(2.0 * math.pi * k * s / n)) for s in S)
            for k in range(n)]


def return_prob(spec, t):
    return sum(math.exp(-l * t) for l in spec) / len(spec)


def ds(spec, t, enforce_window=True):
    """Exact log-derivative spectral dimension; refuses t past the
    window rule t < 0.5/lambda_1 unless told otherwise."""
    lam1 = min(l for l in spec if l > 1e-12)
    if enforce_window and t > 0.5 / lam1:
        return None
    mx = min(l * t for l in spec)
    num = sum(l * math.exp(-(l * t - mx)) for l in spec)
    den = sum(math.exp(-(l * t - mx)) for l in spec)
    return 2.0 * t * num / den


def main():
    out = {"clauses": {}, "detail": {}}

    # (a) anchors
    n = REG["cycle_n"]
    line = circulant_spectrum(n, (1,))
    worst_a = max(abs(ds(line, float(ts)) - v) for ts, v in REG["ds_line_pins"].items())
    dense = circulant_spectrum(n, tuple(REG["dense_circulant"]["S"]))
    worst_a = max(worst_a, max(abs(ds(dense, float(ts), enforce_window=False) - v)
                               for ts, v in REG["dense_circulant"]["crossover_pins"].items()))
    # product additivity re-checked freshly at n = 64
    s1 = circulant_spectrum(64, (1,))
    s2 = [a + b for a in s1 for b in s1]
    worst_a = max(worst_a, abs(ds(s2, 8.0, enforce_window=False)
                               - 2 * ds(s1, 8.0, enforce_window=False)))
    out["clauses"]["a_anchors"] = bool(worst_a < REG["tolerances"]["anchor_abs"])
    out["detail"]["worst_anchor_dev"] = worst_a
    print(f"(a) worst anchor deviation {worst_a:.2e}")

    # (b) Monte Carlo walker tier on C_4096({1..6})
    S = REG["dense_circulant"]["S"]
    steps = [s for s in S] + [-s for s in S]
    rate = float(len(steps))
    t_checks = [0.2, 1.0, 5.0]
    M = 400_000
    rng = random.Random(20260824)
    counts = [0] * len(t_checks)
    t_end = t_checks[-1]
    for _ in range(M):
        pos, tt = 0, 0.0
        ci = 0
        while True:
            tt += -math.log(1.0 - rng.random()) / rate
            while ci < len(t_checks) and tt > t_checks[ci]:
                if pos % n == 0:
                    counts[ci] += 1
                ci += 1
            if ci >= len(t_checks) or tt > t_end:
                break
            pos += steps[int(rng.random() * len(steps))]
    ok_b, rows_b = True, []
    for ci, tc in enumerate(t_checks):
        p_hat = counts[ci] / M
        p_ex = return_prob(dense, tc)
        sig = math.sqrt(p_ex * (1 - p_ex) / M)
        ok_b = ok_b and abs(p_hat - p_ex) < 4 * sig
        rows_b.append(f"t={tc}: MC {p_hat:.5f} vs exact {p_ex:.5f} "
                      f"({abs(p_hat - p_ex) / sig:.2f} sigma)")
    out["clauses"]["b_walkers"] = bool(ok_b)
    out["detail"]["mc"] = rows_b
    print("(b) " + "; ".join(rows_b))

    # (c,d) the P-14 chains
    kmax = 250
    eig = {}
    for prof in ("ramp", "zramp"):
        _, m, J = chain(prof, 1499)
        diag = [(J[i] + J[i + 1]) / m[i] for i in range(1499)]
        off = [-J[i + 1] / math.sqrt(m[i] * m[i + 1]) for i in range(1498)]
        eig[prof] = lowest_eigs_from(diag, off, kmax)
        print(f"chain {prof}: {kmax} modes, omega_1^2 = {eig[prof][0]:.6e}")
    t_grid = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    deltas = {}
    for t in t_grid:
        dr = ds(eig["ramp"], float(t), enforce_window=False)
        dz = ds(eig["zramp"], float(t), enforce_window=False)
        deltas[t] = dr - dz
    max_delta = max(abs(v) for v in deltas.values())
    out["clauses"]["c_leading_blind"] = bool(max_delta < 1e-3)
    ratios = {t: deltas[t] / (2 * VBAR * t) for t in t_grid if t >= 300}
    ok_d = all(0.5 <= r <= 2.0 for r in ratios.values())
    out["clauses"]["d_trace_drift"] = bool(ok_d)
    out["detail"]["deltas"] = {str(t): deltas[t] for t in t_grid}
    out["detail"]["drift_ratios"] = {str(t): ratios[t] for t in ratios}
    print(f"(c) max |Delta d_s| = {max_delta:.2e} over t in [100, 1000]")
    print("(d) Delta d_s / (2 Vbar t): "
          + "; ".join(f"t={t}: {r:.3f}" for t, r in ratios.items()))
    changes = ((out["detail"]["worst_anchor_dev"] > 1e-6)
               or (max_delta > 1e-3)
               or any(r < 0 or r > 5 or r < 0.2 for r in ratios.values()))
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p15_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"changes-my-mind fired: {changes}")
    return 0


def lowest_eigs_from(diag, off, kmax):
    """Sturm bisection (as in p14) on an explicit tridiagonal."""
    n = len(diag)

    def count(lam):
        cnt = 0
        q = diag[0] - lam
        if q < 0:
            cnt += 1
        for i in range(1, n):
            e2 = off[i - 1] * off[i - 1]
            q = diag[i] - lam - (e2 / q if q != 0 else e2 / 1e-300)
            if q < 0:
                cnt += 1
        return cnt

    hi = max(dd + (abs(off[i - 1]) if i else 0) + (abs(off[i]) if i < n - 1 else 0)
             for i, dd in enumerate(diag))
    outv = []
    for kk in range(1, kmax + 1):
        a_, b_ = 0.0, hi
        for _ in range(80):
            mid = 0.5 * (a_ + b_)
            if count(mid) >= kk:
                b_ = mid
            else:
                a_ = mid
        outv.append(0.5 * (a_ + b_))
    return outv


if __name__ == "__main__":
    sys.exit(main())
