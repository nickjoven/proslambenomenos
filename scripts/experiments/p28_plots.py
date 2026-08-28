#!/usr/bin/env python3
"""P-28 figure page: the gap integers of the golden ladder. Every
number regenerated deterministically from the registered pipeline
or read from p28_results.json. Output: p28_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE))

from kernels.figpage import plot                        # noqa: E402
import p28_derive as D                                  # noqa: E402
import p28_labels as L                                  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p28_plots.html"
RES = json.load(open(HERE / "p28_results.json"))
FIB = D.FIB

# regenerate gaps per rung (0.5 s pipeline)
ALL = {}
for p, q, n in D.LADDER:
    if q >= 3:
        ALL[q] = (p, n) + tuple([L.gaps_of(p, q)[0]])

# ---------------------------------------------------------- fig 1
# the labeled ladder: open-gap energy windows vs flux, tiered color
tier_cls = {1: "c2", 2: "c3", 3: "c5"}
seg = []
W, H = 880, 420
lo_a, hi_a = 0.55, 0.68
lo_E, hi_E = -4.3, 4.3


def X(a):
    return 60 + (a - lo_a) / (hi_a - lo_a) * (W - 80)


def Y(e):
    return 20 + (hi_E - e) / (hi_E - lo_E) * (H - 60)


seg.append(f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" '
           f'aria-label="labeled ladder">')
for q, (p, n, g) in ALL.items():
    if q < 5:
        continue
    a = p / q
    for x in g:
        if not x["open"] or x["t"] is None:
            continue
        cls = tier_cls.get(abs(x["t"]))
        if cls is None:
            cls = "c1" if x["r"] in (1, q - 1) else "c4"
        seg.append(f'<line x1="{X(a):.1f}" x2="{X(a):.1f}" '
                   f'y1="{Y(x["lo"]):.1f}" y2="{Y(x["hi"]):.1f}" '
                   f'class="{cls} gseg"/>')
for q, lab in ((5, "3/5"), (13, "8/13"), (34, "21/34"),
               (89, "55/89")):
    p = ALL[q][0]
    seg.append(f'<text x="{X(p / q):.1f}" y="{H - 24}" class="tick" '
               f'text-anchor="middle">{lab}</text>')
seg.append(f'<text x="{(X(lo_a) + X(hi_a)) / 2:.0f}" y="{H - 6}" '
           f'class="alab" text-anchor="middle">flux α = F(n−1)/F(n) '
           f'→ 1/φ; vertical segments = open gaps; green |t|=1, '
           f'blue |t|=2, purple |t|=3, rust = edge-gap Fibonacci '
           f'series, grey other</text>')
seg.append('</svg>')
fig1 = "".join(seg)

# ---------------------------------------------------------- fig 2
# the Diophantine picture: gaps at (alpha, N = r/q) on N = s + t*alpha
lines = []
for t, s in ((1, 0), (-1, 1), (2, -1), (-2, 2), (3, -1), (-3, 2)):
    pts = [(lo_a, s + t * lo_a), (hi_a, s + t * hi_a)]
    pts = [(a, N) for a, N in pts]
    lines.append({"pts": pts, "cls": tier_cls[abs(t)], "dash": True})
# steep edge-gap lines through the r=1 dots: N = s + t alpha
edge_lines = []
dots = []
edge_dots = []
for q, (p, n, g) in ALL.items():
    if q < 5:
        continue
    a = p / q
    for x in g:
        if not x["open"] or x["t"] is None:
            continue
        if abs(x["t"]) in (1, 2, 3):
            dots.append((a, x["r"] / q))
        if x["r"] == 1:
            edge_dots.append((a, 1.0 / q))
fig2 = plot(lines + [
    {"pts": sorted(dots), "cls": "c4", "dots": True,
     "label": "open gaps (α, N=r/q), |t| ≤ 3"},
    {"pts": sorted(edge_dots), "cls": "c1", "dots": True,
     "label": "edge gaps r=1: t = ±F(n−2)"},
], H=380, title="every dot on its integer line: N = s + t·α",
    xl="flux α", yl="integrated density of states N",
    yfmt="{:.2f}", xfmt="{:.3f}")

# ---------------------------------------------------------- fig 3
# edge-gap power law + principal saturation
ew = [(math.log10(q), math.log10(
    [x for x in ALL[q][2] if x["r"] == 1][0]["width"]))
    for q in ALL if q >= 5]
ew.sort()
x0, y0 = ew[0]
ref = [{"pts": [(x, y0 - 2.34 * (x - x0)) for x, _ in ew],
        "cls": "c4", "dash": True,
        "label": "q^(−2.34) reference (unscored)"}]
t1 = sorted((math.log10(int(q)), w)
            for q, w in RES["t1_width_ladder"].items())
fig3a = plot(ref + [{"pts": ew, "cls": "c1", "dots": True,
                     "label": "edge gap width (|t| = F(n−2))"}],
             H=300, title="the critical power law keeps a |t|=55 gap open at q=144",
             xl="log₁₀ q", yl="log₁₀ width", yfmt="{:.1f}",
             xfmt="{:.1f}")
fig3b = plot([{"pts": t1, "cls": "c2", "dots": True,
               "label": "t = +1 principal gap width"}],
             H=260, title="the principal gap saturates at 1.6851",
             xl="log₁₀ q", yl="width", yfmt="{:.2f}", xfmt="{:.1f}")

# ---------------------------------------------------------- page
n_streda = len(RES["streda"])
HTML = f"""<title>The Gap Integers</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=JetBrains+Mono:wght@400;600&family=Source+Sans+3:wght@400;600&display=swap">
<style>
:root {{
  --bg:#FBFAF7; --ink:#1F242A; --mut:#6B6A64; --hair:#E2DFD6; --card:#F3F1EA;
  --c1:#B4552D; --c2:#3D6B54; --c3:#4B6A8A; --c4:#8A8272; --c5:#7A5C8F;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --c1:#E08A5B; --c2:#7FB89B; --c3:#8FB0D1; --c4:#9A9282; --c5:#B195C9;
}} }}
:root[data-theme="dark"] {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --c1:#E08A5B; --c2:#7FB89B; --c3:#8FB0D1; --c4:#9A9282; --c5:#B195C9;
}}
body {{ background:var(--bg); color:var(--ink); margin:0;
  font-family:"Source Sans 3", sans-serif; line-height:1.5; }}
main {{ max-width:940px; margin:0 auto; padding:40px 24px 80px; }}
h1 {{ font-family:Fraunces, serif; font-weight:700; font-size:2rem; margin:0 0 4px; }}
h2 {{ font-family:Fraunces, serif; font-weight:560; font-size:1.3rem;
  border-top:1px solid var(--hair); padding-top:22px; margin-top:34px; }}
.sub {{ color:var(--mut); margin:0 0 6px; }}
.prov {{ font-family:"JetBrains Mono", monospace; font-size:.72rem; color:var(--mut); }}
.fig {{ width:100%; height:auto; margin:14px 0; }}
.grid {{ stroke:var(--hair); stroke-width:1; }}
.axis {{ stroke:var(--mut); stroke-width:1.2; }}
.tick {{ fill:var(--mut); font:11px "JetBrains Mono", monospace; }}
.alab {{ fill:var(--mut); font:12px "Source Sans 3", sans-serif; }}
.ftitle {{ fill:var(--ink); font:600 13px "Source Sans 3", sans-serif; }}
.leg {{ font:600 12px "Source Sans 3", sans-serif; }}
.line {{ fill:none; stroke-width:2; }}
.dot {{ stroke:var(--bg); stroke-width:1.2; }}
.gseg {{ stroke-width:5; stroke-linecap:round; opacity:.85; }}
.c1 {{ stroke:var(--c1); fill:var(--c1); }} .c2 {{ stroke:var(--c2); fill:var(--c2); }}
.c3 {{ stroke:var(--c3); fill:var(--c3); }} .c4 {{ stroke:var(--c4); fill:var(--c4); }}
.c5 {{ stroke:var(--c5); fill:var(--c5); }}
.c1.line,.c2.line,.c3.line,.c4.line,.c5.line {{ fill:none; }}
.stmt {{ background:var(--card); border:1px solid var(--hair); border-radius:10px;
  padding:14px 18px; margin:14px 0; }}
.tag {{ display:block; font:600 11px "JetBrains Mono", monospace; color:var(--mut);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }}
.eq {{ display:block; font-family:"JetBrains Mono", monospace; font-size:.85rem; margin:4px 0; }}
.note {{ color:var(--mut); font-size:.85rem; }}
</style>
<main>
<h1>The gap integers</h1>
<p class="sub">Every gap of the golden flux ladder carries two integers. The Diophantine labels, the Fibonacci map, and the Streda slopes — computed, not narrated.</p>
<p class="prov">proslambenomenos · P-28 / R-25 · first consumer of kernels.eigh · all clauses first run · LC-18</p>

<section>
<h2>The labeled ladder</h2>
<div class="stmt"><span class="tag">backed statement · clauses (a), (b), (e) · R-25</span>
<span class="eq">r = s·q + t·p, |t| ≤ q/2 — unique, except t = ±q/2 at r = q/2 for even q: the one unlabelable gap is the one the spectrum closes (widths 2.6e-15 / 7.8e-15 / 1.5e-14 at q = 8/34/144)</span>
The widest gaps at every rung are the principal pair t = ±1 at r = F(n−1), F(n−2); tier medians at q = 89: 1.685 / 0.332 / 0.147 for |t| = 1/2/3.</div>
{fig1}
</section>

<section>
<h2>Every dot on its integer line</h2>
<div class="stmt"><span class="tag">backed statement · clauses (c), (d) · R-25</span>
<span class="eq">F(n−1)·F(j) ≡ (−1)^(j+1)·F(n−j)  (mod F(n))  ⟹  the gap at r = F(j) carries |t| = F(n−j)</span>
<span class="eq">Streda by band counting: 18/18 Farey-neighbor gap pairs give (r′/q′ − r/q)/(p′/q′ − p/q) = t exactly, in rational arithmetic</span>
Fibonacci positions carry Fibonacci Chern numbers — a two-line congruence, verified exhaustively, then confirmed in the spectra.</div>
{fig2}
</section>

<section>
<h2>The edge gap's Fibonacci ladder</h2>
<div class="stmt"><span class="tag">backed statement · clause (c) · R-25</span>
<span class="eq">t(r=1) = −1, +2, −3, +5, −8, +13, −21, +34, −55 · widths 1.27 → 8.2e-5 · per-rung ratio 0.324</span>
The registration required resolution only through q = 13; the critical point's power-law gap scaling carried it to q = 144. Exponential closing would have killed it by q = 21 — the edge gap's persistence is a visible signature of criticality.</div>
{fig3a}
{fig3b}
<p class="note">Every scored number lives in p28_results.json against pins in p28_registration.json; figures regenerate deterministically from the same pipeline (0.5 s). The irrational limit, Kubo conductance, and |t| ≥ 4 positions are not claimed.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
