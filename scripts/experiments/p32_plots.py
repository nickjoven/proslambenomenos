#!/usr/bin/env python3
"""P-32/P-33 figure page. Numbers from p32/p33 results JSONs.
Output: p32_plots.html."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p32_plots.html"
R32 = json.load(open(HERE / "p32_results.json"))
R33 = json.load(open(HERE / "p33_results.json"))

CLS = {4: ("clean", "c2"), 8: ("clean", "c2"),
       5: ("defect", "c3"), 9: ("defect", "c3"),
       6: ("half", "c5"), 7: ("both", "c1")}

# ---------------------------------------------------------- fig 1
# the class hierarchy at K = 1.2 (and K = 1.0 alt-pin from R32)
w12 = R33["pin_K12"]
w10 = R32["alt_pin_widths"]
W, H = 880, 300
svg = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" '
       f'aria-label="class hierarchy">']
for j, (wmap, label, x0) in enumerate(((w10, "K = 1.0", 60),
                                       (w12, "K = 1.2", 480))):
    svg.append(f'<text x="{x0 + 160}" y="24" class="ftitle" '
               f'text-anchor="middle">{label}</text>')
    for i, N in enumerate(range(4, 10)):
        w = wmap[str(N)] if str(N) in wmap else wmap[N]
        x = x0 + i * 56
        h = w * 1150
        name, cls = CLS[N]
        svg.append(f'<rect x="{x}" y="{240 - h:.0f}" width="40" '
                   f'height="{h:.0f}" class="{cls} bar"/>')
        svg.append(f'<text x="{x + 20}" y="256" class="tick" '
                   f'text-anchor="middle">N={N}</text>')
        svg.append(f'<text x="{x + 20}" y="{234 - h:.0f}" '
                   f'class="tick" text-anchor="middle">{w:.3f}</text>')
svg.append(f'<text x="{W / 2:.0f}" y="{H - 8}" class="alab" '
           f'text-anchor="middle">ALT + pinning 1/2-plateau widths '
           f'— green clean (f=0), blue defect, purple '
           f'half-frustrated, rust both: the four derived classes '
           f'order the widths; frustration narrows, parity fails '
           f'({{6}} sides with {{7}})</text>')
svg.append('</svg>')
fig1 = "".join(svg)

# ---------------------------------------------------------- fig 2
# the telescoping identity / smear diagnosis
W2, H2 = 880, 210
svg = [f'<svg viewBox="0 0 {W2} {H2}" class="fig" role="img" '
       f'aria-label="telescoping">']
svg.append('<text x="60" y="40" class="ftitle">every bias-side '
           '"width", every geometry, every N, every grid point:'
           '</text>')
svg.append('<text x="60" y="80" class="big">w = 0.00080 = 2·TOL / '
           'slope — the smear of an unlocked staircase</text>')
svg.append('<text x="60" y="120" class="ftitle">because the '
           'site-mean advance telescopes:</text>')
svg.append('<text x="60" y="158" class="big">Σᵢ coupling ≡ 0  ⟹  '
           'ρ = I identically (verified 9·10⁻¹⁷) — no Shapiro '
           'step can exist in this observable</text>')
svg.append(f'<text x="60" y="{H2 - 14}" class="alab">0 of 288 '
           f'grid cells locked; the stop rule closed the bias side '
           f'after the second positive-control firing</text>')
svg.append('</svg>')
fig2 = "".join(svg)

HTML = f"""<title>The Parity Factorial</title>
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
.tick {{ fill:var(--mut); font:11px "JetBrains Mono", monospace; }}
.alab {{ fill:var(--mut); font:12px "Source Sans 3", sans-serif; }}
.ftitle {{ fill:var(--ink); font:600 14px "Source Sans 3", sans-serif; }}
.big {{ fill:var(--ink); font:600 17px "JetBrains Mono", monospace; }}
.bar {{ opacity:.85; }}
.c1 {{ fill:var(--c1); }} .c2 {{ fill:var(--c2); }} .c3 {{ fill:var(--c3); }}
.c4 {{ fill:var(--c4); }} .c5 {{ fill:var(--c5); }}
.stmt {{ background:var(--card); border:1px solid var(--hair); border-radius:10px;
  padding:14px 18px; margin:14px 0; }}
.tag {{ display:block; font:600 11px "JetBrains Mono", monospace; color:var(--mut);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }}
.eq {{ display:block; font-family:"JetBrains Mono", monospace; font-size:.85rem; margin:4px 0; }}
.note {{ color:var(--mut); font-size:.85rem; }}
</style>
<main>
<h1>The parity factorial</h1>
<p class="sub">A-2's reconciliation, run as a 2×2 factorial — ending in a four-class hierarchy on the pinned side and a telescoping identity that closes the bias side.</p>
<p class="prov">proslambenomenos · P-32/R-29 (two clauses fired, diagnosed) · P-33/R-30 (stop rule) · LC-23 · claim frustration-classes-organize-the-pinned-ring</p>

<section>
<h2>The four classes order the pinned ring</h2>
<div class="stmt"><span class="tag">backed statement · P-33 clause (b), fresh K · R-30</span>
<span class="eq">f(N) = (⌊N/2⌋/2) mod 1 + defect(N odd) — derived before any cell ran</span>
<span class="eq">K = 1.2: clean 0.1667/0.1666 &gt; defect 0.1537/0.1522 &gt; half 0.0370 &gt; both 0.0159 — f-gap −0.151, fifty times resolution</span>
The imported even/odd claim refines on a ring: {{6}} (even) sides with {{7}} (odd), so plain parity fails and the ring-closure arithmetic wins.</div>
{fig1}
</section>

<section>
<h2>Why the bias side could never work — and how it was caught</h2>
<div class="stmt"><span class="tag">backed statement · R-29/R-30 diagnoses · the stop rule</span>
<span class="eq">first firing: every "width" = the tolerance smear 2·TOL/slope (slope 1.0000) — the null the registration failed to derive</span>
<span class="eq">second firing: ρ = I identically (coupling telescopes) — Shapiro steps impossible in the site-mean observable, by algebra</span>
The sharpened reconciliation: the Josephson parity effect needs per-junction nonlinearity in the driven loop AND a difference-variable observable. E1 has the nonlinearity without the drive; this bias ring had the drive with a telescoping observable; the arrays have both.</div>
{fig2}
<p class="note">Every scored number lives in p32_results.json / p33_results.json against pins in p32_registration.json; the P-9 reproduction landed on all twelve pins.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
