"""On E1's pinned twisted ring, the 1/2-plateau shrinkage ratio r(N) = w_twisted/w_control for N = 4..9 shows no even/odd alternation at (K,J) = (1.0,0.6) or (1.4,0.6) (sign changes of r(N+1)-r(N) do not alternate), and the control width is N-independent under an in-phase initial condition.
Source: recorded computation scripts/experiments/p9_results_attractor.json (sha256-pinned), P-9 / R-6. Mutant: claim Lazarides-type alternation (signs alternate with N)."""
import hashlib, json, sys
from pathlib import Path
from _common import mutant_flag, finish

DATA = Path(__file__).resolve().parents[1] / "scripts/experiments/p9_results_attractor.json"
PIN = "63ed97ee90b2fe55f12c297361e9ae3d2458312738919f7e53729dc99ac3902b"
raw = DATA.read_bytes()
if hashlib.sha256(raw).hexdigest() != PIN:
    print("FAIL: data file hash mismatch"); sys.exit(1)
rat = json.loads(raw)["ratios"]
out = []; ok = True
for K in (1.0, 1.4):
    rs = [r for r in rat if r["K"] == K]
    rs.sort(key=lambda r: r["N"])
    ratios = [r["ratio"] for r in rs]
    signs = [1 if b > a else -1 for a, b in zip(ratios, ratios[1:])]
    alternating = all(s1 == -s2 for s1, s2 in zip(signs, signs[1:]))
    control_const = max(r["w_control"] for r in rs) - min(r["w_control"] for r in rs) < 1e-9
    out.append(f"K={K}: ratios {[round(x, 3) for x in ratios]} signs {signs} alternating {alternating}")
    ok &= control_const and (alternating if mutant_flag() else not alternating)
sys.exit(finish(ok, "; ".join(out)))
