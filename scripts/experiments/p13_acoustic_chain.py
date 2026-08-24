#!/usr/bin/env python3
"""P-13 experiment: integrate the exact chain for the six registered
profiles and score every registered clause against the numbers pinned
at registration (p13_registration.json). Stdlib only; run AFTER the
registration commit - this file postdates the P-13 entry by
construction (git ordering is the attestation).

Measurements (as registered):
  arrival(j)   time of peak |u_j| at the pinned checkpoints
  cross(j)     first time |u_j| >= 0.1 (threshold clause + width)
  E_in         total energy at t = 100 (pulse launched, front still
               left of every inhomogeneity: ramp starts at 150,
               junctions sit at 750)
  R_hat        energy left of the stated cut at the stated time,
               over E_in:  jc/jz: cut 700, t = 1000;
               ramp/zramp: cut 300, t = 1200
Post-hoc diagnostic (labelled, not registered): a step drive on the
control profile to measure the sharp-front width exponent, since the
half-sine pulse's intrinsic width may dominate the registered Airy
clause. It rescues nothing; the registered clause is scored as
registered.
"""
import json
import math
import sys
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p13_profiles as P  # noqa: E402

REG = json.loads((HERE / "p13_registration.json").read_text())
TAU = REG["pulse"]["tau"]
DT = REG["dt"]
CHK = REG["checkpoints"]
THRESH = 0.1
SHUFFLE_BLOCK, SHUFFLE_SEED = 100, 7


def energy(u, v, m, J, lo, hi):
    """Total energy in sites lo..hi-1 and the bonds among them."""
    e = sum(0.5 * m[i] * v[i] * v[i] for i in range(lo, hi))
    e += sum(0.5 * J[i] * (u[i + 1] - u[i]) ** 2 for i in range(lo, hi - 1))
    return e


def integrate(name, dt, drive, t_end, e_cut=None, e_time=None, extra_thresh=None):
    """Euler-Cromer chain integration. Returns peaks, crossings,
    E_in, E_left (if requested), and extra threshold crossings."""
    m, J = P.profile(name)
    n = P.N_SITES
    u = [0.0] * n
    v = [0.0] * n
    dt_over_m = [dt / mi for mi in m]
    peaks = {j: (0.0, 0.0) for j in CHK}
    cross = {j: None for j in CHK}
    xtra = {j: {th: None for th in (extra_thresh or [])} for j in CHK}
    e_in = e_left = None
    steps = int(t_end / dt)
    t_ein = int(100.0 / dt)
    t_ecut = int(e_time / dt) if e_time else -1
    rng_j = range(1, n - 1)
    for s in range(steps + 1):
        t = s * dt
        u[0] = drive(t)
        for i in rng_j:
            v[i] += dt_over_m[i] * (J[i] * (u[i + 1] - u[i]) + J[i - 1] * (u[i - 1] - u[i]))
        for i in rng_j:
            u[i] += dt * v[i]
        for j in CHK:
            au = abs(u[j])
            if au > peaks[j][0]:
                peaks[j] = (au, t)
            if cross[j] is None and au >= THRESH:
                cross[j] = t
            for th in xtra[j]:
                if xtra[j][th] is None and au >= th:
                    xtra[j][th] = t
        if s == t_ein:
            e_in = energy(u, v, m, J, 0, n)
        if s == t_ecut:
            e_left = energy(u, v, m, J, 0, e_cut)
    return {"peaks": {j: peaks[j][1] for j in CHK},
            "peak_amp": {j: peaks[j][0] for j in CHK},
            "cross": cross, "xtra": xtra, "E_in": e_in, "E_left": e_left}


def pulse(t):
    return math.sin(math.pi * t / TAU) if t <= TAU else 0.0


def step_drive(t):
    return 1.0


def t_end_for(name):
    m, J = P.profile(name)
    return P.eikonal(m, J, 0, 1450) + TAU + 40.0


def one_run(job):
    name, dt, kind = job
    if kind == "arrivals":
        cut, etime = (300, 1200.0) if name in ("ramp", "zramp") else (None, None)
        r = integrate(name, dt, pulse, t_end_for(name), e_cut=cut, e_time=etime)
    elif kind == "junction":
        r = integrate(name, dt, pulse, 1000.0, e_cut=700, e_time=1000.0)
    elif kind == "step":
        r = integrate(name, dt, step_drive, 1520.0, extra_thresh=[0.6])
    return (name, dt, kind), r


def fit_line(xs, ys):
    """Least squares y = a + b x; returns (a, b)."""
    nn = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    b = (nn * sxy - sx * sy) / (nn * sxx - sx * sx)
    return (sy - b * sx) / nn, b


def shuffled_eikonal(name):
    """Block-shuffled per-site delays (blocks of SHUFFLE_BLOCK, seeded):
    same multiset of local delays, different arrangement - the registered
    discriminator for 'the arrangement is what the arrival curve reads'."""
    import random
    m, J = P.profile(name)
    delays = [1.0 / P.c_site(m, J, i) for i in range(P.N_SITES - 1)]
    blocks = [delays[i:i + SHUFFLE_BLOCK] for i in range(0, len(delays), SHUFFLE_BLOCK)]
    random.Random(SHUFFLE_SEED).shuffle(blocks)
    flat = [x for bl in blocks for x in bl]
    out, acc, k = {}, 0.0, 0
    for j in CHK:
        while k < j:
            acc += flat[k]
            k += 1
        out[j] = acc
    return out


def rms_rel(meas, pred):
    vals = [((meas[j] - pred[j]) / pred[j]) ** 2 for j in CHK]
    return math.sqrt(sum(vals) / len(vals))


def main():
    jobs = []
    for dt in (DT, DT / 2):
        for name in ("control", "ramp", "lens", "zramp"):
            jobs.append((name, dt, "arrivals"))
        for name in ("jc", "jz"):
            jobs.append((name, dt, "junction"))
    jobs.append(("control", DT, "step"))          # post-hoc diagnostic
    with Pool(min(len(jobs), 13)) as pool:
        runs = dict(pool.map(one_run, jobs))

    tol = REG["tolerances"]
    out = {"params": {"dt": DT, "tau": TAU, "thresh": THRESH,
                      "shuffle": {"block": SHUFFLE_BLOCK, "seed": SHUFFLE_SEED}},
           "clauses": {}, "detail": {}}

    def score(dt):
        res = {}
        ctrl = runs[("control", dt, "arrivals")]
        t0, slope = fit_line(CHK, [ctrl["peaks"][j] for j in CHK])
        res["control_speed"] = 1.0 / slope
        res["control_t0"] = t0
        res["a_speed_ok"] = abs(1.0 / slope - 1.0) < tol["control_speed_rel"]
        # registered width clause: peak-minus-cross width vs site, log-log slope
        widths = [ctrl["peaks"][j] - ctrl["cross"][j] for j in CHK]
        _, p_w = fit_line([math.log(j) for j in CHK], [math.log(w) for w in widths])
        res["airy_exponent"] = p_w
        lo, hi = tol["airy_exponent_band"]
        res["a_airy_ok"] = lo <= p_w <= hi
        # eikonal clauses
        for name in ("ramp", "lens", "zramp"):
            m, J = P.profile(name)
            pred = {j: t0 + P.eikonal(m, J, 0, j) for j in CHK}
            meas = runs[(name, dt, "arrivals")]["peaks"]
            r = rms_rel(meas, pred)
            res[f"{name}_rms"] = r
            res[f"{name}_rms_ok"] = r < tol["eikonal_rms_rel"]
            if name in ("ramp", "lens"):
                shuf = shuffled_eikonal(name)
                rs = rms_rel(meas, {j: t0 + shuf[j] for j in CHK})
                res[f"{name}_shuffle_ratio"] = rs / r if r > 0 else float("inf")
                res[f"{name}_shuffle_ok"] = rs / r >= tol["shuffle_ratio_min"]
        # scattering clauses
        for name in ("jc", "jz"):
            r = runs[(name, dt, "junction")]
            res[f"{name}_R"] = r["E_left"] / r["E_in"]
        res["jc_R_ok"] = abs(res["jc_R"] - REG["fresnel"]["jc"]) < tol["junction_R_abs"]
        res["jz_R_ok"] = res["jz_R"] < tol["quiet_R_max"]
        for name in ("ramp", "zramp"):
            r = runs[(name, dt, "arrivals")]
            res[f"{name}_R"] = r["E_left"] / r["E_in"]
        res["zramp_R_ok"] = res["zramp_R"] < tol["quiet_R_max"]
        return res

    s1, s2 = score(DT), score(DT / 2)
    reported = [k for k in s1 if not k.endswith("_ok")]
    conv = max(abs(s1[k] - s2[k]) / max(1e-12, abs(s2[k])) for k in reported
               if isinstance(s1[k], float) and s1[k] == s1[k])
    out["detail"]["dt"] = s1
    out["detail"]["dt_half"] = s2
    out["clauses"] = {
        "a_speed": s1["a_speed_ok"], "a_airy": s1["a_airy_ok"],
        "b_ramp": s1["ramp_rms_ok"], "b_lens": s1["lens_rms_ok"],
        "b_shuffle": s1["ramp_shuffle_ok"] and s1["lens_shuffle_ok"],
        "c_jc": s1["jc_R_ok"], "c_jz": s1["jz_R_ok"],
        "c_zramp": s1["zramp_R_ok"] and s1["zramp_rms_ok"],
        "d_convergence": conv < tol["dt_halving_rel"],
    }
    out["detail"]["max_dt_halving_rel_change"] = conv
    out["detail"]["dt_halving_per_quantity"] = {
        k: abs(s1[k] - s2[k]) / max(1e-12, abs(s2[k])) for k in reported
        if isinstance(s1[k], float) and s1[k] == s1[k]}
    out["_arrivals"] = {name: {str(j): runs[(name, DT, "arrivals")]["peaks"][j] for j in CHK}
                       for name in ("control", "ramp", "lens", "zramp")}
    # post-hoc diagnostic: sharp-front width exponent under a step drive
    stp = runs[("control", DT, "step")]
    sw = [stp["xtra"][j][0.6] - stp["cross"][j] for j in CHK
          if stp["xtra"][j][0.6] is not None and stp["cross"][j] is not None]
    sj = [j for j in CHK if stp["xtra"][j][0.6] is not None and stp["cross"][j] is not None]
    if len(sw) >= 6:
        _, p_step = fit_line([math.log(j) for j in sj], [math.log(w) for w in sw])
        out["detail"]["posthoc_step_front_exponent"] = p_step
    changes_my_mind = ((s1["zramp_R"] > 0.05) or (s1["jz_R"] > 0.05)
                       or (s1["ramp_rms"] > 0.05)
                       or (abs(s1["jc_R"] - REG["fresnel"]["jc"]) > 0.15))
    out["changes_my_mind_fired"] = changes_my_mind
    (HERE / "p13_results.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    for k, vv in out["clauses"].items():
        print(f"clause {k}: {'as registered' if vv else 'NOT as registered'}")
    print(f"control speed {s1['control_speed']:.5f}, t0 {s1['control_t0']:.2f}; "
          f"airy exp {s1['airy_exponent']:.3f}"
          + (f"; step-front exp {out['detail'].get('posthoc_step_front_exponent', float('nan')):.3f}"
             if "posthoc_step_front_exponent" in out["detail"] else ""))
    print(f"rms: ramp {s1['ramp_rms']:.4f} lens {s1['lens_rms']:.4f} zramp {s1['zramp_rms']:.4f}; "
          f"shuffle ratios ramp {s1['ramp_shuffle_ratio']:.1f} lens {s1['lens_shuffle_ratio']:.1f}")
    print(f"R: jc {s1['jc_R']:.4f} (fresnel {REG['fresnel']['jc']:.3f}) jz {s1['jz_R']:.5f} "
          f"zramp {s1['zramp_R']:.5f} ramp {s1['ramp_R']:.5f}; dt-halving max rel {conv:.2e}")
    print(f"changes-my-mind fired: {changes_my_mind}")


if __name__ == "__main__":
    main()
