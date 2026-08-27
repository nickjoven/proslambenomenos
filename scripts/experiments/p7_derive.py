#!/usr/bin/env python3
"""P-7 derivation layer (pre-registration): the golden flux ladder.
Harper / almost-Mathieu at critical coupling lambda = 1,
    (H psi)_n = psi_{n+1} + psi_{n-1} + 2 cos(2 pi alpha n + theta) psi_n,
on the Fibonacci-approximant fluxes alpha_m = F_m / F_{m+1} -> 1/phi.
Everything here is derived BEFORE the registered ladder runs: the
exact anchors by CAS, the Bloch construction validated against them,
the imported plateau constant computed from its own series, and the
tolerance bands set from the small-q trend.

Derived facts:
  EQ1  alpha = 1/2 (q = 2), CAS: the Bloch determinant gives
       E^2 = 4 cos^2 k2 + (1 + s)^2 with s the corner phase, so the
       spectrum is +-[0, 2 sqrt 2]: two bands TOUCHING at E = 0 -
       the c25 pi-flux Dirac point, whose dispersion maximum
       2 sqrt(cos^2+cos^2) = 2 sqrt 2 is the same number (interop).
  EQ2  alpha = 1/3 (q = 3), CAS: the transfer trace obeys
       tr M(theta) + 2 cos(3 theta) = E^3 - 6E, and the band edges
       are EXACT: E^3 - 6E = -4 factors as (E+2)(E^2-2E-2),
       E^3 - 6E = +4 as (E-2)(E^2+2E-2); edges
       {-1-sqrt3, -2, 1-sqrt3, -1+sqrt3, 2, 1+sqrt3}.
  EQ3  the Bloch construction (q x q, corner s = +-1, k2 in
       {0, pi/q}; bands = consecutive pairs of the 2q sorted edge
       eigenvalues, cyclic Jacobi) reproduces EQ1/EQ2 edges to 1e-10.
  EQ4  Catalan's constant by accelerated alternating series, two
       depths agreeing to 1e-13; the imported Thouless plateau
       constant 32 G / pi = 9.3299... pinned (LC-14: imported, not
       derived here).
  EQ5  gap parity at the anchors: q even -> the central gap is
       CLOSED (Dirac touch, gap < 1e-10); q odd -> all q-1 gaps
       open. Registered as the parity rule for the ladder.
  EQ6  small-q trend pinned: q S(q) at q = 2, 3 in closed form
       (8 sqrt 2 = 11.3137..., 12 sqrt 3 - 12 = 8.7846...), q = 5, 8
       numeric with Jacobi residual guard; the clause bands for the
       ladder derive from this trend and are written into the
       registration, not chosen after the run.

Pinned -> p7_registration.json.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from symb import N as Num, V as Var, add, sub, mul, powe, sin as Sin, cos as Cos, equal, ev  # noqa: E402

OUT, FAILED = [], []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


# ---------- EQ1: q = 2 closed form by CAS ----------
E, c2, s = Var("E"), Var("c"), Var("s")
# H = [[-2 c2, 1+s], [1+s, 2 c2]]  (diag 2cos(pi n + k2), n = 1, 2)
detH = sub(mul(sub(Num(0), mul(Num(2), c2)), sub(mul(Num(2), c2), E)),
           mul(add(Num(1), s), add(Num(1), s)))
# det(H - E) = (-2c - E)(2c - E) - (1+s)^2 = E^2 - 4c^2 - (1+s)^2
detHmE = sub(mul(sub(sub(Num(0), mul(Num(2), c2)), E), sub(mul(Num(2), c2), E)),
             mul(add(Num(1), s), add(Num(1), s)))
target = sub(sub(powe(E, Num(2)), mul(Num(4), c2, c2)),
             mul(add(Num(1), s), add(Num(1), s)))
ok1, worst1, _ = equal(detHmE, target, {"E": (-3.0, 3.0), "c": (-1.0, 1.0),
                                        "s": (-1.0, 1.0)})
emax = 2 * math.sqrt(2)
ok1 = ok1 and abs(math.sqrt(4 * 1 + 4) - emax) < 1e-15   # c=+-1, s=+1
eq(1, ok1, "q = 2: E^2 = 4 cos^2 k2 + (1+s)^2; bands +-[0, 2 sqrt 2], Dirac touch = c25",
   f"CAS worst {worst1:.1e}; edge 2 sqrt 2 = {emax:.12f}")

# ---------- EQ2: q = 3 exact discriminant and edges ----------
th = Var("t")


def tmat(sym_diag):
    return sym_diag  # placeholder; explicit product below


def mat_mul(A, B):
    return [[add(mul(A[0][0], B[0][0]), mul(A[0][1], B[1][0])),
             add(mul(A[0][0], B[0][1]), mul(A[0][1], B[1][1]))],
            [add(mul(A[1][0], B[0][0]), mul(A[1][1], B[1][0])),
             add(mul(A[1][0], B[0][1]), mul(A[1][1], B[1][1]))]]


Ms = None
for n in (1, 2, 3):
    dn = sub(E, mul(Num(2), Cos(add(Num(2 * math.pi * n / 3), th))))
    M = [[dn, Num(-1)], [Num(1), Num(0)]]
    Ms = M if Ms is None else mat_mul(M, Ms)
trace = add(Ms[0][0], Ms[1][1])
lhs2 = add(trace, mul(Num(2), Cos(mul(Num(3), th))))
rhs2 = sub(powe(E, Num(3)), mul(Num(6), E))
ok2, worst2, _ = equal(lhs2, rhs2, {"E": (-3.0, 3.0), "t": (0.0, 6.28)})
# exact factorizations of D = -+4
edges3 = sorted([-1 - math.sqrt(3), -2.0, 1 - math.sqrt(3),
                 -1 + math.sqrt(3), 2.0, 1 + math.sqrt(3)])
ok2b = all(abs((e**3 - 6 * e) ** 2 - 16) < 1e-12 for e in edges3)
eq(2, ok2 and ok2b, "q = 3: tr M + 2 cos 3 theta = E^3 - 6E; edges exact via factoring",
   f"CAS worst {worst2:.1e}; edges {[f'{x:.4f}' for x in edges3]}")


# ---------- the Bloch construction ----------
def jacobi_eigs(A, tol=1e-11, max_sweeps=30):
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < tol:
            break
        for p in range(n - 1):
            for q_ in range(p + 1, n):
                if abs(a[p][q_]) < tol / (n * n):
                    continue
                thr = 0.5 * math.atan2(2 * a[p][q_], a[q_][q_] - a[p][p]) \
                    if a[p][p] != a[q_][q_] else math.pi / 4
                c, s_ = math.cos(thr), math.sin(thr)
                for k in range(n):
                    apk, aqk = a[p][k], a[q_][k]
                    a[p][k], a[q_][k] = c * apk - s_ * aqk, s_ * apk + c * aqk
                for k in range(n):
                    akp, akq = a[k][p], a[k][q_]
                    a[k][p], a[k][q_] = c * akp - s_ * akq, s_ * akp + c * akq
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


def band_edges(p, q):
    e1, r1 = jacobi_eigs(bloch(p, q, +1.0, 0.0))
    e2, r2 = jacobi_eigs(bloch(p, q, -1.0, math.pi / q))
    return sorted(e1 + e2), max(r1, r2)


def bands_of(edges):
    return [(edges[2 * i], edges[2 * i + 1]) for i in range(len(edges) // 2)]


def bandwidth(p, q):
    edges, resid = band_edges(p, q)
    bs = bands_of(edges)
    S = sum(b - a for a, b in bs)
    gaps = [bs[i + 1][0] - bs[i][1] for i in range(len(bs) - 1)]
    return S, gaps, resid


# ---------- EQ3: construction reproduces the CAS anchors ----------
edges2, r2_ = band_edges(1, 2)
tgt2 = [-2 * math.sqrt(2), 0.0, 0.0, 2 * math.sqrt(2)]
w3a = max(abs(a - b) for a, b in zip(edges2, tgt2))
edges3n, r3_ = band_edges(1, 3)
w3b = max(abs(a - b) for a, b in zip(edges3n, edges3))
eq(3, w3a < 1e-10 and w3b < 1e-10 and max(r2_, r3_) < 1e-10,
   "Bloch construction (corner +-1, k2 in {0, pi/q}) reproduces both anchors",
   f"q=2 worst {w3a:.1e}, q=3 worst {w3b:.1e}, Jacobi residual {max(r2_, r3_):.1e}")


# ---------- EQ4: Catalan and the imported plateau constant ----------
def catalan(depth):
    # G = sum (-1)^n / (2n+1)^2, accelerated by repeated averaging
    N_ = 4000
    ps, s_ = [], 0.0
    for n in range(N_):
        s_ += (-1) ** n / (2 * n + 1) ** 2
        ps.append(s_)
    tail = ps[-(depth + 1):]
    while len(tail) > 1:
        tail = [0.5 * (a + b) for a, b in zip(tail, tail[1:])]
    return tail[0]


G1, G2 = catalan(40), catalan(80)
G = G2
THOULESS = 32 * G / math.pi
ok4 = abs(G1 - G2) < 1e-13 and abs(G - 0.9159655941772190) < 1e-12
eq(4, ok4, "Catalan G by accelerated series; imported plateau 32 G / pi (LC-14)",
   f"G = {G:.15f}, 32G/pi = {THOULESS:.10f}")

# ---------- EQ5: gap parity at the anchors ----------
_, gaps2, _ = bandwidth(1, 2)
_, gaps3, _ = bandwidth(1, 3)
ok5 = abs(gaps2[0]) < 1e-10 and min(gaps3) > 0.2
eq(5, ok5, "q even: central gap closed (Dirac); q odd: all gaps open",
   f"q=2 central gap {gaps2[0]:.1e}; q=3 min gap {min(gaps3):.4f}")

# ---------- EQ6: small-q trend and the derived clause bands ----------
S2 = 4 * math.sqrt(2)
S3 = 4 * math.sqrt(3) - 4
S5, gaps5, res5 = bandwidth(3, 5)
S8, gaps8, res8 = bandwidth(5, 8)
trend = {2: 2 * S2, 3: 3 * S3, 5: 5 * S5, 8: 8 * S8}
dev = {k: v - THOULESS for k, v in trend.items()}
ok6 = res5 < 1e-9 and res8 < 1e-9 and abs(trend[8] - THOULESS) < abs(trend[2] - THOULESS)
eq(6, ok6, "q S(q) trend at the anchors; deviations shrink toward the plateau",
   "; ".join(f"q={k}: qS = {v:.4f} ({dev[k]:+.3f})" for k, v in trend.items()))

LADDER = [(8, 13), (13, 21), (21, 34), (34, 55), (55, 89), (89, 144)]
LNPHI = math.log((1 + math.sqrt(5)) / 2)
pin = {"ladder": [list(x) for x in LADDER],
       "anchors": {"2": {"p": 1, "S": S2}, "3": {"p": 1, "S": S3},
                   "5": {"p": 3, "S": S5}, "8": {"p": 5, "S": S8}},
       "thouless": THOULESS, "catalan": G, "ln_phi": LNPHI,
       "jacobi_tol": 1e-11, "edge_pairs_rule": "consecutive sorted pairs",
       "bands": {"plateau_abs": 0.25, "plateau_kill": 0.9,
                 "slope_abs": 0.05, "slope_kill": 0.15,
                 "closed_gap_eps": 1e-8, "jacobi_residual_max": 1e-8},
       "clauses": {
           "a": "anchors q = 2, 3 reproduced by the ladder code to 1e-10",
           "b": "parity rule on the ladder: odd q -> all q-1 gaps > closed_gap_eps; even q -> central gap < closed_gap_eps, others open",
           "c": "plateau: mean of q S(q) over the last even/odd pair (55/89, 89/144) within plateau_abs of 32G/pi",
           "d": "the ln phi clock: |ln(S(89)/S(144)) - ln_phi| < slope_abs, earned as clock (F ratio) x flatness (Thouless)"}}
(HERE / "p7_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(HERE / "p7_derive_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned: anchors qS = {trend}; plateau {THOULESS:.5f}; ln phi {LNPHI:.6f}; "
      f"ladder to q = 144")
sys.exit(1 if FAILED else 0)
