"""P-4 control slip period depends on the dynamic friction coefficient: at N=64, g=0.01, v=0.05, F_N=0.9 the period/round-trip falls from 6.95 (mu_d=0.25) to 5.09 (0.5) to 3.12 (0.75) - a 2.2x swing the loading formula of c12 cannot see.
Source: recorded computation scripts/experiments/p4_mud_results.json (sha256-pinned), found by the 2026-08-22 adversarial audit: the formula assumes re-stick at zero ring force, true only at mu_d = mu_s/2. Mutant: the formula's claim of mu_d-independence (spread < 10%)."""
import hashlib, json, sys
from pathlib import Path
from _common import mutant_flag, finish

DATA = Path(__file__).resolve().parents[1] / "scripts/experiments/p4_mud_results.json"
PIN = "9f1025e7a2af9914dcfe90acd5d1d4f85b50828f83fcde1013aa64ec9d81c6a3"
raw = DATA.read_bytes()
if hashlib.sha256(raw).hexdigest() != PIN:
    print("FAIL: data file hash mismatch")
    sys.exit(1)
rows = sorted(json.loads(raw)["rows"], key=lambda r: r["mu_d"])
ratios = [r["ratio"] for r in rows]
spread = (max(ratios) - min(ratios)) / min(ratios)
monotone = all(a > b for a, b in zip(ratios, ratios[1:]))
ok = (spread < 0.10) if mutant_flag() else (monotone and spread > 1.0)
sys.exit(finish(ok, f"periods {ratios}; spread {spread:.2f}; monotone decreasing {monotone}"))
