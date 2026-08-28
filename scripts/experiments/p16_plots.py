#!/usr/bin/env python3
"""Render the P-16 figures as a self-contained HTML page (stdlib
only): the sprinkled causet, the two spectral-dimension curves, and
the divergence. Scored numbers from p16_registration.json /
p16_results.json; the causet drawing is regenerated deterministically
from a registered seed. Output: p16_plots.html."""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from kernels.causet import hasse_links, sprinkle  # noqa: E402

REG = json.loads((HERE / "p16_registration.json").read_text())
RES = json.loads((HERE / "p16_results.json").read_text())
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p16_plots.html"

# ---------- figure A: the causet ----------
N = 128
pts = sprinkle(N, REG["seed0"] + 97 * N + 0)
links = hasse_links(pts)
W = H = 460
oA = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="sprinkled causal set">']
oA.append(f'<text x="16" y="20" class="ftitle">one sprinkling, N = 128: {len(links)} Hasse links (pin 444.7)</text>')


def XY(u, v):
    x = (v - u) / 2.0
    t = (u + v) / 2.0
    return 230 + x * 380, H - 30 - t * 380


for (j, i) in links:
    x1, y1 = XY(*pts[j])
    x2, y2 = XY(*pts[i])
    oA.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="lk"/>')
for (u, v) in pts:
    x, y = XY(u, v)
    oA.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" class="pt"/>')
oA.append(f'<text x="{W - 14}" y="{H - 10}" class="tick" text-anchor="end">time up; light cones at 45°</text>')
oA.append('</svg>')
figA = "".join(oA)


def plot(series, W=860, H=340, title="", xl="", yl="", logx=False,
         pad=(60, 16, 44, 24), xfmt="{:.2f}", yfmt="{:.1f}"):
    L, R, B, Tp = pad
    tx = (lambda v: math.log10(v)) if logx else (lambda v: v)
    xs = [tx(x) for s in series for x, _ in s["pts"]]
    ys = [y for s in series for _, y in s["pts"]]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    y0, y1 = y0 - 0.06 * (y1 - y0), y1 + 0.10 * (y1 - y0)
    X = lambda x: L + (tx(x) - x0) / (x1 - x0) * (W - L - R)   # noqa: E731
    Y = lambda y: Tp + (y1 - y) / (y1 - y0) * (H - Tp - B)      # noqa: E731
    o = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="{title}">']
    o.append(f'<text x="{L}" y="{Tp - 8}" class="ftitle">{title}</text>')
    for k in range(5):
        yy = y0 + (y1 - y0) * k / 4
        o.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(yy):.1f}" y2="{Y(yy):.1f}" class="grid"/>')
        o.append(f'<text x="{L - 8}" y="{Y(yy) + 4:.1f}" class="tick" text-anchor="end">{yfmt.format(yy)}</text>')
        xxl = x0 + (x1 - x0) * k / 4
        xv = 10 ** xxl if logx else xxl
        o.append(f'<text x="{L + (W - L - R) * k / 4:.1f}" y="{H - B + 18}" class="tick" text-anchor="middle">{xfmt.format(xv)}</text>')
    o.append(f'<line x1="{L}" x2="{W - R}" y1="{H - B}" y2="{H - B}" class="axis"/>')
    o.append(f'<line x1="{L}" x2="{L}" y1="{Tp}" y2="{H - B}" class="axis"/>')
    for s in series:
        p = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in s["pts"])
        dash = ' stroke-dasharray="7 5"' if s.get("dash") else ""
        if s.get("dots"):
            for x, y in s["pts"]:
                o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4" class="{s["cls"]} dot"/>')
        else:
            o.append(f'<polyline points="{p}" class="{s["cls"]} line"{dash}/>')
    for i, s in enumerate(series):
        if s.get("label"):
            o.append(f'<text x="{W - R - 8}" y="{Tp + 16 + 16 * i}" class="leg {s["cls"]}" text-anchor="end">{s["label"]}</text>')
    o.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 4}" class="alab" text-anchor="middle">{xl}</text>')
    o.append(f'<text x="14" y="{(Tp + H - B) / 2:.0f}" class="alab" transform="rotate(-90 14 {(Tp + H - B) / 2:.0f})" text-anchor="middle">{yl}</text>')
    o.append('</svg>')
    return "".join(o)


# ---------- figure B: walk curves ----------
sers = []
cls = {"64": "wA", "128": "wB", "256": "wC"}
for Nn in ("64", "128", "256"):
    cur = RES["detail"][f"N{Nn}_r0"]["curve"]
    sers.append({"pts": cur, "cls": cls[Nn], "label": f"walk d_s, N = {Nn} (seed 0)"})
sers.append({"pts": [(0.05, 2.0), (30, 2.0)], "cls": "ink", "dash": True, "label": "d = 2"})
figB = plot(sers, logx=True, title="the walk definition: superdiffusive peak grows with N "
            f"(seed means {RES['detail']['peaks']['64']:.2f} / {RES['detail']['peaks']['128']:.2f} / "
            f"{RES['detail']['peaks']['256']:.2f}), then the lattice fall (clauses b, d)",
            xl="diffusion time t (log)", yl="d_s")

# ---------- figure C: the d'Alembertian ----------
dal = REG["dalembertian_curve"]
figC = plot([{"pts": dal, "cls": "dal", "label": "regularised nonlocal d'Alembertian (source closed form)"},
             {"pts": [(dal[0][0], 2.0), (dal[-1][0], 2.0)], "cls": "ink", "dash": True, "label": "d = 2"}],
            logx=True, title=f"the d'Alembertian definition: 2 → max {REG['dalembertian_peak']['ds']:.3f} "
            f"at s = {REG['dalembertian_peak']['s']:.2f} → 2 (BBMM Fig. 2 reproduced; printed eq. 15 "
            "defect 4/√π − 2 recorded in LC-15)",
            xl="diffusion parameter s (log)", yl="d_s")

# ---------- figure D: the divergence ----------
walk = RES["detail"]["N256_r0"]["curve"]
figD = plot([{"pts": walk, "cls": "wC", "label": "walk (N = 256): peak grows with N, falls at the lattice"},
             {"pts": dal, "cls": "dal", "label": "d'Alembertian: N-independent, → 2 at short scale"},
             {"pts": [(0.01, 2.0), (300, 2.0)], "cls": "ink", "dash": True, "label": "d = 2"}],
            logx=True, title="one substrate, two answers: the divergence, registered before it was measured (clause d)",
            xl="diffusion scale (log; t and s nominally identified)", yl="d_s")

pk = RES["detail"]["peaks"]
HTML = f"""<title>The Two Spectral Dimensions</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,640&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root {{ --bg:#FBFAF7; --ink:#1F242A; --mut:#6B6A64; --hair:#E2DFD6; --card:#F3F1EA;
  --wA:#9DB4CC; --wB:#5B7A99; --wC:#2E4A66; --dal:#C2582F; --pt:#2E4A66; --lk:#B8A66A; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --wA:#5B7A99; --wB:#83A4C4; --wC:#B4CCE4; --dal:#E07A4A; --pt:#B4CCE4; --lk:#D4B054; }} }}
:root[data-theme="dark"] {{ --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --wA:#5B7A99; --wB:#83A4C4; --wC:#B4CCE4; --dal:#E07A4A; --pt:#B4CCE4; --lk:#D4B054; }}
body {{ background:var(--bg); color:var(--ink); margin:0;
  font-family:"STIX Two Text", Georgia, serif; font-size:17px; line-height:1.55; }}
main {{ max-width:920px; margin:0 auto; padding:40px 22px 80px; }}
h1 {{ font-family:Fraunces, Georgia, serif; font-weight:640; font-size:2.6rem; margin:0 0 4px; text-wrap:balance; }}
h2 {{ font-family:Fraunces, Georgia, serif; font-weight:560; font-size:1.45rem; margin:0 0 10px; }}
.sub {{ color:var(--mut); margin:0 0 6px; }} .prov {{ font-family:"JetBrains Mono", monospace; font-size:.72rem; color:var(--mut); }}
section {{ margin-top:48px; }}
.stmt {{ background:var(--card); border-left:3px solid var(--dal); padding:14px 18px; margin:14px 0 20px; }}
.stmt .eq {{ font-family:"JetBrains Mono", monospace; font-size:.92rem; display:block; margin:6px 0; }}
.stmt .tag {{ font-family:"JetBrains Mono", monospace; font-size:.7rem; color:var(--mut); text-transform:uppercase; letter-spacing:.08em; }}
.fig {{ width:100%; height:auto; }} svg text {{ fill:var(--ink); }}
.ftitle {{ font:600 .8rem "JetBrains Mono", monospace; }}
.tick, .alab {{ font:400 .72rem "JetBrains Mono", monospace; fill:var(--mut); }}
.leg {{ font:600 .74rem "JetBrains Mono", monospace; }}
.grid {{ stroke:var(--hair); }} .axis {{ stroke:var(--mut); stroke-width:1.2; }}
.line {{ fill:none; stroke-width:2.2; }} .dot {{ stroke:var(--bg); stroke-width:1.2; }}
.ink {{ stroke:var(--ink); fill:var(--ink); }}
.wA {{ stroke:var(--wA); fill:var(--wA); }} .wB {{ stroke:var(--wB); fill:var(--wB); }}
.wC {{ stroke:var(--wC); fill:var(--wC); }} .dal {{ stroke:var(--dal); fill:var(--dal); }}
.pt {{ fill:var(--pt); }} .lk {{ stroke:var(--lk); stroke-width:1; opacity:.7; }}
p {{ max-width:66ch; }} .note {{ color:var(--mut); font-size:.9rem; }}
</style>
<main>
<h1>The Two Spectral Dimensions</h1>
<p class="sub">One sprinkled causal set; two published definitions; opposite short-scale answers — the divergence registered before it was measured.</p>
<p class="prov">proslambenomenos · P-16 / R-21 (+ P-25 / R-22) · seeds {REG['seed0']} / 251251 · no winner crowned</p>

<section>
<h2>The substrate</h2>
<div class="stmt"><span class="tag">backed statement · EQ5 · clause (a)</span>
<span class="eq">E[links] = N(N−1) ∫∫ (1−a)(1−b)(1−ab)^(N−2) da db — every cell inside its band</span>
The Hasse degree grows ~ 2 ln N (pins 5.64 / 6.95 / 8.29): the causet's radical nonlocality, and the driver of everything below.</div>
{figA}
</section>

<section>
<h2>The walk says: more dimensions, then none</h2>
<div class="stmt"><span class="tag">backed statement · clauses (b), (d) · R-21</span>
<span class="eq">window peaks {pk['64']:.3f} → {pk['128']:.3f} → {pk['256']:.3f}  (growth 1.023, floor 0.10) ; d_s(lattice) ≤ 0.198</span>
Eichhorn–Mizera's increasing spectral dimension, reproduced on our own sprinklings — and R-22's finding: even the walk's own two clocks separate by parity effects of the triangle-free graph (odd/even returns 0.195 at five steps).</div>
{figB}
</section>

<section>
<h2>The d'Alembertian says: two, always</h2>
<div class="stmt"><span class="tag">backed statement · EQ2–EQ4 · LC-15</span>
<span class="eq">g = −Z e^(Z/2) E₂(Z/2)  (source, exact limits) ;  printed eq. 15 defect = 4/√π − 2 = 0.256758 (derived = measured)</span>
The regularised heat kernel runs 2 → {REG['dalembertian_peak']['ds']:.3f} → 2, N-independent by construction; the unregularised identity d_s = 4ρs is recovered at ratio 1.000.</div>
{figC}
</section>

<section>
<h2>The divergence</h2>
<div class="stmt"><span class="tag">the registered output · clause (d) · derived at EQ7 before measurement</span>
<span class="eq">walk → 0 through an N-growing peak ; d'Alembertian → 2 on a fixed curve — opposite directions, opposite refinement</span>
The short-scale spectral dimension of a causal set is a convention-laden quantity; the cross-paper disagreement is the expected condition. BBMM's own conclusion asks whether a universal interpolation exists — that question is now framed by computation and deliberately left open.</div>
{figD}
<p class="note">Scored numbers live in p16_results.json / p25_results.json against pins in p16_registration.json; the causet drawing regenerates deterministically from the registered seed. The instrument-clause firings (R-21, R-22) and their diagnoses are part of the record, not footnotes.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
