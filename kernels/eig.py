#!/usr/bin/env python3
"""Eigensolver kernels, extracted (not rewritten) from landed artifacts.

Admission (two-artifact rule, mirror of VOCABULARY.md):
  jacobi_cyclic     scripts/experiments/p7_derive.py:110 (jacobi_eigs),
                    scripts/experiments/p7_plots.py:17,
                    scripts/experiments/p16_walk.py:53,
                    scripts/verify/p16_two_dimensions.py:119-136
  jacobi_classical  scripts/experiments/p24_derive.py:181 (jacobi_eigs),
                    scripts/experiments/p24_plots.py:59 (_jacobi_eigs),
                    scripts/verify/p24_memory_hierarchy.py:48
  sturm_count/eigs  scripts/experiments/p14_derive.py:133-157,
                    scripts/experiments/p18_derive.py:202-224
  eigh              new performance minimum (Householder + implicit-shift
                    QL); admitted as the fast route to the SAME spectra the
                    Jacobi kernels already pin - its selftest anchors are
                    the Jacobi anchors.

Selftest anchors (each cites the derive layer that earned it):
  - Sturm bisection = (4/a^2) sin^2(k pi/(2(n+1))) on the uniform chain
    (p14_derive.py EQ6, line 160-168).
  - cyclic Jacobi = circulant closed form 2(1 - cos(2 pi k/n))
    (p15_derive.py EQ1, line 83-92; p7_derive.py EQ3 validates the same
    kernel against CAS band edges).
  - eigh reproduces the Jacobi spectra on the pinned cases (circulant,
    uniform chain, one p16 sprinkling spectrum) to 1e-9, and is timed
    against cyclic Jacobi at n = 128 and 256.

stdlib only. Every function preserves the floating-point operation
order of its source so ported callers keep identical numbers.
"""
import math

EPS = 2.220446049250313e-16


def jacobi_cyclic(A, tol=1e-10, max_sweeps=40, skip=None):
    """Cyclic Jacobi sweeps, as landed in p7/p16 (see module header).
    tol is the Frobenius off-diagonal target checked before each sweep;
    skip is the per-element rotation threshold (default tol/n^2, the
    p7/p16 experiment form; the p16 verify script passes an absolute
    1e-13). Returns the sorted eigenvalues."""
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < tol:
            break
        sk = tol / (n * n) if skip is None else skip
        for p in range(n - 1):
            ap = a[p]
            for q_ in range(p + 1, n):
                if abs(ap[q_]) < sk:
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


def jacobi_classical(A, sweeps=400):
    """Largest-pivot Jacobi, as landed in p24 (see module header).
    Returns the sorted eigenvalues."""
    n = len(A)
    a = [r[:] for r in A]
    for _ in range(sweeps):
        off = max((abs(a[i][j]), i, j) for i in range(n) for j in range(i + 1, n))
        if off[0] < 1e-12:
            break
        _, p, q = off
        th = math.pi / 4 if a[p][p] == a[q][q] else \
            0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(th), math.sin(th)
        for k in range(n):
            apk, aqk = a[p][k], a[q][k]
            a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
        for k in range(n):
            akp, akq = a[k][p], a[k][q]
            a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
    return sorted(a[i][i] for i in range(n))


def sturm_count(diag, off, lam):
    """Sturm-sequence sign count for a symmetric tridiagonal matrix:
    the number of eigenvalues below lam (p14_derive.py:133)."""
    cnt = 0
    q = diag[0] - lam
    if q < 0:
        cnt += 1
    for i in range(1, len(diag)):
        e2 = off[i - 1] * off[i - 1]
        q = diag[i] - lam - (e2 / q if q != 0 else e2 / 1e-300)
        if q < 0:
            cnt += 1
    return cnt


def sturm_eigs(diag, off, kmax, lo, hi, iters=100):
    """The kmax lowest tridiagonal eigenvalues by Sturm bisection on
    [lo, hi] (p14_derive.py:146)."""
    out = []
    for kk in range(1, kmax + 1):
        a_, b_ = lo, hi
        for _ in range(iters):
            mid = 0.5 * (a_ + b_)
            if sturm_count(diag, off, mid) >= kk:
                b_ = mid
            else:
                a_ = mid
        out.append(0.5 * (a_ + b_))
    return out


def _householder_tridiag(A):
    """Householder reduction of a symmetric matrix to tridiagonal form,
    eigenvalues-only variant (no eigenvector accumulation). Returns
    (d, e) with e[i] the subdiagonal coupling d[i-1] <-> d[i]."""
    n = len(A)
    a = [row[:] for row in A]
    d = [0.0] * n
    e = [0.0] * n
    for i in range(n - 1, 0, -1):
        l = i - 1
        h = 0.0
        if l > 0:
            scale = 0.0
            for k in range(l + 1):
                scale += abs(a[i][k])
            if scale == 0.0:
                e[i] = a[i][l]
            else:
                for k in range(l + 1):
                    a[i][k] /= scale
                    h += a[i][k] * a[i][k]
                f = a[i][l]
                g = -math.sqrt(h) if f >= 0 else math.sqrt(h)
                e[i] = scale * g
                h -= f * g
                a[i][l] = f - g
                f = 0.0
                for j in range(l + 1):
                    g = 0.0
                    aj = a[j]
                    ai = a[i]
                    for k in range(j + 1):
                        g += aj[k] * ai[k]
                    for k in range(j + 1, l + 1):
                        g += a[k][j] * ai[k]
                    e[j] = g / h
                    f += e[j] * ai[j]
                hh = f / (h + h)
                for j in range(l + 1):
                    f = a[i][j]
                    e[j] = g = e[j] - hh * f
                    aj = a[j]
                    ai = a[i]
                    for k in range(j + 1):
                        aj[k] -= f * e[k] + g * ai[k]
        else:
            e[i] = a[i][l]
        d[i] = h
    for i in range(n):
        d[i] = a[i][i]
    return d, e


def _ql_implicit(d, e):
    """Implicit-shift QL on a tridiagonal (d, e) pair as produced by
    _householder_tridiag; eigenvalues only. Modifies copies; returns
    the sorted eigenvalues."""
    n = len(d)
    d = d[:]
    e = e[1:] + [0.0]
    for l in range(n):
        its = 0
        while True:
            m = l
            while m < n - 1:
                dd = abs(d[m]) + abs(d[m + 1])
                if abs(e[m]) <= EPS * dd:
                    break
                m += 1
            if m == l:
                break
            its += 1
            if its > 60:
                raise RuntimeError("QL: too many iterations")
            g = (d[l + 1] - d[l]) / (2.0 * e[l])
            r = math.hypot(g, 1.0)
            g = d[m] - d[l] + e[l] / (g + (r if g >= 0 else -r))
            s = c = 1.0
            p = 0.0
            broke = False
            for i in range(m - 1, l - 1, -1):
                f = s * e[i]
                b = c * e[i]
                r = math.hypot(f, g)
                e[i + 1] = r
                if r == 0.0:
                    d[i + 1] -= p
                    e[m] = 0.0
                    broke = True
                    break
                s = f / r
                c = g / r
                g = d[i + 1] - p
                r = (d[i] - g) * s + 2.0 * c * b
                p = s * r
                d[i + 1] = g + p
                g = c * r - b
            if broke:
                continue
            d[l] -= p
            e[l] = g
            e[m] = 0.0
    return sorted(d)


def eigh(A):
    """All eigenvalues of a symmetric matrix by Householder
    tridiagonalization + implicit-shift QL (the performance minimum:
    O(n^3) with a small constant vs Jacobi's repeated full sweeps).
    Returns the sorted eigenvalues; anchored against the Jacobi
    kernels in --selftest."""
    d, e = _householder_tridiag(A)
    return _ql_implicit(d, e)


# ---------------------------------------------------------------- selftest
def _cycle_laplacian(n):
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = 2.0
        L[i][(i + 1) % n] -= 1.0
        L[i][(i - 1) % n] -= 1.0
    return L


def _chain(n):
    A = [[0.0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 2.0
        if i:
            A[i][i - 1] = A[i - 1][i] = -1.0
    return A


def _sprinkling_laplacian():
    """The p16 verify script's own N = 80 sprinkling Laplacian
    (scripts/verify/p16_two_dimensions.py:66-117, seed 31416)."""
    from kernels.causet import sprinkle, hasse_links
    N = 80
    pts = sprinkle(N, 31416)
    links = hasse_links(pts)
    deg = [0] * N
    for (j, i) in links:
        deg[j] += 1
        deg[i] += 1
    L = [[0.0] * N for _ in range(N)]
    for i in range(N):
        L[i][i] = 1.0 if deg[i] else 0.0
    for (j, i) in links:
        w = -1.0 / math.sqrt(deg[j] * deg[i])
        L[j][i] += w
        L[i][j] += w
    return L


def _selftest(full=False):
    import random
    import time
    ok = True

    # anchor 1: Sturm vs the uniform chain's Dirichlet spectrum
    # (p14_derive.py EQ6: (4/a^2) sin^2(k pi/(2(n+1))) with a = 1)
    n = 200
    eig = sturm_eigs([2.0] * n, [-1.0] * (n - 1), 20, 0.0, 4.1)
    exact = [4 * math.sin(k * math.pi / (2 * (n + 1))) ** 2 for k in range(1, 21)]
    w1 = max(abs(e - x) / x for e, x in zip(eig, exact))
    ok &= w1 < 1e-12
    print(f"sturm vs (4/a^2) sin^2 chain spectrum: worst rel dev {w1:.2e}"
          f" {'ok' if w1 < 1e-12 else 'FAIL'}")

    # anchor 2: cyclic and classical Jacobi vs the circulant closed form
    # (p15_derive.py EQ1: lambda_k = 2(1 - cos(2 pi k/n)))
    n = 12
    closed = sorted(2 * (1 - math.cos(2 * math.pi * k / n)) for k in range(n))
    w2 = max(abs(a - b) for a, b in zip(jacobi_cyclic(_cycle_laplacian(n)), closed))
    w2c = max(abs(a - b) for a, b in zip(jacobi_classical(_cycle_laplacian(n)), closed))
    ok &= w2 < 1e-10 and w2c < 1e-10
    print(f"jacobi (cyclic/classical) vs circulant closed form: "
          f"{w2:.2e}/{w2c:.2e} {'ok' if w2 < 1e-10 and w2c < 1e-10 else 'FAIL'}")

    # anchor 3: eigh vs Jacobi on the pinned cases
    cases = [("circulant n=24", _cycle_laplacian(24)),
             ("uniform chain n=32", _chain(32)),
             ("p16 sprinkling N=80", _sprinkling_laplacian())]
    for name, A in cases:
        d = max(abs(a - b) for a, b in zip(eigh(A), jacobi_cyclic(A, tol=1e-12)))
        ok &= d < 1e-9
        print(f"eigh vs jacobi, {name}: worst dev {d:.2e} "
              f"{'ok' if d < 1e-9 else 'FAIL'}")

    # timing: eigh vs cyclic Jacobi at n = 128 (and 256 with --full;
    # the full Jacobi run at 256 alone takes ~25 s, past the ~5 s
    # selftest budget) on a seeded random symmetric matrix.
    # Measured on the reference box: n=128 eigh 0.10 s vs jacobi
    # 2.78 s (x27); n=256 eigh 0.74 s vs jacobi 25.85 s (x35).
    for n in (128, 256) if full else (128,):
        rng = random.Random(1234 + n)
        A = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = A[j][i] = rng.gauss(0.0, 1.0)
        t0 = time.perf_counter()
        eh = eigh(A)
        t_eigh = time.perf_counter() - t0
        t0 = time.perf_counter()
        ej = jacobi_cyclic(A, tol=1e-9)
        t_jac = time.perf_counter() - t0
        dev = max(abs(a - b) for a, b in zip(eh, ej))
        ok &= dev < 1e-8
        print(f"timing n={n}: eigh {t_eigh:.2f} s vs jacobi {t_jac:.2f} s "
              f"(x{t_jac / t_eigh:.1f}); spectra agree to {dev:.1e} "
              f"{'ok' if dev < 1e-8 else 'FAIL'}")

    print("eig selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
        sys.exit(_selftest(full="--full" in sys.argv))
    print(__doc__)
