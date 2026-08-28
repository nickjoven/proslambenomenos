#!/usr/bin/env python3
"""P-30 derivation layer (pre-registration): the order ladder.
A-16 - indefinite causal order attacks the symbol graph's deepest
primitive (order itself); price it with the P-17 machinery. Two
games from the sources (LC-20): the Oreshkov-Costa-Brukner causal
game (causal bound 3/4, process-matrix value (2+sqrt2)/4, arXiv
1105.4464 eqs. 1-2, 7, 20-23) and the van der Lugt-Barrett-
Chiribella device-independent inequality (DRF bound 7/4, quantum-
switch value 1 + (2+sqrt2)/4, arXiv 2208.00719 Thm 1 and eq. 8).
Everything here has a derivable answer and runs before the
registered enumerations and circuit evaluations.

Derived facts:
  EQ1  the affine correspondence: p = (S+4)/8 maps the Bell ladder
       {2, 2 sqrt 2, 4} (P-17's rungs) EXACTLY onto the OCB ladder
       {3/4, (2+sqrt2)/4, 1}; the VLBC ladder is the same plus
       one. The order ladder is the Bell ladder in a causal
       costume - for these games, derived before it is computed.
  EQ2  the OCB process spectrum in closed form: W = (1/4)[1 +
       M/sqrt2] with M = A + B, where A = sz^A2 sz^B1 and
       B = sz^A1 sx^B1 sz^B2 ANTICOMMUTE (sz sx = -sx sz on B1),
       so M^2 = 2 and W has eigenvalues {1/2 x8, 0 x8}: positive,
       rank 8, trace 4. kernels.eigh on the real embedding must
       reproduce this to 1e-12.
  EQ3  process-matrix validity is four checkable identities: W >= 0,
       Tr W = 4, and the bipartite trace-and-replace conditions
       (Araujo et al. form) - verified for the OCB W and violated
       by a pinned invalid perturbation (the mutant target).
  EQ4  the reduced-process anchor: OCB eqs. (25)-(26) give
       P(y | a, b' = 1) = (1/2)[1 + (-1)^{y+a}/sqrt2] - the noisy
       channel Alice-to-Bob with fidelity (2+sqrt2)/4.
  EQ5  the switch third-term anchor: with target frozen at
       x1 = x2 = 0, the switch's control is untouched and Bob-
       Charlie hold |Phi+>; their VLBC measurement angles give
       correlators +-1/sqrt2 and the third term (2+sqrt2)/4 - a
       CHSH game riding inside the causal game; Kraus completeness
       of the measure-reprepare instruments checked for every
       setting.
  EQ6  feasibility: enumeration sizes are exact and small (OCB
       4 x 4 x 256 per order; VLBC per-lambda deterministic
       strategy tables); all checks at 1e-12; no stochastics
       anywhere in the line.
Pinned -> p30_registration.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

from kernels.eig import eigh  # noqa: E402

FAILURES = []
RT2 = math.sqrt(2.0)


def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)
    return ok


# ------------------------------------------------ complex matrix mini-kit
def kron(A, B):
    ra, ca = len(A), len(A[0])
    rb, cb = len(B), len(B[0])
    return [[A[i // rb][j // cb] * B[i % rb][j % cb]
             for j in range(ca * cb)] for i in range(ra * rb)]


def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    Bt = list(zip(*B))
    return [[sum(A[i][k] * Bt[j][k] for k in range(m))
             for j in range(p)] for i in range(n)]


def madd(*Ms):
    n = len(Ms[0])
    return [[sum(M[i][j] for M in Ms) for j in range(n)]
            for i in range(n)]


def mscale(c, M):
    return [[c * x for x in row] for row in M]


def dagger(M):
    return [[M[j][i].conjugate() for j in range(len(M))]
            for i in range(len(M[0]))]


def trace(M):
    return sum(M[i][i] for i in range(len(M)))


def eye(n):
    return [[1.0 + 0j if i == j else 0j for j in range(n)]
            for i in range(n)]


SI = eye(2)
SX = [[0j, 1 + 0j], [1 + 0j, 0j]]
SY = [[0j, -1j], [1j, 0j]]
SZ = [[1 + 0j, 0j], [0j, -1 + 0j]]


def pauli_string(ops):
    M = ops[0]
    for o in ops[1:]:
        M = kron(M, o)
    return M


def herm_eigs(M):
    """Eigenvalues of a Hermitian complex matrix via the real
    symmetric embedding [[Re, -Im], [Im, Re]] (each eigenvalue
    doubled)."""
    n = len(M)
    R = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            R[i][j] = M[i][j].real
            R[i][j + n] = -M[i][j].imag
            R[i + n][j] = M[i][j].imag
            R[i + n][j + n] = M[i][j].real
    e = sorted(eigh(R))
    return e[::2]  # doubled spectrum


# ------------------------------------------------------------ OCB objects
def ocb_W():
    """OCB eq. (7): order A1 (x) A2 (x) B1 (x) B2."""
    A = pauli_string([SI, SZ, SZ, SI])          # sz^A2 sz^B1
    B = pauli_string([SZ, SI, SX, SZ])          # sz^A1 sx^B1 sz^B2
    return madd(mscale(0.25, eye(16)),
                mscale(0.25 / RT2, madd(A, B))), A, B


def trace_replace(W, subsys):
    """_X W: trace out the qubits in subsys (subset of {0,1,2,3})
    and replace with identity/2 on those factors."""
    n = 4
    out = [[0j] * 16 for _ in range(16)]
    keep = [q for q in range(n) if q not in subsys]
    for i in range(16):
        for j in range(16):
            ib = [(i >> (3 - q)) & 1 for q in range(4)]
            jb = [(j >> (3 - q)) & 1 for q in range(4)]
            if any(ib[q] != jb[q] for q in subsys):
                continue
            acc = 0j
            for kbits in range(1 << len(subsys)):
                i2 = list(ib)
                j2 = list(jb)
                for t, q in enumerate(subsys):
                    bit = (kbits >> t) & 1
                    i2[q] = bit
                    j2[q] = bit
                ii = sum(b << (3 - q) for q, b in enumerate(i2))
                jj = sum(b << (3 - q) for q, b in enumerate(j2))
                acc += W[ii][jj]
            out[i][j] = acc / (2 ** len(subsys))
    _ = keep
    return out


def close(A, B, tol=1e-12):
    return max(abs(A[i][j] - B[i][j]) for i in range(len(A))
               for j in range(len(A))) < tol


def eq1():
    print("EQ1 the affine Bell-order correspondence")
    bell = [2.0, 2 * RT2, 4.0]
    ocb = [(s + 4) / 8 for s in bell]
    want = [0.75, (2 + RT2) / 4, 1.0]
    ok = all(abs(a - b) < 1e-15 for a, b in zip(ocb, want))
    check("EQ1 p = (S+4)/8 maps {2, 2rt2, 4} -> {3/4, (2+rt2)/4, 1}",
          ok, f"{ocb}")
    vl = [1 + w for w in want]
    check("EQ1 VLBC ladder = OCB ladder + 1 (7/4, 1+(2+rt2)/4, 2)",
          abs(vl[0] - 7 / 4) < 1e-15 and abs(vl[2] - 2) < 1e-15)
    return {"ocb_ladder": want, "vlbc_ladder": vl}


def eq2():
    print("EQ2 the OCB process spectrum by anticommutation")
    W, A, B = ocb_W()
    AB = matmul(A, B)
    BA = matmul(B, A)
    anti = max(abs(AB[i][j] + BA[i][j]) for i in range(16)
               for j in range(16))
    check("EQ2 {A, B} = 0", anti < 1e-12, f"{anti:.2e}")
    e = herm_eigs(W)
    lo = sum(1 for x in e if abs(x) < 1e-10)
    hi = sum(1 for x in e if abs(x - 0.5) < 1e-10)
    check("EQ2 spectrum {0 x8, 1/2 x8}", lo == 8 and hi == 8,
          f"zeros {lo}, halves {hi}")
    check("EQ2 Tr W = 4", abs(trace(W) - 4) < 1e-12)
    return {"min_eig": min(e), "max_eig": max(e)}


def eq3():
    print("EQ3 process validity as trace-and-replace identities")
    W, _, _ = ocb_W()
    # qubits: 0=A1(in), 1=A2(out), 2=B1(in), 3=B2(out)
    # bipartite validity (Araujo et al.):
    #  (i)  _{B2} W = _{B1 B2} W   would FORBID B->A signaling; the
    #       OCB W deliberately signals, so the correct conditions are
    #       the process-subspace ones:
    #  L_V: W = _{A2}W + _{B2}W - _{A2 B2}W  (no loop terms)
    #  plus _{A1 A2 B2}W = _{A1 A2 B1 B2}W and mirror.
    lhs = madd(trace_replace(W, [1]), trace_replace(W, [3]),
               mscale(-1.0, trace_replace(W, [1, 3])))
    check("EQ3 W = _A2 W + _B2 W - _A2B2 W (no causal loop)",
          close(W, lhs))
    c1 = close(trace_replace(W, [0, 1, 3]),
               trace_replace(W, [0, 1, 2, 3]))
    c2 = close(trace_replace(W, [2, 3, 1]),
               trace_replace(W, [0, 1, 2, 3]))
    check("EQ3 marginal-normalization conditions", c1 and c2)
    # the pinned INVALID perturbation (mutant target): adding
    # sz^A1 sz^A2 sz^B1 sz^B2 x 1/4 creates a loop term
    bad = madd(W, mscale(0.25, pauli_string([SZ, SZ, SZ, SZ])))
    lhs_b = madd(trace_replace(bad, [1]), trace_replace(bad, [3]),
                 mscale(-1.0, trace_replace(bad, [1, 3])))
    check("EQ3 loop perturbation violates the identity",
          not close(bad, lhs_b))
    return {}


def proj(vec_sign, basis):
    """(1 + s*P)/2 for P in {SZ, SX}."""
    return madd(mscale(0.5, SI), mscale(0.5 * vec_sign, basis))


def ocb_probability(x, a, y, b, bp):
    """OCB eqs. (20)-(23): P(xy|abb') = Tr[W (xi (x) eta)]."""
    W, _, _ = ocb_W()
    # OCB eq. (20): xi = (1/4)[1+(-1)^x sz]^A1 (x) [1+(-1)^a sz]^A2
    xi = mscale(0.25, kron(madd(SI, mscale((-1) ** x, SZ)),
                           madd(SI, mscale((-1) ** a, SZ))))
    if bp == 1:
        rho = mscale(0.5, SI)
        eta = mscale(0.5, kron(madd(SI, mscale((-1) ** y, SZ)), rho))
    else:
        eta = mscale(0.25, kron(madd(SI, mscale((-1) ** y, SX)),
                                madd(SI, mscale((-1) ** (b ^ y), SZ))))
    M = kron(xi, eta)
    return trace(matmul(W, M)).real


def eq4():
    print("EQ4 the reduced-process anchor (OCB eqs. 25-26)")
    worst = 0.0
    for a in (0, 1):
        for y in (0, 1):
            p = sum(ocb_probability(x, a, y, b, 1)
                    for x in (0, 1) for b in (0, 1)) / 2
            want = 0.5 * (1 + (-1) ** (y + a) / RT2)
            worst = max(worst, abs(p - want))
    check("EQ4 P(y|a, b'=1) = (1/2)[1 + (-1)^{y+a}/rt2]",
          worst < 1e-12, f"worst {worst:.2e}")
    return {}


def eq5():
    print("EQ5 the switch third-term anchor and Kraus completeness")
    # Kraus completeness of measure-reprepare: sum_a |x><a| dag |x><a|
    for x in (0, 1):
        acc = [[0j] * 2 for _ in range(2)]
        for a in (0, 1):
            K = [[0j] * 2 for _ in range(2)]
            K[x][a] = 1 + 0j
            acc = madd(acc, matmul(dagger(K), K))
        check(f"EQ5 Kraus completeness (x={x})", close(acc, SI))
    # Bob-Charlie correlators on |Phi+> at the VLBC angles
    # E(y,z) = <Phi+| B_y (x) C_z |Phi+> with B_0=Z, B_1=X,
    # C_0=(Z+X)/rt2, C_1=(Z-X)/rt2 -> +-1/rt2; third term (2+rt2)/4
    third = 0.0
    for y in (0, 1):
        for z in (0, 1):
            By = SZ if y == 0 else SX
            Cz = mscale(1 / RT2, madd(SZ, mscale(1 - 2 * z, SX)))
            # <Phi+| B (x) C |Phi+> = Tr[B C^T]/2
            E = 0.5 * trace(matmul(By, [[Cz[j][i] for j in range(2)]
                                        for i in range(2)])).real
            # p(b^c = yz) = (1 + (-1)^{yz} E)/2
            third += 0.25 * 0.5 * (1 + (1 if (y & z) == 0 else -1) * E)
    check("EQ5 third term = (2+rt2)/4", abs(third - (2 + RT2) / 4)
          < 1e-12, f"{third:.12f}")
    return {"third_term": third}


def main():
    pins = {}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    pins["EQ5"] = eq5()
    pins["EQ6"] = {"ocb_strategies_per_order": 4 * 4 * 256,
                   "tolerance": 1e-12}
    print("EQ6 feasibility: exact enumerations, 1e-12, no stochastics")
    out = os.path.join(HERE, "p30_registration.json")
    with open(out, "w") as f:
        json.dump(pins, f, indent=1)
    print(f"\npinned -> {out}")
    if FAILURES:
        print("DERIVATION FAILURES:", FAILURES)
        return 1
    print("all derivations ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
