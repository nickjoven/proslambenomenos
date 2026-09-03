#!/usr/bin/env python3
"""Verification for the P-44 claim jin-engine-corroborated, by
independent live reimplementation: 2x2 closed-form Hermitian
eigenvalues (no iterative eigensolver), a fixed literal instance
(no RNG), its own quadrature for the scalar mass identity, and
the pinned extremal family. Nothing imported from the experiment
scripts, nothing read from results files.

Checks: (1) scalar mass-two: for b inside the disk of radius R,
(R/2pi) int (nu/(R nu - b) + conj) dt = 2 by quadrature at 1e-12
(the n = 1 double layer); (2) the Gramian chain I <= P~ <= 2I and
the k = 1 term on a FIXED legitimate 2x2 instance (literal
numbers) at tau = 1/2; (3) extremal tightness: the pinned family
B = [[eps, 1], [0, -eps]] at eps = 0.01 gives |T| >= 1.999 with
0 < eigmin(2G - P)/|G| <= 1e-6.

--mutant sup-blind   scales f by 1.5 (|f| > 1 on Omega) on the
    extremal instance; the k = 1 inequality fails.
--mutant mass-blind  uses tau = 0.75 (claiming mass 4/3) on the
    extremal instance; the chain breaks.
--mutant gram-blind  keeps the fixed instance's lambda and replaces
    its Gramian by one of correlation 0.999 (S' = [[1, 1], [0,
    0.045]]) - a G that is not the Gramian of the S that carries
    those lambda as f(beta) with |f| <= 1 on a domain containing
    W(B); 2G - P turns indefinite (A-27, R-45a item 3: sup-blind and
    mass-blind both move tau*lambda; this one moves G).
Mutant mode also checks |T| <= 2 on the extremal instance, so the
sup-blind mutant is caught by the bound it violates and not only by
the chain (R-45a).
"""
import cmath
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"sup-blind", "mass-blind", "gram-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)


def eig2_h(a, b, c):
    """Eigenvalues of [[a, b], [conj(b), c]], a c real."""
    tr = a + c
    disc = math.sqrt(max(0.0, (a - c) ** 2 + 4 * abs(b) ** 2))
    return (tr - disc) / 2, (tr + disc) / 2


def chain(G, lam, tau):
    """Return (eigmin(2G-P)/|G|, eigmin(P-G)/|G|, eigmin k1/|G|)
    for 2x2 Hermitian G."""
    P = [[G[i][j] / (1 - tau * tau * lam[i].conjugate() * lam[j])
          for j in range(2)] for i in range(2)]
    sG = eig2_h(G[0][0].real, G[0][1], G[1][1].real)[1]
    def emin(M):
        return eig2_h(M[0][0].real, M[0][1], M[1][1].real)[0]
    twoGP = [[2 * G[i][j] - P[i][j] for j in range(2)]
             for i in range(2)]
    PG = [[P[i][j] - G[i][j] for j in range(2)] for i in range(2)]
    k1 = [[PG[i][j] - tau * tau * lam[i].conjugate() * G[i][j]
           * lam[j] for j in range(2)] for i in range(2)]
    return emin(twoGP) / sG, emin(PG) / sG, emin(k1) / sG


def opnorm2(T):
    """Largest singular value of a 2x2 complex matrix."""
    a = sum(abs(T[i][j]) ** 2 for i in range(2) for j in range(2))
    det = T[0][0] * T[1][1] - T[0][1] * T[1][0]
    d = abs(det) ** 2
    disc = math.sqrt(max(0.0, a * a - 4 * d))
    return math.sqrt((a + disc) / 2)


def extremal(eps, fscale=1.0, tau=0.5):
    S = [[1 + 0j, 1 + 0j], [0j, -2 * eps + 0j]]
    # w(B) by dense angle scan with the closed-form 2x2 eigmax
    wB = 0.0
    B = [[eps + 0j, 1 + 0j], [0j, -eps + 0j]]
    for k in range(2880):
        th = 2 * math.pi * k / 2880
        z = cmath.exp(-1j * th)
        H = [[(z * B[0][0]).real, (z * B[0][1]
              + (z * B[1][0]).conjugate()) / 2],
             [0, (z * B[1][1]).real]]
        wB = max(wB, eig2_h(H[0][0], H[0][1], H[1][1])[1])
    Rdom = 1.0001 * wB
    lam = [fscale * eps / Rdom + 0j, -fscale * eps / Rdom + 0j]
    G = [[sum(S[k][i].conjugate() * S[k][j] for k in range(2))
          for j in range(2)] for i in range(2)]
    # T = S diag(lam) S^-1
    det = S[0][0] * S[1][1] - S[0][1] * S[1][0]
    Si = [[S[1][1] / det, -S[0][1] / det],
          [-S[1][0] / det, S[0][0] / det]]
    T = [[sum(S[i][k] * lam[k] * Si[k][j] for k in range(2))
          for j in range(2)] for i in range(2)]
    return G, lam, T


def main():
    failures = []
    # (1) scalar mass two
    R, b = 1.3, 0.4 + 0.25j
    N = 20000
    acc = 0.0
    for k in range(N):
        t = 2 * math.pi * k / N
        nu = cmath.exp(1j * t)
        v = nu / (R * nu - b)
        acc += 2 * v.real
    mass = R * acc / N
    print(f"scalar mass: {mass:.14f} (want 2)")
    if abs(mass - 2) > 1e-12:
        print("FAIL: the scalar double layer does not have mass two")
        failures.append("mass")

    # (2) fixed legitimate instance: S literal, f = z/1.2 on disk
    # radius 1.2 >= w(B); beta inside
    S = [[1 + 0j, 0.4 - 0.3j], [0.2j, 1.5 + 0j]]
    G = [[sum(S[k][i].conjugate() * S[k][j] for k in range(2))
          for j in range(2)] for i in range(2)]
    beta = [0.3 + 0.2j, -0.25 + 0.1j]
    lam = [bb / 1.2 for bb in beta]
    if MUTANT == "gram-blind":
        Sg = [[1 + 0j, 1 + 0j], [0j, 0.045 + 0j]]
        G = [[sum(Sg[k][i].conjugate() * Sg[k][j] for k in range(2))
              for j in range(2)] for i in range(2)]
    c2, c1, ck = chain(G, lam, 0.5)
    print(f"fixed instance chain{' (gram-blind G)' if MUTANT == 'gram-blind' else ''}: "
          f"2G-P {c2:.3e}, P-G {c1:.3e}, k1 {ck:.3e}")
    if min(c2, c1, ck) < -1e-12:
        if MUTANT == "gram-blind":
            print("FAIL: asserted a Gramian not of the carrying S; the chain "
                  "breaks - as the legitimacy condition demands")
            failures.append("gram")
        else:
            print("FAIL: the Gramian chain breaks on a legitimate "
                  "instance - Theorem 2 + Proposition 1 refuted")
            failures.append("chain")

    # (3) extremal tightness and the mutants
    fs = 1.5 if MUTANT == "sup-blind" else 1.0
    tau = 0.75 if MUTANT == "mass-blind" else 0.5
    G3, lam3, T3 = extremal(0.01, fscale=fs, tau=tau)
    c2e, c1e, cke = chain(G3, lam3, tau)
    nT = opnorm2(T3)
    print(f"extremal eps=0.01 (fscale {fs}, tau {tau}): |T| {nT:.5f} "
          f"chain {c2e:.2e}/{c1e:.2e}/{cke:.2e}")
    if MUTANT is not None and nT > 2.0 + 1e-9:
        print(f"FAIL: |T| = {nT:.5f} exceeds the bound 2 (mutant mode)")
        failures.append("normT")
    if MUTANT == "sup-blind":
        if cke < -1e-12 or c2e < -1e-12:
            print("FAIL: asserted |f| <= 1.5 is legitimate; the "
                  "chain breaks exactly as the bound demands")
            failures.append("sup")
    elif MUTANT == "mass-blind":
        if min(c2e, c1e, cke) < -1e-12:
            print("FAIL: asserted mass 4/3 (tau = 0.75); the chain "
                  "breaks on the extremal instance")
            failures.append("massb")
    else:
        if not (nT >= 1.999 and 0 < c2e <= 1e-6):
            print("FAIL: extremal tightness off the pinned window")
            failures.append("tight")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 3
    if failures:
        return 1
    print("p44 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
