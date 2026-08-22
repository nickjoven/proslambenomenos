#!/usr/bin/env python3
"""Render toda_results.json as an SVG figure page (stdlib only)."""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
d = json.load(open(ROOT / "scripts/experiments/toda_results.json"))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts/experiments/toda_plots.html"


def svg_lines(series, W=820, H=300, xl="", yl="", title="", pad=(48, 14, 40, 18)):
    L, R, B, Tp = pad
    xs = [x for s in series for x, _ in s["pts"]]; ys = [y for s in series for _, y in s["pts"]]
    x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
    if y1 - y0 < 1e-12: y0, y1 = y0 - 0.5, y1 + 0.5
    y0, y1 = y0 - 0.05 * (y1 - y0), y1 + 0.05 * (y1 - y0)
    X = lambda x: L + (x - x0) / (x1 - x0) * (W - L - R)
    Y = lambda y: Tp + (y1 - y) / (y1 - y0) * (H - Tp - B)
    out = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="{title}">']
    out.append(f'<text x="{L}" y="{Tp - 2}" class="t">{title}</text>')
    for k in range(5):
        yy = y0 + (y1 - y0) * k / 4
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(yy):.1f}" y2="{Y(yy):.1f}" class="grid"/>')
        out.append(f'<text x="{L - 6}" y="{Y(yy) + 4:.1f}" class="tick" text-anchor="end">{yy:.2f}</text>')
    for k in range(5):
        xx = x0 + (x1 - x0) * k / 4
        out.append(f'<text x="{X(xx):.1f}" y="{H - B + 16}" class="tick" text-anchor="middle">{xx:.0f}</text>')
    out.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(y0):.1f}" y2="{Y(y0):.1f}" class="axis"/><line x1="{L}" x2="{L}" y1="{Y(y0):.1f}" y2="{Y(y1):.1f}" class="axis"/>')
    for s in series:
        pts = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in s["pts"])
        if s.get("dots"):
            out += [f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4" class="{s["cls"]}"/>' for x, y in s["pts"]]
        else:
            out.append(f'<polyline points="{pts}" class="{s["cls"]}"/>')
    lx = W - R - 10
    for i, s in enumerate(series):
        out.append(f'<text x="{lx}" y="{Tp + 16 + 16 * i}" class="lab {s["cls"]}" text-anchor="end">{s["label"]}</text>')
    out.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 4}" class="tick" text-anchor="middle">{xl}</text>')
    out.append(f'<text x="12" y="{(Tp + H - B) / 2:.0f}" class="tick" transform="rotate(-90 12 {(Tp + H - B) / 2:.0f})" text-anchor="middle">{yl}</text>')
    out.append("</svg>")
    return "\n".join(out)


def snap(key, t): return d[key]["snaps"][str(float(t))]
figs = []
# 1 exact soliton: Toda vs linear at t = 0, 120
figs.append(("1. The exact one-soliton (κ = 1) after 120 time units", svg_lines([
    {"pts": [(n, -v) for n, v in enumerate(snap("exact_k1_toda", 0)) if 90 <= n <= 300], "cls": "s0", "label": "t = 0 (both chains)"},
    {"pts": [(n, -v) for n, v in enumerate(snap("exact_k1_toda", 120)) if 90 <= n <= 300], "cls": "s1", "label": "Toda, t = 120: same shape, 141 sites on"},
    {"pts": [(n, -v) for n, v in enumerate(snap("exact_k1_linear", 120)) if 90 <= n <= 300], "cls": "s2", "label": "linear null, t = 120: dispersed"},
], xl="site n", yl="compression −r")))
# 2 emergence
figs.append(("2. A generic Gaussian pulse: the Toda chain sheds a soliton, the linear chain only spreads", svg_lines([
    {"pts": [(n, -v) for n, v in enumerate(snap("pulse_toda", 0)) if 90 <= n <= 380], "cls": "s0", "label": "t = 0"},
    {"pts": [(n, -v) for n, v in enumerate(snap("pulse_toda", 160)) if 90 <= n <= 380], "cls": "s1", "label": "Toda, t = 160: soliton at n ≈ 340 (v ≈ 1.37c) + tail"},
    {"pts": [(n, -v) for n, v in enumerate(snap("pulse_linear", 160)) if 90 <= n <= 380], "cls": "s2", "label": "linear, t = 160: at n ≈ 278 (v = c), decaying"},
], xl="site n", yl="compression −r")))
# 3 peak vs t
def pk(key): return sorted((float(t), s[1]) for t, s in d[key]["stats"].items())
figs.append(("3. Peak compression against time", svg_lines([
    {"pts": pk("exact_k1_toda"), "cls": "s1", "label": "exact soliton on Toda", "dots": True},
    {"pts": pk("exact_k1_linear"), "cls": "s2", "label": "same profile on linear", "dots": True},
    {"pts": pk("pulse_linear"), "cls": "s3", "label": "Gaussian pulse on linear", "dots": True},
], xl="time", yl="peak −r")))
# 4 speed law
law = d["law"]
ks = [r["kappa"] for r in law]
figs.append(("4. Speed–amplitude law: v/c = sinh(κ)/κ", svg_lines([
    {"pts": [(k / 100, math.sinh(k / 100) / (k / 100)) for k in range(40, 170)], "cls": "s1", "label": "sinh(κ)/κ (Toda 1967)"},
    {"pts": [(r["kappa"], r["v_measured"]) for r in law], "cls": "s2", "label": "measured", "dots": True},
], xl="κ (amplitude parameter; peak = 2 ln cosh κ)", yl="v / c")))

page = """<title>Toda Chain Solitons</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@500;600&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap">
<style>
:root{--bg:#f5f6f8;--panel:#fff;--ink:#1b2230;--mute:#5b6675;--line:#d5dae2;--s0:#8a93a3;--s1:#1f5fa8;--s2:#a83232;--s3:#9a6b1f;--grid:#e7eaef}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#12161d;--panel:#191f28;--ink:#e6e9ee;--mute:#98a3b3;--line:#2c3542;--s0:#7d8796;--s1:#6ea8ff;--s2:#ef7a7a;--s3:#d2a24c;--grid:#242c38}}
:root[data-theme="dark"]{--bg:#12161d;--panel:#191f28;--ink:#e6e9ee;--mute:#98a3b3;--line:#2c3542;--s0:#7d8796;--s1:#6ea8ff;--s2:#ef7a7a;--s3:#d2a24c;--grid:#242c38}
body{background:var(--bg);color:var(--ink);font-family:"Source Sans 3",system-ui,sans-serif;margin:0;padding:28px 20px 60px;line-height:1.45}
main{max-width:900px;margin:0 auto;display:grid;gap:20px}
h1{font-family:"IBM Plex Serif",Georgia,serif;font-weight:600;font-size:1.6rem;margin:0}
h2{font-family:"IBM Plex Serif",Georgia,serif;font-weight:500;font-size:1.02rem;margin:0 0 8px}
p{max-width:70ch;margin:0}
section{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px}
.fig{width:100%;height:auto;display:block;margin-top:6px}
.t{font:600 13px "Source Sans 3",sans-serif;fill:var(--ink)}
.tick{font:11px "IBM Plex Mono",monospace;fill:var(--mute)}
.lab{font:600 12px "Source Sans 3",sans-serif}
.grid{stroke:var(--grid);stroke-width:1}.axis{stroke:var(--line);stroke-width:1}
polyline{fill:none;stroke-width:2}polyline.s0{stroke:var(--s0);stroke-dasharray:4 3}polyline.s1{stroke:var(--s1)}polyline.s2{stroke:var(--s2)}polyline.s3{stroke:var(--s3)}
circle.s1{fill:var(--s1)}circle.s2{fill:var(--s2)}circle.s3{fill:var(--s3)}
text.s0{fill:var(--s0)}text.s1{fill:var(--s1)}text.s2{fill:var(--s2)}text.s3{fill:var(--s3)}
.mono{font-family:"IBM Plex Mono",monospace;font-size:.85rem;color:var(--mute)}
</style>
<main>
<header><h1>Toda Chain Solitons</h1><p class="mono">inertial chain, force 1 − e<sup>−r</sup> (Toda) against its linear null r; unit mass, sound speed 1, fixed ends, velocity-Verlet dt = 0.02; scripts/experiments/toda_solitons.py; catalog c29</p></header>
<section><p>A weak discontinuity on a linear chain spreads (c11). Give the chain inertia <em>and</em> a nonlinear spring and dispersion can be balanced by steepening: a localized packet that keeps its shape, travels faster than sound by an amount fixed by its amplitude, and survives collisions — a soliton. Four demonstrations, each against the same chain with the nonlinearity removed.</p></section>
""" + "\n".join(f'<section><h2>{t}</h2>{s}</section>' for t, s in figs) + """
<section><h2>What the figures say, and what they do not</h2>
<p>1: the Toda chain transports the exact profile unchanged (peak 0.8676 → 0.8672, width 3 sites) at 1.18 c; the linear chain halves the peak and doubles the width — Schrödinger's 1914 spreading. 2: the nonlinearity converts a generic pulse into a soliton plus radiation; the soliton is one to two sites wide, so its sampled peak flickers as it passes between sites (1.24–1.52) — a lattice-scale object, not instability. 3: the three peak histories. 4: the speed law within 1% at five amplitudes. Not shown and not claimed: collisions, multi-soliton solutions, the continuum KdV limit, anything about spacetime — the relation to gravitational solitons (Belinski–Zakharov) and boson stars is by name of the phenomenon only. Every curve is regenerated by the script; c29 re-runs the κ = 1 case in 0.4 s and fails under the linear mutant.</p></section>
</main>"""
OUT.write_text(page)
print(f"wrote {OUT} ({len(page)//1024} KB)")
