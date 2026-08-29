#!/usr/bin/env python3
"""P-34 figure page. Numbers from p34_results.json /
p34_registration.json. Output: p34_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p34_plots.html"
RES = json.load(open(HERE / "p34_results.json"))
REG = json.load(open(HERE / "p34_registration.json"))

from kernels.figpage import plot  # noqa: E402

# ---------------------------------------------------------- fig 1
# the coverage curve (the detector null)
cov = REG["EQ2"]["coverage"]
pts = sorted((float(t), p) for t, p in cov.items())
fig1 = plot([
    {"pts": pts, "cls": "c3", "dots": True,
     "label": "p(match ≤ t) against the codebook"},
    {"pts": pts, "cls": "c3"},
], H=300, title="the detector null: how cheap is a coincidence?",
    xl="mismatch tolerance t (dex)", yl="coverage probability",
    yfmt="{:.2f}", xfmt="{:.2f}")

# ---------------------------------------------------------- fig 2
# the net-bit bars
rows = RES["census"]["planck"]
W, H = 880, 300
svg = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" '
       f'aria-label="net bits">']
x0 = 250
scale = 120
svg.append(f'<line x1="{x0}" x2="{x0}" y1="20" y2="{H - 60}" '
           f'class="axis"/>')
flag = x0 + 3 * scale
svg.append(f'<line x1="{flag}" x2="{flag}" y1="20" y2="{H - 60}" '
           f'class="flagline"/>')
svg.append(f'<text x="{flag}" y="14" class="tick" '
           f'text-anchor="middle">3-bit flag</text>')
y = 34
order = sorted(rows, key=lambda r: r["net_bits"])
for r in order:
    v = r["net_bits"]
    w = abs(v) * scale
    x = x0 if v >= 0 else x0 - w
    cls = "c2" if v <= 0.1 else ("c5" if v < 2 else "c1")
    svg.append(f'<rect x="{x:.0f}" y="{y}" width="{max(w, 1):.0f}" '
               f'height="22" class="{cls} bar"/>')
    svg.append(f'<text x="{x0 - 8 if v >= 0 else x0 + 8}" '
               f'y="{y + 16}" class="tick" text-anchor='
               f'"{"end" if v >= 0 else "start"}">{r["name"]} · '
               f'{v:+.2f} bits · {r["t_dex"]:.3f} dex</text>')
    y += 42
svg.append(f'<text x="{W / 2:.0f}" y="{H - 16}" class="alab" '
           f'text-anchor="middle">net bits = surprisal(coverage) − '
           f'log₂(census of 5) · a₀ and the Weinberg relation price '
           f'at zero; the best entry earns two bits; none reaches '
           f'the flag</text>')
svg.append('</svg>')
fig2 = "".join(svg)

# ---------------------------------------------------------- fig 3
# the slot-collision panel
mechs = RES["k2_mechanisms"]
W3, H3 = 880, 190
svg = [f'<svg viewBox="0 0 {W3} {H3}" class="fig" role="img" '
       f'aria-label="slot collision">']
svg.append(f'<rect x="330" y="60" width="220" height="46" rx="8" '
           f'class="slotbox"/>')
svg.append(f'<text x="440" y="88" class="slotlab" '
           f'text-anchor="middle">ρ ~ ρ_P · μ² (k = 2)</text>')
xs = [80, 300, 560, 760]
for (m, x) in zip(mechs, xs):
    svg.append(f'<text x="{x}" y="30" class="tick" '
               f'text-anchor="middle">{m}</text>')
    svg.append(f'<line x1="{x}" x2="440" y1="36" y2="60" '
               f'class="mline"/>')
svg.append(f'<text x="{W3 / 2:.0f}" y="{H3 - 40}" class="alab" '
           f'text-anchor="middle">four named mechanisms, one slot — '
           f'the rank-3 dimension algebra leaves nowhere else to '
           f'land</text>')
svg.append(f'<text x="{W3 / 2:.0f}" y="{H3 - 18}" class="alab" '
           f'text-anchor="middle">they cannot all be right, and the '
           f'slot they share was cheap (0.012 dex at coverage '
           f'p ≈ 0.05)</text>')
svg.append('</svg>')
fig3 = "".join(svg)

HTML = f"""<title>The Horizon Census</title>
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
.axis {{ stroke:var(--mut); stroke-width:1.4; }}
.tick {{ fill:var(--mut); font:11px "JetBrains Mono", monospace; }}
.alab {{ fill:var(--mut); font:12px "Source Sans 3", sans-serif; }}
.ftitle {{ fill:var(--ink); font:600 13px "Source Sans 3", sans-serif; }}
.leg {{ font:600 12px "Source Sans 3", sans-serif; }}
.line {{ fill:none; stroke-width:2; }}
.dot {{ stroke:var(--bg); stroke-width:1.2; }}
.bar {{ opacity:.85; }}
.flagline {{ stroke:var(--c1); stroke-width:1.4; stroke-dasharray:5 4; }}
.slotbox {{ fill:var(--card); stroke:var(--c1); stroke-width:2; }}
.slotlab {{ fill:var(--ink); font:600 15px "JetBrains Mono", monospace; }}
.mline {{ stroke:var(--mut); stroke-width:1.2; }}
.c1 {{ stroke:var(--c1); fill:var(--c1); }} .c2 {{ stroke:var(--c2); fill:var(--c2); }}
.c3 {{ stroke:var(--c3); fill:var(--c3); }} .c4 {{ stroke:var(--c4); fill:var(--c4); }}
.c5 {{ stroke:var(--c5); fill:var(--c5); }}
.c3.line {{ fill:none; }}
.stmt {{ background:var(--card); border:1px solid var(--hair); border-radius:10px;
  padding:14px 18px; margin:14px 0; }}
.tag {{ display:block; font:600 11px "JetBrains Mono", monospace; color:var(--mut);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }}
.eq {{ display:block; font-family:"JetBrains Mono", monospace; font-size:.85rem; margin:4px 0; }}
.note {{ color:var(--mut); font-size:.85rem; }}
</style>
<main>
<h1>The horizon census</h1>
<p class="sub">Every famous horizon-scale coincidence, priced in bits against one derived codebook — with the detector's null derived before any entry was scored.</p>
<p class="prov">proslambenomenos · P-34 / R-31 · c33 (CKN) · LC-9 (Verlinde, contested) · LC-24 · claim horizon-census-priced</p>

<section>
<h2>The instrument's null, first</h2>
<div class="stmt"><span class="tag">backed statement · EQ1–EQ2 · AGENTS item 8</span>
<span class="eq">rank({{ħ, c, G, H₀}}) = 3 ⟹ every coincidence is (k, prefactor) in μ = H₀t_P = 1.178e-61 — slots are few by algebra</span>
<span class="eq">coverage: p(0.05 dex) = 0.176 · p(0.1) = 0.275 · p(0.3) = 0.374 — factor-two matches are cheap by derivation</span>
Calibrated on the Gibbons–Hawking theorem row (&lt; 1e-9 dex; an equation, excluded from counting).</div>
{fig1}
</section>

<section>
<h2>The verdict</h2>
<div class="stmt"><span class="tag">backed statement · R-31 clause (b)</span>
<span class="eq">a₀ vs cH₀/2π: −0.03 bits · Weinberg m_π: −0.11 bits · why-now: +0.59 · ν scale: +1.49 · ρ_Λ: +2.13 — none reaches the 3-bit flag</span>
The two most famous horizon coincidences are worth nothing once the codebook and the census's own size are charged; the best is worth two bits. (The a₀ row's H₀ sensitivity band fired at 1.06 bits — an underived-band error, attributed in R-31; the row spans −0.03 to +1.03 across the H₀ tension, under the flag either way.)</div>
{fig2}
</section>

<section>
<h2>Four mechanisms, one slot</h2>
{fig3}
<p class="note">c33 lands the CKN arithmetic (1.09 dex from observed, vs 122.9 for the naive cutoff) with its own mutant; LC-9 fills its reserved slot with the contested Verlinde status. Every scored number lives in p34_results.json against pins in p34_registration.json.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
