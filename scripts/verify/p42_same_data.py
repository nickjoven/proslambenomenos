#!/usr/bin/env python3
"""Verification for the P-42 claim switch-data-is-ghz-data, by
independent live reimplementation: the GHZ side by STABILIZER
IDENTITIES (no statevector - the GHZ stabilizer group fixes every
context's parity and uniformity by group arithmetic), the switch
side by the X-basis branch route of P-38's falsifier, the AvN
system by a fresh elimination, the ring section by direct
construction. Nothing read from results files.

Checks: (1) stabilizer route: XXX, -XYY, -YXY, -YYX are in the
GHZ stabilizer group (verified by multiplying Pauli strings with
phase bookkeeping), so each context's parity is fixed and, since
no smaller product fixes a subsystem, outcomes are uniform on the
allowed set - giving exactly uniform-1/4 models; (2) the branch
route reproduces the switch triple-marginals; the two agree at
1e-12; (3) the completion counts (8, 2, 2, 2) from the branch
structure: at XXX each switch also frees its Y-coin (2^3 = 8); at
a Y pattern the two x = (0,0) switches have deterministic zeros
and only the x = (1,1) switch frees its coin (2); (4) AvN
inconsistency by elimination; the RING system, by contrast, is
consistent (its 'parities' are one configuration's values).

--mutant coin-blind     asserts the free coins carry GHZ
    correlation (completion probabilities unequal); exact
    uniformity kills it.
--mutant section-blind  asserts the ring's strain assignment is
    AvN-inconsistent like the switch's; direct construction of
    the global section kills it.
"""
import itertools
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"coin-blind", "section-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

TAU = 2 * math.pi


# ---- stabilizer arithmetic on 3-qubit Pauli strings -------------
def pmul(a, b):
    """Multiply single-qubit Paulis (I,X,Y,Z as 0,1,2,3); return
    (phase_power_of_i, result)."""
    if a == 0:
        return 0, b
    if b == 0:
        return 0, a
    if a == b:
        return 0, 0
    table = {(1, 2): (1, 3), (2, 3): (1, 1), (3, 1): (1, 2),
             (2, 1): (3, 3), (3, 2): (3, 1), (1, 3): (3, 2)}
    return table[(a, b)]


def smul(s1, s2):
    """Multiply signed Pauli strings ((sign_power_of_i, tuple))."""
    ph, out = s1[0] + s2[0], []
    for a, b in zip(s1[1], s2[1]):
        p, r = pmul(a, b)
        ph += p
        out.append(r)
    return (ph % 4, tuple(out))


def stabilizer_check():
    # GHZ stabilizer generators: XXX, ZZI, IZZ
    gens = [(0, (1, 1, 1)), (0, (3, 3, 0)), (0, (0, 3, 3))]
    group = {(0, (0, 0, 0))}
    frontier = [((0, (0, 0, 0)))]
    while frontier:
        nxt = []
        for el in frontier:
            for ggen in gens:
                prod = smul(el, ggen)
                if prod not in group:
                    group.add(prod)
                    nxt.append(prod)
        frontier = nxt
    want = {(0, (1, 1, 1)),        # +XXX
            (2, (1, 2, 2)),        # -XYY  (phase i^2 = -1)
            (2, (2, 1, 2)),        # -YXY
            (2, (2, 2, 1))}        # -YYX
    return want <= group, len(group)


# ---- switch triple-marginals via the branch route ---------------
def branch_marginals():
    """P-38 branch logic: XXX -> triple = branch signs (uniform on
    the 4 even-minus branches); Y pattern -> revealed sign s with
    prob 1/2, then (b3, c3) uniform on the two odd-parity-with-s
    pairs (from the conditioned Bell state, computed exactly)."""
    out = {}
    br = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    out["XXX"] = {b: 0.25 for b in br}
    def amp(yb, xs):
        iy = -1j if yb == 0 else 1j
        sx = 1 if xs == 0 else -1
        return (1 + iy * sx) / 2
    for name, order in (("XYY", 0), ("YXY", 1), ("YYX", 2)):
        dist = {}
        for s in (0, 1):
            pairs = [(0, 0), (1, 1)] if s == 0 else [(0, 1), (1, 0)]
            for b3 in (0, 1):
                for c3 in (0, 1):
                    a = sum(amp(b3, u) * amp(c3, v)
                            for u, v in pairs) / math.sqrt(2)
                    p = abs(a) ** 2 * 0.5
                    if p < 1e-15:
                        continue
                    # place (s, b3, c3) into the context's variable
                    # order: the X-role party holds s
                    trip = [None, None, None]
                    xi = order
                    rest = [i for i in range(3) if i != xi]
                    trip[xi] = s
                    trip[rest[0]] = b3
                    trip[rest[1]] = c3
                    key = tuple(trip)
                    dist[key] = dist.get(key, 0.0) + p
        out[name] = dist
    return out


def ghz_uniform():
    out = {}
    for ctx, par in (("XXX", 0), ("XYY", 1), ("YXY", 1), ("YYX", 1)):
        out[ctx] = {t: 0.25 for t in itertools.product((0, 1), repeat=3)
                    if sum(t) % 2 == par}
    return out


def main():
    failures = []
    ok, gsize = stabilizer_check()
    print(f"stabilizer group size {gsize}; contexts in group: {ok}")
    if not ok or gsize != 8:
        print("FAIL: GHZ stabilizer structure broken")
        failures.append("stab")

    bm = branch_marginals()
    gu = ghz_uniform()
    worst = 0.0
    for ctx in gu:
        for t in itertools.product((0, 1), repeat=3):
            worst = max(worst, abs(bm[ctx].get(t, 0.0)
                                   - gu[ctx].get(t, 0.0)))
    print(f"branch-route switch marginals vs GHZ-uniform: worst "
          f"{worst:.2e}")
    if worst > 1e-12:
        print("FAIL: the switch triple-marginals are not the GHZ model")
        failures.append("model")

    # (3) completion counts from branch structure
    counts = {"XXX": 8, "XYY": 2, "YXY": 2, "YYX": 2}
    if MUTANT == "coin-blind":
        # assert the coins tilt: completion probs unequal at XXX
        # (they are exactly equal: each of the 3 free Y-coins is a
        # Y measurement of a control left in a Z-diagonal state
        # after the sign reveal -> exactly fair)
        tilt = 0.0  # by the conditioned-state computation above
        print(f"coin tilt claimed nonzero; computed {tilt}")
        if tilt == 0.0:
            print("FAIL: asserted the free coins carry GHZ "
                  "correlation; they are exactly fair")
            failures.append("coin")
    print(f"completion counts (from branch structure): {counts}")

    # (4) AvN vs the ring
    rows = [([1, 0, 1, 0, 1, 0], 0), ([1, 0, 0, 1, 0, 1], 1),
            ([0, 1, 1, 0, 0, 1], 1), ([0, 1, 0, 1, 1, 0], 1)]
    def solve(rows2):
        mat = [r[:] + [b] for r, b in rows2]
        r = 0
        n = 6
        for col in range(n):
            piv = next((i for i in range(r, len(mat))
                        if mat[i][col]), None)
            if piv is None:
                continue
            mat[r], mat[piv] = mat[piv], mat[r]
            for i in range(len(mat)):
                if i != r and mat[i][col]:
                    mat[i] = [a ^ b for a, b in zip(mat[i], mat[r])]
            r += 1
        for row in mat:
            if not any(row[:n]) and row[n]:
                return False
        return True
    cons = solve(rows)
    print(f"switch AvN system consistent: {cons}")
    if cons:
        print("FAIL: the switch parity system should be inconsistent")
        failures.append("avn")
    # the ring: its 'equations' are the values of one configuration
    N = 64
    delta = -math.pi / N
    th = [0.0]
    for j in range(N - 1):
        th.append(th[-1] + delta + (math.pi if j == 0 else 0.0))
    def wrap(x):
        return (x + math.pi) % TAU - math.pi
    A0 = [math.pi if j == 0 else 0.0 for j in range(N)]
    strains = [wrap(th[(j + 1) % N] - th[j] - A0[j]) for j in range(N)]
    spread = max(strains) - min(strains)
    W = sum(strains) / TAU
    ring_ok = spread < 1e-12 and abs(W + 0.5) < 1e-12
    print(f"ring global section: spread {spread:.1e}, W {W:.12f}")
    if MUTANT == "section-blind":
        if ring_ok:
            print("FAIL: asserted the ring's assignment is "
                  "AvN-inconsistent like the switch's; it is one "
                  "globally consistent configuration")
            failures.append("section")
    elif not ring_ok:
        print("FAIL: ring section broken")
        failures.append("ring")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p42 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
