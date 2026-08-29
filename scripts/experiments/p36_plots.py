#!/usr/bin/env python3
"""P-36 figure page. Numbers from p36_results.json /
p36_channel.json / p35_derive.json. Output: p36_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p36_plots.html"
RES = json.load(open(HERE / "p36_results.json"))
CH = json.load(open(HERE / "p36_channel.json"))

from kernels.figpage import page, plot  # noqa: E402

LIGHT = {"bg": "#f7f5f0", "ink": "#1b2230", "mut": "#5b6675",
         "hair": "#d8d3c8", "card": "#ffffff", "c1": "#1f7a4d",
         "c2": "#a83232", "c3": "#2b5fa3", "c4": "#9a6b1f"}
DARK = {"bg": "#12161d", "ink": "#e6e9ee", "mut": "#98a3b3",
        "hair": "#2c3542", "card": "#191f28", "c1": "#4cc38a",
        "c2": "#e06c6c", "c3": "#7fb0e0", "c4": "#d2a24c"}


def profile(N, total, f):
    lo, hi = -0.999999, 1.0 - (N - 1) * f / N - 1e-9

    def S(c):
        return sum(math.asin(c + m * f / N) for m in range(N))

    slo = S(lo)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if (S(mid) - total) * (slo - total) <= 0:
            hi = mid
        else:
            lo, slo = mid, S(lo)
    c = 0.5 * (lo + hi)
    return [c + m * f / N for m in range(N)]


# ---------------------------------------------------------- fig 1
# the two fold profiles at N = 64
N = 64
fc = CH["EQ8"]["64"]["fold_solver"]
ft = CH["EQ9"]["64"]["fold_twisted"]
pc = profile(N, 0.0, fc - 1e-6)
pt = profile(N, math.pi, ft - 1e-6)
fig1 = plot([
    {"pts": [(m, 1.0) for m in range(N)], "cls": "c2", "dash": True,
     "label": "bond capacity ±1"},
    {"pts": [(m, -1.0) for m in range(N)], "cls": "c2", "dash": True},
    {"pts": list(enumerate(pc)), "cls": "c3",
     "label": "control at its fold — both contact bonds saturate"},
    {"pts": list(enumerate(pt)), "cls": "c1",
     "label": "twisted at its fold — the top bond saturates alone"},
], H=320, title="the fold profiles: sin(sⱼ) climbing around the loop",
    xl="bonds, walked from the contact", yl="sin(covariant strain)",
    yfmt="{:.1f}", xfmt="{:.0f}")

# ---------------------------------------------------------- fig 2
# derived fold ratio vs N, measured onset ratios on top
def fold_fc(N_, total):
    def sum_s(c, f):
        s = 0.0
        for m in range(N_):
            x = c + m * f / N_
            if x <= -1.0 or x >= 1.0:
                return None
            s += math.asin(x)
        return s

    def has_root(f):
        lo, hi = -0.999999, 1.0 - (N_ - 1) * f / N_ - 1e-12
        if hi <= lo:
            return False
        slo, shi = sum_s(lo, f), sum_s(hi, f)
        if slo is None or shi is None:
            return False
        return (slo - total) * (shi - total) <= 0

    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if has_root(mid):
            lo = mid
        else:
            hi = mid
    return lo


curve = [(n, fold_fc(n, math.pi) / fold_fc(n, 0.0))
         for n in range(56, 137, 8)]
meas = [(int(k), RES["clauses"][k]["ratio"]) for k in ("64", "96", "128")]
fig2 = plot([
    {"pts": curve, "cls": "c1",
     "label": "derived fold ratio (the static strain budget)"},
    {"pts": meas, "cls": "c4", "dots": True,
     "label": "measured onset ratio, registered cells"},
], H=300, title="the O(1/N) budget, derived then measured",
    xl="ring size N", yl="onset(twisted) / onset(control)",
    yfmt="{:.3f}", xfmt="{:.0f}")

# ---------------------------------------------------------- fig 3
# the channel across every registered cell
cells = [("control", "c2"), ("twist0", "c1"), ("twist1", "c1")]
cols = [("N64_g0.02", "N=64"), ("N96_g0.02", "N=96"),
        ("N128_g0.02", "N=128"), ("N64_g0.01", "γ=.01"),
        ("N64_g0.04", "γ=.04")]
W3, H3 = 860, 210
sv = [f'<svg viewBox="0 0 {W3} {H3}" class="fig" role="img" '
      f'aria-label="channels">']
x0, y0, cw, chh = 170, 46, 128, 46
for ci, (ck, lab) in enumerate(cols):
    sv.append(f'<text x="{x0 + ci * cw + cw / 2}" y="{y0 - 14}" '
              f'class="leg ink" text-anchor="middle">{lab}</text>')
for ri, (tag, cls) in enumerate(cells):
    nice = {"control": "control", "twist0": "sector −½",
            "twist1": "sector +½"}[tag]
    sv.append(f'<text x="{x0 - 12}" y="{y0 + ri * chh + 28}" '
              f'class="leg ink" text-anchor="end">{nice}</text>')
    for ci, (ck, lab) in enumerate(cols):
        cell = RES["cells"].get(f"{tag}_{ck}")
        d = cell["detail"]
        dw = d.get("dW_first")
        txt = "ΔW = 0 · paired" if dw is None else f"ΔW = {dw:+d} · single"
        sv.append(f'<rect x="{x0 + ci * cw + 3}" y="{y0 + ri * chh + 3}" '
                  f'width="{cw - 6}" height="{chh - 6}" rx="6" '
                  f'fill="none" stroke="var(--{cls})" '
                  f'stroke-width="1.6"/>')
        sv.append(f'<text x="{x0 + ci * cw + cw / 2}" '
                  f'y="{y0 + ri * chh + 28}" class="leg" '
                  f'fill="var(--{cls})" text-anchor="middle">{txt}</text>')
sv.append("</svg>")
fig3 = "".join(sv)

ev = RES["clauses"]
body = f"""
<section>
<h2>What the clamp destroyed, derived back</h2>
<div class="stmt"><span class="tag">backed statement · EQ4 / EQ8 / EQ9</span>
<span class="eq">control fold = 2N/(N−1) — the contact pair saturates together, symmetrically</span>
<span class="eq">twisted loop constraint Σs = ±π de-centers the profile — the top bond saturates alone, fold ratio 0.96629 / 0.97782 / 0.98350 at N = 64 / 96 / 128</span>
R-3 showed the clamped P-4 ring was gauge-equivalent to its control; on the free ring the π bond pre-spends
an O(1/N) share of the strain budget, and the two twisted sectors are exactly degenerate by reflection.</div>
{fig1}
</section>

<section>
<h2>The budget, measured</h2>
<div class="stmt"><span class="tag">backed statement · R-34 clauses (b)(c)(d)</span>
<span class="eq">onset ratios {ev['64']['ratio']:.5f} / {ev['96']['ratio']:.5f} / {ev['128']['ratio']:.5f} — every cell inside its ~0.005 band around the derived ratio</span>
<span class="eq">sector splits 3.6e-5 / 2.4e-5 / 1.8e-5 — the exact-degeneracy instrument floor, three orders under one grid step</span>
No dynamical selection beyond the static budget: P-4's mind-change condition, finally measurable, did not fire.</div>
{fig2}
</section>

<section>
<h2>The holonomy selects the channel</h2>
<div class="stmt"><span class="tag">backed statement · R-34 clause (e)</span>
<span class="eq">control: first event is a paired slip through the two contact bonds — winding-neutral, invisible to net W (R-33's diagnosis)</span>
<span class="eq">twisted: first event is a single slip — ΔW = +1 in sector −½ and −1 in sector +½, mirror images, in every cell</span>
P-4 asked which orbits close on the base vs the double cover; this is that question with an answer.</div>
{fig3}
<p class="note">Every number on this page lives in p36_results.json (registered grid), p36_channel.json (the
derived channel structure), and p35_derive.json (the pre-registration layer); the falsifier
scripts/verify/p36_free_ring.py re-derives the folds and re-runs both channels with its own integrator.</p>
</section>
"""

HTML = page(
    "The Reopened Ring",
    "P-35/P-36 · the holonomy budget P-4 could not measure — a free π ring under a dead load: "
    "an O(1/N) strain budget, exactly degenerate sectors, and a slip channel the bundle class picks",
    "proslambenomenos · P-35/R-33 · P-36/R-34 · claim holonomy-selects-the-slip-channel · 2026-08-29",
    body, LIGHT, DARK)
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
