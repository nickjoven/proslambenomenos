#!/usr/bin/env python3
"""Verification for the P-30 claim order-ladder-priced, by
independent live reimplementation: its own complex-matrix kit, a
WIDER causal enumeration (four-letter messages - the bound must
not move), the OCB value by its own trace evaluation, the switch
by DENSITY-MATRIX evolution on the full C (x) B (x) T space (not
the experiment's amplitude-branch bookkeeping), and its own
separability null. Nothing read from results files.

Checks: (1) the OCB causal maximum stays 3/4 even with 4-letter
messages (a strictly larger strategy class than the experiment's);
(2) the OCB process value lands on (2+sqrt2)/4 and the process
passes the no-loop identity; (3) the switch value by density
matrices lands on 1 + (2+sqrt2)/4 and the Alice-marginal equals
the classical order mixture at 1e-12.

--mutant two-way     lets Bob's guess see Alice's bit while Alice's
    guess sees Bob's (bidirectional signalling); the enumeration
    reaches 1 and the 3/4 check kills it.
--mutant loop-blind  adds the pinned loop term
    (1/4) sz sz sz sz to W and asserts validity; the no-loop
    identity breaks and check (2) kills it.
"""
import itertools
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"two-way", "loop-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

RT2 = math.sqrt(2.0)


def kron(A, B):
    ra, ca = len(A), len(A[0])
    rb, cb = len(B), len(B[0])
    return [[A[i // rb][j // cb] * B[i % rb][j % cb]
             for j in range(ca * cb)] for i in range(ra * rb)]


def mm(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt]
            for row in A]


def tr(M):
    return sum(M[i][i] for i in range(len(M)))


def dag(M):
    return [[M[j][i].conjugate() for j in range(len(M))]
            for i in range(len(M[0]))]


I2 = [[1 + 0j, 0j], [0j, 1 + 0j]]
X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]


def paulis(ops):
    M = ops[0]
    for o in ops[1:]:
        M = kron(M, o)
    return M


def build_W():
    W = [[0.25 * (1 + 0j) if i == j else 0j for j in range(16)]
         for i in range(16)]
    A = paulis([I2, Z, Z, I2])
    B = paulis([Z, I2, X, Z])
    for i in range(16):
        for j in range(16):
            W[i][j] += (A[i][j] + B[i][j]) / (4 * RT2)
    if MUTANT == "loop-blind":
        L = paulis([Z, Z, Z, Z])
        for i in range(16):
            for j in range(16):
                W[i][j] += 0.25 * L[i][j]
    return W


def trace_replace(W, subsys):
    out = [[0j] * 16 for _ in range(16)]
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
                ii = sum(bb << (3 - q) for q, bb in enumerate(i2))
                jj = sum(bb << (3 - q) for q, bb in enumerate(j2))
                acc += W[ii][jj]
            out[i][j] = acc / (2 ** len(subsys))
    return out


def main():
    failures = []

    # (1) causal max with 4-letter messages
    best = 0.0
    if MUTANT == "two-way":
        # bidirectional: x sees (a, b); y sees (b, b', a)
        for gx in itertools.product((0, 1), repeat=4):
            for gy in itertools.product((0, 1), repeat=4):
                s = 0.0
                for a in (0, 1):
                    for b in (0, 1):
                        x = gx[a * 2 + b]
                        y = gy[b * 2 + a]
                        s += 0.25 * (0.5 * (x == b) + 0.5 * (y == a))
                best = max(best, s)
    else:
        # A -> B with message m in {0,1,2,3} = f(a) - a strictly
        # larger message class than the experiment's single bit;
        # only the b' = 1 branch uses y, so y = g(m, b) (8 inputs)
        for f in itertools.product(range(4), repeat=2):
            for gA in itertools.product((0, 1), repeat=2):
                for g in itertools.product((0, 1), repeat=8):
                    s = 0.0
                    for a in (0, 1):
                        for b in (0, 1):
                            x = gA[a]
                            y = g[f[a] * 2 + b]
                            s += 0.25 * (0.5 * (x == b)
                                         + 0.5 * (y == a))
                    best = max(best, s)
        # B -> A mirrored, message m = f(b) (b' = 0 branch matters)
        for f in itertools.product(range(4), repeat=2):
            for gB in itertools.product((0, 1), repeat=2):
                for g in itertools.product((0, 1), repeat=8):
                    s = 0.0
                    for a in (0, 1):
                        for b in (0, 1):
                            y = gB[b]
                            x = g[f[b] * 2 + a]
                            s += 0.25 * (0.5 * (x == b)
                                         + 0.5 * (y == a))
                    best = max(best, s)
    want = 1.0 if MUTANT == "two-way" else 0.75
    print(f"causal max (this route): {best}")
    if abs(best - 0.75) > 1e-15:
        print(f"FAIL: causal maximum is not 3/4 (got {best})")
        failures.append("causal")

    # (2) OCB process value + no-loop identity
    W = build_W()
    lhs = trace_replace(W, [1])
    rhs2 = trace_replace(W, [3])
    both = trace_replace(W, [1, 3])
    diff = max(abs(W[i][j] - lhs[i][j] - rhs2[i][j] + both[i][j])
               for i in range(16) for j in range(16))
    if diff > 1e-12:
        print(f"FAIL: no-loop validity identity broken ({diff:.2e})")
        failures.append("validity")
    else:
        print("no-loop validity identity ok")

    def proj(sign, P):
        return [[0.5 * (I2[i][j] + sign * P[i][j]) for j in range(2)]
                for i in range(2)]

    p0 = p1 = 0.0
    for a in (0, 1):
        for b in (0, 1):
            for x in (0, 1):
                for y in (0, 1):
                    xi = kron(proj((-1) ** x, Z), proj((-1) ** a, Z))
                    # b'=1: Bob z-measures, reprep maximally mixed
                    eta1 = kron(proj((-1) ** y, Z),
                                [[0.5 + 0j, 0j], [0j, 0.5 + 0j]])
                    # b'=0: x-measure, encode b XOR y in z
                    eta0 = kron(proj((-1) ** y, X),
                                proj((-1) ** (b ^ y), Z))
                    M1 = kron(xi, eta1)
                    M0 = kron(xi, eta0)
                    pr1 = tr(mm(W, M1)).real
                    pr0 = tr(mm(W, M0)).real
                    if y == a:
                        p1 += pr1 / 4
                    if x == b:
                        p0 += pr0 / 4
    val = 0.5 * (p0 + p1)
    wantv = (2 + RT2) / 4
    print(f"OCB process value: {val:.12f} vs {wantv:.12f}")
    if abs(val - wantv) > 1e-10:
        print("FAIL: OCB process value off (2+sqrt2)/4")
        failures.append("ocb-value")

    # (3) switch by density matrices on C (x) B (x) T (dim 8)
    def op8(mats):
        return paulis(mats)  # kron chain

    def dm_evolve():
        # |psi0> = |Phi+>_{CB} (x) |0>_T
        v = [0j] * 8
        # index = c*4 + b*2 + t
        v[0] = 1 / RT2      # c=0,b=0,t=0
        v[6] = 1 / RT2      # c=1,b=1,t=0
        rho = [[v[i] * v[j].conjugate() for j in range(8)]
               for i in range(8)]

        def Kt(x, a):
            M = [[0j] * 2 for _ in range(2)]
            M[x][a] = 1 + 0j
            return M

        worst_sep = 0.0
        terms = [0.0, 0.0, 0.0]
        for x1 in (0, 1):
            for x2 in (0, 1):
                margins = {}
                for a1 in (0, 1):
                    for a2 in (0, 1):
                        K1 = Kt(x1, a1)
                        K2 = Kt(x2, a2)
                        FE = mm(K2, K1)
                        EF = mm(K1, K2)
                        # switch Kraus on (C,T): |0><0| (x) FE +
                        # |1><1| (x) EF, with B untouched
                        S = [[0j] * 8 for _ in range(8)]
                        for c in (0, 1):
                            blk = FE if c == 0 else EF
                            for bq in (0, 1):
                                for t1 in (0, 1):
                                    for t2 in (0, 1):
                                        S[c * 4 + bq * 2 + t1][
                                            c * 4 + bq * 2 + t2] \
                                            += blk[t1][t2]
                        out = mm(mm(S, rho), dag(S))
                        margins[(a1, a2)] = tr(out).real
                        # accumulate measured terms
                        for y in (0, 1):
                            By = Z if y == 0 else X
                            for z in (0, 1):
                                Cz = [[(Z[i][j] + (1 - 2 * z)
                                        * X[i][j]) / RT2
                                       for j in range(2)]
                                      for i in range(2)]
                                for b_out in (0, 1):
                                    for c_out in (0, 1):
                                        PB = [[0.5 * (I2[i][j]
                                              + (1 - 2 * b_out)
                                              * By[i][j])
                                              for j in range(2)]
                                              for i in range(2)]
                                        PC = [[0.5 * (I2[i][j]
                                              + (1 - 2 * c_out)
                                              * Cz[i][j])
                                              for j in range(2)]
                                              for i in range(2)]
                                        Pfull = op8([PC, PB, I2])
                                        pr = tr(mm(Pfull, out)).real
                                        if y == 0:
                                            if b_out == 0 and \
                                                    a2 == x1:
                                                terms[0] += pr / 8
                                            if b_out == 1 and \
                                                    a1 == x2:
                                                terms[1] += pr / 8
                                        if x1 == 0 and x2 == 0:
                                            if (b_out ^ c_out) == \
                                                    (y & z):
                                                terms[2] += pr / 4
                        # separability: classical mixture marginal
                        pm = 0.5 * sum(abs(mm(K2, K1)[t][0]) ** 2
                                       for t in (0, 1)) \
                            + 0.5 * sum(abs(mm(K1, K2)[t][0]) ** 2
                                        for t in (0, 1))
                        worst_sep = max(worst_sep,
                                        abs(margins[(a1, a2)] - pm))
        return sum(terms), worst_sep

    sval, wsep = dm_evolve()
    wants = 1 + (2 + RT2) / 4
    print(f"switch value (density-matrix route): {sval:.12f} vs "
          f"{wants:.12f}; separability worst {wsep:.2e}")
    if abs(sval - wants) > 1e-10:
        print("FAIL: switch value off 1 + (2+sqrt2)/4")
        failures.append("switch")
    if wsep > 1e-12:
        print("FAIL: switch Alice-marginal differs from the "
              "classical order mixture")
        failures.append("separability")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p30 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
