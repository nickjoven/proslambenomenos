#!/usr/bin/env python3
"""wavebench demo on P-36 physics: the twisted ring held 2% over
its fold. Records the wrapped covariant strain field s_j(t) through
the top-bond slip - the loaded profile, the slip, and the launched
wave circulating the loop - and renders it with the wavebench
engine (profile + space-time + cylinder). Unregistered
visualization; every number is recomputed here, nothing is claimed.

Run: python3 scripts/experiments/p36_waves.py [out.html]
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc, ground_state, winding  # noqa: E402
from wavebench import wave_page  # noqa: E402

TAU = 2 * math.pi


def wrap(x):
    return (x + math.pi) % TAU - math.pi


def record(N=64, sector=1, gamma=0.02, dt=0.02,
           t_start=140.0, t_end=440.0, dtf=0.5):
    ft = fold_fc(N, (2 * sector - 1) * math.pi)
    f_target = 1.02 * ft
    A, th = ground_state(N, True, sector)
    s0 = [wrap(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
    w = [0.0] * N
    b = N // 2
    W0 = winding(th, A, N)
    frames, events = [], []
    seen_bond, seen_w = False, False
    steps = int(t_end / dt)
    rec_every = int(dtf / dt)
    for s in range(steps):
        f = f_target * min(1.0, (s + 1) * dt / 200.0)
        for j in range(N):
            Dr = th[(j + 1) % N] - th[j] - A[j]
            Dl = th[j] - th[j - 1] - A[j - 1]
            acc = (math.sin(Dr) - math.sin(Dl) - gamma * w[j]
                   + (f if j == b else 0.0))
            w[j] += dt * acc
        for j in range(N):
            th[j] += dt * w[j]
        t = (s + 1) * dt
        if (s + 1) % rec_every == 0:
            sw = [wrap(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
            if t >= t_start:
                frames.append([round(v, 3) for v in sw])
            if not seen_bond:
                # transit detector: a bond's wrapped strain far from
                # its base value (the slip passes through the wrap)
                if max(abs(v - s0[j]) for j, v in enumerate(sw)) > 2.6:
                    events.append({"t": t, "label": "slip"})
                    seen_bond = True
            if seen_bond and not seen_w:
                if abs(winding(th, A, N) - W0) > 0.6:
                    events.append({"t": t, "label": "ΔW"})
                    seen_w = True
    return frames, events, ft, t_start, dtf


def main():
    frames, events, ft, t0, dtf = record()
    html = wave_page(
        title="One Slip, Three Ways",
        subtitle=("The P-36 twisted ring (N = 64, sector +½) held 2%% over "
                  "its fold f = %.4f: the wrapped covariant strain field "
                  "sⱼ(t) through the top-bond slip. The same history "
                  "as an animated profile, a space–time sheet, and a "
                  "rotatable cylinder (site angle around, time along the "
                  "axis, strain as radius). Recomputed here from the "
                  "registered equations; nothing on this page is a claim."
                  % ft),
        series=[{"name": "wrapped covariant strain sⱼ",
                 "frames": frames, "color": "#d2a24c"}],
        t0=t0, dtf=dtf, vmin=-math.pi, vmax=math.pi,
        events=events,
        note=("Engine: scripts/experiments/wavebench.py — one "
              "recorder convention (frames of N floats) in, three "
              "synchronized views out, no libraries, artifact-CSP "
              "safe. The heatmap and cylinder render the first "
              "series; the profile overlays all of them."))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "p36_waves.html")
    with open(out, "w") as fh:
        fh.write(html)
    print("wrote %s (%d frames, %d events: %s)"
          % (out, len(frames), len(events),
             [(e["t"], e["label"]) for e in events]))


if __name__ == "__main__":
    main()
