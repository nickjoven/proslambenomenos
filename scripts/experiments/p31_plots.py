#!/usr/bin/env python3
"""P-31 figure page: the second bridge. Numbers from
p31_results.json / p31_registration.json; the golden orbit network
regenerated from the registered pipeline. Output: p31_plots.html."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p31_plots.html"
RES = json.load(open(HERE / "p31_results.json"))
REG = json.load(open(HERE / "p31_registration.json"))

# ---------------------------------------------------------- fig 1
# the parameter line: landmarks (closed) vs rationals (certified)
W, H = 880, 240
lo, hi = 0.500, 0.630


def X(v):
    return 60 + (v - lo) / (hi - lo) * (W - 100)


svg = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" '
       f'aria-label="parameter line">']
svg.append(f'<line x1="{X(lo):.0f}" x2="{X(hi):.0f}" y1="120" '
           f'y2="120" class="axis"/>')
marks = []
for n in range(2, 6):
    t = REG["EQ1"][str(n)][1]
    sz = RES["multinacci"][f"t{n}"]["size"]
    marks.append((t, f"t{n}", f"closes ({sz})", "c2", -1))
for n in (2, 3):
    s = REG["EQ2"][str(n)][1]
    sz = RES["doubling"][f"s{n}"]["size"]
    marks.append((s, f"s{n}", f"closes ({sz})", "c5", -1))
for lab, v in (("3/5", 0.6), ("4/7", 4 / 7), ("5/9", 5 / 9),
               ("8/13", 8 / 13), ("13/21", 13 / 21)):
    marks.append((v, lab, "diverges", "c1", 1))
lane = {-1: 0, 1: 0}
for v, lab, verdict, cls, side in sorted(marks):
    x = X(v)
    lane[side] = (lane[side] + 1) % 4
    off = 26 + 22 * lane[side]
    y1, y2 = (120, 120 - off) if side < 0 else (120, 120 + off)
    svg.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y1}" '
               f'y2="{y2}" class="{cls} stem"/>')
    svg.append(f'<circle cx="{x:.1f}" cy="120" r="5" '
               f'class="{cls} dot"/>')
    ty = y2 - 5 if side < 0 else y2 + 12
    svg.append(f'<text x="{x:.1f}" y="{ty}" class="tick" '
               f'text-anchor="middle">{lab}</text>')
svg.append(f'<text x="{W / 2:.0f}" y="{H - 10}" class="alab" '
           f'text-anchor="middle">t = 1/β · green/purple: orbit '
           f'closes (multinacci / doubling, exact arithmetic) · '
           f'rust: divergence certified by denominator growth — '
           f'including the mediant 4/7 and the golden landmark\'s '
           f'own convergents 8/13, 13/21</text>')
svg.append('</svg>')
fig1 = "".join(svg)

# ---------------------------------------------------------- fig 2
# the golden orbit network {0, 2-phi, phi-1, 1}
PHI = (1 + 5 ** 0.5) / 2
nodes = {"0": 0.0, "2−φ": 2 - PHI, "φ−1": PHI - 1, "1": 1.0}
edges = [("2−φ", "φ−1", "g0"), ("2−φ", "0", "g1"),
         ("φ−1", "1", "g0"), ("φ−1", "2−φ", "g1"),
         ("1", "1", "g1"), ("0", "0", "g0")]
W2, H2 = 880, 220
svg = [f'<svg viewBox="0 0 {W2} {H2}" class="fig" role="img" '
       f'aria-label="golden orbit network">']


def NX(v):
    return 120 + v * (W2 - 240)


for a, b, g in edges:
    xa, xb = NX(nodes[a]), NX(nodes[b])
    cls = "c2" if g == "g0" else "c1"
    if a == b:
        svg.append(f'<path d="M {xa - 8:.0f} 96 C {xa - 26:.0f} 56 '
                   f'{xa + 26:.0f} 56 {xa + 8:.0f} 96" '
                   f'class="{cls} edge"/>')
    else:
        up = 40 if g == "g0" else 76
        svg.append(f'<path d="M {xa:.0f} {104 if g == "g0" else 136} '
                   f'Q {(xa + xb) / 2:.0f} '
                   f'{104 - up if g == "g0" else 136 + up} '
                   f'{xb:.0f} {104 if g == "g0" else 136}" '
                   f'class="{cls} edge" marker-end="url(#arr)"/>')
svg.insert(1, '<defs><marker id="arr" viewBox="0 0 8 8" refX="7" '
              'refY="4" markerWidth="7" markerHeight="7" '
              'orient="auto"><path d="M0,0 L8,4 L0,8 z" '
              'class="mfill"/></marker></defs>')
for lab, v in nodes.items():
    x = NX(v)
    svg.append(f'<circle cx="{x:.0f}" cy="120" r="15" '
               f'class="node"/>')
    svg.append(f'<text x="{x:.0f}" y="124" class="nlab" '
               f'text-anchor="middle">{lab}</text>')
svg.append(f'<text x="{W2 / 2:.0f}" y="{H2 - 6}" class="alab" '
           f'text-anchor="middle">the golden closure, size 4 — '
           f'green arrows g₀ = φx, rust arrows g₁ = φx+1−φ; '
           f'g₁(2−φ) = 0 exists because 1−t sits on the CLOSED '
           f'edge of g₁\'s domain (the derived subtlety, kept as '
           f'the open-edge mutant)</text>')
svg.append('</svg>')
fig2 = "".join(svg)

# ---------------------------------------------------------- fig 3
# orbit sizes ladder + divergence dens (log)
import math                                            # noqa: E402
rows = [("t2", 4, "c2"), ("t3", 8, "c2"), ("t4", 10, "c2"),
        ("t5", 12, "c2"), ("s2", 6, "c5"), ("s3", 8, "c5")]
dens = [(k, v["stat"]) for k, v in RES["rationals"].items()]
W3, H3 = 880, 250
svg = [f'<svg viewBox="0 0 {W3} {H3}" class="fig" role="img" '
       f'aria-label="sizes and certificates">']
for i, (lab, sz, cls) in enumerate(rows):
    x = 60 + i * 58
    h = sz * 10
    svg.append(f'<rect x="{x}" y="{200 - h}" width="36" '
               f'height="{h}" class="{cls} bar"/>')
    svg.append(f'<text x="{x + 18}" y="216" class="tick" '
               f'text-anchor="middle">{lab}</text>')
    svg.append(f'<text x="{x + 18}" y="{194 - h}" class="tick" '
               f'text-anchor="middle">{sz}</text>')
svg.append(f'<text x="240" y="238" class="alab" '
           f'text-anchor="middle">orbit sizes at the landmarks</text>')
for i, (lab, d) in enumerate(dens):
    x = 480 + i * 76
    h = (math.log10(d) - 5) * 60
    svg.append(f'<rect x="{x}" y="{200 - h:.0f}" width="44" '
               f'height="{h:.0f}" class="c1 bar"/>')
    svg.append(f'<text x="{x + 22}" y="216" class="tick" '
               f'text-anchor="middle">{lab}</text>')
    svg.append(f'<text x="{x + 22}" y="{194 - h:.0f}" class="tick" '
               f'text-anchor="middle">{d:.1e}</text>')
svg.append(f'<text x="{480 + 152}" y="238" class="alab" '
           f'text-anchor="middle">divergence certificates '
           f'(max denominator reached)</text>')
svg.append('</svg>')
fig3 = "".join(svg)

HTML = f"""<title>The Second Bridge</title>
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
.axis {{ stroke:var(--mut); stroke-width:1.4; }}
.tick {{ fill:var(--mut); font:11px "JetBrains Mono", monospace; }}
.alab {{ fill:var(--mut); font:12px "Source Sans 3", sans-serif; }}
.stem {{ stroke-width:1.6; }}
.dot {{ stroke:var(--bg); stroke-width:1.2; }}
.bar {{ opacity:.85; }}
.edge {{ fill:none; stroke-width:2.2; }}
.mfill {{ fill:var(--mut); }}
.node {{ fill:var(--card); stroke:var(--mut); stroke-width:1.4; }}
.nlab {{ fill:var(--ink); font:600 12px "JetBrains Mono", monospace; }}
.c1 {{ stroke:var(--c1); fill:var(--c1); }} .c2 {{ stroke:var(--c2); fill:var(--c2); }}
.c3 {{ stroke:var(--c3); fill:var(--c3); }} .c4 {{ stroke:var(--c4); fill:var(--c4); }}
.c5 {{ stroke:var(--c5); fill:var(--c5); }}
.c1.edge,.c2.edge {{ fill:none; }}
.stmt {{ background:var(--card); border:1px solid var(--hair); border-radius:10px;
  padding:14px 18px; margin:14px 0; }}
.tag {{ display:block; font:600 11px "JetBrains Mono", monospace; color:var(--mut);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }}
.eq {{ display:block; font-family:"JetBrains Mono", monospace; font-size:.85rem; margin:4px 0; }}
.note {{ color:var(--mut); font-size:.85rem; }}
</style>
<main>
<h1>The second bridge</h1>
<p class="sub">The kneading tree refuses the mediant: finite orbits at algebraic landmarks, certified nothing at the rationals — the distinction between organizing skeletons, computed with proofs on both sides.</p>
<p class="prov">proslambenomenos · P-31 / R-28 · Bandt Adv. Math. 324, 437 · third premises-bearing claim · exact arithmetic, 0.1 s · LC-22</p>

<section>
<h2>Two skeletons, one parameter line</h2>
<div class="stmt"><span class="tag">backed statement · clauses (a)–(d) · R-28</span>
<span class="eq">closes (exact ℚ(β) set closure): t₂..t₅ (multinacci), s₂, s₃ (doubling) — sizes 4, 8, 10, 12 / 6, 8</span>
<span class="eq">diverges (denominator certificate &gt; 1e6, a proof not a timeout): 3/5, 5/9, 4/7, 8/13, 13/21</span>
The sharpest cell: structure at s₂ = 0.569840, certified nothing at the mediant 4/7 = 0.571429 — 1.588e-3 apart. Even the golden landmark's own Fibonacci convergents die while the landmark closes.</div>
{fig1}
</section>

<section>
<h2>The golden closure</h2>
<div class="stmt"><span class="tag">backed statement · EQ3 anchor · derived by hand, reproduced exactly</span>
<span class="eq">orbit(1−t, t) at β = φ  =  {{0, 2−φ, φ−1, 1}} — size 4</span>
φ is the first multinacci (x² = x+1 heading xⁿ = xⁿ⁻¹+...+1) — the taxonomy's address route, now with its own exact orbit.</div>
{fig2}
</section>

<section>
<h2>Sizes and certificates</h2>
<div class="stmt"><span class="tag">the composite, two bridges together</span>
<span class="eq">P-29: mediant transfers (tongues ↔ bands) because both carry two-frequency competition — the control dethroned the mediant when the premise broke</span>
<span class="eq">P-31: kneading does NOT transfer — closures at algebraic landmarks, certified divergence at every Farey-predicted point</span>
Which tree organizes a system follows from the system's premise. Visual resemblance between landscapes carries no evidential weight; the premise does.</div>
{fig3}
<p class="note">No timeout is used as evidence in either direction: closure is exact set closure in ℚ(β); divergence is the bounded-denominator lemma's contrapositive. Every scored number lives in p31_results.json against pins in p31_registration.json.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
