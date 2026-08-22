#!/usr/bin/env python3
"""Render handoff.json as the companion recap page (recap.html).
Run after scripts/handoff.py; publish via the Artifact tool."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "handoff.json").read_text())
w, s, o = d["where"], d["state"], d["open"]
e = html.escape

SEM = {"proven": "good", "refuted": "crit", "imported": "neutral", "asserted": "warn",
       "coincidence-unruled": "warn", "conditional": "warn", "argued": "warn", "verified": "good"}
chips = "".join(f'<span class="chip {SEM.get(k, "neutral")}"><b>{v}</b> {e(k)}</span>'
                for k, v in sorted(s["claims"].items()))
gate_ok = "rc: 0" in w["gates"]


def items(lst):
    return "".join(f"<li>{e(x)}</li>" for x in lst)


def owner(lst):
    out = []
    for i in lst:
        cmd = i.get("command", "")
        row = f'<div class="act"><div class="act-h"><span class="id">{e(i["id"])}</span>{e(i["item"])}</div>'
        if cmd:
            row += (f'<div class="cmd"><code>{e(cmd)}</code>'
                    f'<button type="button" data-cmd="{e(cmd)}">Copy</button></div>')
        row += "</div>"
        out.append(row)
    return "".join(out)


def agent(lst):
    return "".join(f'<li><span class="id">{e(i["id"])}</span>{e(i["item"])}</li>' for i in lst)


page = f"""<title>Proslambenomenos Handoff</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@500;600&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap">
<style>
:root{{--bg:#f5f6f8;--panel:#ffffff;--ink:#1b2230;--mute:#5b6675;--line:#d5dae2;--accent:#9a6b1f;--accent-ink:#5e3f0c;
--good:#1f7a4d;--warn:#9a6b1f;--crit:#a83232;--code:#eef1f5;--chip:#e9edf3}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#12161d;--panel:#191f28;--ink:#e6e9ee;--mute:#98a3b3;--line:#2c3542;--accent:#d2a24c;--accent-ink:#f0d28a;
--good:#4cc38a;--warn:#d2a24c;--crit:#e06c6c;--code:#0f1318;--chip:#242c38}}}}
:root[data-theme="dark"]{{--bg:#12161d;--panel:#191f28;--ink:#e6e9ee;--mute:#98a3b3;--line:#2c3542;--accent:#d2a24c;--accent-ink:#f0d28a;
--good:#4cc38a;--warn:#d2a24c;--crit:#e06c6c;--code:#0f1318;--chip:#242c38}}
body{{background:var(--bg);color:var(--ink);font-family:"Source Sans 3",system-ui,sans-serif;font-size:16px;line-height:1.45;margin:0;padding:28px 20px 60px}}
main{{max-width:860px;margin:0 auto;display:grid;gap:18px}}
h1{{font-family:"IBM Plex Serif",Georgia,serif;font-weight:600;font-size:1.6rem;margin:0;text-wrap:balance}}
h2{{font-family:"IBM Plex Serif",Georgia,serif;font-weight:500;font-size:1.05rem;margin:0 0 10px;letter-spacing:.01em}}
.where{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.86rem;color:var(--mute);display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center}}
.gate{{display:inline-block;padding:2px 9px;border-radius:3px;font-weight:500;color:#fff;background:{'var(--good)' if gate_ok else 'var(--crit)'}}}
section{{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.chip{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.82rem;background:var(--chip);border-radius:3px;padding:3px 9px;border-left:3px solid var(--mute)}}
.chip.good{{border-left-color:var(--good)}}.chip.crit{{border-left-color:var(--crit)}}.chip.warn{{border-left-color:var(--warn)}}
.chip b{{font-weight:500}}
ul{{margin:0;padding-left:1.1em;display:grid;gap:5px}}
li{{max-width:68ch}}
.id{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.8rem;color:var(--mute);margin-right:8px}}
.owner{{border-left:4px solid var(--accent)}}
.act{{display:grid;gap:6px;padding:10px 0;border-top:1px solid var(--line)}}
.act:first-of-type{{border-top:0;padding-top:0}}
.act-h{{max-width:70ch}}
.cmd{{display:flex;gap:8px;align-items:stretch;overflow-x:auto}}
.cmd code{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.82rem;background:var(--code);padding:7px 10px;border-radius:4px;flex:1;white-space:pre;overflow-x:auto}}
.cmd button{{font:inherit;font-size:.8rem;font-weight:600;color:var(--accent-ink);background:transparent;border:1px solid var(--accent);border-radius:4px;padding:0 12px;cursor:pointer}}
.cmd button:hover,.cmd button:focus-visible{{background:var(--accent);color:#fff;outline:none}}
.cmd button.done{{background:var(--good);border-color:var(--good);color:#fff}}
.small{{font-size:.9rem;color:var(--mute)}}
.mono{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.84rem}}
a{{color:var(--accent-ink)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media (max-width:700px){{.two{{grid-template-columns:1fr}}}}
</style>
<main>
<header>
<h1>Proslambenomenos Handoff</h1>
<div class="where"><span>{e(w['last_link'])}</span><span>{e(w['branch'])} @ {e(w['tip'])}</span><span class="gate">{'gates clean' if gate_ok else 'gates RED'}</span><span>law {e(s['laws'])}</span><span>litcheck {e(s['litchecks'])}</span></div>
</header>
<section><h2>Claim census</h2><div class="chips">{chips}</div>
<p class="small mono" style="margin:10px 0 0">predictions {e(', '.join(s['predictions']))}; resolved {e(', '.join(f'{r}→{p}' for r, p in s['resolved']))}</p></section>
<section class="owner"><h2>Needs you</h2>{owner(o['owner'])}</section>
<div class="two">
<section><h2>Decided since last packet</h2><ul>{items(o['decided_since_parent'])}</ul></section>
<section><h2>Retracted since last packet</h2><ul>{items(o['retracted_since_parent'])}</ul></section>
</div>
<section><h2>Next for an agent, in order</h2><ul>{agent(o['agent'])}</ul></section>
<section><h2>Do not recompute</h2><ul>{items(o['do_not_recompute'])}</ul></section>
<section><h2>Pointers</h2><p class="small mono">compendium: <a href="{e(o['artifact'])}">{e(o['artifact'])}</a><br>{e(w['repo'])} — notes/ claims/ PREDICTIONS.md LITCHECKS.md LAWCHANGES.md CATALOG.md RELEASES.md OPEN.yml<br>handoff store: ~/code/handoffs (catbus)</p></section>
</main>
<script>
document.querySelectorAll('button[data-cmd]').forEach(b=>{{b.addEventListener('click',async()=>{{try{{await navigator.clipboard.writeText(b.dataset.cmd);b.textContent='Copied';b.classList.add('done');setTimeout(()=>{{b.textContent='Copy';b.classList.remove('done')}},1600)}}catch(e){{b.textContent='Select + copy'}}}})}});
</script>
"""
(ROOT / "recap.html").write_text(page)
print("recap.html written")
