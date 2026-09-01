#!/usr/bin/env python3
"""Ellipse-domain test: the adjoint-algebra defect is NON-scalar here, so this
genuinely tests Prop 1's alg(B*) membership + Thm 2's cancellation."""
import cmath, math, random
from p44_spotcheck import (zeros, eye, mm, madd, dag, smul, inv, herm_part,
                              fro, fro_offdiag, eigmin, eigmax, opnorm, randc, PQ)

def ellipse_run(seed=7):
    out = {}
    rng = random.Random(seed)
    n = 4
    # instance
    beta = []
    while len(beta) < n:
        z = randc(rng, 0.5)
        if all(abs(z-b) > 1e-2 for b in beta): beta.append(z)
    S0 = [[randc(rng) for _ in range(n)] for _ in range(n)]
    D = [10**rng.uniform(-1.5, 1.5) for _ in range(n)]
    S = [[S0[i][j]*D[j] for j in range(n)] for i in range(n)]
    Si = inv(S)
    Lb = [[beta[i] if i == j else 0j for j in range(n)] for i in range(n)]
    B = mm(S, mm(Lb, Si))
    wB = 0.0
    for k in range(720):
        th = 2*math.pi*k/720
        wB = max(wB, eigmax(herm_part(smul(cmath.exp(-1j*th), B))))
    a, b = 1.6*wB, 1.05*wB      # ellipse semi-axes, contains disk radius wB
    N = 4096
    # boundary data
    gam, nus, ss = [], [], []
    for k in range(N):
        t = 2*math.pi*k/N
        g = complex(a*math.cos(t), b*math.sin(t))
        gp = complex(-a*math.sin(t), b*math.cos(t))
        s = abs(gp)
        nu = gp/(1j*s)
        gam.append(g); nus.append(nu); ss.append(s)
    # f: random poly normalized on ellipse boundary
    deg = 6
    coeffs = [randc(rng) for _ in range(deg+1)]
    M = max(abs(sum(c*g**j for j, c in enumerate(coeffs))) for g in gam)
    coeffs = [c/(M*(1+1e-9)) for c in coeffs]
    f = lambda z: sum(c*z**j for j, c in enumerate(coeffs))
    lam = [f(bb) for bb in beta]
    T = mm(S, mm([[lam[i] if i == j else 0j for j in range(n)] for i in range(n)], Si))
    G = mm(dag(S), S)
    out['normT'] = opnorm(T)
    print('|T| = %.4f   max|lam| = %.4f   wB=%.3f  ellipse a=%.3f b=%.3f' %
          (out['normT'], max(abs(l) for l in lam), wB, a, b))
    # first layer A1[t] = nu_t (gamma I - B)^-1, density D = (s/2pi)(A1+A1*)
    A1 = []
    for k in range(N):
        Rt = inv(madd(smul(gam[k], eye(n)), B, 1, -1))
        A1.append(smul(nus[k], Rt))
    dt = 2*math.pi/N
    # positivity of density at a few t
    dmin = min(eigmin(herm_part(madd(A1[k], dag(A1[k])))) for k in range(0, N, 256))
    out['density_min'] = dmin
    print('min eig of density samples (>=0 expected): % .3e' % dmin)
    Mass = zeros(n)
    for k in range(N):
        Mass = madd(Mass, smul(ss[k]*dt/(2*math.pi), madd(A1[k], dag(A1[k]))))
    out['mass_defect'] = fro(madd(Mass, smul(2, eye(n)), 1, -1))
    print('mass defect |int D - 2I|_F = %.2e' % out['mass_defect'])

    def H_of_w(w):
        Acc = zeros(n)
        for k in range(N):
            fw = w*f(gam[k])
            c = (1+fw)/(1-fw)
            Dk = madd(A1[k], dag(A1[k]))
            cc = c*ss[k]
            for i in range(n):
                Ai, Di = Acc[i], Dk[i]
                for j in range(n): Ai[j] += cc*Di[j]
        return smul(dt/(4*math.pi), Acc)   # (1/2)*(1/2pi)*sum*dt

    Sd = dag(S); Sdi = inv(Sd)
    out['reH_min'] = 9e9
    out['od_right_max'] = 0.0
    out['od_wrong_min'] = 9e9
    for w in [0.45+0.3j, -0.8+0j, 0.6j]:
        H = H_of_w(w)
        E = madd(H, inv(madd(eye(n), T, 1, -w)), 1, -1)
        Th_right = mm(Sd, mm(E, Sdi))
        Swrong = [[randc(rng) for _ in range(n)] for _ in range(n)]
        Th_wrong = mm(dag(Swrong), mm(E, inv(dag(Swrong))))
        scal = max(1e-300, fro(Th_right))
        # subtract scalar part to show defect itself is non-scalar
        tr = sum(Th_right[i][i] for i in range(n))/n
        nonscal = fro(madd(Th_right, smul(tr, eye(n)), 1, -1))/scal
        rh = eigmin(herm_part(H))
        odr = fro_offdiag(Th_right)/scal
        odw = fro_offdiag(Th_wrong)/max(1e-300, fro(Th_wrong))
        out['reH_min'] = min(out['reH_min'], rh)
        out['od_right_max'] = max(out['od_right_max'], odr)
        out['od_wrong_min'] = min(out['od_wrong_min'], odw)
        print('w=%s eigmin(ReH)=% .3e offdiag(right)=%.2e offdiag(wrong)=%.2e nonscalar=%.2f'
              % (w, rh, odr, odw, nonscal))

    # sampled kernel end-to-end at w_i = conj(lam_i)/2, w_0 = 0
    tau = 0.5
    P, Q = PQ(G, lam, tau)
    wpts = [tau*l.conjugate() for l in lam]
    Hs = [mm(Sd, mm(H_of_w(w), S)) for w in wpts]
    H0 = mm(Sd, mm(H_of_w(0j), S))
    Big = zeros(2*n)
    for i in range(n):
        for j in range(n):
            Kij = madd(Hs[i], dag(Hs[j]))
            Big[i][j] = Kij[i][j]/(1 - wpts[i]*wpts[j].conjugate())
    for i in range(n):
        Krow = madd(Hs[i], dag(H0))
        for j in range(n):
            Big[i][n+j] = Krow[i][j]
            Big[n+j][i] = Krow[i][j].conjugate()
    K00 = madd(H0, dag(H0))
    for i in range(n):
        for j in range(n):
            Big[n+i][n+j] = K00[i][j]
    out['big_min_rel'] = eigmin(herm_part(Big))/eigmax(herm_part(Big))
    print('eigmin(Big Gram)/scale = % .3e' % out['big_min_rel'])
    Gi = inv(G)
    Y = madd(Q, P, 1, -1)
    Mm = madd(smul(2, P), smul(4.0, Y))
    R0 = madd(G, Q)
    C1 = mm(R0, mm(Gi, P))
    Comp = madd(madd(Mm, madd(C1, dag(C1)), 1, -1), smul(2, mm(P, mm(Gi, P))))
    GiP = mm(Gi, P)
    X = [[(1+0j if i == j else 0j) for j in range(n)] for i in range(n)] + \
        [[-GiP[i][j] for j in range(n)] for i in range(n)]
    CompTrue = mm(dag(X), mm(Big, X))
    out['comp_min_rel'] = eigmin(herm_part(Comp))/eigmax(G)
    print('eigmin(compressed (22))/|G| = % .3e' % out['comp_min_rel'])
    out['cancel_rel'] = fro(madd(Comp, CompTrue, 1, -1))/max(1e-300, fro(Comp))
    print('Psi-cancellation: |Comp_formula - Comp_true|/|Comp| = %.2e'
          % out['cancel_rel'])
    out['chain_2G_P'] = eigmin(madd(smul(2, G), P, 1, -1))/eigmax(G)
    out['chain_P_G'] = eigmin(madd(P, G, 1, -1))/eigmax(G)
    print('Gramian chain: eigmin(2G-P)/|G|=% .3e  eigmin(P-G)/|G|=% .3e'
          % (out['chain_2G_P'], out['chain_P_G']))
    return out


def main():
    ellipse_run()


if __name__ == '__main__':
    main()
