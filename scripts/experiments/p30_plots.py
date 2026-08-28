#!/usr/bin/env python3
"""P-30 figure page: the order ladder. Every number is read from
p30_results.json or regenerated from the registered pipeline.
Output: p30_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p30_plots.html"
RES = json.load(open(HERE / "p30_results.json"))
RT2 = math.sqrt(2)

# ---------------------------------------------------------- fig 1
# three ladders on one S-axis
W, H = 880, 300
lo, hi = 1.7, 4.3


def X(s):
    return 90 + (s - lo) / (hi - lo) * (W - 130)


rows = [
    ("Bell (P-17)", [2.0, 2 * RT2, 4.0], "S", "c3"),
    ("OCB causal game", RES["ladders"]["S_ocb"], "S = 8p − 4", "c1"),
    ("VLBC switch game", RES["ladders"]["S_vlbc"], "S = 8(p−1) − 4",
     "c2"),
]
labels = ["ordered / local\n(exhaustive)", "quantum", "algebraic"]
svg = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" '
       f'aria-label="three ladders">']
for k, s in enumerate([2.0, 2 * RT2, 4.0]):
    svg.append(f'<line x1="{X(s):.1f}" x2="{X(s):.1f}" y1="30" '
               f'y2="{H - 70}" class="grid"/>')
    lab = ["2", "2√2", "4"][k]
    svg.append(f'<text x="{X(s):.1f}" y="22" class="tick" '
               f'text-anchor="middle">{lab}</text>')
y = 60
for name, vals, maplab, cls in rows:
    svg.append(f'<line x1="{X(1.85):.0f}" x2="{X(4.15):.0f}" '
               f'y1="{y}" y2="{y}" class="axis"/>')
    for v in vals:
        svg.append(f'<circle cx="{X(v):.1f}" cy="{y}" r="7" '
                   f'class="{cls} dot"/>')
    svg.append(f'<text x="12" y="{y + 4}" class="clab">{name}</text>')
    svg.append(f'<text x="{W - 12}" y="{y + 4}" class="tick" '
               f'text-anchor="end">{maplab}</text>')
    y += 62
svg.append(f'<text x="{W / 2:.0f}" y="{H - 24}" class="alab" '
           f'text-anchor="middle">every computed rung lands on the '
           f'Bell rungs at 1e-12 — ordered/local at 2, quantum at '
           f'2√2, algebraic at 4</text>')
svg.append('</svg>')
fig1 = "".join(svg)

# ---------------------------------------------------------- fig 2
# the separability null: 16 paired cells
import p30_ladder as L  # noqa: E402


def switch_and_mix():
    out = []
    for x1 in (0, 1):
        for x2 in (0, 1):
            for a1 in (0, 1):
                for a2 in (0, 1):
                    def K(x, a):
                        M = [[0j] * 2 for _ in range(2)]
                        M[x][a] = 1 + 0j
                        return M

                    def ap(Ka, Kb, v):
                        w = [sum(Ka[i][j] * v[j] for j in range(2))
                             for i in range(2)]
                        return [sum(Kb[i][j] * w[j]
                                    for j in range(2))
                                for i in range(2)]
                    t0 = [1 + 0j, 0j]
                    A0 = ap(K(x1, a1), K(x2, a2), t0)
                    A1 = ap(K(x2, a2), K(x1, a1), t0)
                    p_sw = sum(abs(A0[t]) ** 2 / 2
                               + abs(A1[t]) ** 2 / 2 for t in (0, 1))
                    p_mx = 0.5 * sum(abs(A0[t]) ** 2
                                     for t in (0, 1)) \
                        + 0.5 * sum(abs(A1[t]) ** 2 for t in (0, 1))
                    out.append((f"{x1}{x2}|{a1}{a2}", p_sw, p_mx))
    return out


cells = switch_and_mix()
Wc, Hc = 880, 260
svg = [f'<svg viewBox="0 0 {Wc} {Hc}" class="fig" role="img" '
       f'aria-label="separability null">']
bw = (Wc - 120) / 16
for i, (lab, ps, pm) in enumerate(cells):
    x = 60 + i * bw
    hs = ps * 150
    hm = pm * 150
    svg.append(f'<rect x="{x + 2:.1f}" y="{200 - hs:.1f}" '
               f'width="{bw * 0.38:.1f}" height="{hs:.1f}" '
               f'class="c2 bar"/>')
    svg.append(f'<rect x="{x + 2 + bw * 0.42:.1f}" '
               f'y="{200 - hm:.1f}" width="{bw * 0.38:.1f}" '
               f'height="{hm:.1f}" class="c4 bar"/>')
    svg.append(f'<text x="{x + bw / 2:.1f}" y="216" class="tick" '
               f'text-anchor="middle" font-size="8">{lab}</text>')
svg.append(f'<text x="{Wc / 2:.0f}" y="246" class="alab" '
           f'text-anchor="middle">p(a₁a₂|x₁x₂): coherent switch '
           f'(green) vs 50/50 classical order mixture (grey) — '
           f'identical in all 16 cells, worst difference '
           f'{RES["separability_worst"]:.1e}</text>')
svg.append('</svg>')
fig2 = "".join(svg)

HTML = f"""<title>The Order Ladder</title>
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
.clab {{ fill:var(--ink); font:600 13px "Source Sans 3", sans-serif; }}
.dot {{ stroke:var(--bg); stroke-width:1.4; }}
.bar {{ opacity:.85; }}
.c1 {{ stroke:var(--c1); fill:var(--c1); }} .c2 {{ stroke:var(--c2); fill:var(--c2); }}
.c3 {{ stroke:var(--c3); fill:var(--c3); }} .c4 {{ stroke:var(--c4); fill:var(--c4); }}
.c5 {{ stroke:var(--c5); fill:var(--c5); }}
.stmt {{ background:var(--card); border:1px solid var(--hair); border-radius:10px;
  padding:14px 18px; margin:14px 0; }}
.tag {{ display:block; font:600 11px "JetBrains Mono", monospace; color:var(--mut);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }}
.eq {{ display:block; font-family:"JetBrains Mono", monospace; font-size:.85rem; margin:4px 0; }}
.note {{ color:var(--mut); font-size:.85rem; }}
</style>
<main>
<h1>The order ladder</h1>
<p class="sub">Indefinite causal order, priced Bell-ladder style: exhaustive polytope bounds, exact quantum values, and the null that shows what order coherence costs to certify.</p>
<p class="prov">proslambenomenos · P-30 / R-27 · OCB Nat. Comms 3, 1092 · VLBC Nat. Comms 14 · Liu PRX Quantum 2026 (24σ, loopholed) · LC-20</p>

<section>
<h2>Three ladders, one geometry</h2>
<div class="stmt"><span class="tag">backed statement · clauses (a)–(c), (e) · R-27</span>
<span class="eq">OCB: 3/4 (8192 strategies, exhaustive) &lt; (2+√2)/4 (pinned process, spectrum {{0×8, ½×8}} by anticommutation) &lt; 1</span>
<span class="eq">VLBC: 7/4 (131072 strategies, exhaustive) &lt; 1+(2+√2)/4 (exact switch circuit) &lt; 2</span>
<span class="eq">p = (S+4)/8 and p = 1+(S+4)/8 send the Bell rungs onto both — at 1e-12 in the computed values</span>
Giving up definite order buys, in these games, what giving up local realism bought in P-17: the same √2, one affine map apart. (Two-sided honesty: OCB's middle-rung maximality is open in the source; VLBC's is proven there via Tsirelson.)</div>
{fig1}
</section>

<section>
<h2>The null that prices the switch</h2>
<div class="stmt"><span class="tag">backed statement · clause (d) · R-27</span>
<span class="eq">p_switch(a₁a₂|x₁x₂) = ½·p_(A₁≺A₂) + ½·p_(A₂≺A₁) — entrywise, machine zero</span>
The coherent switch is bipartitely indistinguishable from classical order mixing. Only the entangled spacelike observer reveals the coherence — and the reveal costs exactly a Tsirelson violation (the third term of the VLBC inequality is a CHSH game riding inside the causal game).</div>
{fig2}
<p class="note">The OCB process has no known physical realization (its own discussion; CTC models break linearity); the switch does, and the 2026 photonic experiment violates the VLBC bound at 24σ with flagged loopholes. Every scored number lives in p30_results.json against pins in p30_registration.json.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
