"""P-4 control slip periods at mu_d = mu_s/2, g = 0.01: period/round-trip = F_N/(4 J v) within 25% on every stick-slip row whose prediction is >= 3 (16 rows), and the formula has no mu_d term (see c13 for why that limits it).
Source: notes/p4_twisted_inertial_ring.md run 5 + corrections; data scripts/experiments/p4_results_lowdamp.json (sha256-pinned). Mutant: stiffness 2J/N.
Of record: v1 of this entry claimed 'all loading-limited rows' and failed at 27-37% near the Helmholtz period; v2 cut F_N <= 1.5 and >= 3, which also dropped rows at 18-21% (audit); v3 keeps all rows with prediction >= 3 and states 25%."""
import hashlib, json, sys
from pathlib import Path
from _common import mutant_flag, finish

DATA = Path(__file__).resolve().parents[1] / "scripts/experiments/p4_results_lowdamp.json"
PIN = "65614a1e00992a8a63d334cb9525300731a24708960d1a9493bc129380038ff0"
raw = DATA.read_bytes()
if hashlib.sha256(raw).hexdigest() != PIN:
    print("FAIL: data file hash mismatch - p4_results_lowdamp.json changed since this entry was written")
    sys.exit(1)
rows = json.loads(raw)
stiff = 2.0 if mutant_flag() else 4.0
sel = [r for r in rows if r["g"] == 0.01 and r["regime"] == "stick-slip" and r["F_N"] / (4.0 * r["v"]) >= 3.0 - 1e-9]
errs = [abs(r["ratio"] - r["F_N"] / (stiff * r["v"])) / r["ratio"] for r in sel]
ok = len(sel) >= 14 and max(errs) < 0.25
sys.exit(finish(ok, f"{len(sel)} rows with predicted period >= 3; worst relative error of F/({stiff:.0f}Jv): {max(errs):.2f}"))
