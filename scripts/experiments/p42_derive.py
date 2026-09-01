#!/usr/bin/env python3
"""P-42 derivation layer (pre-registration): the switch's data is
GHZ's data, and its half is not the ring's half.

Item 1 + item 3 of the 2026-09-01 theoretical press (lessons
consulted per AGENTS 8d: L-9 - anchor the roles first). Two
questions with one machinery:

(1) DATA IDENTITY. Is P-38's switch empirical model, restricted
to its registered contexts, EXACTLY the GHZ empirical model
tensored with independent fair coins and deterministic copies?
If yes, indefinite causal order adds no correlations here - the
novelty is entirely which hidden-variable class the data excludes
(orders vs local states), and 'ICO as a new resource' conflates
data with causal hypothesis.

(2) THE TWO HALVES. The switch's parity obstruction and the
pi-ring's half-integer winding both read as '1/2'. Abramsky-
Brandenburger: contextuality = no global section of the support
presheaf; AvN (all-vs-nothing) over Z2 implies a nonvanishing
cohomological obstruction (imported, LC-31). The ring's half, by
contrast, IS a global configuration. The halves differ by
global-section existence - a refusal of their identification.

Derived facts:
  EQ1  the GHZ empirical model, own stabilizer-free computation:
       3-qubit statevector, contexts {XXX, XYY, YXY, YYX};
       outcome distributions are uniform-over-fixed-parity
       (parity 0 for XXX, 1 for the others), each allowed
       outcome at 1/4, forbidden at 0 - amplitude-level.
  EQ2  the switch marginals: P-38's run_pattern marginalized onto
       the registered triple per context equals EQ1 EXACTLY
       (difference at machine zero).
  EQ3  the remainder factorizes: conditioned on the GHZ triple,
       the remaining six output bits are (i) deterministic copies
       (a2 = 1 xor a1 at x = (1,1); zeros at x = (0,0)) and (ii)
       independent fair coins (the unused third outcomes), with
       the conditional distribution EXACTLY uniform - verified as
       an exact factorization of the 512-outcome joint.
  EQ4  AvN over Z2, exact: the four parity equations in the six
       effective unknowns form an inconsistent linear system
       (rank of coefficient matrix vs augmented matrix, integer
       arithmetic) - all-vs-nothing, hence (imported) nonzero
       cohomological obstruction; the 64-assignment exhaustion of
       P-38 is the same fact as no-global-section.
  EQ5  the ring's global section: the P-35 ground state assigns
       every bond strain simultaneously (one configuration, no
       contexts); recomputed here: uniform covariant strain at
       machine zero, winding exactly -1/2. A model with a global
       section has ZERO obstruction - the two halves are
       different objects by computation.

Run: python3 scripts/experiments/p42_derive.py
"""
import itertools
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p38_derive import IDX, PATTERNS, run_pattern  # noqa: E402

TAU = 2 * math.pi


# ---------------------------------------------------------------
# EQ1: GHZ empirical model from a 3-qubit statevector
# ---------------------------------------------------------------
def ghz_model():
    """P(o1 o2 o3 | m1 m2 m3) for m in the four paradox contexts;
    measurement X or Y per party on (|000> + |111>)/sqrt2."""
    inv = 1 / math.sqrt(2)
    state = {0b000: inv + 0j, 0b111: inv + 0j}
    # projector amplitude <o|m> for one qubit: X: |0/1 +-> ;
    # Y: |+i/-i>
    def amp(m, o, bit):
        if m == "X":
            s = 1 if o == 0 else -1
            return (1 if bit == 0 else s) * inv
        s = 1j if o == 0 else -1j
        return (1 if bit == 0 else -s) * inv  # <o| conj of |o>
    out = {}
    for ctx in ("XXX", "XYY", "YXY", "YYX"):
        dist = {}
        for os_ in itertools.product((0, 1), repeat=3):
            aa = 0j
            for basis, c in state.items():
                term = c
                for q in range(3):
                    bit = (basis >> (2 - q)) & 1
                    term *= amp(ctx[q], os_[q], bit)
                aa += term
            dist[os_] = abs(aa) ** 2
        out[ctx] = dist
    return out


# ---------------------------------------------------------------
# EQ2/EQ3: switch marginals and factorization
# ---------------------------------------------------------------
CTX_OF_PATTERN = ["XXX", "XYY", "YXY", "YYX"]


def switch_marginals():
    out = {}
    joints = {}
    for i, ((xs, ys, zs), vars3, parity) in enumerate(PATTERNS):
        probs = run_pattern(xs, ys, zs)
        joints[CTX_OF_PATTERN[i]] = (probs, vars3)
        marg = {}
        for k, p in probs.items():
            trip = tuple(k[IDX[v]] for v in vars3)
            marg[trip] = marg.get(trip, 0.0) + p
        out[CTX_OF_PATTERN[i]] = marg
    return out, joints


def factorization_check(joints):
    """Conditioned on the GHZ triple, the remaining bits must be
    exactly: deterministic where forced, uniform elsewhere, and
    independent of the triple. Verified by checking every joint
    probability equals marg(triple) * uniform(free bits)."""
    worst = 0.0
    detail = {}
    for ctx, (probs, vars3) in joints.items():
        # classify the other six indices per this context
        used = [IDX[v] for v in vars3]
        # group outcomes by triple
        by_trip = {}
        for k, p in probs.items():
            trip = tuple(k[i] for i in used)
            by_trip.setdefault(trip, []).append((k, p))
        n_free = None
        for trip, items in by_trip.items():
            tot = sum(p for _, p in items)
            n = len(items)
            if n_free is None:
                n_free = n
            if n != n_free:
                return {"factorizes": False,
                        "reason": f"unequal completion counts {ctx}"}
            for _, p in items:
                worst = max(worst, abs(p - tot / n))
        detail[ctx] = {"triples": len(by_trip),
                       "completions_each": n_free}
    return {"factorizes": True, "worst_nonuniformity": worst,
            "detail": detail}


# ---------------------------------------------------------------
# EQ4: AvN over Z2 by integer linear algebra
# ---------------------------------------------------------------
def avn_rank():
    # unknowns: (xA, yA, xB, yB, xC, yC) = a1@x=1, a3@x=0 etc.
    rows = [
        ([1, 0, 1, 0, 1, 0], 0),
        ([1, 0, 0, 1, 0, 1], 1),
        ([0, 1, 1, 0, 0, 1], 1),
        ([0, 1, 0, 1, 1, 0], 1),
    ]
    def rank2(mat):
        mat = [row[:] for row in mat]
        r = 0
        for col in range(len(mat[0])):
            piv = next((i for i in range(r, len(mat))
                        if mat[i][col]), None)
            if piv is None:
                continue
            mat[r], mat[piv] = mat[piv], mat[r]
            for i in range(len(mat)):
                if i != r and mat[i][col]:
                    mat[i] = [(a ^ b) for a, b in zip(mat[i], mat[r])]
            r += 1
        return r
    A = [r for r, _ in rows]
    Aug = [r + [b] for r, b in rows]
    return {"rank_A": rank2(A), "rank_aug": rank2(Aug),
            "inconsistent": rank2(Aug) == rank2(A) + 1}


# ---------------------------------------------------------------
# EQ5: the ring's global section (P-35 machinery, recomputed)
# ---------------------------------------------------------------
def ring_section():
    sys.path.insert(0, HERE)
    from p35_ring import ground_state, winding
    N = 64
    A, th = ground_state(N, True, 0)
    W = winding(th, A, N)
    def wrap(x):
        return (x + math.pi) % TAU - math.pi
    strains = [wrap(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
    spread = max(strains) - min(strains)
    return {"winding": W, "strain_spread": spread,
            "global_section": True}


def main():
    g = ghz_model()
    sm, joints = switch_marginals()
    worst_eq = 0.0
    for ctx in g:
        for os_ in itertools.product((0, 1), repeat=3):
            worst_eq = max(worst_eq, abs(g[ctx].get(os_, 0.0)
                                         - sm[ctx].get(os_, 0.0)))
    fac = factorization_check(joints)
    res = {"EQ1_EQ2_worst_diff": worst_eq,
           "EQ1_sample": {ctx: {str(k): round(v, 6)
                                for k, v in g[ctx].items() if v > 1e-12}
                          for ctx in ("XXX", "XYY")},
           "EQ3": fac, "EQ4": avn_rank(), "EQ5": ring_section()}
    with open(os.path.join(HERE, "p42_registration.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
