#!/usr/bin/env python3
"""P-16 registered computation: sprinkled causal sets, both walk
instruments on the Hasse graph, scored against p16_registration.json
alongside the pinned d'Alembertian curve."""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p16_registration.json").read_text())
B = REG["bands"]


def sprinkle(N, seed):
    rng = random.Random(seed)
    pts = sorted((rng.random(), rng.random()) for _ in range(N))  # sort by u
    return pts


def hasse_links(pts):
    """past[i] = bitmask of causal predecessors (u sorted, so only
    j < i can precede); future[j] built by transposition; link (j, i)
    iff j precedes i with empty interval: past[i] & future[j] == 0."""
    N = len(pts)
    past = [0] * N
    for i in range(N):
        vi = pts[i][1]
        m = 0
        for j in range(i):
            if pts[j][1] < vi:
                m |= (1 << j)
        past[i] = m
    future = [0] * N
    for i in range(N):
        m = past[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            future[j] |= (1 << i)
    links = []
    for i in range(N):
        m = past[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if past[i] & future[j] == 0:
                links.append((j, i))
    return links


def jacobi_eigs(A, tol=1e-10, max_sweeps=40):
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < tol:
            break
        skip = tol / (n * n)
        for p in range(n - 1):
            ap = a[p]
            for q_ in range(p + 1, n):
                if abs(ap[q_]) < skip:
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
    return sorted(a[i][i] for i in range(n))


def walk_spectrum(N, links):
    deg = [0] * N
    for (j, i) in links:
        deg[j] += 1
        deg[i] += 1
    isolated = [i for i in range(N) if deg[i] == 0]
    L = [[0.0] * N for _ in range(N)]
    for i in range(N):
        L[i][i] = 1.0 if deg[i] > 0 else 0.0
    for (j, i) in links:
        w = -1.0 / math.sqrt(deg[j] * deg[i])
        L[j][i] += w
        L[i][j] += w
    return jacobi_eigs(L), deg, isolated


def ds_ct(t, lams):
    num = sum(x * math.exp(-t * x) for x in lams)
    den = sum(math.exp(-t * x) for x in lams)
    return 2 * t * num / den


def ds_disc(lams, N, n):
    mus = [1 - x for x in lams]
    def pbar(m):
        return sum(mu ** m for mu in mus) / N
    return -2 * (math.log(pbar(n + 2)) - math.log(pbar(n))) / \
        (math.log(n + 2) - math.log(n))


def main():
    out = {"clauses": {}, "detail": {}}
    ok_a = ok_b = ok_c = True
    peaks = {}
    for N in REG["N_ladder"]:
        Lpin = REG["links_pin"][str(N)]
        cell_peaks = []
        for r in range(REG["R_seeds"]):
            seed = REG["seed0"] + 97 * N + r
            pts = sprinkle(N, seed)
            links = hasse_links(pts)
            nl = len(links)
            band = B["links_sigma"] * math.sqrt(Lpin)
            good_l = abs(nl - Lpin) < band
            ok_a = ok_a and good_l
            lams, deg, isolated = walk_spectrum(N, links)
            lam_pos = [x for x in lams if x > 1e-9]
            lam1 = min(lam_pos)
            t_hi = 0.5 / lam1
            # window scan for the peak
            ts = [t_hi * (0.02 * 1.25 ** k) for k in range(22) if 0.02 * 1.25 ** k <= 1.0]
            curve = [(t, ds_ct(t, lams)) for t in ts]
            pk_t, pk = max(curve, key=lambda x: x[1])
            cell_peaks.append(pk)
            # instrument agreement at the window centre
            t_mid = t_hi * 0.2
            v_ct = ds_ct(t_mid, lams)
            # Poissonization: exp(-tL) ~ P^n at n ~ t; even steps
            n_step = max(4, 2 * round(t_mid / 2))
            v_dc = ds_disc(lams, N, n_step)
            agree = abs(v_ct - v_dc)
            ok_c = ok_c and agree < B["instr_agree"]
            out["detail"][f"N{N}_r{r}"] = {
                "ds_lattice": ds_ct(0.1, lams),
                "links": nl, "links_pin": Lpin, "links_ok": bool(good_l),
                "mean_deg": sum(deg) / N, "isolated": len(isolated),
                "lam1": lam1, "peak_t": pk_t, "peak_ds": pk,
                "ct_mid": v_ct, "disc_mid": v_dc, "agree": agree,
                "curve": curve}
            print(f"N={N} r={r}: links {nl} (pin {Lpin:.1f}), peak d_s = {pk:.3f} "
                  f"at t = {pk_t:.2f}, ct/disc {v_ct:.3f}/{v_dc:.3f}, "
                  f"isolated {len(isolated)}")
        peaks[str(N)] = sum(cell_peaks) / len(cell_peaks)
    out["clauses"]["a_links"] = bool(ok_a)

    for N in REG["N_ladder"]:
        if N >= 128 and peaks[str(N)] <= B["superdiff_min"]:
            ok_b = False
    growth = peaks["256"] - peaks["64"]
    ok_b = ok_b and growth > B["peak_growth_min"]
    out["clauses"]["b_superdiffusion"] = bool(ok_b)
    out["detail"]["peaks"] = peaks
    out["detail"]["peak_growth"] = growth
    out["clauses"]["c_instruments"] = bool(ok_c)

    # (d) the divergence, from the measured curves + the pinned continuum curve
    dal = REG["dalembertian_curve"]
    ds_small_dal = min(dal, key=lambda x: x[0])[1]
    # lattice-scale walk value: fixed t = 0.1, below every window
    lat_vals = [out["detail"][f"N{N}_r{r}"]["ds_lattice"]
                for N in REG["N_ladder"] for r in range(REG["R_seeds"])]
    ok_d = all(v < 1.0 for v in lat_vals) and abs(ds_small_dal - 2) < B["dal_uv_tol"]
    out["clauses"]["d_divergence"] = bool(ok_d)
    out["detail"]["divergence"] = {"walk_at_lattice": lat_vals,
                                   "dal_at_smallest_s": ds_small_dal}

    changes = not (ok_a and ok_b and ok_c and ok_d)
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p16_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"peaks {peaks}, growth {growth:.3f}; walk at lattice scale "
          f"{max(lat_vals):.3f} max vs dal(s->0) = {ds_small_dal:.3f}")
    print(f"changes-my-mind fired: {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
