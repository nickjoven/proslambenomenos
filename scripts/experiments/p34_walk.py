#!/usr/bin/env python3
"""Walk the horizon census in first person (P-34/R-31).

A stdlib terminal raycaster whose world IS the census cell: the
x-axis is log-value (6 map units per dex). The codebook's twenty
prefactors stand as a forest of blue pillars around the slot
center; the five census entries are colored monoliths at their
measured offsets - walk up to one and its plaque appears (matched
expression, mismatch, net bits). Leave the cloud and the corridor
goes EMPTY for the rest of the 10.155-dex cell: the sparseness of
the codebook, rendered as space you have to walk across. The far
door is the next k-slot.

Controls:  W/S forward/back   A/D turn   Q/E strafe
           M toggle overhead map          X or Ctrl-C quit
Modes:     --demo N   scripted walk, render frame N, exit (CI)
           --ascii    pure-ASCII shading ramp

Every number is the pinned P-34/R-31 value, embedded; illustration
only - the evidence lives in the P-34 chain. stdlib only."""
import math
import os
import select
import shutil
import sys
import time

CSI = "\x1b["
RESET = CSI + "0m"
BOLD = CSI + "1m"
DIM = CSI + "2m"
COL = {"blue": 34, "cyan": 36, "green": 32, "magenta": 35,
       "red": 31, "yellow": 33, "grey": 90, "white": 37}

ASCII = "--ascii" in sys.argv
DEMO = None
if "--demo" in sys.argv:
    DEMO = int(sys.argv[sys.argv.index("--demo") + 1])

RAMP = "#%+=-." if ASCII else "█▓▒░░·"

# ---- pinned census (P-34/R-31) ----------------------------------
PREFACTORS = {
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "1/2": 0.5,
    "1/3": 1 / 3, "1/4": 0.25, "pi": math.pi, "2pi": 2 * math.pi,
    "4pi": 4 * math.pi, "pi^2": math.pi ** 2,
    "4pi^2": 4 * math.pi ** 2, "8pi": 8 * math.pi,
    "1/pi": 1 / math.pi, "1/2pi": 1 / (2 * math.pi),
    "1/4pi": 1 / (4 * math.pi), "1/pi^2": 1 / math.pi ** 2,
    "1/4pi^2": 1 / (4 * math.pi ** 2), "3/8pi": 3 / (8 * math.pi),
    "8pi/3": 8 * math.pi / 3,
}
CENSUS = [
    ("a0 (RAR)", "c*H0/2pi", "1/2pi", +0.0612, -0.03),
    ("m_pi (Weinberg)", "2*(hb^2 H0/Gc)^1/3", "2", +0.0668, -0.11),
    ("Omega_L/Omega_m", "just 2", "2", +0.0364, +0.59),
    ("nu mass scale", "4pi*m_P*mu^1/2", "4pi", -0.0190, +1.49),
    ("rho_Lambda", "M_P^2 H0^2/4pi", "1/4pi", +0.0118, +2.13),
]
CELL_DEX = 10.155
SCALE = 6.0  # map units per dex

# ---- world ------------------------------------------------------
# x: 0 .. (CELL_DEX)*SCALE + margins; cloud centered at x0
MARGIN = 4.0
X0 = MARGIN + 1.7 * SCALE          # slot center map-x
WORLD_W = int(MARGIN * 2 + CELL_DEX * SCALE + 3)
WORLD_H = 17
MIDY = WORLD_H / 2.0


def build_world():
    objs = []  # (x, y, kind, payload)
    for i, (name, v) in enumerate(sorted(PREFACTORS.items(),
                                         key=lambda kv: kv[1])):
        x = X0 + math.log10(v) * SCALE
        y = 3.2 if i % 2 == 0 else WORLD_H - 3.2
        objs.append((x, y, "pillar", name))
    objs.append((X0, MIDY, "center", "slot center (k)"))
    for j, (name, expr, pref, dm, net) in enumerate(CENSUS):
        x = X0 + (math.log10(PREFACTORS[pref]) + dm) * SCALE
        y = MIDY + (-2.0 if j % 2 else 2.0)
        objs.append((x, y, "census", (name, expr, dm, net)))
    objs.append((WORLD_W - MARGIN + 1, MIDY, "door",
                 "the next k-slot"))
    return objs


OBJS = build_world()
R_OBJ = 0.30  # cylinder radius


def cast(px, py, dx, dy, maxd=40.0):
    """March a ray against walls and object cylinders; returns
    (dist, kind, payload) of the first hit."""
    best = (maxd, "sky", None)
    # only the end walls render (x = 0.5 and the door wall); the
    # sides are open void so the pillar forest reads as columns
    for val in (0.5, WORLD_W - 0.5):
        if abs(dx) > 1e-9:
            t = (val - px) / dx
            if 0 < t < best[0]:
                best = (t, "wall", None)
    for (ox, oy, kind, payload) in OBJS:
        # ray-circle intersection
        fx, fy = px - ox, py - oy
        b = fx * dx + fy * dy
        c = fx * fx + fy * fy - R_OBJ * R_OBJ
        disc = b * b - c
        if disc <= 0:
            continue
        t = -b - math.sqrt(disc)
        if 0 < t < best[0]:
            best = (t, kind, payload)
    return best


KIND_COLOR = {"pillar": "blue", "center": "cyan", "door": "yellow",
              "wall": "grey"}


def census_color(net):
    return "green" if net <= 0.1 else ("magenta" if net < 2
                                       else "red")


def render(px, py, ang, W, H, show_map):
    dirx, diry = math.cos(ang), math.sin(ang)
    planex, planey = -diry * 0.66, dirx * 0.66
    rows = [[(" ", "") for _ in range(W)] for _ in range(H)]
    plaque = None
    for col in range(W):
        camx = 2 * col / W - 1
        rx, ry = dirx + planex * camx, diry + planey * camx
        d, kind, payload = cast(px, py, rx, ry)
        d_perp = d * (rx * dirx + ry * diry) / math.hypot(rx, ry)
        if kind == "sky":
            continue
        h = min(H, int(H / max(d_perp * 0.8, 0.5)))
        top = (H - h) // 2
        shade = RAMP[min(len(RAMP) - 1, int(d_perp / 3.2))]
        if kind == "census":
            colname = census_color(payload[3])
        else:
            colname = KIND_COLOR[kind]
        color = CSI + str(COL[colname]) + "m"
        for r in range(top, top + h):
            rows[r][col] = (shade, color)
        if col == W // 2 and kind == "census" and d < 5.0:
            plaque = payload
        if col == W // 2 and kind in ("center", "door") and d < 5.0:
            plaque = ("__loc__", payload, 0, 0)
    if plaque is None:
        # proximity trigger: standing near a monolith reads it
        for (ox, oy, kind, payload) in OBJS:
            if kind == "census" and (px - ox) ** 2 + (py - oy) ** 2 \
                    < 2.2 ** 2:
                plaque = payload
                break
    # floor shading
    for r in range(H * 2 // 3, H):
        for col in range(W):
            if rows[r][col][0] == " ":
                rows[r][col] = ("·" if not ASCII else ".",
                                CSI + str(COL["grey"]) + "m" + DIM)
    out = []
    dex = (px - X0) / SCALE
    out.append(BOLD + CSI + "36m" + " WALK THE HORIZON CENSUS" + RESET
               + DIM + f"   position {dex:+.2f} dex from slot center"
               f"   [WASD move/turn, QE strafe, M map, X quit]"
               + RESET)
    for r in rows:
        line = []
        cur = None
        for ch, color in r:
            if color != cur:
                line.append(RESET + color)
                cur = color
            line.append(ch)
        out.append("".join(line) + RESET)
    if plaque:
        if plaque[0] == "__loc__":
            out.append(BOLD + CSI + "33m" + f"  >> {plaque[1]}"
                       + RESET)
        else:
            name, expr, dm, net = plaque
            colname = census_color(net)
            out.append(BOLD + CSI + str(COL[colname]) + "m"
                       + f"  >> {name}: {expr}  |mismatch| = "
                       f"{abs(dm):.4f} dex  net {net:+.2f} bits"
                       + RESET)
    else:
        out.append(DIM + "  (walk to a colored monolith to read its "
                   "plaque; the door at the far end is the next "
                   "k-slot)" + RESET)
    if show_map:
        # overhead strip
        strip = [" "] * min(W - 4, 100)
        def mx(x):
            return int(x / WORLD_W * (len(strip) - 1))
        for (ox, oy, kind, payload) in OBJS:
            ch = {"pillar": "|", "center": "+", "door": "]",
                  "census": "o"}[kind]
            strip[mx(ox)] = ch
        strip[max(0, min(len(strip) - 1, mx(px)))] = "@"
        out.append(DIM + "  map: " + "".join(strip) + RESET)
    return "\n".join(out)


# ---- input ------------------------------------------------------
def interactive():
    import termios
    import tty
    if not sys.stdin.isatty():
        print("stdin is not a tty; use --demo N for a scripted "
              "frame, or run in a real terminal")
        return
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    cols, rows_t = shutil.get_terminal_size((100, 30))
    W = min(cols, 110)
    H = min(rows_t - 4, 26)
    px, py, ang = X0 - 2.5 * SCALE / 6 * 6, MIDY, 0.0
    px = MARGIN + 1.0
    show_map = True
    try:
        tty.setcbreak(fd)
        sys.stdout.write(CSI + "?1049h" + CSI + "?25l")
        while True:
            sys.stdout.write(CSI + "H")
            sys.stdout.write(render(px, py, ang, W, H, show_map))
            sys.stdout.flush()
            r, _, _ = select.select([sys.stdin], [], [], 0.05)
            if not r:
                continue
            ch = os.read(fd, 3).decode(errors="ignore")
            step, rot = 0.55, 0.16
            nx, ny = px, py
            if ch in ("x", "X", "\x03", "\x1b\x1b"):
                break
            if "w" in ch or "\x1b[A" in ch:
                nx, ny = px + math.cos(ang) * step, \
                    py + math.sin(ang) * step
            if "s" in ch or "\x1b[B" in ch:
                nx, ny = px - math.cos(ang) * step, \
                    py - math.sin(ang) * step
            if "a" in ch or "\x1b[D" in ch:
                ang -= rot
            if "d" in ch or "\x1b[C" in ch:
                ang += rot
            if "q" in ch:
                nx, ny = px + math.sin(ang) * step, \
                    py - math.cos(ang) * step
            if "e" in ch:
                nx, ny = px - math.sin(ang) * step, \
                    py + math.cos(ang) * step
            if "m" in ch:
                show_map = not show_map
            # collision: stay off walls and cylinders
            if 1.0 < nx < WORLD_W - 1.0 and 1.0 < ny < WORLD_H - 1.0 \
                    and all((nx - ox) ** 2 + (ny - oy) ** 2
                            > (R_OBJ + 0.3) ** 2
                            for ox, oy, _k, _p in OBJS):
                px, py = nx, ny
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        sys.stdout.write(CSI + "?25h" + CSI + "?1049l")
        sys.stdout.flush()


def demo(n):
    """Scripted walk: start left of the cloud facing +x, walk
    through the cloud past the census markers; render frame n."""
    W, H = 100, 24
    px, py, ang = MARGIN + 1.0, MIDY, 0.0
    frame = 0
    for step in range(600):
        frame += 1
        if frame == n:
            print(render(px, py, ang, W, H, True))
            return
        # walk the clear center lane, sweeping the gaze
        px += 0.30
        py = MIDY
        ang = 0.22 * math.sin(step / 7.0)
        if px > WORLD_W - 2:
            break
    print(render(px, py, ang, W, H, True))


if __name__ == "__main__":
    if DEMO is not None:
        demo(DEMO)
    else:
        interactive()
