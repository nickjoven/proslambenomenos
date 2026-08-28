#!/usr/bin/env python3
"""Figure-page kernels: the SVG plot helper, the ring-of-phases
drawing, the three-state theme scaffold, and the HTML page shell used
by the repo's figure pages. Extracted, not rewritten.

Admission (two-artifact rule):
  plot / ring_svg   scripts/experiments/p24_plots.py:115-180
                    (verbatim); scripts/experiments/p16_plots.py:49-85
                    carries the same plot pattern, p7_plots.py the
                    same SVG/legend idiom
  theme_css / page  the three-state theme token pattern used
                    identically in p7_plots.py:176-215,
                    p16_plots.py, p24_plots.py:294-349: light palette
                    on bare :root, dark under BOTH the guarded media
                    query (:root:not([data-theme="light"])) AND
                    :root[data-theme="dark"], body background from a
                    token.

Selftest anchors:
  - the rendered page defines the light palette on bare :root, the
    dark palette under the guarded @media block and under
    :root[data-theme="dark"], and paints body from var(--bg).
  - plot() emits one polyline per line series, one circle per dot,
    and the axis/grid furniture; ring_svg emits N arrows.

stdlib only.
"""
import math

FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;"
         "9..144,640&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&family="
         "JetBrains+Mono:wght@400;600&display=swap")

# The shared page skeleton of p7/p16/p24 (typography, statement cards,
# figure furniture); palette tokens come from theme_css.
BASE_CSS = """\
body { background:var(--bg); color:var(--ink); margin:0;
  font-family:"STIX Two Text", Georgia, serif; font-size:17px; line-height:1.55; }
main { max-width:920px; margin:0 auto; padding:40px 22px 80px; }
h1 { font-family:Fraunces, Georgia, serif; font-weight:640; font-size:2.6rem;
  margin:0 0 4px; text-wrap:balance; }
h2 { font-family:Fraunces, Georgia, serif; font-weight:560; font-size:1.45rem;
  margin:0 0 10px; }
.sub { color:var(--mut); margin:0 0 6px; }
.prov { font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.72rem;
  color:var(--mut); letter-spacing:.04em; }
section { margin-top:52px; }
.stmt { background:var(--card); border-left:3px solid var(--rc, var(--ink));
  padding:14px 18px; margin:14px 0 20px; }
.stmt .eq { font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.95rem;
  display:block; margin:6px 0; }
.stmt .tag { font-family:"JetBrains Mono", ui-monospace, monospace; font-size:.7rem;
  color:var(--mut); text-transform:uppercase; letter-spacing:.08em; }
.row { display:flex; gap:16px; flex-wrap:wrap; }
.row > svg { flex:1 1 380px; }
.fig, .ringfig { width:100%; height:auto; }
svg text { fill:var(--ink); }
.ftitle { font:600 .82rem "JetBrains Mono", monospace; }
.tick, .alab, .rlab { font:400 .72rem "JetBrains Mono", monospace; fill:var(--mut); }
.leg { font:600 .74rem "JetBrains Mono", monospace; }
.grid { stroke:var(--hair); stroke-width:1; }
.axis { stroke:var(--mut); stroke-width:1.2; fill:none; }
.line { fill:none; stroke-width:2.2; }
.ink { stroke:var(--ink); fill:var(--ink); }
.dot { stroke:var(--bg); stroke-width:1.5; }
.ebar { stroke-width:1.4; }
.arrow { stroke-width:2.6; }
.ringpath { fill:none; stroke:var(--hair); stroke-width:1; }
p { max-width:66ch; }
.note { color:var(--mut); font-size:.9rem; }
"""


def _block(tokens):
    return " ".join(f"--{k}:{v};" for k, v in tokens.items())


def theme_css(light, dark):
    """The three-state theme token pattern (p7/p16/p24): the complete
    light palette on bare :root; the dark palette under the guarded
    media query AND under [data-theme="dark"], so the viewer's toggle
    wins in both directions."""
    return (f':root {{ {_block(light)} }}\n'
            f'@media (prefers-color-scheme: dark) {{ '
            f':root:not([data-theme="light"]) {{ {_block(dark)} }} }}\n'
            f':root[data-theme="dark"] {{ {_block(dark)} }}\n')


def page(title, subtitle, prov, body, light, dark, extra_css=""):
    """Assemble the standard figure page: <title>, fonts, three-state
    theme tokens, the shared skeleton, and the caller's sections
    inside <main>. The light/dark dicts must define at least bg, ink,
    mut, hair, card."""
    return (f"<title>{title}</title>\n"
            f'<link rel="stylesheet" href="{FONTS}">\n'
            f"<style>\n{theme_css(light, dark)}{BASE_CSS}{extra_css}</style>\n"
            f"<main>\n<h1>{title}</h1>\n"
            f'<p class="sub">{subtitle}</p>\n'
            f'<p class="prov">{prov}</p>\n'
            f"{body}\n</main>\n")


def plot(series, W=860, H=320, title="", xl="", yl="", logy=False,
         pad=(64, 16, 44, 22), yfmt="{:.2f}", xfmt="{:.2f}"):
    """The p24_plots.py:115 SVG plot helper, verbatim: series is a
    list of dicts with pts [(x, y), ...], cls, and optional dots/err/
    dash/label keys."""
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
    phase differences (site phase = cumulative sum)
    (p24_plots.py:163, verbatim)."""
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


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True
    light = {"bg": "#FBFAF7", "ink": "#1F242A", "mut": "#6B6A64",
             "hair": "#E2DFD6", "card": "#F3F1EA", "acc": "#B08A2A"}
    dark = {"bg": "#14181C", "ink": "#E8E4DC", "mut": "#98948A",
            "hair": "#2A3038", "card": "#1B2127", "acc": "#E3C55C"}
    html = page("T", "s", "p", "<section>x</section>", light, dark)

    g1 = ":root { --bg:#FBFAF7;" in html
    g2 = ('@media (prefers-color-scheme: dark) { '
          ':root:not([data-theme="light"]) { --bg:#14181C;') in html
    g3 = ':root[data-theme="dark"] { --bg:#14181C;' in html
    g4 = "body { background:var(--bg);" in html
    ok &= g1 and g2 and g3 and g4
    print(f"three-state theme: bare root {g1}, guarded media {g2}, "
          f"data-theme dark {g3}, body from token {g4}")

    s = plot([{"pts": [(0, 1), (1, 2), (2, 4)], "cls": "acc", "label": "l"},
              {"pts": [(0, 4), (2, 1)], "cls": "ink", "dots": True}],
             title="t", xl="x", yl="y")
    g5 = s.count("<polyline") == 1 and s.count("<circle") == 2 \
        and s.count('class="axis"') == 2 and s.count('class="grid"') == 5
    ok &= g5
    print(f"plot: 1 polyline, 2 dots, axes and grid {'ok' if g5 else 'FAIL'}")

    r = ring_svg([2 * math.pi / 8] * 8, "w = 1", "acc")
    g6 = r.count("<line") == 8 and r.count('class="ringpath"') == 1
    ok &= g6
    print(f"ring_svg: 8 arrows on the ring {'ok' if g6 else 'FAIL'}")

    print("figpage selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
