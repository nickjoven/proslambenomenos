#!/usr/bin/env python3
"""Render perspectives_plots.html: one object, several perspectives.
Three landed geometries, each drawn from at least two cameras through
kernels/project.py (camera, perspective/orthographic projection,
painter's sort) on the kernels/figpage.py page scaffold:

  (a) ring phase states from P-24/P-6 as closed curves on a torus
      (site position on the ring circle, phase as the fiber angle):
      w = 0, w = 1, and the pinned saddle configuration
      Delta* = pi(N-3)/(N-2) from p24_registration.json;
  (b) the pi-flux Dirac dispersion E = +-2 sqrt(cos^2 kx + cos^2 ky)
      (catalog c25) as a perspective surface with the Dirac points
      visible;
  (c) the Hardy measurement geometry from p21_results.json (the
      optimal state's four measurement directions) on a wireframe
      Bloch sphere.

Numbers come only from committed JSONs (p24_registration.json,
p21_results.json) and the c25 closed form; every surface and curve is
regenerated deterministically - deterministic illustration, not
scored. Output: perspectives_plots.html."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from kernels.figpage import page                                   # noqa: E402
from kernels.project import (camera, painter_sort, polyline_svg,   # noqa: E402
                             project, seg_depth, surface_mesh,
                             surface_svg, wireframe_svg)

P24 = json.loads((HERE / "p24_registration.json").read_text())
P21 = json.loads((HERE / "p21_results.json").read_text())
OUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "perspectives_plots.html"


def fit(cam, pts, W, H, margin=30, mode="persp"):
    """Scale/center so the projected points fill the viewBox."""
    pj = [project(cam, p, mode) for p in pts]
    xs = [p[0] for p in pj]
    ys = [p[1] for p in pj]
    sx = (W - 2 * margin) / (max(xs) - min(xs))
    sy = (H - 2 * margin) / (max(ys) - min(ys))
    s = min(sx, sy)
    cx = W / 2 - s * (max(xs) + min(xs)) / 2
    cy = H / 2 + s * (max(ys) + min(ys)) / 2
    return s, cx, cy


def svg_wrap(body, W, H, label, cap):
    return (f'<svg viewBox="0 0 {W} {H}" class="fig3d" role="img" '
            f'aria-label="{label}">{body}'
            f'<text x="{W / 2:.0f}" y="{H - 8}" class="rlab" '
            f'text-anchor="middle">{cap}</text></svg>')


# ---------------- panel (a): ring phases on the torus ----------------
RT, rt = 2.2, 0.85
N_RING = 16
DSTAR = P24["delta_star"]["16"]


def torus(a, phi):
    return ((RT + rt * math.cos(phi)) * math.cos(a),
            (RT + rt * math.cos(phi)) * math.sin(a),
            rt * math.sin(phi))


def ring_curve(phis, na=240):
    """Closed curve through the site phases, fiber angle interpolated
    linearly between sites (phase graph over the ring)."""
    pts = []
    n = len(phis)
    ext = phis + [phis[0] + 2 * math.pi]     # w = 1 closes after a full fiber turn
    for k in range(na + 1):
        x = k * n / na
        i = min(int(x), n - 1)
        f = x - i
        a = 2 * math.pi * x / n
        pts.append(torus(a, ext[i] + f * (ext[i + 1] - ext[i])))
    return pts


def torus_wire():
    segs = []
    for iu in range(16):                     # tube circles
        a = 2 * math.pi * iu / 16
        ring = [torus(a, 2 * math.pi * k / 24) for k in range(25)]
        segs += list(zip(ring, ring[1:]))
    for iv in range(8):                      # axial circles
        phi = 2 * math.pi * iv / 8
        ring = [torus(2 * math.pi * k / 48, phi) for k in range(49)]
        segs += list(zip(ring, ring[1:]))
    return segs


PH_W1 = [2 * math.pi * i / N_RING for i in range(N_RING)]
PH_W0 = [0.0] * N_RING
rest = (2 * math.pi - DSTAR) / (N_RING - 1)
PH_SAD = [0.0]
for b in [DSTAR] + [rest] * (N_RING - 2):
    PH_SAD.append(PH_SAD[-1] + b)


def curve_w0(na=240):
    return [torus(2 * math.pi * k / na, 0.0) for k in range(na + 1)]


def panel_a(eye, cap, W=430, H=390):
    cam = camera(eye, (0.0, 0.0, 0.0))
    ref = [torus(2 * math.pi * i / 48, 2 * math.pi * j / 12)
           for i in range(48) for j in range(12)]
    s, cx, cy = fit(cam, ref, W, H)
    o = [wireframe_svg(cam, torus_wire(), s, cx, cy, cls="wire")]
    curves = [(curve_w0(), "w0"), (ring_curve(PH_W1), "w1"),
              (ring_curve(PH_SAD), "sad")]
    drawn = []
    for pts, cls in curves:
        pj = [project(cam, p) for p in pts]
        drawn.append((seg_depth(pj), pts, cls))
    for _, pts, cls in painter_sort(drawn, lambda t: t[0]):
        o.append(polyline_svg(cam, pts, s, cx, cy, cls=cls))
    for i in range(N_RING):                  # site markers on the w = 1 curve
        x, y, _ = project(cam, torus(2 * math.pi * i / N_RING, PH_W1[i]))
        o.append(f'<circle cx="{cx + s * x:.1f}" cy="{cy - s * y:.1f}" '
                 f'r="3.2" class="w1 dot"/>')
    return svg_wrap("".join(o), W, H, "ring phases on the torus", cap)


figA1 = panel_a((6.3, -5.2, 3.6), "camera 1: eye (6.3, −5.2, 3.6)")
figA2 = panel_a((0.4, 0.05, 7.8), "camera 2: eye (0.4, 0.05, 7.8), top-down")

# ---------------- panel (b): the pi-flux Dirac dispersion ----------------


def band(sign):
    def f(kx, ky):
        return (kx, ky, sign * 0.5 * 2 * math.sqrt(
            math.cos(kx) ** 2 + math.cos(ky) ** 2))
    return f


DIRAC = [(sx * math.pi / 2, sy * math.pi / 2, 0.0)
         for sx in (-1, 1) for sy in (-1, 1)]


def panel_b(eye, nu, cap, W=430, H=390, mode="persp"):
    cam = camera(eye, (0.0, 0.0, 0.0))
    quads = (surface_mesh(band(+1), -math.pi, math.pi, nu, -math.pi, math.pi, nu)
             + surface_mesh(band(-1), -math.pi, math.pi, nu, -math.pi, math.pi, nu))
    ref = [q[0] for q in quads]
    s, cx, cy = fit(cam, ref, W, H, mode=mode)

    def cls_of(q):
        return "faceP" if sum(p[2] for p in q) >= 0 else "faceM"
    o = [surface_svg(cam, quads, s, cx, cy, mode=mode, class_of=cls_of)]
    for p in DIRAC:
        x, y, _ = project(cam, p, mode)
        o.append(f'<circle cx="{cx + s * x:.1f}" cy="{cy - s * y:.1f}" '
                 f'r="4" class="dirac dot"/>')
    return svg_wrap("".join(o), W, H, "pi-flux dispersion", cap)


figB1 = panel_b((8.0, -6.0, 4.6), 24, "camera 1: eye (8, −6, 4.6), perspective")
figB2 = panel_b((5.2, -8.4, 2.2), 18,
                "camera 2: eye (5.2, −8.4, 2.2), low perspective", mode="persp")

# ---------------- panel (c): the Hardy measurement geometry ----------------
TH, A0, A1, B0, B1 = P21["best_penalized"]["x"]


def bloch(t):
    """A real one-qubit state cos t |0> + sin t |1> sits on the x-z
    great circle of the Bloch sphere at polar angle 2t."""
    return (math.sin(2 * t), 0.0, math.cos(2 * t))


DIRS = [(bloch(A0), "a0", "A₀"), (bloch(A1), "a1", "A₁"),
        (bloch(B0), "b0", "B₀"), (bloch(B1), "b1", "B₁")]


def sphere_wire():
    segs = []
    for im in range(8):                      # meridians
        lon = math.pi * im / 4
        arc = [(math.sin(t) * math.cos(lon), math.sin(t) * math.sin(lon),
                math.cos(t)) for t in [math.pi * k / 24 for k in range(25)]]
        segs += list(zip(arc, arc[1:]))
    for ip in range(1, 6):                   # parallels
        lat = math.pi * ip / 6
        ring = [(math.sin(lat) * math.cos(a), math.sin(lat) * math.sin(a),
                 math.cos(lat)) for a in [2 * math.pi * k / 36 for k in range(37)]]
        segs += list(zip(ring, ring[1:]))
    return segs


def panel_c(eye, cap, W=430, H=390):
    cam = camera(eye, (0.0, 0.0, 0.0))
    ref = [(math.cos(a), math.sin(a), z) for a in
           [2 * math.pi * k / 24 for k in range(24)] for z in (-1.0, 1.0)]
    s, cx, cy = fit(cam, ref, W, H, margin=42)
    o = [wireframe_svg(cam, sphere_wire(), s, cx, cy, cls="wire")]
    circle = [(math.sin(t), 0.0, math.cos(t))
              for t in [2 * math.pi * k / 96 for k in range(97)]]
    o.append(polyline_svg(cam, circle, s, cx, cy, cls="gc"))
    for vec, cls, lab in DIRS:
        x, y, _ = project(cam, vec)
        o.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + s * x:.1f}" '
                 f'y2="{cy - s * y:.1f}" class="{cls} arrow"/>')
        o.append(f'<circle cx="{cx + s * x:.1f}" cy="{cy - s * y:.1f}" '
                 f'r="3.4" class="{cls} dot"/>')
        lx, ly = cx + 1.13 * s * x, cy - 1.13 * s * y
        o.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="dlab {cls}" '
                 f'text-anchor="middle">{lab}</text>')
    return svg_wrap("".join(o), W, H, "Hardy measurement directions", cap)


figC1 = panel_c((2.6, 2.3, 1.3), "camera 1: eye (2.6, 2.3, 1.3), generic view")
figC2 = panel_c((0.05, 3.6, 0.02),
                "camera 2: eye (0.05, 3.6, 0.02), edge-on: the four "
                "directions are coplanar")

# ---------------- the page ----------------
LIGHT = {"bg": "#FBFAF7", "ink": "#1F242A", "mut": "#6B6A64", "hair": "#E2DFD6",
         "card": "#F3F1EA", "gold": "#B08A2A", "indigo": "#4A5A8A",
         "teal": "#2E7D64", "ember": "#C2582F", "wire": "#D8D4C8",
         "facep": "#7FAF9B", "facem": "#8FA1D6"}
DARK = {"bg": "#14181C", "ink": "#E8E4DC", "mut": "#98948A", "hair": "#2A3038",
        "card": "#1B2127", "gold": "#E3C55C", "indigo": "#8FA1D6",
        "teal": "#57A98C", "ember": "#E07A4A", "wire": "#2E3640",
        "facep": "#3E7A64", "facem": "#4A5A8A"}

EXTRA = """\
.fig3d { width:100%; height:auto; }
.wire { stroke:var(--wire); stroke-width:.7; }
.w1 { stroke:var(--gold); fill:var(--gold); }
.w0 { stroke:var(--teal); fill:none; }
.sad { stroke:var(--ember); fill:none; }
.w0, .sad, .w1curve { stroke-width:2.4; }
polyline.w1 { fill:none; stroke-width:2.4; }
.faceP { fill:var(--facep); stroke:var(--bg); stroke-width:.4; opacity:.85; }
.faceM { fill:var(--facem); stroke:var(--bg); stroke-width:.4; opacity:.85; }
.dirac { fill:var(--ember); stroke:var(--bg); }
.gc { stroke:var(--hair); stroke-width:1.6; fill:none; stroke-dasharray:5 4; }
.a0, .a1 { stroke:var(--gold); fill:var(--gold); }
.b0, .b1 { stroke:var(--indigo); fill:var(--indigo); }
.dlab { font:600 .8rem "JetBrains Mono", monospace; }
.asec { --rc:var(--gold); } .bsec { --rc:var(--teal); } .csec { --rc:var(--indigo); }
"""

BODY = f"""
<section class="asec">
<h2>(a) Ring phase states on the torus</h2>
<div class="stmt"><span class="tag">one object, two perspectives · P-24 / P-6 geometry</span>
<span class="eq">site i at ring angle 2πi/N; phase φᵢ as the fiber angle: the phase graph is a closed curve on the torus</span>
The winding number is which class the closed curve is in: w = 0 (teal) never wraps the fiber; w = 1 (gold, N = 16 uniform twist, site markers) wraps it once; the pinned saddle (ember, one bond clamped at Δ* = {DSTAR:.4f} from p24_registration.json) is the w = 1 curve caught mid-escape. The two cameras change every coordinate and neither class changes — that is what a topological label means.</div>
<div class="row">{figA1}{figA2}</div>
</section>

<section class="bsec">
<h2>(b) The π-flux Dirac dispersion</h2>
<div class="stmt"><span class="tag">one object, two perspectives · catalog c25</span>
<span class="eq">E(k) = ±2√(cos²kₓ + cos²k_y) over the full zone; band touchings at (±π/2, ±π/2)</span>
The two sheets (upper teal-green, lower indigo) meet at four conical Dirac points (ember). The cameras move; the touchings stay point-like — the linear density of states is a property of the object, not of the view.</div>
<div class="row">{figB1}{figB2}</div>
</section>

<section class="csec">
<h2>(c) The Hardy measurement geometry</h2>
<div class="stmt"><span class="tag">one object, two perspectives · p21_results.json</span>
<span class="eq">α₀ = {A0:.6f}, α₁ = {A1:.6f}, β₀ = {B0:.6f}, β₁ = {B1:.6f} → Bloch directions (sin 2t, 0, cos 2t)</span>
The four optimal measurement directions of the registered Hardy search (best penalized point; Alice gold, Bob indigo — the pairs coincide to 1e-8, which is the α = β symmetry of the optimum). Camera 1 shows four scattered arrows; camera 2 looks along the plane's normal and they collapse onto one great circle (dashed): real-amplitude measurements are coplanar on the Bloch sphere, and only a change of perspective makes that visible.</div>
<div class="row">{figC1}{figC2}</div>
<p class="note">All numbers are pinned/committed (p24_registration.json, p21_results.json, the c25 closed form); curves and surfaces are regenerated deterministically by this script — deterministic illustration, not scored evidence. Projection and painter's sort from kernels/project.py (cross-ratio preservation anchored in its selftest).</p>
</section>
"""

HTML = page(
    "One Object, Several Perspectives",
    "Three landed geometries, each drawn from two cameras: what changes is the view; what the claims cite does not.",
    "proslambenomenos · kernels/project.py + kernels/figpage.py · pinned sources: p24_registration.json, p21_results.json, catalog c25",
    BODY, LIGHT, DARK, extra_css=EXTRA)
OUT_PATH.write_text(HTML)
print(f"wrote {OUT_PATH} ({len(HTML)} bytes)")
