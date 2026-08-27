#!/usr/bin/env python3
"""Render the P-24 memory-hierarchy figures as a self-contained HTML
page (stdlib only). Every figure is tied to a backed statement:
scored numbers come from p24_registration.json / p24_results.json;
illustrative traces are regenerated deterministically and labeled as
such. Output: p24_plots.html (published as an artifact)."""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p24_registration.json").read_text())
RES = json.loads((HERE / "p24_results.json").read_text())
OUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p24_plots.html"
K = REG["K"]
EPS = REG["eps2"]


# ---------- shared physics helpers (closed forms only) ----------
def mfpt(D, n=1500):
    hy = math.pi / n
    U = lambda x: -(EPS / 2) * math.cos(2 * x) / D   # noqa: E731
    ys = [-math.pi / 2 + j * hy for j in range(n + 1)]
    emu = [math.exp(-U(y)) for y in ys]
    cum = [0.0]
    for j in range(n):
        cum.append(cum[-1] + 0.5 * (emu[j] + emu[j + 1]) * hy)
    def inner(xv):
        j = (xv + math.pi / 2) / hy
        j0 = min(int(j), n - 1)
        return cum[j0] + (j - j0) * (cum[j0 + 1] - cum[j0])
    nx = n // 2
    hx = (math.pi / 2) / nx
    tot = 0.0
    for i in range(nx + 1):
        w = 0.5 if i in (0, nx) else 1.0
        tot += w * math.exp(U(i * hx)) * inner(i * hx)
    return tot * hx / D


def E_delta(Delta, N):
    return K * (1 - math.cos(Delta)) + K * (N - 1) * (1 - math.cos((2 * math.pi - Delta) / (N - 1)))


def E1(N):
    return N * K * (1 - math.cos(2 * math.pi / N))


def dstar(N):
    return math.pi * (N - 3) / (N - 2)


def barrier(N):
    return E_delta(dstar(N), N) - E1(N)


def _jacobi_eigs(A, sweeps=400):
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(sweeps):
        off = max((abs(a[i][j]), i, j) for i in range(n) for j in range(i + 1, n))
        if off[0] < 1e-12:
            break
        _, p, q = off
        th = math.pi / 4 if a[p][p] == a[q][q] else \
            0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(th), math.sin(th)
        for k in range(n):
            apk, aqk = a[p][k], a[q][k]
            a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
        for k in range(n):
            akp, akq = a[k][p], a[k][q]
            a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
    return sorted(a[i][i] for i in range(n))


def _hessian(bonds):
    n = len(bonds)
    c = [K * math.cos(b) for b in bonds]
    H = [[0.0] * n for _ in range(n)]
    for j in range(n):
        i, ip = j, (j + 1) % n
        H[i][i] += c[j]
        H[ip][ip] += c[j]
        H[i][ip] -= c[j]
        H[ip][i] -= c[j]
    return H


_PREF_CACHE = {}


def langer_pref(N):
    """Full Langer prefactor, same construction as p24_derive EQ4."""
    if N in _PREF_CACHE:
        return _PREF_CACHE[N]
    lmin = _jacobi_eigs(_hessian([2 * math.pi / N] * N))
    ds = dstar(N)
    lsad = _jacobi_eigs(_hessian([ds] + [(2 * math.pi - ds) / (N - 1)] * (N - 1)))
    lmin_nz = [x for x in lmin if abs(x) > 1e-9]
    lam_u = -[x for x in lsad if x < -1e-9][0]
    lsad_nz = [x for x in lsad if abs(x) > 1e-9 and x > 0]
    logdet = sum(map(math.log, lmin_nz)) - sum(map(math.log, lsad_nz)) - math.log(lam_u)
    _PREF_CACHE[N] = N * (lam_u / (2 * math.pi)) * math.exp(0.5 * logdet)
    return _PREF_CACHE[N]


def langer_tau(N, D):
    return 1.0 / (langer_pref(N) * math.exp(-barrier(N) / D))


# ---------- svg helpers ----------
def plot(series, W=860, H=320, title="", xl="", yl="", logy=False,
         pad=(64, 16, 44, 22), yfmt="{:.2f}", xfmt="{:.2f}"):
    L, R, B, Tp = pad
    def ty(v):
        return math.log10(v) if logy else v
    xs = [x for s in series for x, _ in s["pts"]]
    ys = [ty(y) for s in series for _, y in s["pts"] if (not logy) or y > 0]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    if y1 - y0 < 1e-12:
        y0, y1 = y0 - 0.5, y1 + 0.5
    y0, y1 = y0 - 0.06 * (y1 - y0), y1 + 0.06 * (y1 - y0)
    X = lambda x: L + (x - x0) / (x1 - x0) * (W - L - R)      # noqa: E731
    Y = lambda y: Tp + (y1 - ty(y)) / (y1 - y0) * (H - Tp - B)  # noqa: E731
    o = [f'<svg viewBox="0 0 {W} {H}" class="fig" role="img" aria-label="{title}">']
    if title:
        o.append(f'<text x="{L}" y="{Tp - 6}" class="ftitle">{title}</text>')
    for k in range(5):
        yy = y0 + (y1 - y0) * k / 4
        ypix = Tp + (y1 - yy) / (y1 - y0) * (H - Tp - B)
        o.append(f'<line x1="{L}" x2="{W - R}" y1="{ypix:.1f}" y2="{ypix:.1f}" class="grid"/>')
        lab = yfmt.format(10 ** yy if logy else yy)
        o.append(f'<text x="{L - 8}" y="{ypix + 4:.1f}" class="tick" text-anchor="end">{lab}</text>')
        xx = x0 + (x1 - x0) * k / 4
        o.append(f'<text x="{X(xx):.1f}" y="{H - B + 18}" class="tick" text-anchor="middle">{xfmt.format(xx)}</text>')
    o.append(f'<line x1="{L}" x2="{W - R}" y1="{H - B}" y2="{H - B}" class="axis"/>')
    o.append(f'<line x1="{L}" x2="{L}" y1="{Tp}" y2="{H - B}" class="axis"/>')
    for s in series:
        pts = [(x, y) for x, y in s["pts"] if (not logy) or y > 0]
        if s.get("dots"):
            for x, y in pts:
                o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4.5" class="{s["cls"]} dot"/>')
                if s.get("err"):
                    e = s["err"]
                    o.append(f'<line x1="{X(x):.1f}" x2="{X(x):.1f}" y1="{Y(max(y - e, 1e-12)):.1f}" y2="{Y(y + e):.1f}" class="{s["cls"]} ebar"/>')
        else:
            p = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts)
            dash = ' stroke-dasharray="6 5"' if s.get("dash") else ""
            o.append(f'<polyline points="{p}" class="{s["cls"]} line"{dash}/>')
    for i, s in enumerate(series):
        if s.get("label"):
            o.append(f'<text x="{W - R - 8}" y="{Tp + 18 + 17 * i}" class="leg {s["cls"]}" text-anchor="end">{s["label"]}</text>')
    o.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 4}" class="alab" text-anchor="middle">{xl}</text>')
    o.append(f'<text x="16" y="{(Tp + H - B) / 2:.0f}" class="alab" transform="rotate(-90 16 {(Tp + H - B) / 2:.0f})" text-anchor="middle">{yl}</text>')
    o.append('</svg>')
    return "".join(o)


def ring_svg(bonds, label, cls, W=250, H=250):
    """Draw N phases as arrows on a circle; bonds = list of successive
    phase differences (site phase = cumulative sum)."""
    N = len(bonds)
    cx, cy, Rr, ar = W / 2, H / 2 - 6, W / 2 - 34, 13
    o = [f'<svg viewBox="0 0 {W} {H}" class="ringfig" role="img" aria-label="{label}">']
    phase = 0.0
    for i in range(N):
        a = 2 * math.pi * i / N - math.pi / 2
        x, y = cx + Rr * math.cos(a), cy + Rr * math.sin(a)
        dx, dy = math.cos(phase), math.sin(phase)
        o.append(f'<line x1="{x - ar * dx:.1f}" y1="{y - ar * dy:.1f}" x2="{x + ar * dx:.1f}" y2="{y + ar * dy:.1f}" class="{cls} arrow"/>')
        o.append(f'<circle cx="{x + ar * dx:.1f}" cy="{y + ar * dy:.1f}" r="2.6" class="{cls} tip"/>')
        phase += bonds[i]
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{Rr}" class="ringpath"/>')
    o.append(f'<text x="{cx}" y="{H - 6}" class="rlab" text-anchor="middle">{label}</text>')
    o.append('</svg>')
    return "".join(o)


# ---------- figure 1: rung 1 ----------
D1 = REG["rung1"]["D"]
rng = random.Random(4711)
traces = []
for _ in range(5):
    th, tr = 0.0, [(0.0, 0.0)]
    for i in range(400):
        th += math.sqrt(2 * D1 * 0.01) * rng.gauss(0, 1)
        tr.append(((i + 1) * 0.01, th))
    traces.append({"pts": tr, "cls": "r1faint"})
fig1a = plot(traces, W=420, H=300, title="phase trajectories (illustrative, D = 0.5)",
             xl="t", yl="θ(t)", yfmt="{:.1f}")
curve = {"pts": [(t / 50, math.exp(-D1 * t / 50)) for t in range(1, 220)],
         "cls": "ink", "label": "e^{−Dt}  (derived, EQ1)"}
meas = {"pts": [(float(t), RES["detail"]["rung1"][t]["C"]) for t in RES["detail"]["rung1"]],
        "cls": "r1", "dots": True, "label": "ensemble ⟨cos θ⟩ (measured)",
        "err": max(RES["detail"]["rung1"][t]["band"] for t in RES["detail"]["rung1"]) / 2}
fig1b = plot([curve, meas], W=420, H=300, logy=True,
             title="memory decay", xl="t", yl="C(t)", yfmt="{:.2f}")

# ---------- figure 2: rung 2 ----------
pot = {"pts": [(x / 100, -(EPS / 2) * math.cos(2 * x / 100)) for x in range(-314, 315)],
       "cls": "r2", "label": "U(θ) = −(ε/2)cos 2θ"}
fig2a = plot([pot], W=420, H=280, title="the locked bit: two wells, barrier = ε (EQ2)",
             xl="θ", yl="U", yfmt="{:.2f}", xfmt="{:.1f}")
rng = random.Random(4712)
th, well, tel = 0.0, 0, [(0.0, 0)]
Dtel = 0.28
for i in range(600000):
    th += (-EPS * math.sin(2 * th)) * 0.004 + math.sqrt(2 * Dtel * 0.004) * rng.gauss(0, 1)
    w = round(th / math.pi)
    if w != well and abs(th - math.pi * w) < math.pi / 4:
        well = w
    if i % 300 == 0:
        tel.append((i * 0.004, well))
fig2b = plot([{"pts": tel, "cls": "r2", "label": "well index (illustrative, D = 0.28)"}],
             W=420, H=280, title="the telegraph", xl="t", yl="stored value",
             yfmt="{:.0f}", xfmt="{:.0f}")
Ds = [0.18 + 0.02 * i for i in range(8)]
arr_curve = {"pts": [(1 / d, mfpt(d)) for d in Ds], "cls": "ink",
             "label": "exact MFPT quadrature"}
arr_pins = {"pts": [(1 / float(d), REG["tau2_pin"][d]) for d in REG["tau2_pin"]],
            "cls": "r2", "dots": True, "label": "pinned τ₂ (registered)"}
arr_meas = {"pts": [(1 / float(d), REG["T2"] / RES["detail"]["rung2"][d]["hops"])
                    for d in REG["D2_ladder"] for d in [str(d)]],
            "cls": "r2b", "dots": True, "label": "measured T/N_hops"}
fig2c = plot([arr_curve, arr_pins, arr_meas], W=860, H=300, logy=True,
             title="Arrhenius: lifetime vs 1/D — slope is the CAS barrier ε (clause b)",
             xl="1/D", yl="τ₂", yfmt="{:.0f}", xfmt="{:.1f}")

# ---------- figure 3: rung 3 ----------
N3 = 16
rings = (
    ring_svg([2 * math.pi / N3] * N3, "w = 1 (uniform twist)", "r3"),
    ring_svg([dstar(N3)] + [(2 * math.pi - dstar(N3)) / (N3 - 1)] * (N3 - 1),
             "the saddle: one bond at Δ*", "r3s"),
    ring_svg([0.0] * N3, "w = 0 (forgotten)", "r1faint"),
)
prof = {"pts": [(x / 100, E_delta(x / 100, N3)) for x in range(30, 315)],
        "cls": "r3", "label": "E(Δ) closed form (EQ3)"}
marks = {"pts": [(2 * math.pi / N3, E1(N3)), (dstar(N3), E_delta(dstar(N3), N3))],
         "cls": "r3s", "dots": True, "label": "minimum · saddle"}
fig3b = plot([prof, marks], W=420, H=300, title=f"the unwinding path, N = {N3}",
             xl="clamped bond Δ", yl="E", yfmt="{:.1f}", xfmt="{:.1f}")
bar_curve = {"pts": [(n, barrier(n)) for n in range(4, 65)], "cls": "r3",
             "label": "ΔE(N) closed form"}
asym = {"pts": [(4, 2 * K), (64, 2 * K)], "cls": "ink", "dash": True,
        "label": "2K saturation (EQ5)"}
cells = {"pts": [(int(k.split('_')[0]), barrier(int(k.split('_')[0])))
                 for k in REG["rate_pin"]], "cls": "r3s", "dots": True,
         "label": "registered cells"}
fig3c = plot([bar_curve, asym, cells], W=420, H=300,
             title="no extensive protection", xl="N", yl="barrier ΔE",
             yfmt="{:.1f}", xfmt="{:.0f}")

# ---------- figure 4: the hierarchy ----------
inv = [1 / (0.12 + 0.02 * i) for i in range(18)]
h_series = [
    {"pts": [(x, x) for x in inv], "cls": "r1", "label": "rung 1: τ = 1/D"},
    {"pts": [(x, mfpt(1 / x)) for x in inv], "cls": "r2", "label": "rung 2: exact MFPT (ε = 1)"},
]
for n, cls in ((8, "r3a"), (16, "r3"), (32, "r3b")):
    h_series.append({"pts": [(x, langer_tau(n, 1 / x)) for x in inv],
                     "cls": cls, "label": f"rung 3: Langer, N = {n}"})
mpts = []
for k, v in RES["detail"]["rung3"].items():
    if "_" in k and not k.startswith("ratio"):
        n, d = k.split("_")
        mpts.append((1 / float(d), 1.0 / v["rate"]))
h_series.append({"pts": mpts, "cls": "r3s", "dots": True, "label": "measured escape times"})
m2 = [(1 / float(d), REG["T2"] / RES["detail"]["rung2"][str(d)]["hops"]) for d in REG["D2_ladder"]]
h_series.append({"pts": m2, "cls": "r2b", "dots": True, "label": "measured τ₂"})
fig4 = plot(h_series, W=860, H=420, logy=True,
            title="the memory hierarchy (clauses a–d): every curve derived before any point was measured",
            xl="1/D", yl="lifetime τ", yfmt="{:.0f}", xfmt="{:.1f}")
tauN_16 = {"pts": [(n, langer_tau(n, 0.16)) for n in range(6, 65, 2)],
           "cls": "r3", "label": "D = 0.16 (derived)"}
tauN_06 = {"pts": [(n, langer_tau(n, 0.6)) for n in range(6, 65, 2)],
           "cls": "r1", "label": "D = 0.6 (derived: inverted)"}
mN = {"pts": [(8, 1 / RES["detail"]["rung3"]["8_0.16"]["rate"]),
              (16, 1 / RES["detail"]["rung3"]["16_0.16"]["rate"])],
      "cls": "r3s", "dots": True, "label": "measured (D = 0.16)"}
fig5 = plot([tauN_16, tauN_06, mN], W=860, H=320, logy=True,
            title="size helps, then hurts: the derived crossover (EQ5, clause d)",
            xl="ring size N", yl="τ₃", yfmt="{:.0f}", xfmt="{:.0f}")

o = RES["detail"]["order"]
r3 = RES["detail"]["rung3"]

HTML = f"""<title>How Substrates Forget</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,640&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root {{
  --bg:#FBFAF7; --ink:#1F242A; --mut:#6B6A64; --hair:#E2DFD6; --card:#F3F1EA;
  --r1:#5B7A99; --r2:#C2582F; --r2b:#8C3D1E; --r3:#2E7D64; --r3a:#7FAF9B;
  --r3b:#174F3D; --r3s:#B08A2A;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --r1:#7FA3C4; --r2:#E07A4A; --r2b:#F0A985; --r3:#57A98C; --r3a:#3E7A64;
  --r3b:#8FD3BA; --r3s:#D4B054;
}} }}
:root[data-theme="dark"] {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --r1:#7FA3C4; --r2:#E07A4A; --r2b:#F0A985; --r3:#57A98C; --r3a:#3E7A64;
  --r3b:#8FD3BA; --r3s:#D4B054;
}}
body {{ background:var(--bg); color:var(--ink); margin:0;
  font-family:"STIX Two Text", Georgia, serif; font-size:17px; line-height:1.55; }}
main {{ max-width:920px; margin:0 auto; padding:40px 22px 80px; }}
h1 {{ font-family:Fraunces, Georgia, serif; font-weight:640; font-size:2.6rem;
  margin:0 0 4px; text-wrap:balance; }}
h2 {{ font-family:Fraunces, Georgia, serif; font-weight:560; font-size:1.45rem;
  margin:0 0 10px; }}
.sub {{ color:var(--mut); margin:0 0 6px; }}
.prov {{ font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.72rem;
  color:var(--mut); letter-spacing:.04em; }}
section {{ margin-top:52px; }}
.stmt {{ background:var(--card); border-left:3px solid var(--rc, var(--ink));
  padding:14px 18px; margin:14px 0 20px; }}
.stmt .eq {{ font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.95rem;
  display:block; margin:6px 0; }}
.stmt .tag {{ font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.7rem;
  color:var(--mut); text-transform:uppercase; letter-spacing:.08em; }}
.row {{ display:flex; gap:16px; flex-wrap:wrap; }}
.row > svg {{ flex:1 1 380px; }}
.fig, .ringfig {{ width:100%; height:auto; }}
svg text {{ fill:var(--ink); }}
.ftitle {{ font:600 .82rem "JetBrains Mono", monospace; }}
.tick, .alab, .rlab {{ font:400 .72rem "JetBrains Mono", monospace; fill:var(--mut); }}
.leg {{ font:600 .74rem "JetBrains Mono", monospace; }}
.grid {{ stroke:var(--hair); stroke-width:1; }}
.axis {{ stroke:var(--mut); stroke-width:1.2; fill:none; }}
.line {{ fill:none; stroke-width:2.2; }}
.ink {{ stroke:var(--ink); fill:var(--ink); }}
.r1 {{ stroke:var(--r1); fill:var(--r1); }} .r1faint {{ stroke:var(--r1); fill:var(--r1); opacity:.45; }}
.r2 {{ stroke:var(--r2); fill:var(--r2); }} .r2b {{ stroke:var(--r2b); fill:var(--r2b); }}
.r3 {{ stroke:var(--r3); fill:var(--r3); }} .r3a {{ stroke:var(--r3a); fill:var(--r3a); }}
.r3b {{ stroke:var(--r3b); fill:var(--r3b); }} .r3s {{ stroke:var(--r3s); fill:var(--r3s); }}
.dot {{ stroke:var(--bg); stroke-width:1.5; }}
.ebar {{ stroke-width:1.4; }}
.arrow {{ stroke-width:2.6; }} .tip {{ }}
.ringpath {{ fill:none; stroke:var(--hair); stroke-width:1; }}
.r1sec {{ --rc:var(--r1); }} .r2sec {{ --rc:var(--r2); }} .r3sec {{ --rc:var(--r3); }}
p {{ max-width:66ch; }}
.note {{ color:var(--mut); font-size:.9rem; }}
</style>
<main>
<h1>How Substrates Forget</h1>
<p class="sub">Three classical memories, every lifetime derived before it was measured.</p>
<p class="prov">proslambenomenos · P-24 / R-19 · registered {REG['seeds']} · all curves closed-form or exact quadrature; points are seeded simulations</p>

<section class="r1sec">
<h2>Rung 1 — the untended phase</h2>
<div class="stmt"><span class="tag">backed statement · EQ1 · clause (a)</span>
<span class="eq">dθ = √(2D) dW  ⇒  ⟨cos θ(t)⟩ = e^(−Dt),  τ₁ = 1/D</span>
cos θ is the eigenfunction of the diffusion generator with eigenvalue −1 (CAS-checked); nothing tends the phase, so memory leaks at the bare noise rate.</div>
<div class="row">{fig1a}{fig1b}</div>
</section>

<section class="r2sec">
<h2>Rung 2 — the locked bit</h2>
<div class="stmt"><span class="tag">backed statement · EQ2 · clause (b)</span>
<span class="eq">dθ = −ε sin(2θ) dt + √(2D) dW  ⇒  C(t) = e^(−2rt),  r = 1/(2·T_MFPT),  barrier = ε exactly</span>
The P-22 doublet as a memory element: two locked phases π apart, hop rate from exact first-passage quadrature — a flip-flop priced from first principles.</div>
<div class="row">{fig2a}{fig2b}</div>
{fig2c}
</section>

<section class="r3sec">
<h2>Rung 3 — the winding number</h2>
<div class="stmt"><span class="tag">backed statement · EQ3–EQ5 · clauses (c), (d)</span>
<span class="eq">E(Δ) = K(1−cos Δ) + K(N−1)(1−cos((2π−Δ)/(N−1))),  Δ* = π(N−3)/(N−2)</span>
<span class="eq">ΔE(N) = E(Δ*) − NK(1−cos(2π/N)) ↑ 2K,   rate = N·(λᵤ/2π)·√(det′H_min/|det′H_saddle|)·e^(−ΔE/D)</span>
The saddle is analytic: clamp one bond, the rest relax uniform. The barrier grows with N only because the twisted state's own strain relaxes — it saturates at 2K. Classical 1D topology buys no extensive protection; a chat-level guess to the contrary died at EQ5, pre-registration.</div>
<div class="row">{rings[0]}{rings[1]}{rings[2]}</div>
<div class="row">{fig3b}{fig3c}</div>
</section>

<section>
<h2>The hierarchy</h2>
<div class="stmt"><span class="tag">backed statement · clauses (a)–(d) · R-19</span>
<span class="eq">τ₁ = 1/D   ≪   τ₂ ~ e^(ε/D)   ~   τ₃(N) = e^(ΔE(N)/D)/(N·prefactor),  ΔE(N) ↑ 2K</span>
Measured escape times: N=8: {1/r3['8_0.16']['rate']:.0f} vs Langer {1/r3['8_0.16']['langer']:.0f}; N=16: {1/r3['16_0.16']['rate']:.0f} vs {1/r3['16_0.16']['langer']:.0f} (D=0.16). Size ratio measured {o['measured_ratio']:.1f}× against derived {o['derived_ratio']:.1f}×. At D=0.6 the derived ordering inverts (τ₃₂/τ₈ = {REG['crossover_check']['tau32_over_tau8_D06']:.2f}).</div>
{fig4}
{fig5}
<p class="note">Illustrative traces are regenerated deterministically by p24_plots.py and are not scored; every scored number lives in p24_results.json against pins in p24_registration.json. Electron clouds are out of scope for this classical line, by declaration.</p>
</section>
</main>
"""
OUT_PATH.write_text(HTML)
print(f"wrote {OUT_PATH} ({len(HTML)} bytes)")
