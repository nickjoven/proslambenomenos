#!/usr/bin/env python3
"""Numerical spot-checks of Jin, 'The Numerical Range Is a 2-Spectral Set' (v4).

Pure stdlib. Targets the NEW intermediate objects, not the classical inequality:
  A. mass-2 of the numerical-range double layer (eq. 34)
  B. Carathéodory properties + adjoint-algebra (diagonal) defect of H (Prop 1)
  C. the derived Gramian inequalities I <= P~ <= 2I and tau^2 T~*T~ <= P~ - I
     (the heart of Theorem 2's conclusion), on random legitimate instances
  D. end-to-end sampled-kernel check: Big Gram PSD, exact Psi-cancellation,
     compressed inequality (22) PSD
  E. mutants (falsifier teeth): |f|>1, mass<2 (tau>1/2), wrong auxiliary basis
"""
import cmath, math, random

# ---------- complex linear algebra (lists of lists) ----------
def zeros(n, m=None):
    m = n if m is None else m
    return [[0j]*m for _ in range(n)]

def eye(n):
    A = zeros(n)
    for i in range(n): A[i][i] = 1+0j
    return A

def mm(A, B):
    n, k, m = len(A), len(B), len(B[0])
    C = zeros(n, m)
    for i in range(n):
        Ai = A[i]
        for l in range(k):
            a = Ai[l]
            if a == 0: continue
            Bl = B[l]
            Ci = C[i]
            for j in range(m): Ci[j] += a*Bl[j]
    return C

def madd(A, B, ca=1, cb=1):
    return [[ca*A[i][j]+cb*B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def dag(A):
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]

def smul(c, A):
    return [[c*x for x in row] for row in A]

def inv(A):
    n = len(A)
    M = [row[:] + [1j*0 if j != i else 1+0j for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[p][col]) < 1e-300: raise ZeroDivisionError('singular')
        M[col], M[p] = M[p], M[col]
        piv = M[col][col]
        M[col] = [x/piv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [xr - f*xc for xr, xc in zip(M[r], M[col])]
    return [row[n:] for row in M]

def herm_part(A):
    return smul(0.5, madd(A, dag(A)))

def fro_offdiag(A):
    return math.sqrt(sum(abs(A[i][j])**2 for i in range(len(A)) for j in range(len(A)) if i != j))

def fro(A):
    return math.sqrt(sum(abs(x)**2 for row in A for x in row))

def jacobi_eig(Ain, tol=1e-13, maxsweep=100):
    """Hermitian eigenvalues (real list, ascending) via complex Jacobi."""
    n = len(Ain)
    A = [row[:] for row in Ain]
    for _ in range(maxsweep):
        off = fro_offdiag(A)
        if off < tol*max(1e-300, fro(A)): break
        for p in range(n-1):
            for q in range(p+1, n):
                g = A[p][q]
                if abs(g) < 1e-300: continue
                app, aqq = A[p][p].real, A[q][q].real
                phi = cmath.phase(g)
                absg = abs(g)
                if abs(app-aqq) < 1e-300:
                    theta = math.pi/4
                else:
                    theta = 0.5*math.atan2(2*absg, app-aqq)
                c, s = math.cos(theta), math.sin(theta)
                eip = cmath.exp(1j*phi)
                # U columns: up = c*ep + s*e^{-iphi}... apply rotation on p,q
                # new vectors: |p'> = c|p> + s e^{-i phi}|q>, |q'> = -s e^{i phi}|p> + c|q>
                for k in range(n):  # A <- U* A (rows)
                    akp, akq = A[p][k], A[q][k]
                    A[p][k] = c*akp + s*eip.conjugate().conjugate()*0 + s*(eip.conjugate())*akq*0 + s*eip*akq if False else c*akp + s*eip*akq
                    A[q][k] = -s*eip.conjugate()*akp + c*akq
                for k in range(n):  # A <- A U (cols)
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c*akp + s*eip.conjugate()*akq
                    A[k][q] = -s*eip*akp + c*akq
    return sorted(A[i][i].real for i in range(n))

def eigmin(A): return jacobi_eig(A)[0]
def eigmax(A): return jacobi_eig(A)[-1]

def opnorm(A): return math.sqrt(max(0.0, eigmax(mm(dag(A), A))))

# ---------- instance construction ----------
def randc(rng, r=1.0):
    return complex(rng.uniform(-r, r), rng.uniform(-r, r))

def make_instance(rng, n, cond_pow=2.0, deg=5):
    """B = S diag(beta) S^-1 simple spectrum; Omega = disk radius Rdom > w(B);
    f = random poly normalized to sup<=1 on Omega closure. Returns dict."""
    beta = []
    while len(beta) < n:
        z = randc(rng, 0.6)
        if all(abs(z-b) > 1e-3 for b in beta): beta.append(z)
    S0 = [[randc(rng) for _ in range(n)] for _ in range(n)]
    D = [10**rng.uniform(-cond_pow, cond_pow) for _ in range(n)]
    S = [[S0[i][j]*D[j] for j in range(n)] for i in range(n)]
    Si = inv(S)
    B = mm(S, mm([[beta[i] if i == j else 0j for j in range(n)] for i in range(n)], Si))
    # numerical radius
    wB = 0.0
    for k in range(360):
        th = 2*math.pi*k/360
        wB = max(wB, eigmax(herm_part(smul(cmath.exp(-1j*th), B))))
    Rdom = 1.02*wB
    coeffs = [randc(rng) for _ in range(deg+1)]
    # normalize on |z|=Rdom
    M = max(abs(sum(c*(Rdom*cmath.exp(2j*math.pi*k/512))**j for j, c in enumerate(coeffs)))
            for k in range(512))
    coeffs = [c/(M*(1+1e-9)) for c in coeffs]
    f = lambda z: sum(c*z**j for j, c in enumerate(coeffs))
    lam = [f(b) for b in beta]
    T = mm(S, mm([[lam[i] if i == j else 0j for j in range(n)] for i in range(n)], Si))
    G = mm(dag(S), S)
    return dict(n=n, beta=beta, S=S, Si=Si, B=B, T=T, G=G, lam=lam, f=f, Rdom=Rdom, wB=wB)

def PQ(G, lam, tau):
    n = len(lam)
    P = [[G[i][j]/(1 - tau*tau*lam[i].conjugate()*lam[j]) for j in range(n)] for i in range(n)]
    Q = [[G[i][j]/(1 - tau*lam[i].conjugate()*lam[j]) for j in range(n)] for i in range(n)]
    return P, Q

def core_checks(inst, tau=0.5):
    """Check c: 2G-P >=0, P-G >= 0, P-G-tau^2 Lam* G Lam >= 0, |T| <= 1/tau*1(f<=1)."""
    G, lam, n = inst['G'], inst['lam'], inst['n']
    P, Q = PQ(G, lam, tau)
    LGL = [[lam[i].conjugate()*G[i][j]*lam[j] for j in range(n)] for i in range(n)]
    sG = eigmax(G)
    r = {}
    r['min_2G_P'] = eigmin(madd(smul(2, G), P, 1, -1))/sG      # P~ <= 2I
    r['min_P_G'] = eigmin(madd(P, G, 1, -1))/sG                # P~ >= I
    r['min_k1'] = eigmin(madd(madd(P, G, 1, -1), LGL, 1, -tau*tau))/sG  # k=1 term
    r['normT'] = opnorm(inst['T'])
    return r

# ---------- quadrature layer ----------
def double_layer(inst, N=1024):
    """A1[t] = nu*(gamma I - B)^-1 on circle |z|=Rdom. D = (R/2pi)(A1+A1*)."""
    B, R = inst['B'], inst['Rdom']
    n = inst['n']
    A1 = []
    gam = []
    for k in range(N):
        t = 2*math.pi*k/N
        nu = cmath.exp(1j*t)
        g = R*nu
        Rt = inv(madd(smul(g, eye(n)), B, 1, -1))
        A1.append(smul(nu, Rt))
        gam.append(g)
    return A1, gam

def H_of_w(inst, A1, gam, w, N):
    """H(w) = (1/2) * int c_w(t) D_B(t) dt, D_B = (R/2pi)(A1 + A1^*)."""
    n, R = inst['n'], inst['Rdom']
    f = inst['f']
    Acc = zeros(n)
    for k in range(N):
        fw = w*f(gam[k])
        c = (1+fw)/(1-fw)
        Dk = madd(A1[k], dag(A1[k]))
        for i in range(n):
            for j in range(n):
                Acc[i][j] += c*Dk[i][j]
    return smul(R/(2*N), Acc)   # (1/2)*(R/2pi)*(2pi/N) = R/(2N)

def main():
    rng = random.Random(20260901)
    print('=== A+B+D: quadrature checks on one moderate instance (n=4) ===')
    inst = make_instance(rng, 4, cond_pow=1.2)
    n = inst['n']
    N = 2048
    A1, gam = double_layer(inst, N)
    # A: mass
    Mass = zeros(n)
    for k in range(N):
        Dk = madd(A1[k], dag(A1[k]))
        Mass = madd(Mass, smul(inst['Rdom']/N, Dk))
    print('  mass defect |int D - 2I|_F =', '%.2e' % fro(madd(Mass, smul(2, eye(n)), 1, -1)))
    # B: Caratheodory + diagonal defect
    S, Si, T, G = inst['S'], inst['Si'], inst['T'], inst['G']
    Sd = dag(S); Sdi = inv(Sd)
    ws = [0j, 0.3+0.4j, -0.7+0j, 0.5j, 0.85*cmath.exp(2.1j)]
    for w in ws:
        H = H_of_w(inst, A1, gam, w, N)
        E = madd(H, inv(madd(eye(n), T, 1, -w)), 1, -1)   # H - (I-wT)^-1
        Theta = mm(Sd, mm(E, Sdi))
        reHmin = eigmin(herm_part(H))
        od = fro_offdiag(Theta)/max(1e-300, fro(Theta)) if fro(Theta) > 1e-12 else 0.0
        print('  w=%s  eigmin(ReH)=% .3e  |offdiag(Theta)|/|Theta|=%.2e' % (str(w), reHmin, od))
    # D: sampled kernel end-to-end
    tau = 0.5
    lam = inst['lam']
    P, Q = PQ(G, lam, tau)
    wpts = [ (tau*l.conjugate()) for l in lam ]
    Hs = [mm(Sd, mm(H_of_w(inst, A1, gam, w, N), S)) for w in wpts]   # H~(w_i)
    H0 = mm(Sd, mm(H_of_w(inst, A1, gam, 0j, N), S))
    # Big 2n x 2n Gram in (u, v)
    Big = zeros(2*n)
    for i in range(n):
        for j in range(n):
            Kij = madd(Hs[i], dag(Hs[j]))
            Big[i][j] = Kij[i][j]/(1 - wpts[i]*wpts[j].conjugate())
    for i in range(n):
        Krow = madd(Hs[i], dag(H0))   # K(w_i, 0), denominator 1
        for j in range(n):
            Big[i][n+j] = Krow[i][j]
            Big[n+j][i] = Krow[i][j].conjugate()
    K00 = madd(H0, dag(H0))
    for i in range(n):
        for j in range(n):
            Big[n+i][n+j] = K00[i][j]
    sBig = max(1.0, eigmax(herm_part(Big)))
    print('  eigmin(Big sampled Gram)/scale = % .3e' % (eigmin(herm_part(Big))/sBig,))
    # compressed (22): M - R0 G^-1 P - P G^-1 R0 + 2 P G^-1 P with M=2P+4Y, R0=G+Q
    Gi = inv(G)
    Y = madd(Q, P, 1, -1)
    Mm = madd(smul(2, P), smul(4*tau/(1-tau), Y))
    R0 = madd(smul(2*(1-tau), G), smul(2*tau, Q))
    C1 = mm(R0, mm(Gi, P))
    Comp = madd(madd(Mm, madd(C1, dag(C1)), 1, -1), smul(2, mm(P, mm(Gi, P))))
    print('  eigmin(compressed (22))/|G| = % .3e' % (eigmin(herm_part(Comp))/eigmax(G),))
    # cancellation: Comp should equal [I;-G^-1 P]* Big [I;-G^-1 P] (built from TRUE H incl. Psi)
    GiP = mm(Gi, P)
    X = [[ (1+0j if i == j else 0j) for j in range(n)] for i in range(n)] + \
        [[ -GiP[i][j] for j in range(n)] for i in range(n)]
    CompTrue = mm(dag(X), mm(Big, X))
    print('  |Comp_formula - Comp_from_true_H|/|Comp| = %.2e' %
          (fro(madd(Comp, CompTrue, 1, -1))/max(1e-300, fro(Comp)),))

    print()
    print('=== C: Gramian inequality hunt, random legitimate instances ===')
    worst = {'min_2G_P': 1e9, 'min_P_G': 1e9, 'min_k1': 1e9}
    maxT = 0.0
    trials = 400
    for t in range(trials):
        nn = rng.choice([2, 2, 3, 3, 4, 5])
        cp = rng.uniform(0.5, 3.0)
        ins = make_instance(rng, nn, cond_pow=cp, deg=rng.choice([1, 2, 3, 5, 8]))
        r = core_checks(ins)
        for k in worst: worst[k] = min(worst[k], r[k])
        maxT = max(maxT, r['normT'])
    print('  trials=%d  worst eigmin(2G-P)/|G| = % .3e  (negative => paper REFUTED)' % (trials, worst['min_2G_P']))
    print('  worst eigmin(P-G)/|G| = % .3e   worst k=1 slack = % .3e' % (worst['min_P_G'], worst['min_k1']))
    print('  max |T| over trials = %.4f (claim: <= 2)' % maxT)

    print()
    print('=== near-extremal Jordan stress (ratio -> 2) ===')
    for eps in [0.3, 0.1, 0.03, 0.01]:
        # B ~ [[eps, 1],[0, -eps]] in basis S=I ; f = z / Rdom-normalized identity-ish
        beta = [eps, -eps]
        S = [[1+0j, 0j], [0j, 1e-0j+0j]]
        # use S=I but the matrix B=[[eps,1],[0,-eps]] means S is eigenvector matrix:
        # eigenvectors: v1=(1,0), v2=(1, -2eps) approx; construct directly
        B = [[eps+0j, 1+0j], [0j, -eps+0j]]
        # eigendecomp by hand
        v2 = [1+0j, -2*eps+0j]
        S = [[1+0j, v2[0]], [0j, v2[1]]]
        Si = inv(S)
        wB = 0.0
        for k in range(720):
            th = 2*math.pi*k/720
            wB = max(wB, eigmax(herm_part(smul(cmath.exp(-1j*th), B))))
        Rdom = 1.0001*wB
        f = lambda z, R=Rdom: z/R
        lam = [f(b) for b in beta]
        G = mm(dag(S), S)
        T = mm(S, mm([[lam[0], 0j], [0j, lam[1]]], Si))
        r = {'G': G, 'lam': lam, 'T': T, 'n': 2}
        rr = core_checks({'G': G, 'lam': lam, 'T': T, 'n': 2})
        # eigmax of P~ : largest gen-eig of P vs G -> report via bisection on 2G-P .. use eigmax(G^-1P) approx
        print('  eps=%.3g |T|=%.5f  eigmin(2G-P)/|G|=% .3e  eigmin(P-G)/|G|=% .3e' %
              (eps, rr['normT'], rr['min_2G_P'], rr['min_P_G']))

    print()
    print('=== E: mutants (the checks must be able to fail) ===')
    fails = {'m1_f1.5': 0, 'm2_tau0.75': 0}
    trials_m = 150
    for t in range(trials_m):
        ins = make_instance(rng, rng.choice([2, 3, 4]), cond_pow=rng.uniform(0.5, 2.5))
        lam15 = [1.5*l for l in ins['lam']]
        P15, _ = PQ(ins['G'], lam15, 0.5)
        if eigmin(madd(smul(2, ins['G']), P15, 1, -1)) < 0: fails['m1_f1.5'] += 1
        P75, _ = PQ(ins['G'], ins['lam'], 0.75)
        if eigmin(madd(smul(2, ins['G']), P75, 1, -1)) < 0: fails['m2_tau0.75'] += 1
    print('  mutant |f|<=1.5 (illegal): 2G-P fails in %d/%d trials' % (fails['m1_f1.5'], trials_m))
    print('  mutant tau=0.75 (mass 4/3 < 2): 2G-P_tau fails in %d/%d trials' % (fails['m2_tau0.75'], trials_m))
    # m3: wrong auxiliary basis -> Theta not diagonal
    ins = make_instance(rng, 3, cond_pow=1.0)
    N2 = 1024
    A1b, gamb = double_layer(ins, N2)
    H = H_of_w(ins, A1b, gamb, 0.4+0.3j, N2)
    E1 = madd(H, inv(madd(eye(3), ins['T'], 1, -(0.4+0.3j))), 1, -1)
    Swrong = [[randc(rng) for _ in range(3)] for _ in range(3)]
    Thw = mm(dag(Swrong), mm(E1, inv(dag(Swrong))))
    Thr = mm(dag(ins['S']), mm(E1, inv(dag(ins['S']))))
    print('  mutant wrong-basis Theta offdiag ratio: right=%.2e wrong=%.2e' %
          (fro_offdiag(Thr)/fro(Thr), fro_offdiag(Thw)/fro(Thw)))

if __name__ == '__main__':
    main()
