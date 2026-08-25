#!/usr/bin/env python3
"""P-17 derivation layer (pre-registration): the Bell ladder - every
rung derived exactly before any simulation runs. The design principle
is the expansion/contraction asymmetry: expanding the correlation set
is cheap (each rung below is one purchasable resource, priced
exactly); contracting it back down is where the theorems live, and
the only known principled contraction lands exactly on the quantum
boundary.

EQ1  the local ceiling: over ALL 16 deterministic strategies,
     max CHSH S = 2 (exhaustive, exact integers).
EQ2  shared randomness buys nothing: S is linear, so mixtures stay
     inside [-2, 2] (200 random mixtures sampled as a check).
EQ3  the quantum ceiling: the 4x4 CHSH operator at the optimal
     settings has norm 2 sqrt 2 (power iteration to 1e-12), satisfies
     Landau's identity S^2 = 4I -/+ [A0,A1]x[B0,B1] entrywise, and
     the singlet expectation is 2 sqrt 2.
EQ4  the best honest machine: the shared-rotor LHV gives the zigzag
     E(theta) = 2 theta/pi - 1 (closed form vs fine-grid integral)
     and saturates S = 2 at the same angles where quantum reaches
     2 sqrt 2 - the gap between zigzag and cosine is the prize.
EQ5  one bit, spent bluntly: sending the setting gives deterministic
     S = 4 exactly (the algebraic maximum; constructed).
EQ6  the detection rung: lambda uniform on the sphere, Alice always
     answers -sign(a.lambda), Bob detects with probability
     |b.lambda| and answers sign(b.lambda). Two sphere identities -
     E[(b.lambda) sign(a.lambda)] = cos(theta)/2 and E|b.lambda| =
     1/2 - give post-selected E = -cos(theta) EXACTLY at mean
     efficiency (1 + 1/2)/2 = 3/4, below the symmetric threshold
     2/(1+sqrt 2) = 0.8284 (Garg-Mermin) as it must be.
EQ7  the expansion extreme: with PR boxes, the n-bit inner product
     needs ONE bit of communication (van Dam) - protocol implemented
     and checked exhaustively at n = 8 (65,536 input pairs).
EQ8  the contraction: information causality. The nested random-
     access-code quantity f(E, k) = 2^k (1 - h((1+E^k)/2)) stays
     bounded by 1/(2 ln 2) = 0.7213 at E = 1/sqrt 2 (Tsirelson),
     crosses 1 at finite depth for any E > 1/sqrt 2, and explodes
     as 2^k at the PR box - the boundary of the principle is
     exactly the quantum ceiling.
Pinned outputs -> p17_registration.json.
"""
import itertools
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT, FAILED = [], []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


def chsh(E):
    return E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)]


def main():
    rng = random.Random(20260824)

    # EQ1: exhaustive local strategies
    best = -10
    for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4):
        E = {(0, 0): a0 * b0, (0, 1): a0 * b1, (1, 0): a1 * b0, (1, 1): a1 * b1}
        best = max(best, abs(chsh(E)))
    eq(1, best == 2, "max |S| over all 16 deterministic local strategies = 2 (exact)",
       f"max = {best}")

    # EQ2: mixtures
    worst2 = 0.0
    strategies = list(itertools.product((-1, 1), repeat=4))
    for _ in range(200):
        w = [rng.random() for _ in strategies]
        tot = sum(w)
        E = {(x, y): 0.0 for x in (0, 1) for y in (0, 1)}
        for wi, (a0, a1, b0, b1) in zip(w, strategies):
            a = (a0, a1)
            b = (b0, b1)
            for x in (0, 1):
                for y in (0, 1):
                    E[(x, y)] += wi / tot * a[x] * b[y]
        worst2 = max(worst2, abs(chsh(E)))
    eq(2, worst2 <= 2 + 1e-12, "shared randomness stays inside |S| <= 2 (linearity)",
       f"max over 200 mixtures = {worst2:.12f}")

    # EQ3: quantum ceiling
    Z = [[1, 0], [0, -1]]
    X = [[0, 1], [1, 0]]
    s2 = math.sqrt(2)

    def mat_add(A, B, ca=1.0, cb=1.0):
        return [[ca * A[i][j] + cb * B[i][j] for j in range(len(A))] for i in range(len(A))]

    def mat_mul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(len(A))) for j in range(len(A))]
                for i in range(len(A))]

    def kron(A, B):
        na, nb = len(A), len(B)
        return [[A[i // nb][j // nb] * B[i % nb][j % nb] for j in range(na * nb)]
                for i in range(na * nb)]

    B0 = mat_add(Z, X, 1 / s2, 1 / s2)
    B1 = mat_add(Z, X, 1 / s2, -1 / s2)
    S_op = mat_add(mat_add(kron(Z, B0), kron(Z, B1)), mat_add(kron(X, B0), kron(X, B1), 1, -1))
    S2 = mat_mul(S_op, S_op)
    comm = lambda A, B: mat_add(mat_mul(A, B), mat_mul(B, A), 1, -1)  # noqa: E731
    CC = kron(comm(Z, X), comm(B0, B1))
    I4 = [[4.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    dev_minus = max(abs(S2[i][j] - I4[i][j] + CC[i][j]) for i in range(4) for j in range(4))
    dev_plus = max(abs(S2[i][j] - I4[i][j] - CC[i][j]) for i in range(4) for j in range(4))
    landau = min(dev_minus, dev_plus)
    sign = "-" if dev_minus < dev_plus else "+"
    v = [rng.gauss(0, 1) for _ in range(4)]
    for _ in range(300):
        w = [sum(S2[i][j] * v[j] for j in range(4)) for i in range(4)]
        nv = math.sqrt(sum(x * x for x in w))
        v = [x / nv for x in w]
    norm = math.sqrt(nv)
    psi = [0.0, 1 / s2, -1 / s2, 0.0]
    sv = [sum(S_op[i][j] * psi[j] for j in range(4)) for i in range(4)]
    exp_singlet = sum(psi[i] * sv[i] for i in range(4))
    eq(3, landau < 1e-12 and abs(norm - 2 * s2) < 1e-12 and abs(abs(exp_singlet) - 2 * s2) < 1e-12,
       f"Landau: S^2 = 4I {sign} [A0,A1]x[B0,B1]; ||S|| = <singlet|S|singlet> = 2 sqrt 2",
       f"identity dev {landau:.2e}; norm {norm:.14f}; singlet {abs(exp_singlet):.14f}")

    # EQ4: the rotor zigzag and its saturation at S = 2
    def zig(theta):
        return 2 * abs(theta) / math.pi - 1

    worst4 = 0.0
    for theta in (0.3, 0.9, 1.6, 2.4, 3.0):
        m = 200000
        acc = 0
        for i in range(m):
            mu = (i + 0.5) / m * 2 * math.pi
            acc += (1 if math.cos(mu) > 0 else -1) * (-1 if math.cos(mu - theta) > 0 else 1)
        worst4 = max(worst4, abs(acc / m - zig(theta)))
    ang = {"a": (0.0, math.pi / 2), "b": (math.pi / 4, -math.pi / 4)}
    Ez = {}
    for x in (0, 1):
        for y in (0, 1):
            Ez[(x, y)] = zig(abs(ang["a"][x] - ang["b"][y]) if abs(ang["a"][x] - ang["b"][y]) <= math.pi
                             else 2 * math.pi - abs(ang["a"][x] - ang["b"][y]))
    s_zig = abs(chsh(Ez))
    Eq = {k: -math.cos(ang["a"][k[0]] - ang["b"][k[1]]) for k in Ez}
    s_cos = abs(chsh(Eq))
    eq(4, worst4 < 1e-4 and abs(s_zig - 2) < 1e-12 and abs(s_cos - 2 * s2) < 1e-12,
       "rotor LHV: E = 2 theta/pi - 1 (grid check); S_zigzag = 2 and S_cos = 2 sqrt 2 at the SAME angles",
       f"zigzag worst dev {worst4:.2e}; S_zig = {s_zig:.12f}; S_cos = {s_cos:.12f}")

    # EQ5: one blunt bit -> S = 4
    E5 = {}
    for x in (0, 1):
        for y in (0, 1):
            a = 1
            b = 1 if x * y == 0 else -1     # Bob knows x: the sent bit IS the setting
            E5[(x, y)] = a * b
    eq(5, chsh(E5) == 4, "one bit spent bluntly (send the setting): deterministic S = 4",
       f"S = {chsh(E5)}")

    # EQ6: detection rung - sphere identities by quadrature
    def sphere_identities(theta, grid=800):
        num = eabs = 0.0
        for iu in range(grid):
            u = -1 + (iu + 0.5) * 2 / grid          # b.lambda uniform on [-1,1]
            s = math.sqrt(max(0.0, 1 - u * u))
            inner = 0.0
            for ip in range(grid):
                phi = (ip + 0.5) / grid * 2 * math.pi
                adl = u * math.cos(theta) + s * math.sin(theta) * math.cos(phi)
                inner += (1 if adl > 0 else -1)
            num += u * inner / grid
            eabs += abs(u)
        return num / grid, eabs / grid

    worst6 = 0.0
    for theta in (0.4, 1.1, 2.0, 2.8):
        ident, eu = sphere_identities(theta)
        worst6 = max(worst6, abs(ident - math.cos(theta) / 2), abs(eu - 0.5))
    eta_thresh = 2 / (1 + s2)
    eq(6, worst6 < 2e-3, "E[(b.l) sign(a.l)] = cos/2 and E|b.l| = 1/2  =>  post-selected E = -cos exactly at mean eta = 3/4",
       f"worst quadrature dev {worst6:.2e}; threshold 2/(1+sqrt2) = {eta_thresh:.6f} > 0.75")

    # EQ7: van Dam collapse - inner product with PR boxes + 1 bit, exhaustive n = 8
    nbits = 8
    ok7 = True
    for uu in range(2 ** nbits):
        for vv in range(2 ** nbits):              # truly exhaustive: 65,536 pairs
            a_x = 0
            b_x = 0
            for i in range(nbits):
                ui, vi = (uu >> i) & 1, (vv >> i) & 1
                ai = rng.getrandbits(1)           # PR box: a random, b = a XOR (u_i v_i)
                bi = ai ^ (ui & vi)
                a_x ^= ai
                b_x ^= bi
            ip = 0
            for i in range(nbits):
                ip ^= ((uu >> i) & 1) & ((vv >> i) & 1)
            if (a_x ^ b_x) != ip:                 # Bob computes b_x XOR (the 1 sent bit a_x)
                ok7 = False
    eq(7, ok7, "PR boxes collapse communication: n-bit inner product from ONE sent bit (exhaustive grid, n = 8)",
       "all checked input pairs exact")

    # EQ8: information causality ladder
    def h(p):
        if p <= 0 or p >= 1:
            return 0.0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def f(E, k):
        return (2 ** k) * (1 - h((1 + E ** k) / 2))

    table = {}
    for Ename, Eval in (("tsirelson", 1 / s2), ("above", 0.73), ("pr", 1.0)):
        table[Ename] = {str(k): f(Eval, k) for k in (1, 2, 5, 8, 10, 12, 15, 20)}
    ts_vals = [f(1 / s2, k) for k in range(1, 21)]
    bound_ts = max(ts_vals)
    decreasing = all(a >= b - 1e-12 for a, b in zip(ts_vals, ts_vals[1:]))
    k_cross = min(int(k) for k, v in table["above"].items() if v > 1.0)
    eq(8, bound_ts < 1.0 and decreasing
       and abs(ts_vals[-1] - 1 / (2 * math.log(2))) < 1e-3
       and k_cross <= 12 and table["pr"]["20"] == 2 ** 20,
       "IC: f(E,k) < 1 for all k at Tsirelson (max at k=1, decreasing to 1/(2 ln 2)), crosses 1 by k = 12 at E = 0.73, explodes as 2^k at the PR box",
       f"max f(1/sqrt2, k) = {bound_ts:.6f} at k=1, f(.,20) = {ts_vals[-1]:.6f} "
       f"(asymptote {1/(2*math.log(2)):.6f}); E=0.73 crosses 1 at k = {k_cross}; f(1, 20) = 2^20")

    pin = {"local_max": 2, "tsirelson": 2 * s2, "algebraic_max": 4,
           "chsh_angles": {"a": [0.0, math.pi / 2], "b": [math.pi / 4, -math.pi / 4]},
           "zigzag_S": 2.0, "detection": {"mean_eta": 0.75, "threshold": eta_thresh},
           "ic_table": table, "ic_asymptote_at_tsirelson": 1 / (2 * math.log(2)),
           "experiments": {
               "AGR1982": {"S": 2.697, "err": 0.015,
                           "source": "Aspect, Grangier, Roger, PRL 49, 91 (1982); S_QM(apparatus) = 2.70 +/- 0.05"},
               "FC1972": {"delta": 0.050, "err": 0.008,
                          "source": "Freedman, Clauser, PRL 28, 938 (1972); bound delta <= 0"}},
           "mc": {"pairs": 1000000, "angles": [0.4, 1.1, 2.0, 2.8], "seed": 20260824},
           "tolerances": {"mc_sigma": 4.0}}
    (HERE / "p17_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
    (HERE / "p17_derive_out.txt").write_text("\n".join(OUT) + "\n")
    print(f"\npinned: ladder 2 < {2*s2:.6f} < 4; detection 3/4 vs threshold {eta_thresh:.4f}; "
          f"IC asymptote {1/(2*math.log(2)):.4f}")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
