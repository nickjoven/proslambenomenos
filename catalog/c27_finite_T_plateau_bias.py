"""Model-free plateau widths of the sine circle map measured over T iterations converge as w(T) = w_inf + c T^(-a) with a ~ 2 (the saddle-node passage-time law), not a ~ 1 (resolution), for the 1/2 and 1/3 plateaus at K = 0.5 and K = 1.
Source: recorded computation scripts/experiments/p8_results.json (sha256-pinned), P-8 / R-5; mechanism: an orbit with pi/sqrt(mu) > T is misjudged locked, displacing the edge by O(T^-2). Mutant: claim a ~ 1."""
import hashlib, json, sys
from pathlib import Path
from _common import mutant_flag, finish

DATA = Path(__file__).resolve().parents[1] / "scripts/experiments/p8_results.json"
PIN = "cd5e27296f05af10f082a0ba07059723175bf04b1bc7c0d2d23c051fccc5b16c"
raw = DATA.read_bytes()
if hashlib.sha256(raw).hexdigest() != PIN:
    print("FAIL: data file hash mismatch"); sys.exit(1)
fits = json.loads(raw)["fits"]
exps = [f["exponent_a"] for f in fits if f["exponent_a"] is not None]
claimed = 1.0 if mutant_flag() else 2.0
ok = len(exps) == 4 and all(abs(a - claimed) < 0.3 for a in exps)
sys.exit(finish(ok, f"fitted exponents {[round(a, 2) for a in exps]} (claimed ~{claimed:.0f})"))
