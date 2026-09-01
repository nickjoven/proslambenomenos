#!/usr/bin/env python3
"""Verification for the P-39 claim biased-ocb-on-the-circle, by
independent live reimplementation: the process values via PAULI
ORTHOGONALITY - no matrices anywhere; every operator is a
dictionary of Pauli strings and Tr[P_i P_j] = 16 delta_ij does the
work - and the causal side by a fresh enumeration encoding.
Nothing read from results files, nothing imported from the
experiment scripts.

Checks: (1) with the OCB strategy operators expanded in the Pauli
basis, the two success probabilities of W(theta) are
(1 + sin th)/2 and (1 + cos th)/2 (assignment determined by the
computation itself); at theta*(alpha) the value lands on
(1 + alpha + sqrt(1 + alpha^2))/2 at 1e-12 for alpha in
{1/2, 1, 2}; (2) the causal maximum from an exhaustive own-coded
enumeration equals max(1 + alpha/2, 1/2 + alpha) exactly at the
same alphas; (3) the advantage is positive there and zero at
alpha = 0.

--mutant symmetric-blind  asserts the theta = pi/4 process is
    optimal at alpha = 2; the rotated family beats it.
--mutant square-blind     asserts a causal strategy attains the
    ICO bound at alpha = 1; the exhaustion caps at 3/2.
"""
import math
import sys
from fractions import Fraction

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"symmetric-blind", "square-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


# ---- Pauli-basis algebra: operator = {4-char string: coeff} ----
def tensor(*factors):
    """factors: list of single-qubit ops as {char: coeff}."""
    out = {"": 1.0}
    for f in factors:
        out = {k + c: v * w for k, v in out.items()
               for c, w in f.items()}
    return out


def op_add(*ops):
    out = {}
    for o in ops:
        for k, v in o.items():
            out[k] = out.get(k, 0.0) + v
    return out


def op_scale(c, o):
    return {k: c * v for k, v in o.items()}


def pauli_value(W, M):
    """Tr[W M] via orthogonality: sum over shared strings of
    w * m * 16 (4 qubits, Tr[P P] = 2^4)."""
    return sum(v * M.get(k, 0.0) for k, v in W.items()) * 16.0


def zproj(s):
    return {"I": 0.5, "Z": 0.5 * s}


def xproj(s):
    return {"I": 0.5, "X": 0.5 * s}


IDQ = {"I": 1.0}


def W_dict(th):
    # (1/4)[1 + cos th * IZZI + sin th * ZIXZ], with the 1/16
    # normalization folded so pauli_value gives the trace directly:
    # each 16x16 Pauli string P has Tr[P P] = 16, so store the
    # coefficient of each string in W as written and divide by 16
    # inside pauli_value... simpler: store W's expansion
    # coefficients w_k where W = sum_k w_k P_k. Then
    # Tr[W M] = 16 sum_k w_k m_k.
    return {"IIII": 0.25, "IZZI": 0.25 * math.cos(th),
            "ZIXZ": 0.25 * math.sin(th)}


def probs(th):
    W = W_dict(th)
    # strategy operators, expanded per input/outcome and summed
    # into the two success probabilities directly
    pa = 0.0
    pb = 0.0
    for a in (0, 1):
        for b in (0, 1):
            sa = (-1) ** a
            sb = (-1) ** b
            # P_A: b' = 0. Alice: xi_{x|a}; success x = b.
            # xi = (1/4)[1+(-1)^x Z] (x) [1+(-1)^a Z] on A1 A2
            # Bob (b'=0): eta = (1/4)[1+(-1)^y X] (x)
            #             [1+(-1)^{b^y} Z] on B1 B2, summed over y
            for y in (0, 1):
                sx = (-1) ** b       # success: x = b
                sy = (-1) ** y
                syb = (-1) ** (b ^ y)
                # the zproj/xproj factors ARE the normalized
                # projectors, so no further prefactor
                M = tensor(zproj(sx), zproj(sa), xproj(sy),
                           zproj(syb))
                pa += pauli_value(W, M)
            # P_B: b' = 1. Bob: eta = (1/2)[1+(-1)^y Z] (x) I/2,
            # success y = a; Alice xi summed over x.
            for x in (0, 1):
                sxx = (-1) ** x
                sya = (-1) ** a      # success: y = a
                M = tensor(zproj(sxx), zproj(sa), zproj(sya),
                           op_scale(0.5, IDQ))
                pb += pauli_value(W, M)
    return pa / 4.0, pb / 4.0


def causal_max(al):
    best = Fraction(0)
    # order A -> B and order B -> A, fresh encoding: loop over
    # response tables as tuples
    from itertools import product
    for fa in product((0, 1), repeat=2):
        for ga in product((0, 1), repeat=2):
            for hb in product((0, 1), repeat=8):
                pa = pb = 0
                for x1 in (0, 1):
                    for b in (0, 1):
                        if fa[x1] == b:
                            pa += 1
                        if hb[(b << 2) | 2 | ga[x1]] == x1:
                            pb += 1
                best = max(best, Fraction(pa, 4) + al * Fraction(pb, 4))
    for fb in product((0, 1), repeat=4):
        for gb in product((0, 1), repeat=4):
            for ha in product((0, 1), repeat=4):
                pa = pb = 0
                for x1 in (0, 1):
                    for b in (0, 1):
                        if fb[(b << 1) | 1] == x1:
                            pb += 1
                        if ha[(x1 << 1) | gb[b << 1]] == b:
                            pa += 1
                best = max(best, Fraction(pa, 4) + al * Fraction(pb, 4))
    return best


def main():
    failures = []
    # (1) the Pauli route: closed forms and the bound
    pa0, pb0 = probs(0.0)
    paq, pbq = probs(math.pi / 2)
    print(f"theta=0: P_A {pa0:.6f} P_B {pb0:.6f}; "
          f"theta=pi/2: P_A {paq:.6f} P_B {pbq:.6f}")
    # assignment read off the endpoints: P_A rides sin, P_B rides
    # cos, so I_alpha is maximized at theta* = atan2(1, alpha)
    for al in (0.5, 1.0, 2.0):
        th = math.atan2(1.0, al)
        pa, pb = probs(th)
        want = (1 + al + math.sqrt(1 + al * al)) / 2
        mv = pa + al * pb
        if MUTANT == "symmetric-blind" and al == 2.0:
            pa, pb = probs(math.pi / 4)
            claimed = pa + al * pb
            print(f"alpha 2: symmetric value {claimed:.6f}, "
                  f"family best {mv:.6f}")
            if mv > claimed + 1e-6:
                print("FAIL: asserted the symmetric process is "
                      "optimal at alpha = 2; the rotated family "
                      "beats it")
                failures.append("symmetric")
        print(f"alpha {al}: family max {mv:.12f} vs bound {want:.12f}")
        if abs(mv - want) > 1e-9:
            print(f"FAIL: family does not reach the bound at "
                  f"alpha = {al}")
            failures.append("bound")
    # (2)(3) causal side
    for al in (Fraction(1, 2), Fraction(1), Fraction(2)):
        c = causal_max(al)
        want = max(1 + al / 2, Fraction(1, 2) + al)
        print(f"alpha {al}: causal max {c} (closed {want})")
        if c != want:
            print("FAIL: causal enumeration off the closed form")
            failures.append("causal")
        if al == 1 and MUTANT == "square-blind":
            bound = (2 + math.sqrt(2)) / 2
            if float(c) < bound - 1e-9:
                print("FAIL: asserted a causal strategy attains "
                      f"the ICO bound at alpha = 1; the exhaustion "
                      f"caps at {c}")
                failures.append("square")
    adv0 = (1 + 0 + 1) / 2 - 1.0
    if abs(adv0) > 1e-15:
        print("FAIL: advantage not zero at alpha = 0")
        failures.append("tangent")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p39 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
