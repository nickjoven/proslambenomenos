"""P-4 loading-limited slip periods obey period/round-trip = mu_s F_N/(4 J v) to <20% wherever that prediction is >= 3 (away from the Helmholtz period 2).
Source: notes/p4_twisted_inertial_ring.md run 5 + correction; data scripts/experiments/p4_results_lowdamp.json. Mutant: stiffness 2J/N.
Of record: the first version of this entry claimed all loading-limited rows and failed at 27-37% on the rows with predicted period near 2."""
import json, sys
from pathlib import Path
from _common import mutant_flag, finish

rows = json.load(open(Path(__file__).resolve().parents[1] / "scripts/experiments/p4_results_lowdamp.json"))
stiff = 2.0 if mutant_flag() else 4.0
# loading-limited regime: g = 0.01 (corner dead), stick-slip rows, F_N <= 1.5 (sine saturation beyond)
sel = [r for r in rows if r["g"] == 0.01 and r["regime"] == "stick-slip" and r["F_N"] <= 1.5
       and r["F_N"] / (4.0 * r["v"]) >= 3.0]
errs = [abs(r["ratio"] - r["F_N"] / (stiff * r["v"])) / r["ratio"] for r in sel]
ok = len(sel) >= 8 and max(errs) < 0.2
sys.exit(finish(ok, f"{len(sel)} loading-limited rows; worst relative error of F/({stiff:.0f}Jv): {max(errs):.2f}"))
