"""A uniform gravitational field exerts zero net torque about the center of mass.
Source: Goldstein ch. 1 (weight acts at the CM). Mutant: torque about a point displaced from the CM, which is nonzero."""
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
g = [0, 0, -9.81]
about = [R[k] + (0.3 if mutant_flag() else 0.0) for k in range(3)]
tau = [sum(cross([r[i][j] - about[j] for j in range(3)], [m[i] * g[k] for k in range(3)])[kk] for i in range(N)) for kk in range(3)]
scale = M * 9.81
ok = max(abs(t) for t in tau) / scale < 1e-12
sys.exit(finish(ok, f"|torque| / (M g) = {max(abs(t) for t in tau) / scale:.1e}"))
