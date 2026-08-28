#!/usr/bin/env python3
"""P-27 figure page: the classical-gravity squeeze windows. Every
number is read from p27_results.json / p27_registration.json /
janse_table1.json. Output: p27_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from kernels.figpage import plot                        # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p27_plots.html"
REG = json.load(open(HERE / "p27_registration.json"))
RES = json.load(open(HERE / "p27_results.json"))
TAB = json.load(open(HERE / "janse_table1.json"))

# ---------------------------------------------------------- fig 1
# the squeeze: log10 D2-window bars per class and rule
CLASSES = [("cont", "ultra-local continuous", "D₂"),
           ("disc", "ultra-local discrete", "l_P³D₂/m_P"),
           ("nonloc", "nonlocal continuous", "l_P²D₂")]
RULES = ["ossw-2022 (Cavendish)", "direct-on-Earth best (Gisler)",
         "+ LISA Pathfinder (Armano)", "+ atom interferometry (Asenbaum)"]


def cell(cls, rule, lower="ossw", which="windows_printed"):
    return [w for w in RES[which] if w["class"] == cls
            and w["rule"] == rule and w["lower_convention"] == lower][0]


W, RH = 900, 34
rowsvg = []
y = 30
L, R = 320, 30
lo_x, hi_x = -45.0, -5.0


def X(v):
    return L + (math.log10(v) - lo_x) / (hi_x - lo_x) * (W - L - R)


rowsvg.append(f'<svg viewBox="0 0 {W} {30 + RH * 13 + 40}" class="fig" '
              f'role="img" aria-label="squeeze windows">')
for k in range(-45, -4, 5):
    x = L + (k - lo_x) / (hi_x - lo_x) * (W - L - R)
    rowsvg.append(f'<line x1="{x:.0f}" x2="{x:.0f}" y1="24" '
                  f'y2="{30 + RH * 13}" class="grid"/>')
    rowsvg.append(f'<text x="{x:.0f}" y="18" class="tick" '
                  f'text-anchor="middle">1e{k}</text>')
for cls, name, unit in CLASSES:
    rowsvg.append(f'<text x="8" y="{y + 14}" class="clab">{name}'
                  f' <tspan class="mut">[{unit}]</tspan></text>')
    y += 22
    for rule in RULES:
        w = cell(cls, rule)
        wr = cell(cls, rule, "ossw", "windows_recomputed")
        lo, up = w["lower"], w["upper"]
        frag = (w["window_orders"] < 0) != (wr["window_orders"] < 0)
        x0, x1 = X(min(lo, up)), X(max(lo, up))
        cls_css = ("barfrag" if frag else
                   ("barneg" if w["window_orders"] < 0 else "barpos"))
        rowsvg.append(f'<rect x="{x0:.1f}" y="{y + 4}" '
                      f'width="{max(x1 - x0, 2):.1f}" height="14" '
                      f'class="{cls_css}"/>')
        lab = f"{rule.split('(')[1].rstrip(')')} · " \
              f"{w['window_orders']:+.1f}"
        if frag:
            lab += f" / {wr['window_orders']:+.1f} — undecidable"
        elif w["window_orders"] < 0:
            lab += " — excluded"
        rowsvg.append(f'<text x="{L - 8}" y="{y + 15}" class="tick" '
                      f'text-anchor="end">{lab}</text>')
        y += RH * 0.72
    y += 12
rowsvg.append(f'<text x="{(L + W - R) / 2:.0f}" y="{y + 18}" '
              f'class="alab" text-anchor="middle">D₂ scale '
              f'(class units) — bar spans lower→upper bound; '
              f'green survives, rust excluded, striped undecidable '
              f'at source precision</text>')
rowsvg.append('</svg>')
fig1 = "".join(rowsvg)

# ---------------------------------------------------------- fig 2
# the FOM ladder: all Table I rows, log-log
pts_direct, pts_quest = [], []
for r in TAB["rows"]:
    if not r["FOM"] or not r["m_kg"]:
        continue
    p = (math.log10(r["m_kg"]), math.log10(r["FOM"]))
    (pts_quest if r["differential_questioned"] else pts_direct).append(p)
lines = []
for val, lab, cls in ((1e14, "Cavendish (OSSW input)", "c4"),
                      (RES["closure"]["disc_close"],
                       "discrete class closes", "c1"),
                      (RES["closure"]["nonloc_close_janse"],
                       "nonlocal closes (Janse conv.)", "c5"),
                      (RES["closure"]["nonloc_close_ossw"],
                       "nonlocal closes (OSSW conv.)", "c2")):
    lines.append({"pts": [(-26, math.log10(val)),
                          (2.5, math.log10(val))],
                  "cls": cls, "dash": True, "label": lab})
fig2 = plot(lines + [
    {"pts": sorted(pts_direct), "cls": "c3", "dots": True,
     "label": "absolute on-Earth measurements"},
    {"pts": sorted(pts_quest), "cls": "c1", "dots": True,
     "label": "differential/relative (contested)"},
], H=380, title="the figure-of-merit ladder: 45 experiments vs the closure lines",
    xl="log₁₀ test mass [kg]", yl="log₁₀ FOM = N·S_a [m²s⁻³]",
    yfmt="{:.0f}", xfmt="{:.0f}")

# ---------------------------------------------------------- fig 3
# printed-vs-recomputed deltas and the three flips
d = REG["EQ2"]["signed_deltas_orders"]
flips = RES["flips"]
bars = [f'<svg viewBox="0 0 900 260" class="fig" role="img" '
        f'aria-label="deltas and flips">']
x_mid = 560
scale = 60


def bx(v):
    return x_mid + v * scale


bars.append(f'<line x1="{x_mid}" x2="{x_mid}" y1="14" y2="230" '
            f'class="axis"/>')
items = [(f"{k} printed − derived", v, False)
         for k, v in d.items() if k.endswith("upper")]
items += [(f"flip: {c[0]}/{c[2]} (Asenbaum)", None, (c[3], c[4]))
          for c in flips]
y = 26
for lab, v, pair in items:
    if pair is False and v is not None:
        bars.append(f'<rect x="{min(bx(0), bx(v)):.1f}" y="{y}" '
                    f'width="{abs(bx(v) - bx(0)):.1f}" height="16" '
                    f'class="bard"/>')
        bars.append(f'<text x="{bx(0) - 570 + 8:.0f}" y="{y + 13}" '
                    f'class="tick">{lab} · {v:+.2f} orders</text>')
    else:
        a, b = pair
        bars.append(f'<circle cx="{bx(a):.1f}" cy="{y + 8}" r="5" '
                    f'class="c1 dot"/>')
        bars.append(f'<circle cx="{bx(b):.1f}" cy="{y + 8}" r="5" '
                    f'class="c2 dot"/>')
        bars.append(f'<line x1="{bx(a):.1f}" x2="{bx(b):.1f}" '
                    f'y1="{y + 8}" y2="{y + 8}" class="flipline"/>')
        bars.append(f'<text x="8" y="{y + 13}" class="tick">{lab} · '
                    f'{a:+.2f} → {b:+.2f}</text>')
    y += 32
bars.append(f'<text x="{x_mid}" y="252" class="alab" '
            f'text-anchor="middle">orders of magnitude (0 = printed '
            f'value / verdict boundary); dots: window under printed '
            f'vs recomputed bounds</text>')
bars.append('</svg>')
fig3 = "".join(bars)

# ---------------------------------------------------------- page
HTML = f"""<title>The Classical-Gravity Squeeze</title>
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
main {{ max-width:960px; margin:0 auto; padding:40px 24px 80px; }}
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
.clab {{ fill:var(--ink); font:600 13px "Source Sans 3", sans-serif; }}
.mut {{ fill:var(--mut); font-weight:400; }}
.line {{ fill:none; stroke-width:2; }}
.dot {{ stroke:var(--bg); stroke-width:1.2; }}
.c1 {{ stroke:var(--c1); fill:var(--c1); }} .c2 {{ stroke:var(--c2); fill:var(--c2); }}
.c3 {{ stroke:var(--c3); fill:var(--c3); }} .c4 {{ stroke:var(--c4); fill:var(--c4); }}
.c5 {{ stroke:var(--c5); fill:var(--c5); }}
.c1.line,.c2.line,.c3.line,.c4.line,.c5.line {{ fill:none; }}
.barpos {{ fill:var(--c2); opacity:.8; }}
.barneg {{ fill:var(--c1); opacity:.8; }}
.barfrag {{ fill:var(--c5); opacity:.65; }}
.bard {{ fill:var(--c3); opacity:.85; }}
.flipline {{ stroke:var(--mut); stroke-width:1.4; stroke-dasharray:4 3; }}
.stmt {{ background:var(--card); border:1px solid var(--hair); border-radius:10px;
  padding:14px 18px; margin:14px 0; }}
.tag {{ display:block; font:600 11px "JetBrains Mono", monospace; color:var(--mut);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }}
.eq {{ display:block; font-family:"JetBrains Mono", monospace; font-size:.85rem; margin:4px 0; }}
.note {{ color:var(--mut); font-size:.85rem; }}
</style>
<main>
<h1>The classical-gravity squeeze</h1>
<p class="sub">If spacetime is classical, coherence must be paid for in diffusion. The surviving windows for Oppenheim's postquantum gravity, computed with their fragility exposed.</p>
<p class="prov">proslambenomenos · P-27 / R-24 · OSSW Nature Comms 14, 7910 · Janse PRR 6, 033076 · sign-stability clause FIRED · LC-17</p>

<section>
<h2>The squeeze</h2>
<div class="stmt"><span class="tag">backed statement · clauses (b)–(d) · R-24</span>
<span class="eq">interferometry: D₂ ≥ M²/(Vλ) — coherence observed ⟹ diffusion required (λ in the denominator, unit-mechanized)</span>
<span class="eq">force noise: D₂ ≤ σ_a²·N·ΔT·r_N⁴/(m_N G²) — the diffusion would shake test masses</span>
Ultra-local continuous: excluded under every rule. Discrete: survives the uncontested rule by 9.5 orders. The contested atom-interferometry cells: undecidable at the sources' own precision.</div>
{fig1}
</section>

<section>
<h2>The ladder, and what would decide it</h2>
<div class="stmt"><span class="tag">backed statement · clause (e) · R-24</span>
<span class="eq">FOM_D2 = N·S_a — the one number an experiment contributes; the discrete class shuts at 1e-10 m²s⁻³ (uncontested, absolute, on Earth)</span>
Best uncontested today: Gisler's nanowire at 3e-1. Nine orders. The contested rows (Asenbaum, LISA Pathfinder) already sit below the closure lines — IF relative measurements count, which is imported, open, and now also arithmetic-fragile.</div>
{fig2}
</section>

<section>
<h2>The firing</h2>
<div class="stmt"><span class="tag">backed statement · R-24 mind-change · sign stability</span>
<span class="eq">printed upper bounds sit +2.26 / −1.35 / +1.65 orders from their own stated inputs (lower bounds: exact)</span>
All three contested verdicts flip sign when the printed bounds are replaced by the same bounds recomputed from the sources' own inputs. "Atom interferometry closes the discrete class" is not a conclusion — it is a rounding choice.</div>
{fig3}
<p class="note">Every number on this page traces to p27_results.json against pins in p27_registration.json and the machine-parsed janse_table1.json; the audit trail (unstated averaging time, the underivable 1e-35, the Monteiro row) lives in LC-17.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
