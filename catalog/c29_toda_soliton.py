"""On the Toda chain (force 1 - e^-r, unit mass) the exact one-soliton keeps its peak to 0.1% over 40 time units and travels at v/c = sinh(k)/k > 1 (within 3%), while the same profile on the linear chain (force r, same sound speed) loses more than a quarter of its peak: nonlinearity balancing dispersion in an inertial medium is what makes a corner survive.
Source: Toda, J. Phys. Soc. Jpn. 22, 431 (1967); Toda, Theory of Nonlinear Lattices (1989); the linear null is Schrodinger 1914 (c11). Mutant: linear force - the soliton disperses."""
import math, sys
from _common import mutant_flag, finish

N, DT, T, kap, x0 = 240, 0.02, 40.0, 1.0, 60
toda = not mutant_flag()
force = (lambda r: 1.0 - math.exp(-r)) if toda else (lambda r: r)
sech2 = lambda x: 0.0 if abs(x) > 350 else 1.0 / math.cosh(x) ** 2
beta = math.sinh(kap)
rt = lambda n, t: -math.log(1 + math.sinh(kap) ** 2 * sech2(kap * (n - x0) - beta * t))
def disp(t):
    u = [0.0] * N
    for n in range(1, N): u[n] = u[n - 1] + rt(n - 1, t)
    return u
h = 1e-4
u = disp(0.0); um = disp(-h); w = [(a - b) / h for a, b in zip(u, um)]
def accel(u):
    a = [0.0] * N
    for i in range(1, N - 1): a[i] = force(u[i + 1] - u[i]) - force(u[i] - u[i - 1])
    return a
def peak(u):
    r = [u[i + 1] - u[i] for i in range(N - 1)]
    i = min(range(N - 1), key=lambda n: r[n]); return i, -r[i]
p0, pk0 = peak(u)
a = accel(u)
for _ in range(int(T / DT)):
    for i in range(N): w[i] += 0.5 * DT * a[i]; u[i] += DT * w[i]
    a = accel(u)
    for i in range(N): w[i] += 0.5 * DT * a[i]
p1, pk1 = peak(u)
v = (p1 - p0) / T; vth = math.sinh(kap) / kap
kept = pk1 / pk0
ok = kept > 0.999 and abs(v - vth) / vth < 0.03
sys.exit(finish(ok, f"peak retained {kept:.4f}; speed {v:.3f} vs sinh(k)/k = {vth:.3f}"))
