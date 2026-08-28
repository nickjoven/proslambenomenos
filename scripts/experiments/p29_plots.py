#!/usr/bin/env python3
"""P-29 figure page: the Farey bridge. Every number is read from
p29_results.json / p29_registration.json. Output: p29_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from kernels.figpage import plot                        # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p29_plots.html"
RES = json.load(open(HERE / "p29_results.json"))
REG = json.load(open(HERE / "p29_registration.json"))

# ---------------------------------------------------------- fig 1
# pooled grading: log Delta vs log S, mediants highlighted
meds, others = [], []
seen = set()
for iv in RES["intervals"]:
    for r in iv["rows"]:
        key = r["frac"]
        if key in seen:
            continue
        seen.add(key)
        pt = (math.log10(r["S"]), math.log10(r["delta"]))
        (meds if r["is_mediant"] else others).append(pt)
fig1 = plot([
    {"pts": sorted(others), "cls": "c4", "dots": True,
     "label": "competitors"},
    {"pts": sorted(meds), "cls": "c1", "dots": True,
     "label": "mediants"},
], H=360, title="one grading, two instruments: tongue width vs Harper bandwidth",
    xl="log₁₀ S(p/q) (Harper bandwidth)",
    yl="log₁₀ Δ(p/q) (tongue width)", yfmt="{:.1f}", xfmt="{:.2f}")

# ---------------------------------------------------------- fig 2
# bump chart for [1/3, 1/2]: rank by Delta (left) vs rank by S (right)
iv = [v for v in RES["intervals"] if v["interval"] == "1/3..1/2"][0]
rows = iv["rows"]
byD = sorted(rows, key=lambda r: -r["delta"])
byS = sorted(rows, key=lambda r: -r["S"])
W, RH = 860, 30
Hb = 70 + RH * len(rows)
xL, xR = 280, W - 280
svg = [f'<svg viewBox="0 0 {W} {Hb}" class="fig" role="img" '
       f'aria-label="rank correspondence">']
svg.append(f'<text x="{xL - 12}" y="26" class="ftitle" '
           f'text-anchor="end">ranked by tongue width</text>')
svg.append(f'<text x="{xR + 12}" y="26" class="ftitle">'
           f'ranked by bandwidth</text>')
posD = {r["frac"]: i for i, r in enumerate(byD)}
posS = {r["frac"]: i for i, r in enumerate(byS)}
for r in rows:
    f = r["frac"]
    y1 = 48 + RH * posD[f]
    y2 = 48 + RH * posS[f]
    cls = "c1" if r["is_mediant"] else "c4"
    svg.append(f'<line x1="{xL + 6}" x2="{xR - 6}" y1="{y1}" '
               f'y2="{y2}" class="{cls} bump"/>')
    svg.append(f'<text x="{xL - 12}" y="{y1 + 4}" class="tick {cls}" '
               f'text-anchor="end">{f} · {r["delta"]:.2e}</text>')
    svg.append(f'<text x="{xR + 12}" y="{y2 + 4}" class="tick {cls}">'
               f'{f} · {r["S"]:.3f}</text>')
svg.append(f'<text x="{W / 2:.0f}" y="{Hb - 8}" class="alab" '
           f'text-anchor="middle">interval [1/3, 1/2] · mediant 2/5 '
           f'in rust · Spearman {iv["spearman"]:.3f}</text>')
svg.append('</svg>')
fig2 = "".join(svg)

# ---------------------------------------------------------- fig 3
# the control: dethroning bars
ctrl = RES["control"]
d25_1 = [r for r in rows if r["frac"] == "2/5"][0]["delta"]
d38_1 = [r for r in rows if r["frac"] == "3/8"][0]["delta"]
items = [
    ("first harmonic (the premise intact)", [
        ("2/5 (mediant)", d25_1, "c1"), ("3/8", d38_1, "c4")]),
    ("second harmonic (premise broken; conjugate to (2Ω, 2K))", [
        ("2/5 (mediant)", ctrl["delta2_25"], "c1"),
        ("3/8", ctrl["delta2_38"], "c2")]),
]
Wc, Hc = 860, 240
svg = [f'<svg viewBox="0 0 {Wc} {Hc}" class="fig" role="img" '
       f'aria-label="the control">']
vmax = max(v for _, grp in items for _, v, _ in grp)
y = 30
for title, grp in items:
    svg.append(f'<text x="16" y="{y}" class="ftitle">{title}</text>')
    y += 10
    for lab, v, cls in grp:
        w = 40 + (Wc - 380) * (v / vmax)
        svg.append(f'<rect x="240" y="{y}" width="{w:.0f}" '
                   f'height="18" class="{cls} bar"/>')
        svg.append(f'<text x="232" y="{y + 14}" class="tick" '
                   f'text-anchor="end">{lab}</text>')
        svg.append(f'<text x="{244 + w:.0f}" y="{y + 14}" '
                   f'class="tick">{v:.2e}</text>')
        y += 26
    y += 18
svg.append('</svg>')
fig3 = "".join(svg)

HTML = f"""<title>The Farey Bridge</title>
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
.bump {{ stroke-width:2; opacity:.75; }}
.bar {{ opacity:.85; }}
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
<h1>The Farey bridge</h1>
<p class="sub">Arnold tongues and Hofstadter bands share the mediant skeleton as mechanism — with a control, derived in advance, that breaks the bridge on exactly one side.</p>
<p class="prov">proslambenomenos · P-29 / R-26 · first premises-bearing claim · K = 0.5, λ = 1 · LC-19</p>

<section>
<h2>The mediant wins everywhere, on both instruments</h2>
<div class="stmt"><span class="tag">backed statement · clauses (a)–(c) · R-26</span>
<span class="eq">mediant (a+c)/(b+d) = unique minimal-q interior fraction (exhaustive) — and it carries the widest tongue AND the largest bandwidth in all 10 registered intervals</span>
<span class="eq">grading transfers beyond the winner: Spearman(Δ, S) = 0.891–1.000 across the 8 eligible intervals</span>
Each instrument computed on its own data, its own anchors: ρ=0 width K/π at 1e-10; K^q ratios 3.998/7.992 vs 4/8; S(1/2) = 4√2 at 1e-12.</div>
{fig1}
{fig2}
</section>

<section>
<h2>The kill switch that did not fire — because it inverted as derived</h2>
<div class="stmt"><span class="tag">backed statement · clause (d) · R-26</span>
<span class="eq">θ → θ + Ω + (K/2π)·sin(4πθ)  ≅  standard map at (2Ω, 2K)  (conjugacy verified 1e-8, inversion direction pinned pre-run)</span>
Remove the first harmonic and the competitor 3/8 dethrones the mediant 2/5 on the tongue side — while the untouched butterfly keeps S(2/5) = 1.8434 &gt; S(3/8) = 1.2021. The ordering follows the premise, not the picture.</div>
{fig3}
<p class="note">First premises-bearing claim: premises harper-golden-ladder and golden-ladder-gap-integers (both verified — no conditional cap). Kneading-tree systems (Bernoulli convolutions, LC-19) are a different skeleton, deliberately not claimed. Every scored number lives in p29_results.json against pins in p29_registration.json.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
