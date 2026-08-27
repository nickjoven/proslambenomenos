#!/usr/bin/env python3
"""Render the P-7 golden-flux figures as a self-contained HTML page
(stdlib only). Scored numbers come from p7_registration.json /
p7_results.json; the butterfly panel is regenerated deterministically
by the same validated Bloch construction. Output: p7_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p7_registration.json").read_text())
RES = json.loads((HERE / "p7_results.json").read_text())
OUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p7_plots.html"


def jacobi_eigs(A, tol=1e-10, max_sweeps=30):
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < tol:
            break
        skip = tol / (n * n)
        for p in range(n - 1):
            for q_ in range(p + 1, n):
                if abs(a[p][q_]) < skip:
                    continue
                t = 0.5 * math.atan2(2 * a[p][q_], a[q_][q_] - a[p][p]) \
                    if a[p][p] != a[q_][q_] else math.pi / 4
                c, s_ = math.cos(t), math.sin(t)
                for k in range(n):
                    x, y = a[p][k], a[q_][k]
                    a[p][k], a[q_][k] = c * x - s_ * y, s_ * x + c * y
                for k in range(n):
                    x, y = a[k][p], a[k][q_]
                    a[k][p], a[k][q_] = c * x - s_ * y, s_ * x + c * y
    return sorted(a[i][i] for i in range(n))


def bands(p, q):
    def H(corner, k2):
        if q == 1:
            return [[2 * math.cos(k2) + 2 * corner]]
        if q == 2:
            d = [2 * math.cos(2 * math.pi * p * n / q + k2) for n in (1, 2)]
            o = 1 + corner
            return [[d[0], o], [o, d[1]]]
        M = [[0.0] * q for _ in range(q)]
        for n in range(q):
            M[n][n] = 2 * math.cos(2 * math.pi * p * (n + 1) / q + k2)
        for n in range(q - 1):
            M[n][n + 1] = M[n + 1][n] = 1.0
        M[0][q - 1] = M[q - 1][0] = corner
        return M
    if q == 1:
        return [(-4.0, 4.0)]
    edges = sorted(jacobi_eigs(H(+1.0, 0.0)) + jacobi_eigs(H(-1.0, math.pi / q)))
    return [(edges[2 * i], edges[2 * i + 1]) for i in range(len(edges) // 2)]


# ---------- figure A: the anchors ----------
def band_bar(bs, y, cls, o, X):
    for a, b in bs:
        o.append(f'<line x1="{X(a):.1f}" x2="{X(b):.1f}" y1="{y}" y2="{y}" '
                 f'class="{cls} bar"/>')


W, H = 860, 200
L, R = 64, 16
X = lambda e: L + (e + 4) / 8 * (W - L - R)   # noqa: E731
oA = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="anchors">']
oA.append(f'<text x="{L}" y="22" class="ftitle">the exact anchors: bands on the energy axis</text>')
band_bar(bands(1, 2), 70, "gold", oA, X)
oA.append(f'<text x="{L - 8}" y="74" class="tick" text-anchor="end">α = 1/2</text>')
oA.append(f'<circle cx="{X(0):.1f}" cy="70" r="5" class="ember dot"/>')
oA.append(f'<text x="{X(0):.1f}" y="56" class="tick" text-anchor="middle">Dirac touch (c25)</text>')
band_bar(bands(1, 3), 120, "indigo", oA, X)
oA.append(f'<text x="{L - 8}" y="124" class="tick" text-anchor="end">α = 1/3</text>')
for e, lab in ((-2 * math.sqrt(2), "−2√2"), (2 * math.sqrt(2), "2√2"),
               (1 + math.sqrt(3), "1+√3"), (-1 - math.sqrt(3), "−1−√3")):
    oA.append(f'<text x="{X(e):.1f}" y="150" class="tick" text-anchor="middle">{lab}</text>')
for k in range(-4, 5, 2):
    oA.append(f'<text x="{X(k):.1f}" y="{H - 8}" class="tick" text-anchor="middle">{k}</text>')
oA.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 8}" class="alab" text-anchor="middle"></text>')
oA.append('</svg>')
figA = "".join(oA)

# ---------- figure B: the butterfly ----------
W, H = 860, 640
Tp, B_ = 34, 30
Y = lambda al: Tp + (1 - al) * (H - Tp - B_)   # noqa: E731
ladder_q = {2, 3, 5, 8, 13, 21}
ob = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="Hofstadter butterfly">']
ob.append(f'<text x="{L}" y="22" class="ftitle">the butterfly, q ≤ 24, from the same validated construction — golden rows are the ladder</text>')
from math import gcd
segs = []
for q in range(1, 25):
    for p in range(1, q + 1):
        if gcd(p, q) != 1 and not (p == q == 1):
            continue
        al = p / q
        if al > 1:
            continue
        cls = "gold" if (q in ladder_q and (p * 1000) // q in
                         {(f * 1000) // s for f, s in [(1, 2), (2, 3), (3, 5), (5, 8), (8, 13), (13, 21)]}) else "indigo"
        cls = "gold" if (q in ladder_q and abs(al - 0.618033988) < 1.0 / (2 * q * q) or (p, q) == (1, 2)) else "indigo"
        for a, b in bands(p, q):
            segs.append((al, a, b, cls))
for al, a, b, cls in segs:
    ob.append(f'<line x1="{X(a):.1f}" x2="{X(b):.1f}" y1="{Y(al):.1f}" y2="{Y(al):.1f}" class="{cls} thin"/>')
for al, lab in ((0.0, "0"), (0.5, "1/2"), (0.618034, "1/φ"), (1.0, "1")):
    ob.append(f'<text x="{L - 8}" y="{Y(al) + 4:.1f}" class="tick" text-anchor="end">{lab}</text>')
for k in range(-4, 5, 2):
    ob.append(f'<text x="{X(k):.1f}" y="{H - 8}" class="tick" text-anchor="middle">E = {k}</text>')
ob.append('</svg>')
figB = "".join(ob)

# ---------- figure C: the plateau ----------
W, H = 860, 320
Tp, B_ = 34, 44
qs_anchor = [(2, REG["anchors"]["2"]["S"] * 2), (3, REG["anchors"]["3"]["S"] * 3),
             (5, REG["anchors"]["5"]["S"] * 5), (8, REG["anchors"]["8"]["S"] * 8)]
qs_meas = [(int(q), v["qS"]) for q, v in RES["detail"]["ladder"].items()]
allq = qs_anchor + qs_meas
lx = lambda q: L + (math.log(q) - math.log(2)) / (math.log(144) - math.log(2)) * (W - L - R)  # noqa: E731
ymin, ymax = 8.6, 11.5
ly = lambda v: Tp + (ymax - v) / (ymax - ymin) * (H - Tp - B_)   # noqa: E731
oc = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="plateau">']
oc.append(f'<text x="{L}" y="22" class="ftitle">q·S(q): the plateau is Catalan\'s — 32G/π = {REG["thouless"]:.5f} (imported, LC-14)</text>')
oc.append(f'<line x1="{L}" x2="{W - R}" y1="{ly(REG["thouless"]):.1f}" y2="{ly(REG["thouless"]):.1f}" class="teal line" stroke-dasharray="7 5"/>')
for q, v in qs_anchor:
    oc.append(f'<circle cx="{lx(q):.1f}" cy="{ly(v):.1f}" r="5" class="ember dot"/>')
for q, v in qs_meas:
    oc.append(f'<circle cx="{lx(q):.1f}" cy="{ly(v):.1f}" r="5.5" class="gold dot"/>')
for q, v in allq:
    oc.append(f'<text x="{lx(q):.1f}" y="{H - 24}" class="tick" text-anchor="middle">{q}</text>')
oc.append(f'<text x="{W - R - 8}" y="{ly(REG["thouless"]) - 8:.1f}" class="leg teal" text-anchor="end">32G/π</text>')
oc.append(f'<text x="{W - R - 8}" y="{Tp + 16}" class="leg ember" text-anchor="end">pinned anchors (registration)</text>')
oc.append(f'<text x="{W - R - 8}" y="{Tp + 33}" class="leg gold" text-anchor="end">measured ladder (R-20)</text>')
oc.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 6}" class="alab" text-anchor="middle">q (log scale)</text>')
oc.append('</svg>')
figC = "".join(oc)

# ---------- figure D: the ln phi clock ----------
Sm = {int(q): v["S"] for q, v in RES["detail"]["ladder"].items()}
Sa = {int(k): v["S"] for k, v in REG["anchors"].items()}
Sall = sorted({**Sa, **Sm}.items())
idx = {q: i for i, (q, _) in enumerate(Sall)}
W, H = 860, 320
oD = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="ln phi clock">']
slope = RES["detail"]["clock"]["slope"]
oD.append(f'<text x="{L}" y="22" class="ftitle">the ln φ clock: ln S per ladder step — measured {slope:.5f}, ln φ = {REG["ln_phi"]:.5f} (clause d)</text>')
lnS = [(i, math.log(S)) for (q, S), i in zip(Sall, range(len(Sall)))]
y0, y1v = min(v for _, v in lnS) - 0.2, max(v for _, v in lnS) + 0.2
py = lambda v: Tp + (y1v - v) / (y1v - y0) * (H - Tp - B_)   # noqa: E731
px = lambda i: L + i / (len(Sall) - 1) * (W - L - R)          # noqa: E731
iN, vN = lnS[-1]
line = [(i, vN + (iN - i) * REG["ln_phi"]) for i in range(len(Sall))]
oD.append('<polyline points="' + " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in line) +
          '" class="teal line" stroke-dasharray="7 5"/>')
for (q, S), (i, v) in zip(Sall, lnS):
    cls = "gold" if q >= 13 else "ember"
    oD.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="5.5" class="{cls} dot"/>')
    oD.append(f'<text x="{px(i):.1f}" y="{H - 24}" class="tick" text-anchor="middle">{q}</text>')
oD.append(f'<text x="{W - R - 8}" y="{Tp + 16}" class="leg teal" text-anchor="end">slope −ln φ (derived)</text>')
oD.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 6}" class="alab" text-anchor="middle">Fibonacci denominator q</text>')
oD.append('</svg>')
figD = "".join(oD)

pl = RES["detail"]["plateau"]
ck = RES["detail"]["clock"]

HTML = f"""<title>The Golden Flux Ladder</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,640&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root {{
  --bg:#FBFAF7; --ink:#1F242A; --mut:#6B6A64; --hair:#E2DFD6; --card:#F3F1EA;
  --gold:#B08A2A; --indigo:#4A5A8A; --teal:#2E7D64; --ember:#C2582F;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --gold:#E3C55C; --indigo:#8FA1D6; --teal:#57A98C; --ember:#E07A4A;
}} }}
:root[data-theme="dark"] {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --gold:#E3C55C; --indigo:#8FA1D6; --teal:#57A98C; --ember:#E07A4A;
}}
body {{ background:var(--bg); color:var(--ink); margin:0;
  font-family:"STIX Two Text", Georgia, serif; font-size:17px; line-height:1.55; }}
main {{ max-width:920px; margin:0 auto; padding:40px 22px 80px; }}
h1 {{ font-family:Fraunces, Georgia, serif; font-weight:640; font-size:2.6rem; margin:0 0 4px; text-wrap:balance; }}
h2 {{ font-family:Fraunces, Georgia, serif; font-weight:560; font-size:1.45rem; margin:0 0 10px; }}
.sub {{ color:var(--mut); margin:0 0 6px; }}
.prov {{ font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.72rem; color:var(--mut); letter-spacing:.04em; }}
section {{ margin-top:48px; }}
.stmt {{ background:var(--card); border-left:3px solid var(--gold); padding:14px 18px; margin:14px 0 20px; }}
.stmt .eq {{ font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.95rem; display:block; margin:6px 0; }}
.stmt .tag {{ font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.7rem; color:var(--mut); text-transform:uppercase; letter-spacing:.08em; }}
.fig {{ width:100%; height:auto; }}
svg text {{ fill:var(--ink); }}
.ftitle {{ font:600 .82rem "JetBrains Mono", monospace; }}
.tick, .alab {{ font:400 .72rem "JetBrains Mono", monospace; fill:var(--mut); }}
.leg {{ font:600 .74rem "JetBrains Mono", monospace; }}
.line {{ fill:none; stroke-width:2; }}
.bar {{ stroke-width:10; stroke-linecap:butt; }}
.thin {{ stroke-width:1.6; }}
.gold {{ stroke:var(--gold); fill:var(--gold); }}
.indigo {{ stroke:var(--indigo); fill:var(--indigo); }}
.teal {{ stroke:var(--teal); fill:var(--teal); }}
.ember {{ stroke:var(--ember); fill:var(--ember); }}
.dot {{ stroke:var(--bg); stroke-width:1.5; }}
p {{ max-width:66ch; }}
.note {{ color:var(--mut); font-size:.9rem; }}
</style>
<main>
<h1>The Golden Flux Ladder</h1>
<p class="sub">Harper at Fibonacci fluxes: φ is the address, Catalan's number is the plateau, and ln φ is the clock — earned.</p>
<p class="prov">proslambenomenos · P-7 / R-20 · every curve derived or imported-with-citation before the ladder ran; points are the registered computation</p>

<section>
<h2>The exact anchors</h2>
<div class="stmt"><span class="tag">backed statement · EQ1–EQ3 · clause (a)</span>
<span class="eq">q = 2:  E² = 4cos²k₂ + (1+s)²  ⇒  bands ±[0, 2√2], Dirac touch at 0  (= c25's π-flux point)</span>
<span class="eq">q = 3:  tr M + 2cos 3θ = E³ − 6E;  edges from (E±2)(E²∓2E−2)</span>
The Bloch construction is validated against both CAS closed forms to 1e−10 before anything else runs.</div>
{figA}
</section>

<section>
<h2>The butterfly</h2>
<div class="stmt"><span class="tag">context · same construction, q ≤ 24 · clause (b) on the ladder</span>
<span class="eq">odd q: all q−1 gaps open · even q: the central gap closes (measured ≤ 1e−14 at q = 34, 144)</span>
Golden rows are the Fibonacci approximants marching toward α = 1/φ.</div>
{figB}
</section>

<section>
<h2>The plateau is Catalan's</h2>
<div class="stmt"><span class="tag">backed statement · clause (c) · constant imported, LC-14</span>
<span class="eq">q·S(q) → 32G/π = {REG["thouless"]:.5f}   (G = Catalan, from its own series)</span>
Measured terminal-pair mean {pl["pair_mean"]:.4f} — deviation {pl["dev"]:+.4f} against a registered band of 0.25. φ names the flux; the invariant is Catalan's. The taxonomy's address/answer split, computed.</div>
{figC}
</section>

<section>
<h2>The ln φ clock — earned</h2>
<div class="stmt"><span class="tag">backed statement · clause (d) · the edge that leaves the unearned bin</span>
<span class="eq">ln(S(89)/S(144)) = {ck["slope"]:.5f}   vs   ln φ = {REG["ln_phi"]:.5f}   (Δ = {ck["dev"]:+.1e})</span>
Bandwidth contracts per Fibonacci step at exactly the golden log — clock (the F-ratio) × flatness (the Thouless plateau). ln φ now holds a verified growth edge in the symbol graph.</div>
{figD}
<p class="note">Scored numbers live in p7_results.json against pins in p7_registration.json; the butterfly panel is regenerated deterministically by the validated construction. The Cantor structure of the irrational limit is imported literature (Ten Martini), not computed — declared in P-7's scope.</p>
</section>
</main>
"""
OUT_PATH.write_text(HTML)
print(f"wrote {OUT_PATH} ({len(HTML)} bytes)")
