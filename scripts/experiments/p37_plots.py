#!/usr/bin/env python3
"""P-37 figure page. Numbers from p37_results.json /
p37_registration.json. Output: p37_plots.html."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p37_plots.html"
RES = json.load(open(HERE / "p37_results.json"))
REG = json.load(open(HERE / "p37_registration.json"))

from kernels.figpage import page, plot  # noqa: E402

LIGHT = {"bg": "#f7f5f0", "ink": "#1b2230", "mut": "#5b6675",
         "hair": "#d8d3c8", "card": "#ffffff", "c1": "#1f7a4d",
         "c2": "#a83232", "c3": "#2b5fa3", "c4": "#9a6b1f"}
DARK = {"bg": "#12161d", "ink": "#e6e9ee", "mut": "#98a3b3",
        "hair": "#2c3542", "card": "#191f28", "c1": "#4cc38a",
        "c2": "#e06c6c", "c3": "#7fb0e0", "c4": "#d2a24c"}


def cells(D, a, kind="main"):
    out = []
    for k, c in RES["cells"].items():
        parts = k.split("_")
        if (parts[0] == str(D) and parts[1] == "a" + str(a)
                and parts[3] == kind):
            out.append((float(parts[2][1:]), c))
    return sorted(out)


# fig 1: the wall at a=2.4, D=0.22 - work and error vs tau
row = cells(0.22, 2.4) + [(t, c) for t, c in cells(0.22, 2.4, "wall")
                          if t == 55]
wpts = [(t, c["W"]) for t, c in row]
epts = [(t, max(c["p"], 1e-4) * 10) for t, c in row]
fig1 = plot([
    {"pts": wpts, "cls": "c3", "dots": True,
     "label": "mean work ⟨W⟩ — falls past the optimum"},
    {"pts": epts, "cls": "c2", "dots": True,
     "label": "error × 10 — rises past it (the substrate forgets)"},
], H=310, title="the wall (a = 2.4, D = 0.22): patience buys work back, sells fidelity",
    xl="write duration τ", yl="work · (error × 10)",
    yfmt="{:.1f}", xfmt="{:.0f}")

# fig 2: every cell against its combined bound
pts_ab = []
for k, c in RES["cells"].items():
    pts_ab.append((c["floor_plus_sl"], c["W"]))
lim = max(max(x for x, _ in pts_ab), max(y for _, y in pts_ab)) * 1.05
fig2 = plot([
    {"pts": [(0, 0), (lim, lim)], "cls": "c2", "dash": True,
     "label": "W = bound (violation region below)"},
    {"pts": sorted(pts_ab), "cls": "c1", "dots": True,
     "label": "26 registered cells"},
], H=310, title="every cell above its floor + speed limit",
    xl="D[ln2 − H(p)] + W₂²/τ  (derived, per cell)",
    yl="measured ⟨W⟩", yfmt="{:.1f}", xfmt="{:.1f}")

# fig 3: measured error vs the unregistered Kramers overlay, a=2.4
figs3 = []
for D, cls in ((0.22, "c3"), (0.28, "c4")):
    ov = REG["EQ4_p_kin"][str(D)]["2.4"]
    kpts = sorted((float(t), v) for t, v in ov.items())
    mpts = [(t, c["p"]) for t, c in cells(D, 2.4)]
    mpts += [(t, c["p"]) for t, c in cells(D, 2.4, "wall")]
    figs3.append({"pts": kpts, "cls": cls,
                  "label": f"Kramers overlay D = {D} (unregistered)"})
    figs3.append({"pts": sorted(mpts), "cls": cls, "dots": True})
fig3 = plot(figs3, H=310, logy=True,
            title="error vs duration, a = 2.4: measured dots on the derived overlay",
            xl="write duration τ", yl="error p (log)",
            yfmt="{:.3f}", xfmt="{:.0f}")

n22 = RES["nulls"]["0.22"]
n28 = RES["nulls"]["0.28"]
w22 = RES["wall"]["0.22"]
w28 = RES["wall"]["0.28"]
body = f"""
<section>
<h2>The wall the substrate builds</h2>
<div class="stmt"><span class="tag">backed statement · R-36 clause (d)</span>
<span class="eq">D = 0.22: error 0.0088 → 0.0150 while work 1.51 → 1.05 (gap {w22['gap']:.4f} over floor {3 * w22['sigma']:.4f} — held)</span>
<span class="eq">D = 0.28: gap {w28['gap']:.4f} under floor {3 * w28['sigma']:.4f} — FIRED, direction consistent; the power budget had leaned on the unregistered overlay (attributed)</span>
You cannot write slowly on a substrate that forgets: rung 2's own P-24-pinned hop rate leaks the bit back while the protocol lingers.</div>
{fig1}
</section>

<section>
<h2>Two theorems, twenty-six cells</h2>
<div class="stmt"><span class="tag">backed statement · R-36 clauses (a)(b)(c)</span>
<span class="eq">⟨W⟩ ≥ D[ln2 − H(p)] and ⟨W⟩ ≥ D[ln2 − H(p)] + W₂²/τ — W₂ cut-scanned on the circle against the empirical commit sample</span>
<span class="eq">Jarzynski nulls {n22['jarz']:.4f} ± {n22['jarz_se']:.4f} and {n28['jarz']:.4f} ± {n28['jarz_se']:.4f}; dt/2 inside its band</span>
Both floors are load-bearing: the H(p) refund and the 1/τ charge each carry a mutant in the falsifier.</div>
{fig2}
</section>

<section>
<h2>The overlay it refused to register</h2>
{fig3}
<p class="note">The Kramers two-state curve was computed in the derive layer and its magnitudes deliberately left
unregistered (P-2's lesson) — the one clause that fired did so because the power budget used what the bands
refused; R-36 extends the corollary to power calculations. Every number lives in p37_results.json against
pins in p37_registration.json.</p>
</section>
"""

HTML = page(
    "The Price of a Bit",
    "P-37/R-36 · writing on a substrate that forgets — the Landauer floor with its H(p) refund, "
    "the optimal-transport speed charge, and the wall inherited from P-24's derived hop rate",
    "proslambenomenos · P-37/R-36 · claim writing-a-bit-pays-its-floors · LC-27 · 2026-08-30",
    body, LIGHT, DARK)
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
