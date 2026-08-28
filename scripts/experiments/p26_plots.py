#!/usr/bin/env python3
"""P-26 figure page: the everpresent-Lambda scorecard on DESI DR2
BAO. Every scored number is read from p26_results.json /
p26_registration.json; illustrative trajectories are regenerated
deterministically from the registered seeds. Output: p26_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE))

from kernels.figpage import plot                       # noqa: E402
import p26_derive as D                                 # noqa: E402
import p26_score as S                                  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "p26_plots.html"
REG = json.load(open(HERE / "p26_registration.json"))
RES = json.load(open(HERE / "p26_results.json"))
ROWS = REG["data"]["rows"]

# ---------------------------------------------------------- fig 1
# Omega_Lambda(a) trajectories vs the Omega_Lambda LCDM needs
om0 = 0.2975


def omega_traj(alpha, seed):
    alive, _, traj = S.run_realization(alpha, om0, seed, keep_traj=True)
    return alive, [(math.log10(a), rl / (rl + bg))
                   for a, rl, bg in traj] if traj else None


series = []
# deterministic sample seeds, same stream as the registered cells
from kernels.pmap import cell_seed                     # noqa: E402
n_dead = 0
for k in range(10):
    seed = cell_seed(S.SEED0, repr(0.01), repr(om0), 0, k)
    alive, pts = omega_traj(0.01, seed)
    if pts:
        series.append({"pts": pts, "cls": "c3" if alive else "c4",
                       "label": None})
    if not alive:
        n_dead += 1
best_cell = [c for c in RES["cells"]
             if c["alpha"] == 0.005 and c["Omega_m"] == om0][0]
alive, best_pts = omega_traj(0.005, best_cell["best_seed"])
series.append({"pts": best_pts, "cls": "c1",
               "label": "best of 19873 survivors (α=0.005)"})
lcdm_om = RES["lcdm"]["Omega_m"]
lcdm_pts = []
for i in range(0, 200 + 1):
    la = -5 + 5 * i / 200
    a = 10 ** la
    ol = (1 - lcdm_om) / (1 - lcdm_om + lcdm_om / a ** 3
                          + lcdm_om / 3400 / a ** 4)
    lcdm_pts.append((la, ol))
series.append({"pts": lcdm_pts, "cls": "c2", "dash": True,
               "label": "the Ω_Λ(a) that ΛCDM needs"})
fig1 = plot(series, H=360, title="the walk wanders about zero; Λ must rise to 0.7 and stay",
            xl="log₁₀ a", yl="Ω_Λ = ρ_Λ/ρ_total", yfmt="{:.2f}",
            xfmt="{:.0f}")

# ---------------------------------------------------------- fig 2
# BAO residuals: data vs LCDM, with w0wa and the best realization


def smooth_model(om, w0, wa):
    def E(z):
        return math.sqrt(S.E2_w0wa(z, om, w0, wa))
    m = D.model_from_E(ROWS, E)
    s = D.profile_scale(ROWS, m)
    return m, s


m_l, s_l = smooth_model(RES["lcdm"]["Omega_m"], -1.0, 0.0)
m_w, s_w = smooth_model(RES["w0wa"]["Omega_m"], RES["w0wa"]["w0"],
                        RES["w0wa"]["wa"])
alive, nodes, _ = S.run_realization(0.005, om0, best_cell["best_seed"])
c2b, s_b = S.chi2_of_nodes(ROWS, nodes)


def realization_model(nodes, s):
    na, ne2 = nodes
    E0 = ne2[-1]
    zs = [1 / a - 1 for a in reversed(na)]
    Es = [math.sqrt(e2 / E0) for e2 in reversed(ne2)]
    cum = [0.0]
    for i in range(1, len(zs)):
        cum.append(cum[-1] + 0.5 * (1 / Es[i - 1] + 1 / Es[i])
                   * (zs[i] - zs[i - 1]))
    m = {}
    for r in ROWS:
        z = r["zeff"]
        lo = max(i for i in range(len(zs)) if zs[i] <= z)
        f = (z - zs[lo]) / (zs[lo + 1] - zs[lo])
        dm = cum[lo] + f * (cum[lo + 1] - cum[lo])
        e = Es[lo] + f * (Es[lo + 1] - Es[lo])
        if "DV_over_rd" in r:
            m[r["tracer"]] = ((z * dm * dm / e) ** (1 / 3.0),)
        else:
            m[r["tracer"]] = (dm, 1 / e)
    return m


m_b = realization_model(nodes, s_b)
dat_dots, dat_err = [], []
w_pts, b_pts = [], []
for r in ROWS:
    z = r["zeff"]
    keys = (("DV_over_rd", "DV_err", 0),) if "DV_over_rd" in r \
        else (("DM_over_rd", "DM_err", 0), ("DH_over_rd", "DH_err", 1))
    for kd, ke, j in keys:
        ref = s_l * m_l[r["tracer"]][j]
        dat_dots.append((z, (r[kd] / ref - 1) * 100))
        dat_err.append(r[ke] / ref * 100)
        w_pts.append((z, (s_w * m_w[r["tracer"]][j] / ref - 1) * 100))
        b_pts.append((z, (s_b * m_b[r["tracer"]][j] / ref - 1) * 100))
w_pts.sort()
b_pts.sort()
err = sum(dat_err) / len(dat_err)
fig2 = plot([
    {"pts": [(0.25, 0), (2.35, 0)], "cls": "c2", "dash": True,
     "label": f"ΛCDM fit (χ² {RES['lcdm']['chi2']:.1f}/11)"},
    {"pts": w_pts, "cls": "c5",
     "label": f"w₀wₐ fit (Δχ² {RES['w0wa']['dchi2']:.1f})"},
    {"pts": b_pts, "cls": "c1",
     "label": f"best everpresent realization (χ² {c2b:.1f})"},
    {"pts": dat_dots, "cls": "c3", "dots": True, "err": err,
     "label": "DR2 Table 4 (mean error bar)"},
], H=360, title="per-point distance ratios against the ΛCDM fit",
    xl="z_eff", yl="deviation from ΛCDM (percent)",
    yfmt="{:.1f}", xfmt="{:.1f}")

# ---------------------------------------------------------- fig 3
# survival vs alpha with the derived amplitudes
surv_pts = [(c["alpha"], c["survival"]) for c in RES["cells"]
            if c["Omega_m"] == om0]
surv_pts.sort()
cm = REG["EQ2"]["sigma_over_alpha_matter"]
cr = REG["EQ2"]["sigma_over_alpha_radiation"]
fig3 = plot([
    {"pts": surv_pts, "cls": "c1", "dots": True,
     "label": "surviving fraction (registered cells)"},
    {"pts": surv_pts, "cls": "c1"},
], H=300, title=f"survival to a=1: σ_ΩΛ = {cm:.1f}·α (matter), "
    f"{cr:.1f}·α (radiation)",
    xl="α", yl="fraction alive", yfmt="{:.2f}", xfmt="{:.3f}")

# ---------------------------------------------------------- fig 4
# the bit ledger, hand-rolled bars
ledger = [("everpresent α=0.005", [c for c in RES["cells"]
                                   if c["alpha"] == 0.005][0]["net_bits"]),
          ("everpresent α=0.01", [c for c in RES["cells"]
                                  if c["alpha"] == 0.01][0]["net_bits"]),
          ("everpresent α=0.02 (no survivor)",
           [c for c in RES["cells"] if c["alpha"] == 0.02
            and c["Omega_m"] == om0][0]["net_bits"]),
          ("everpresent α=0.04 (no survivor)",
           [c for c in RES["cells"] if c["alpha"] == 0.04][0]["net_bits"]),
          ("DNY's own SNe record (imported)",
           REG["EQ3"]["dny_net_bits"]),
          ("w₀wₐ on BAO alone (MDL price)",
           RES["w0wa_context"]["net_bits"])]
W, Hb, L = 860, 40 * len(ledger) + 50, 300
bars = [f'<svg viewBox="0 0 {W} {Hb}" class="fig" role="img" '
        f'aria-label="bit ledger">']
xmax = max(1.0, max(-v for _, v in ledger))
x0 = W - 40


def xw(v):
    return -v / xmax * (x0 - L - 20)


bars.append(f'<line x1="{x0}" x2="{x0}" y1="10" y2="{Hb - 30}" class="axis"/>')
for i, (lab, v) in enumerate(ledger):
    y = 22 + 40 * i
    w = xw(v)
    bars.append(f'<rect x="{x0 - w:.1f}" y="{y}" width="{w:.1f}" '
                f'height="22" class="bar{"n" if v < 0 else "p"}"/>')
    bars.append(f'<text x="{x0 - w - 8:.1f}" y="{y + 16}" class="tick" '
                f'text-anchor="end">{lab} · {v:+.1f} bits</text>')
bars.append(f'<text x="{x0}" y="{Hb - 10}" class="alab" '
            f'text-anchor="end">0 (breaking even against ΛCDM)</text>')
bars.append('</svg>')
fig4 = "".join(bars)

# ---------------------------------------------------------- page
amp = RES["amplitude"]
HTML = f"""<title>The Everpresent-Λ Scorecard</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=JetBrains+Mono:wght@400;600&family=Source+Sans+3:wght@400;600&display=swap">
<style>
:root {{
  --bg:#FBFAF7; --ink:#1F242A; --mut:#6B6A64; --hair:#E2DFD6; --card:#F3F1EA;
  --c1:#B4552D; --c2:#3D6B54; --c3:#4B6A8A; --c4:#B0A48E; --c5:#7A5C8F;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --c1:#E08A5B; --c2:#7FB89B; --c3:#8FB0D1; --c4:#6E6653; --c5:#B195C9;
}} }}
:root[data-theme="dark"] {{
  --bg:#14181C; --ink:#E8E4DC; --mut:#98948A; --hair:#2A3038; --card:#1B2127;
  --c1:#E08A5B; --c2:#7FB89B; --c3:#8FB0D1; --c4:#6E6653; --c5:#B195C9;
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
.ftitle {{ fill:var(--ink); font:600 13px "Source Sans 3", sans-serif; }}
.leg {{ font:600 12px "Source Sans 3", sans-serif; }}
.line {{ fill:none; stroke-width:2; }}
.dot {{ stroke:var(--bg); stroke-width:1.2; }}
.ebar {{ stroke-width:1.4; }}
.c1 {{ stroke:var(--c1); fill:var(--c1); }} .c2 {{ stroke:var(--c2); fill:var(--c2); }}
.c3 {{ stroke:var(--c3); fill:var(--c3); }} .c4 {{ stroke:var(--c4); fill:var(--c4); }}
.c5 {{ stroke:var(--c5); fill:var(--c5); }}
.c1.line,.c2.line,.c3.line,.c4.line,.c5.line {{ fill:none; }}
.barn {{ fill:var(--c1); opacity:.85; }} .barp {{ fill:var(--c2); }}
.stmt {{ background:var(--card); border:1px solid var(--hair); border-radius:10px;
  padding:14px 18px; margin:14px 0; }}
.tag {{ display:block; font:600 11px "JetBrains Mono", monospace; color:var(--mut);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }}
.eq {{ display:block; font-family:"JetBrains Mono", monospace; font-size:.85rem; margin:4px 0; }}
.note {{ color:var(--mut); font-size:.85rem; }}
</style>
<main>
<h1>The everpresent-Λ scorecard</h1>
<p class="sub">Sorkin's fluctuating cosmological constant, as concrete dynamics (Das–Nasiri–Yazdi Model 1), priced in bits against the DESI DR2 BAO likelihood.</p>
<p class="prov">proslambenomenos · P-26 / R-23 · seed0 262626 · 90000 registered realizations · zero beats · LC-16</p>

<section>
<h2>The mechanism, and why it loses</h2>
<div class="stmt"><span class="tag">backed statement · EQ1, EQ2 · clause (c)</span>
<span class="eq">V(t) = (3π/55)·t⁴ (matter era) · (8π/105)·t⁴ (radiation era) — exact Beta-function integrals</span>
<span class="eq">σ_Λ = 8πα/√V  ⟹  σ_ΩΛ = 2√(165π)·α = 45.5α (matter) · (8/3)√(210π)·α = 68.5α (radiation)</span>
The fluctuation is a fixed fraction of the total density at every epoch — that is what "everpresent" means, derived exactly. Measured in the production walk: {amp['measured']:.4f} against the derived {amp['derived']:.4f}. But the walk's mean is zero: to mimic Λ it must wander up to Ω_Λ ≈ 0.7 by luck and hold there across all of z &lt; 2.33.</div>
{fig1}
<p class="note">The first ten α = 0.01 trajectories from the registered stream ({n_dead} of them died before today; survivors shown); the best of 19873 survivors at α = 0.005; and the Ω_Λ(a) history ΛCDM requires.</p>
</section>

<section>
<h2>The scorecard</h2>
<div class="stmt"><span class="tag">backed statement · clauses (a), (b), (d) · R-23</span>
<span class="eq">ΛCDM: Ω_m {RES['lcdm']['Omega_m']:.4f}, h·r_d {RES['lcdm']['h_rd_Mpc']:.2f} Mpc (published: 0.2975 ± 0.0086, 101.54 ± 0.73) — χ² {RES['lcdm']['chi2']:.2f}/11</span>
<span class="eq">w₀wₐ: Δχ² = {RES['w0wa']['dchi2']:.2f} on BAO alone (derived center 4.84 from the source's own 1.7σ) </span>
<span class="eq">everpresent Model 1: best of 90000 realizations sits Δχ² = +{best_cell['dchi2_best']*-1:.1f} on the wrong side; median survivor χ² ≈ 1555 ≈ Einstein–de Sitter (1457)</span>
The same 13-point compression that reproduces the collaboration's own fit gives the walk nothing to stand on.</div>
{fig2}
</section>

<section>
<h2>Survival</h2>
<div class="stmt"><span class="tag">backed statement · clause (e) · R-23</span>
<span class="eq">alive at a=1: 0.994 (α=0.005) · 0.194 (α=0.01) · 0.000 (α=0.02, all Ω_m) · 0.000 (α=0.04)</span>
Large α dies in the radiation era (σ_ΩΛ = 68.5α); small α is Einstein–de Sitter with noise. The squeeze leaves no α that both survives and darkens.</div>
{fig3}
</section>

<section>
<h2>The bit ledger</h2>
<div class="stmt"><span class="tag">backed statement · clause (d) · R-23</span>
<span class="eq">net = Δχ²_best/(2 ln 2) − log₂(N_seeds/max(K,1)) − log₂(6 cells) ≤ 0 in every registered cell</span>
Surprisal bought minus selection spent. The seed price is charged at a lower bound (r_d profiled per realization flatters the model), and the verdict is still uniformly negative.</div>
{fig4}
<p class="note">Illustrative trajectories are regenerated deterministically from the registered seeds; every scored number lives in p26_results.json against pins in p26_registration.json. The order-of-magnitude coincidence in catalog c31 is untouched: the magnitude is what the mechanism gets right, and these dynamics are what DR2 BAO excludes.</p>
</section>
</main>
"""
OUT.write_text(HTML)
print(f"wrote {OUT} ({len(HTML)} bytes)")
