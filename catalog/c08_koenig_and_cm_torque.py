"""Koenig: L = R_cm x P + L_about_cm and T = M V_cm^2/2 + T_rel; uniform gravity exerts zero torque about the CM.
Source: Goldstein, Classical Mechanics ch. 1. Mutant: omit the CM term in L."""
import random, sys
from _common import mutant_flag, finish

random.seed(5)
N = 7
m = [random.uniform(0.5, 2) for _ in range(N)]
r = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(N)]
v = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(N)]
M = sum(m)
R = [sum(m[i] * r[i][k] for i in range(N)) / M for k in range(3)]
V = [sum(m[i] * v[i][k] for i in range(N)) / M for k in range(3)]
cross = lambda a, b: [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
L = [sum(m[i] * cross(r[i], v[i])[k] for i in range(N)) for k in range(3)]
L_rel = [sum(m[i] * cross([r[i][j] - R[j] for j in range(3)], [v[i][j] - V[j] for j in range(3)])[k] for i in range(N)) for k in range(3)]
L_cm = cross(R, [M * V[k] for k in range(3)])
L_pred = [L_rel[k] + (0 if mutant_flag() else L_cm[k]) for k in range(3)]
T = sum(0.5 * m[i] * sum(v[i][k] ** 2 for k in range(3)) for i in range(N))
T_pred = 0.5 * M * sum(V[k] ** 2 for k in range(3)) + sum(0.5 * m[i] * sum((v[i][k] - V[k]) ** 2 for k in range(3)) for i in range(N))
g = [0, 0, -9.81]
tau_cm = [sum(cross([r[i][j] - R[j] for j in range(3)], [m[i] * g[k] for k in range(3)])[kk] for i in range(N)) for kk in range(3)]
errL = max(abs(L[k] - L_pred[k]) for k in range(3))
ok = errL < 1e-12 and abs(T - T_pred) < 1e-12 and max(abs(t) for t in tau_cm) < 1e-12
sys.exit(finish(ok, f"|L - (R x P + L_cm)| = {errL:.1e}; |T - split| = {abs(T - T_pred):.1e}; |torque about CM| = {max(abs(t) for t in tau_cm):.1e}"))
