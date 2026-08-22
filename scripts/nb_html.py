#!/usr/bin/env python3
"""Render notebooks/*.ipynb to notebooks/index.html (stdlib only): one
page, every notebook's markdown + code + captured stdout, inline SVGs
captured through nbkit.SVG_SINK. Cells are executed via nb_run's
run_notebook(), so the page shows what the gate ran. Theme-aware CSS
tokens match compendium/index.html; the only external asset is Google
Fonts.

Usage: python3 scripts/nb_html.py [--out notebooks/index.html]"""
import html
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "notebooks"))
import nb_run  # noqa: E402
import nbkit  # noqa: E402

ANSI = re.compile(r"\x1b\[[0-9;]*m")


# ───────────────────────── minimal markdown ─────────────────────────
def inline(s: str) -> str:
    """Escape, then render `code`, $math$, **bold**, *italic*."""
    out = []
    pos = 0
    token = re.compile(r"(`[^`]+`|\$[^$]+\$|\*\*[^*]+\*\*|\*[^*]+\*)")
    for m in token.finditer(s):
        out.append(html.escape(s[pos:m.start()]))
        t = m.group(0)
        if t.startswith("`"):
            out.append(f"<code>{html.escape(t[1:-1])}</code>")
        elif t.startswith("$"):
            out.append(f'<span class="math">{html.escape(t[1:-1])}</span>')
        elif t.startswith("**"):
            out.append(f"<strong>{html.escape(t[2:-2])}</strong>")
        else:
            out.append(f"<em>{html.escape(t[1:-1])}</em>")
        pos = m.end()
    out.append(html.escape(s[pos:]))
    return "".join(out)


def markdown(src: str) -> str:
    lines = src.splitlines()
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(x.strip() for x in para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        h = re.match(r"^(#{1,6})\s+(.*)$", line)
        if h:
            flush()
            lvl = len(h.group(1))
            out.append(f"<h{lvl}>{inline(h.group(2))}</h{lvl}>")
            i += 1
            continue
        if re.match(r"^\s*\d+\.\s", line):
            flush()
            items = []
            while i < len(lines) and (re.match(r"^\s*\d+\.\s", lines[i]) or (lines[i].startswith("   ") and items)):
                if re.match(r"^\s*\d+\.\s", lines[i]):
                    items.append(re.sub(r"^\s*\d+\.\s", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        if not line.strip():
            flush()
            i += 1
            continue
        para.append(line)
        i += 1
    flush()
    return "\n".join(out)


# ───────────────────────── page ─────────────────────────
CSS = """
  :root {
    --bg: #FAFAF7; --panel: #F1F1EC; --line: #DDDDD4;
    --ink: #1C2025; --muted: #5A6068; --faint: #8A9098;
    --accent: #2F4BC7; --s1: #2F4BC7; --s2: #B45309;
    --ok: #1E7B45; --ok-bg: #E4F2E9; --bad: #B3261E; --bad-bg: #F7E5E3;
    --note-bg: #F5EEDD; --note-ink: #6B5416; --chip-bg: #E9E9E2;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #14161A; --panel: #1C1F25; --line: #2E323A;
      --ink: #E8E9E6; --muted: #A2A8B0; --faint: #6C737C;
      --accent: #8CA3F5; --s1: #6E82D9; --s2: #BF7C35;
      --ok: #6FCF97; --ok-bg: #16281D; --bad: #E88980; --bad-bg: #2E1A18;
      --note-bg: #262115; --note-ink: #D9BC6A; --chip-bg: #262A31;
    }
  }
  :root[data-theme="dark"] {
    --bg: #14161A; --panel: #1C1F25; --line: #2E323A;
    --ink: #E8E9E6; --muted: #A2A8B0; --faint: #6C737C;
    --accent: #8CA3F5; --s1: #6E82D9; --s2: #BF7C35;
    --ok: #6FCF97; --ok-bg: #16281D; --bad: #E88980; --bad-bg: #2E1A18;
    --note-bg: #262115; --note-ink: #D9BC6A; --chip-bg: #262A31;
  }
  * { box-sizing: border-box; }
  body { background: var(--bg); color: var(--ink); margin: 0;
         font-family: 'Source Serif 4', Charter, 'Bitstream Charter', Cambria, Georgia, serif;
         font-size: 17px; line-height: 1.55; }
  main { max-width: 62rem; margin: 0 auto; padding: 2.5rem 1.25rem 5rem; }
  header h1 { font-size: 2rem; margin: 0 0 .4rem; letter-spacing: -.01em; }
  .subtitle { color: var(--muted); margin: 0 0 1rem; max-width: 62ch; }
  .provenance { border: 1px solid var(--line); background: var(--panel); border-radius: 6px;
                padding: .8rem 1rem; font-size: .92rem; color: var(--muted); }
  .provenance strong { color: var(--ink); }
  nav.index { display: flex; flex-wrap: wrap; gap: .5rem 1.2rem; margin: 1.2rem 0 2rem; font-size: .95rem; }
  nav.index a { color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--line); }
  nav.index a:hover { border-color: var(--accent); }
  section.nb { border-top: 1px solid var(--line); padding-top: 1.8rem; margin-top: 2.2rem; }
  section.nb > .nb-head { display: flex; align-items: baseline; gap: .8rem; flex-wrap: wrap; }
  .cnum { font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
          color: var(--accent); font-size: .9rem; }
  .chip { font-size: .78rem; padding: .1rem .5rem; border-radius: 999px; background: var(--chip-bg); color: var(--muted); }
  .chip.ok { background: var(--ok-bg); color: var(--ok); }
  .chip.bad { background: var(--bad-bg); color: var(--bad); }
  .md h1 { font-size: 1.55rem; margin: .2rem 0 .8rem; }
  .md h2 { font-size: 1.15rem; margin: 1.4rem 0 .5rem; }
  .md p, .md li { max-width: 70ch; }
  .md code, .math { font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .88em; }
  .math { color: var(--note-ink); background: var(--note-bg); padding: 0 .2em; border-radius: 3px; }
  pre { margin: 0; white-space: pre; overflow-x: auto; font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: .8rem; line-height: 1.38; }
  .cell { margin: .9rem 0; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
  .cell .src { background: var(--panel); padding: .7rem .9rem; border-left: 3px solid var(--accent); }
  .cell .out { padding: .7rem .9rem; border-top: 1px dashed var(--line); }
  .cell .out pre { color: var(--muted); }
  .cell .out pre .tag { color: var(--ink); }
  .cell.failed .src { border-left-color: var(--bad); }
  .cell .err { background: var(--bad-bg); color: var(--bad); padding: .6rem .9rem; }
  .svgs { display: flex; flex-wrap: wrap; gap: 1rem; padding: .6rem .9rem; }
  .svgs svg { max-width: 100%; height: auto; color: var(--ink); }
  footer { margin-top: 3rem; color: var(--faint); font-size: .85rem; }
"""

SCRIPT = """
  // readable PASS/FAIL lines without any external library
  document.querySelectorAll('.out pre').forEach(pre => {
    pre.innerHTML = pre.innerHTML.replace(/^(.*\\b(PASS|FAIL|fails as required|as required)\\b.*)$/gm,
      '<span class="tag">$1</span>');
  });
"""


def render_notebook(path: Path, idx: int) -> tuple:
    parts = [f'<section class="nb" id="{html.escape(path.stem)}">']
    ok = True
    ncells = 0
    t0 = time.perf_counter()
    body = []
    for cell, out, err in nb_run.run_notebook(path, quiet=True):
        if cell["cell_type"] == "markdown":
            body.append(f'<div class="md">{markdown(nb_run.source(cell))}</div>')
            continue
        ncells += 1
        svgs = list(nbkit.SVG_SINK or [])
        nbkit.SVG_SINK.clear()
        cls = "cell failed" if err else "cell"
        body.append(f'<div class="{cls}"><div class="src"><pre>{html.escape(nb_run.source(cell))}</pre></div>')
        text = ANSI.sub("", out).rstrip()
        if text:
            body.append(f'<div class="out"><pre>{html.escape(text)}</pre></div>')
        if svgs:
            body.append('<div class="svgs">' + "".join(svgs) + "</div>")
        if err:
            ok = False
            body.append(f'<div class="err">{type(err).__name__}: {html.escape(str(err))}</div>')
        body.append("</div>")
    dt = time.perf_counter() - t0
    chip = '<span class="chip ok">ran: all cells</span>' if ok else '<span class="chip bad">a cell raised</span>'
    parts.append(f'<div class="nb-head"><span class="cnum">{idx}</span>{chip}'
                 f'<span class="chip">{ncells} code cells · {dt:.1f}s</span>'
                 f'<span class="chip"><code>notebooks/{html.escape(path.name)}</code></span></div>')
    parts.extend(body)
    parts.append("</section>")
    return "\n".join(parts), ok


def main(argv) -> int:
    out_path = ROOT / "notebooks/index.html"
    if "--out" in argv:
        out_path = Path(argv[argv.index("--out") + 1])
    paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    nbkit.SVG_SINK = []
    sections, all_ok = [], True
    titles = []
    for i, p in enumerate(paths):
        first = next((c for c in nb_run.load(p)["cells"] if c["cell_type"] == "markdown"), None)
        title = re.sub(r"^#\s*", "", nb_run.source(first).splitlines()[0]) if first else p.stem
        titles.append((p.stem, title))
        sec, ok = render_notebook(p, i)
        all_ok &= ok
        sections.append(sec)
        print(f"  {'ok' if ok else 'FAIL'}: {p.stem}")
    nav = "".join(f'<a href="#{html.escape(s)}">{html.escape(t)}</a>' for s, t in titles)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Temporal-First Curriculum</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<main>
<header>
  <h1>Temporal-first curriculum, run</h1>
  <p class="subtitle">Eight notebooks (T0–T6 and a capstone) arranged from
  <code>notes/temporal_first_curriculum.md</code>: every fact is computed in a cell or cited;
  every module ends by running a named mutant and requiring it to fail.</p>
  <div class="provenance"><strong>Provenance.</strong> This page is the captured stdout of
  <code>python3 scripts/nb_run.py</code> (stdlib Python; plots by <code>scripts/termplot.py</code>).
  Nothing here is a claim: the statuses that matter live in <code>claims/</code> and are derived by the gates.
  Generated {time.strftime('%Y-%m-%d')}; all notebooks ran: <strong>{'yes' if all_ok else 'NO'}</strong>.</div>
  <nav class="index">{nav}</nav>
</header>
{chr(10).join(sections)}
<footer>Rendered by <code>scripts/nb_html.py</code>; source notebooks in <code>notebooks/</code>;
authoring source <code>scripts/nb_build.py</code>.</footer>
</main>
<script>{SCRIPT}</script>
</body>
</html>
"""
    out_path.write_text(page)
    print(f"wrote {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path} ({len(page) // 1024} KB); all ran: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
