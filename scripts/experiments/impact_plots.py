#!/usr/bin/env python3
"""Render impact_results.json as an SVG figure page (stdlib)."""
import json, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
d = json.load(open(ROOT / "scripts/experiments/impact_results.json"))
OUT = Path(sys.argv[1])

def frame(W, H, x0, x1, y0, y1, title, xl, yl, pad=(52, 14, 40, 20), xfmt="{:.2f}", yfmt="{:.2f}"):
    L, R, B, Tp = pad
    X = lambda x: L + (x - x0) / (x1 - x0) * (W - L - R)
    Y = lambda y: Tp + (y1 - y) / (y1 - y0) * (H - Tp - B)
    out = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="{title}">', f'<text x="{L}" y="{Tp - 4}" class="t">{title}</text>']
    for k in range(5):
        yy = y0 + (y1 - y0) * k / 4; xx = x0 + (x1 - x0) * k / 4
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(yy):.1f}" y2="{Y(yy):.1f}" class="grid"/>')
        out.append(f'<text x="{L - 6}" y="{Y(yy) + 4:.1f}" class="tick" text-anchor="end">{yfmt.format(yy)}</text>')
        out.append(f'<text x="{X(xx):.1f}" y="{H - B + 16}" class="tick" text-anchor="middle">{xfmt.format(xx)}</text>')
    out.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(y0):.1f}" y2="{Y(y0):.1f}" class="axis"/><line x1="{L}" x2="{L}" y1="{Y(y0):.1f}" y2="{Y(y1):.1f}" class="axis"/>')
    out.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 4}" class="tick" text-anchor="middle">{xl}</text>')
    out.append(f'<text x="12" y="{(Tp + H - B) / 2:.0f}" class="tick" transform="rotate(-90 12 {(Tp + H - B) / 2:.0f})" text-anchor="middle">{yl}</text>')
    return out, X, Y

figs = []
# A bifurcation
bif = d["bifurcation"]; A = d["A"]
pts = [(b["sigma"] / A, v) for b in bif for v in b["v"]]
ys = [v for _, v in pts]
out, X, Y = frame(860, 320, 0.1, 1.0, 0, max(ys) * 1.05, "A. Bifurcation diagram: steady-state impact speeds against clearance σ/A (ω = 2.8, r = 0.8)", "σ / A (1 = grazing)", "|impact velocity|")
out += [f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="1.4" class="s1"/>' for x, y in pts]
out.append("</svg>"); figs.append("".join(out))
# B grazing
gz = [g for g in d["grazing"] if g["v_first"]]
out, X, Y = frame(860, 280, 0, 0.033, 0, 0.27, "B. Grazing: first-impact speed against wall depth d below the grazing clearance", "d = A − σ", "v_first", xfmt="{:.3f}")
th = [(k / 1000, math.sqrt(2 * A * 2.8 ** 2 * k / 1000)) for k in range(0, 34)]
out.append('<polyline points="' + " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in th) + '" class="s1"/>')
out += [f'<circle cx="{X(g["d"]):.1f}" cy="{Y(g["v_first"]):.1f}" r="4" class="s2"/>' for g in gz]
out.append(f'<text x="{X(0.02):.0f}" y="{Y(0.1):.0f}" class="lab s1">v = √(2Aω² d): infinite slope at d = 0</text>')
out.append("</svg>"); figs.append("".join(out))
# C census heat: labels on grid
cen = d["census"]
ws = sorted({c["omega"] for c in cen}); ss = sorted({c["sigma"] for c in cen})
colors = {"0/1": "var(--grid)", "1": "var(--s1)", "1/2": "var(--s2)", "2/3": "var(--s3)"}
L, R, B, Tp = 52, 14, 40, 22; W, H = 860, 420
cw = (W - L - R) / len(ws); ch = (H - Tp - B) / len(ss)
out = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="census">', f'<text x="{L}" y="{Tp - 6}" class="t">C. (m, n) census: impacts per forcing period in steady state over (ω, σ); grey = no impacts, blue = 1, red = 1/2 (the f₀/2 orbit), ochre = 2/3, white = other</text>']
for c in cen:
    i = ws.index(c["omega"]); j = ss.index(c["sigma"])
    col = colors.get(c["label"], "var(--panel)")
    out.append(f'<rect x="{L + i * cw:.1f}" y="{Tp + (len(ss) - 1 - j) * ch:.1f}" width="{cw:.1f}" height="{ch:.1f}" fill="{col}" stroke="var(--line)" stroke-width="0.5"/>')
for i, w in enumerate(ws):
    if i % 5 == 0: out.append(f'<text x="{L + (i + 0.5) * cw:.1f}" y="{H - B + 16}" class="tick" text-anchor="middle">{w:.1f}</text>')
for j, s in enumerate(ss):
    if j % 3 == 0: out.append(f'<text x="{L - 6}" y="{Tp + (len(ss) - 0.5 - j) * ch + 4:.1f}" class="tick" text-anchor="end">{s:.2f}</text>')
out.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 4}" class="tick" text-anchor="middle">ω (forcing frequency, ω₀ = 1)</text>')
out.append(f'<text x="12" y="{(Tp + H - B) / 2:.0f}" class="tick" transform="rotate(-90 12 {(Tp + H - B) / 2:.0f})" text-anchor="middle">σ (clearance)</text></svg>')
figs.append("".join(out))
# D chatter
ch_ = d["chatter"]; gaps = ch_["gaps"]
imin = min(range(len(gaps)), key=lambda i: gaps[i]); seg = gaps[max(0, imin - 14): imin + 1]
out, X, Y = frame(860, 280, 0, len(seg) - 1, -9, 1, "D. Complete chatter (ω = 0.5, r = 0.5): successive impact gaps fall geometrically, ratio → r", "impact index within the accumulation", "ln(gap)", xfmt="{:.0f}", yfmt="{:.0f}")
out += [f'<circle cx="{X(i):.1f}" cy="{Y(math.log(g)):.1f}" r="4" class="s2"/>' for i, g in enumerate(seg) if g > 0]
out.append(f'<text x="{X(1):.0f}" y="{Y(-7):.0f}" class="lab s2">slope = ln r = {math.log(0.5):.3f}</text>')
out.append("</svg>"); figs.append("".join(out))
# E Volterra
vo = d["volterra"]
out, X, Y = frame(860, 260, 0, 130, 0, 1.3, "E. Volterra strain on a ring glued with phase π: elastic energy N(1 − cos(π/N)) against N, with π²/2N", "N (sites)", "energy / J", xfmt="{:.0f}")
out.append('<polyline points="' + " ".join(f"{X(N):.1f},{Y(math.pi ** 2 / (2 * N)):.1f}" for N in range(4, 131)) + '" class="s1"/>')
out += [f'<circle cx="{X(v["N"]):.1f}" cy="{Y(v["energy"]):.1f}" r="4" class="s2"/>' for v in vo]
out.append(f'<text x="{X(60):.0f}" y="{Y(0.5):.0f}" class="lab s1">π²/2N — the holonomy became strain, and strain vanishes with N</text>')
out.append("</svg>"); figs.append("".join(out))

style = open(ROOT / "scripts/experiments/toda_plots.py").read().split("<style>")[1].split("</style>")[0]
page = f"""<title>Impact Oscillator Lens</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@500;600&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap">
<style>{style}rect{{shape-rendering:crispEdges}}</style>
<main>
<header><h1>Impact Oscillator Lens</h1><p class="mono">x'' + 2ζx' + x = cos ωt, wall at σ, restitution r (Shaw & Holmes 1983); exact flights between impacts, bisection on the wall; scripts/experiments/impact_oscillator.py; catalog c30</p></header>
<section><p>A linear oscillator whose only nonlinearity is a point — the wall. Its natural transform is flow → impact map: the continuous motion collapses to (phase, velocity) at each impact, and the f₀/2 oscillation is the (1,2) orbit of that map, a count. Five demonstrations.</p></section>
{"".join(f'<section>{f}</section>' for f in figs)}
<section><h2>Reading</h2><p>A: at ω = 2.8 the orbit below grazing jumps straight to a large-impact (1,1) orbit, then period-doubles and period-adds as σ falls — the non-smooth route. B: the impact map has a square-root singularity at grazing (v² = 2Aω²d, measured 2.28 vs 2.29) — infinite slope, the reason grazing produces jumps instead of smooth bifurcations. C: the (m, n) census over (ω, σ): the (1,2) f₀/2 orbit occupies a tongue-like region; the count is the structural datum, the three dimensionless groups (ω/ω₀, r, σ/A) are the anchors. D: complete chatter — gap ratio 0.500 over the last five impacts of the accumulation, infinitely many impacts in finite time — the phenomenon P-4's "chatter" was. E: gluing a ring with phase π is a Volterra disclination: uniform strain π/N, energy π²/2N, vanishing with N — why the twist is invisible to every linear observable. Not shown: anything with a loop and impacts together.</p></section>
</main>"""
OUT.write_text(page); print("wrote", OUT, len(page) // 1024, "KB")
