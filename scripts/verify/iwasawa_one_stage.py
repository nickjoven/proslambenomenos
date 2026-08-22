#!/usr/bin/env python3
"""Verification for sl2r-connected-subgroups and refutation of
iwasawa-one-stage-original (P-3). Written by a context-free auditor
2026-08-22; reviewed. Sections: (1) one-parameter classification by
sign of det X with closed-form vs series exp; (2) the Borel subgroup
AN: unique a*n factorisation, closure, non-abelian; (3) a generic
one-parameter subgroup inside AN equal to none of K, A, N but
conjugate to A; (4) Iwasawa g = k a n for random SL(2,R). The
--mutant asserts the v1 reading (every connected H != {e} is
one-parameter, hence abelian) on H = AN and must fail."""
import sys, math, random
MUTANT = '--mutant' in sys.argv
random.seed(int(sys.argv[sys.argv.index('--seed')+1]) if '--seed' in sys.argv else 3)
EPS = 1e-9
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def add(A,B,s=1): return [[A[i][j]+s*B[i][j] for j in range(2)] for i in range(2)]
def sc(A,s): return [[A[i][j]*s for j in range(2)] for i in range(2)]
def det(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def tr(A): return A[0][0]+A[1][1]
def inv(A): d=det(A); return [[A[1][1]/d,-A[0][1]/d],[-A[1][0]/d,A[0][0]/d]]
def close(A,B,tol=1e-7): return all(abs(A[i][j]-B[i][j])<tol for i in range(2) for j in range(2))
I=[[1.,0.],[0.,1.]]
def exp_series(X,terms=60):
    S=[[1.,0.],[0.,1.]]; T=[[1.,0.],[0.,1.]]
    for n in range(1,terms): T=sc(mm(T,X),1.0/n); S=add(S,T)
    return S
def exp_closed(X):   # X traceless: X^2 = -det(X) I
    d=det(X)
    if d>EPS:  r=math.sqrt(d);  return add(sc(I,math.cos(r)), sc(X,math.sin(r)/r))
    if d<-EPS: r=math.sqrt(-d); return add(sc(I,math.cosh(r)),sc(X,math.sinh(r)/r))
    return add(I,X)
def rand_sl2(scale=1.5):
    a,b,c=(random.uniform(-scale,scale) for _ in range(3)); return [[a,b],[c,-a]]
def kind(X):
    d=det(X)
    return 'elliptic' if d>EPS else ('hyperbolic' if d<-EPS else 'parabolic')
fails=0
def check(cond,msg):
    global fails
    if not cond: fails+=1; print('FAIL:',msg)

# 1. exp classification: sign of det X  <->  trace of exp X vs 2
for _ in range(2000):
    X=rand_sl2(); E=exp_series(X); k=kind(X)
    check(close(E,exp_closed(X)),'closed form != series')
    check(abs(det(E)-1)<1e-7,'exp not in SL(2)')
    t=tr(E)
    if k=='hyperbolic': check(t>2+EPS,'hyperbolic but tr<=2')
    if k=='elliptic':   check(t<2-EPS and t>=-2-EPS,'elliptic but tr not in [-2,2)')
    # parabolic: construct exactly
    a=random.uniform(-1.5,1.5); b=random.uniform(0.2,1.5)*random.choice((-1,1)); P=[[a,b],[-a*a/b,-a]]
    check(abs(det(P))<1e-9 and abs(tr(exp_series(P))-2)<1e-7,'parabolic tr != 2')
    # elliptic with sqrt(det)=2*pi gives exp=I, tr=2: the measure-zero caveat
J=[[0.,-1.],[1.,0.]]
check(close(exp_series(sc(J,2*math.pi)),I),'exp(2 pi J) != I (caveat case)')

# 2. Borel: every upper-triangular g with positive diagonal is a*n uniquely, AN is a group
for _ in range(2000):
    p=math.exp(random.uniform(-2,2)); q=random.uniform(-3,3)
    g=[[p,q],[0.,1/p]]
    a=[[p,0.],[0.,1/p]]; n=[[1.,q/p],[0.,1.]]
    check(close(mm(a,n),g),'g != a n')
    n2=[[1.,q*p],[0.,1.]]                 # g = n' a as well (NA = AN)
    check(close(mm(n2,a),g),'g != n a')
    p2=math.exp(random.uniform(-2,2)); q2=random.uniform(-3,3); h=[[p2,q2],[0.,1/p2]]
    gh=mm(g,h); check(abs(gh[1][0])<EPS and gh[0][0]>0,'AN not closed')
# AN is 2-dimensional and non-abelian: D, N+ independent, [D,N+]=2N+ != 0
D=[[1.,0.],[0.,-1.]]; Np=[[0.,1.],[0.,0.]]
comm=add(mm(D,Np),mm(Np,D),-1)
check(close(comm,sc(Np,2)),'[D,N+] != 2N+')
A1=exp_series(D); N1=exp_series(Np)
abelian=close(mm(A1,N1),mm(N1,A1))
if MUTANT:
    # v1 reading: every connected H != {e} kills exactly ONE stage, i.e. is a
    # one-parameter (hence abelian) subgroup.  AN is connected, nontrivial, not abelian.
    check(abelian,'MUTANT: AN should be abelian if it were one-parameter')
else:
    check(not abelian,'AN unexpectedly abelian')
# 3. generic one-parameter subgroup in AN that is none of K, A, N but conjugate to A
X=add(D,Np)                       # [[1,1],[0,-1]], hyperbolic, upper triangular
g=[[1.,-0.5],[0.,1.]]             # g D g^-1 = D + N+  (n_s D n_s^-1 = D - 2s N+)
check(close(mm(mm(g,D),inv(g)),X),'conjugator wrong')
for _ in range(200):
    t=random.uniform(-2,2); E=exp_series(sc(X,t))
    check(abs(E[1][0])<EPS,'exp(tX) not in AN')
    check(close(E,mm(mm(g,exp_series(sc(D,t))),inv(g))),'exp(tX) not conjugate of A element')
    check(not (abs(E[0][1])<EPS) or abs(t)<EPS,'exp(tX) lies in A')   # off-diagonal nonzero
# 4. Iwasawa g = k a n for random SL(2,R) (Gram-Schmidt on columns)
for _ in range(2000):
    while True:
        M=[[random.uniform(-2,2) for _ in range(2)] for _ in range(2)]
        if abs(det(M))>0.1: break
    s=math.sqrt(abs(det(M))); M=sc(M,1/s)
    if det(M)<0: M=[[M[0][0],-M[0][1]],[M[1][0],-M[1][1]]]
    r=math.hypot(M[0][0],M[1][0]); c,sn=M[0][0]/r,M[1][0]/r
    k=[[c,-sn],[sn,c]]; R=mm(inv(k),M)      # R upper triangular, R00=r>0, R11=1/r
    check(abs(R[1][0])<1e-9 and R[0][0]>0,'KAN: remainder not in AN')
    a=[[R[0][0],0.],[0.,1/R[0][0]]]; n=[[1.,R[0][1]/R[0][0]],[0.,1.]]
    check(close(mm(mm(k,a),n),M),'KAN reconstruction failed')
print('mutant' if MUTANT else 'normal', 'fails =',fails)
sys.exit(1 if fails else 0)
