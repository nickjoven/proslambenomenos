#!/usr/bin/env python3
"""wavebench: the waveform-through-time engine (prototype).

One recorder convention + one player. Any experiment that can dump
frames gets, for free, a self-contained page with three synchronized
views of the same field history:

  profile    the 1D field at the current instant, animated
  space-time the full history as a heatmap with a time cursor
  cylinder   the 3D embedding for ring geometry - site angle around,
             time along the axis, amplitude as radial displacement -
             drag to rotate, no external library

Everything is inlined (the artifact CSP allows no fetch and no
external CSS), the player is plain canvas, and the generator is
stdlib-only like the rest of the repo. Lives in experiments/ until
it earns a kernels/ promotion (which would be a LAW entry).

API:
    from wavebench import wave_page
    html = wave_page(
        title="...", subtitle="...",
        series=[{"name": ..., "frames": [[f0...], [f1...], ...]}],
        t0=0.0, dtf=1.0,             # time of frame 0, frame spacing
        vmin=-3.2, vmax=3.2,          # display range
        events=[{"t": 205, "label": "tear"}],
        note="...")
Frames are lists of N floats; all series share N and frame count.
"""
import json


def wave_page(title, subtitle, series, t0=0.0, dtf=1.0,
              vmin=-1.0, vmax=1.0, events=None, note=""):
    payload = json.dumps({
        "series": series, "t0": t0, "dtf": dtf,
        "vmin": vmin, "vmax": vmax, "events": events or [],
    }, separators=(",", ":"))
    return (HEAD.replace("__TITLE__", title)
            + "<main>\n<h1>" + title + "</h1>\n"
            + '<p class="sub">' + subtitle + "</p>\n"
            + BODY
            + ('<p class="note">' + note + "</p>\n" if note else "")
            + "</main>\n<script>\nconst DATA = " + payload + ";\n"
            + PLAYER + "</script>\n")


HEAD = """<title>__TITLE__</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap">
<style>
:root{--bg:#f5f6f8;--panel:#ffffff;--ink:#1b2230;--mut:#5b6675;
 --hair:#d5dae2;--accent:#9a6b1f}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
 --bg:#12161d;--panel:#191f28;--ink:#e6e9ee;--mut:#98a3b3;
 --hair:#2c3542;--accent:#d2a24c}}
:root[data-theme="dark"]{--bg:#12161d;--panel:#191f28;--ink:#e6e9ee;
 --mut:#98a3b3;--hair:#2c3542;--accent:#d2a24c}
body{background:var(--bg);color:var(--ink);margin:0;
 font-family:"Source Sans 3",system-ui,sans-serif;font-size:15.5px;
 line-height:1.5;padding:26px 14px 60px}
main{max-width:960px;margin:0 auto}
h1{font-size:1.5rem;margin:0 0 4px;text-wrap:balance}
.sub{color:var(--mut);margin:0 0 14px;max-width:76ch}
.views{display:grid;gap:14px}
.panel{background:var(--panel);border:1px solid var(--hair);
 border-radius:8px;padding:12px 14px}
.panel h2{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;
 color:var(--mut);margin:0 0 8px;font-weight:600}
canvas{display:block;width:100%;height:auto;border-radius:4px;
 touch-action:none}
.bar{display:flex;gap:10px;align-items:center;margin:12px 0 2px;
 font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.85rem}
.bar button{font:inherit;background:transparent;color:var(--ink);
 border:1px solid var(--accent);border-radius:5px;padding:4px 14px;
 cursor:pointer}
.bar button:hover,.bar button:focus-visible{background:var(--accent);
 color:#fff;outline:none}
.bar input[type=range]{flex:1;accent-color:var(--accent)}
.bar .t{min-width:9ch;text-align:right;color:var(--mut)}
.legend{display:flex;gap:16px;flex-wrap:wrap;margin:6px 0 0;
 font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.82rem;
 color:var(--mut)}
.legend .sw{display:inline-block;width:14px;height:3px;
 vertical-align:middle;margin-right:6px;border-radius:2px}
.note{color:var(--mut);font-size:.92rem;max-width:76ch;margin-top:14px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:760px){.two{grid-template-columns:1fr}}
</style>
"""

BODY = """<div class="bar">
 <button id="play">play</button>
 <input id="scrub" type="range" min="0" value="0" step="1">
 <span class="t" id="tlab"></span>
</div>
<div class="legend" id="legend"></div>
<div class="views" style="margin-top:10px">
 <div class="panel"><h2>profile &mdash; the field now</h2>
  <canvas id="prof" width="920" height="240"></canvas></div>
 <div class="two">
  <div class="panel"><h2>space&ndash;time &mdash; the whole history</h2>
   <canvas id="st" width="450" height="330"></canvas></div>
  <div class="panel"><h2>cylinder &mdash; drag to rotate</h2>
   <canvas id="cyl" width="450" height="330"></canvas></div>
 </div>
</div>
"""

PLAYER = r"""
"use strict";
const S = DATA.series, NF = S[0].frames.length, N = S[0].frames[0].length;
const PAL = ["#2b7de0", "#d2a24c", "#4cc38a", "#e06c6c", "#b195c9"];
S.forEach((s, i) => { s.color = s.color || PAL[i % PAL.length]; });
let frame = 0, playing = false, rotX = -1.05, rotZ = 0.55;

const css = (n) => getComputedStyle(document.documentElement)
  .getPropertyValue(n).trim();
function setup(id) {
  const cv = document.getElementById(id);
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const w = cv.width, h = cv.height;
  cv.width = w * dpr; cv.height = h * dpr;
  const ctx = cv.getContext("2d");
  ctx.scale(dpr, dpr);
  return [cv, ctx, w, h];
}
const [,ctxP, WP, HP] = setup("prof");
const [cvS, ctxS, WS, HS] = setup("st");
const [cvC, ctxC, WC, HC] = setup("cyl");

// diverging palette for the heatmap (blue - panel - red)
function heat(v) {
  const x = Math.max(-1, Math.min(1, (2 * (v - DATA.vmin)
    / (DATA.vmax - DATA.vmin)) - 1));
  const r = x > 0 ? 224 : 43 + (1 + x) * 130;
  const g = 120 + (1 - Math.abs(x)) * 60;
  const b = x < 0 ? 224 : 76 + (1 - x) * 120;
  return [r, g, b];
}

// ---- space-time, drawn once per series-visibility to an offscreen
const off = document.createElement("canvas");
off.width = NF; off.height = N;
(function drawST() {
  const o = off.getContext("2d");
  const img = o.createImageData(NF, N);
  const fr = S[0].frames;
  for (let k = 0; k < NF; k++)
    for (let j = 0; j < N; j++) {
      const [r, g, b] = heat(fr[k][j]);
      const p = 4 * (j * NF + k);
      img.data[p] = r; img.data[p + 1] = g; img.data[p + 2] = b;
      img.data[p + 3] = 255;
    }
  o.putImageData(img, 0, 0);
})();

function drawSTView() {
  ctxS.clearRect(0, 0, WS, HS);
  const L = 40, T = 8, W = WS - L - 10, H = HS - T - 40;
  ctxS.imageSmoothingEnabled = false;
  ctxS.drawImage(off, L, T, W, H);
  ctxS.strokeStyle = css("--ink"); ctxS.lineWidth = 1.4;
  const x = L + (frame + 0.5) / NF * W;
  ctxS.beginPath(); ctxS.moveTo(x, T); ctxS.lineTo(x, T + H); ctxS.stroke();
  ctxS.fillStyle = css("--mut");
  ctxS.font = "11px 'IBM Plex Mono', monospace";
  ctxS.fillText("site", 6, T + 12);
  ctxS.textAlign = "center";
  ctxS.fillText("time →", L + W / 2, HS - 20);
  for (const ev of DATA.events) {
    const ex = L + ((ev.t - DATA.t0) / DATA.dtf + 0.5) / NF * W;
    ctxS.fillStyle = css("--accent");
    ctxS.fillText("▼ " + ev.label, ex, T + H + 14);
  }
  ctxS.textAlign = "left";
}

// ---- profile
function drawProf() {
  ctxP.clearRect(0, 0, WP, HP);
  const L = 46, T = 10, W = WP - L - 14, H = HP - T - 34;
  ctxP.strokeStyle = css("--hair"); ctxP.lineWidth = 1;
  const Y = (v) => T + (DATA.vmax - v) / (DATA.vmax - DATA.vmin) * H;
  for (const v of [DATA.vmin, 0, DATA.vmax]) {
    ctxP.beginPath(); ctxP.moveTo(L, Y(v)); ctxP.lineTo(L + W, Y(v));
    ctxP.stroke();
    ctxP.fillStyle = css("--mut");
    ctxP.font = "11px 'IBM Plex Mono', monospace";
    ctxP.textAlign = "right";
    ctxP.fillText(v.toFixed(1), L - 6, Y(v) + 4);
  }
  ctxP.textAlign = "left";
  ctxP.fillText("site around the ring →", L, HP - 12);
  for (const s of S) {
    ctxP.strokeStyle = s.color; ctxP.lineWidth = 1.8;
    ctxP.beginPath();
    s.frames[frame].forEach((v, j) => {
      const x = L + j / (N - 1) * W, y = Y(v);
      j ? ctxP.lineTo(x, y) : ctxP.moveTo(x, y);
    });
    ctxP.stroke();
  }
}

// ---- cylinder: site angle around, time along the axis
function drawCyl() {
  ctxC.clearRect(0, 0, WC, HC);
  const cx = WC / 2, cy = HC / 2, R = 78, AXIS = 230, AMP = 26;
  const vspan = Math.max(Math.abs(DATA.vmin), Math.abs(DATA.vmax));
  const ca = Math.cos(rotX), sa = Math.sin(rotX);
  const cb = Math.cos(rotZ), sb = Math.sin(rotZ);
  function proj(j, k, v) {
    const ph = j / N * 2 * Math.PI;
    const r = R + AMP * v / vspan;
    let x = r * Math.cos(ph), y = r * Math.sin(ph);
    let z = (k / (NF - 1) - 0.5) * AXIS;
    let x1 = x * cb - y * sb, y1 = x * sb + y * cb;
    let y2 = y1 * ca - z * sa, z2 = y1 * sa + z * ca;
    return [cx + x1, cy - z2, y2];
  }
  const fr = S[0].frames;
  ctxC.lineWidth = 1;
  const step = Math.max(1, Math.floor(NF / 56));
  for (let k = 0; k < NF; k += step) {
    const cur = k <= frame && frame < k + step;
    ctxC.strokeStyle = cur ? css("--accent") : css("--mut");
    ctxC.globalAlpha = cur ? 1 : 0.32;
    ctxC.lineWidth = cur ? 2 : 1;
    ctxC.beginPath();
    for (let j = 0; j <= N; j++) {
      const [x, y] = proj(j % N, k, fr[k][j % N]);
      j ? ctxC.lineTo(x, y) : ctxC.moveTo(x, y);
    }
    ctxC.stroke();
  }
  ctxC.globalAlpha = 0.22;
  ctxC.strokeStyle = css("--ink");
  for (let j = 0; j < N; j += Math.max(1, N / 16)) {
    ctxC.beginPath();
    for (let k = 0; k < NF; k += 4) {
      const [x, y] = proj(j, k, fr[k][j]);
      k ? ctxC.lineTo(x, y) : ctxC.moveTo(x, y);
    }
    ctxC.stroke();
  }
  ctxC.globalAlpha = 1;
  ctxC.fillStyle = css("--mut");
  ctxC.font = "11px 'IBM Plex Mono', monospace";
  ctxC.fillText("time along the axis · amplitude = radius", 10, HC - 10);
}

// ---- controls
const scrub = document.getElementById("scrub");
scrub.max = NF - 1;
const tlab = document.getElementById("tlab");
const playBtn = document.getElementById("play");
function redraw() {
  tlab.textContent = "t = " + (DATA.t0 + frame * DATA.dtf).toFixed(0);
  scrub.value = frame;
  drawProf(); drawSTView(); drawCyl();
}
scrub.addEventListener("input", () => { frame = +scrub.value; redraw(); });
playBtn.addEventListener("click", () => {
  playing = !playing;
  playBtn.textContent = playing ? "pause" : "play";
});
let last = 0;
function tick(ts) {
  if (playing && ts - last > 40) {
    frame = (frame + 1) % NF; last = ts; redraw();
  }
  requestAnimationFrame(tick);
}
let drag = null;
cvC.addEventListener("pointerdown", (e) => {
  drag = [e.clientX, e.clientY]; cvC.setPointerCapture(e.pointerId);
});
cvC.addEventListener("pointermove", (e) => {
  if (!drag) return;
  rotZ += (e.clientX - drag[0]) * 0.008;
  rotX += (e.clientY - drag[1]) * 0.008;
  drag = [e.clientX, e.clientY]; drawCyl();
});
cvC.addEventListener("pointerup", () => { drag = null; });
document.getElementById("legend").innerHTML = S.map((s) =>
  '<span><span class="sw" style="background:' + s.color + '"></span>'
  + s.name + "</span>").join("");
const mq = matchMedia("(prefers-color-scheme: dark)");
mq.addEventListener?.("change", redraw);
redraw();
requestAnimationFrame(tick);
"""
