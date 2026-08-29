#!/usr/bin/env python3
"""The horizon census as a terminal animation (P-34/R-31).

An unscored visualization of the pinned census: the codebook's
prefactor cloud, the coverage sweep (the detector null - why
order-one coincidences are cheap), each census entry dropping onto
its nearest codebook value while its bits-meter pays the coverage
surprisal and the census charge, the four-mechanisms-one-slot
vignette, and the scoreboard. Every number is the pinned value
from p34_results.json / p34_registration.json (embedded here as
constants so the animation runs standalone); nothing here is
evidence - the evidence lives in the P-34 chain.

Usage:
  python3 p34_terminal.py            # full animation (ANSI, ~45 s)
  python3 p34_terminal.py --fast     # ~12 s
  python3 p34_terminal.py --plain    # no alternate screen buffer
  python3 p34_terminal.py --frames N # render N frames, no delays,
                                     # print the final board (CI)
stdlib only."""
import math
import shutil
import sys
import time

CSI = "\x1b["
RESET = CSI + "0m"
BOLD = CSI + "1m"
DIM = CSI + "2m"
FG = {"green": CSI + "32m", "yellow": CSI + "33m", "red": CSI + "31m",
      "cyan": CSI + "36m", "magenta": CSI + "35m", "blue": CSI + "34m",
      "grey": CSI + "90m"}

FAST = "--fast" in sys.argv
PLAIN = "--plain" in sys.argv
FRAMES_CAP = None
if "--frames" in sys.argv:
    FRAMES_CAP = int(sys.argv[sys.argv.index("--frames") + 1])

# ---- pinned numbers (P-34/R-31; see p34_results.json) ------------
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
CELL_DEX = 10.155          # minimal k-cell width
CENSUS_CHARGE = math.log2(5)
# (name, signed mismatch dex, matched prefactor, net bits, expr)
CENSUS = [
    ("a0 (RAR)", +0.0612, "1/2pi", -0.03, "c*H0/2pi"),
    ("m_pi (Weinberg)", +0.0668, "2", -0.11, "2*(hb^2*H0/Gc)^1/3"),
    ("Omega_L/Omega_m", +0.0364, "2", +0.59, "2"),
    ("nu mass scale", -0.0190, "4pi", +1.49, "4pi*m_P*mu^1/2"),
    ("rho_Lambda", +0.0118, "1/4pi", +2.13, "M_P^2*H0^2/4pi"),
]
MECHS = ["CKN 1999", "Sorkin 1990s", "Zeldovich 1967",
         "holographic DE 2004"]


def coverage(t):
    logs = sorted(math.log10(v) for v in PREFACTORS.values())
    merged = []
    for v in logs:
        lo, hi = v - t, v + t
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(hi, merged[-1][1])
        else:
            merged.append([lo, hi])
    return min(sum(b - a for a, b in merged) / CELL_DEX, 1.0)


# ---- tiny screen ------------------------------------------------
COLS, ROWS = shutil.get_terminal_size((100, 30))
COLS = min(COLS, 110)
ROWS = min(ROWS, 32)
AXIS_ROW = ROWS - 7
SPAN = 2.3  # dex shown either side of the slot center


def X(dex):
    return int((dex + SPAN) / (2 * SPAN) * (COLS - 12)) + 6


class Screen:
    def __init__(self):
        self.buf = {}
        self.frame_count = 0

    def put(self, r, c, s, color=""):
        for i, ch in enumerate(s):
            if 0 <= c + i < COLS and 0 <= r < ROWS:
                self.buf[(r, c + i)] = (ch, color)

    def clear(self):
        self.buf = {}

    def render(self):
        out = []
        for r in range(ROWS):
            line = []
            cur = None
            for c in range(COLS):
                ch, color = self.buf.get((r, c), (" ", ""))
                if color != cur:
                    line.append(RESET + color)
                    cur = color
                line.append(ch)
            out.append("".join(line) + RESET)
        return "\n".join(out)

    def flush(self, delay):
        self.frame_count += 1
        if FRAMES_CAP is not None:
            if self.frame_count == FRAMES_CAP:
                print(self.render())
            if self.frame_count > FRAMES_CAP:
                return False
            return True
        sys.stdout.write(CSI + "H" + self.render())
        sys.stdout.flush()
        time.sleep(delay * (0.3 if FAST else 1.0))
        return True


def axis_base(scr, t_now=None):
    scr.put(1, 4, "THE HORIZON CENSUS", BOLD + FG["cyan"])
    scr.put(1, 24, "· every coincidence is (k, prefactor) in "
                   "mu = H0·t_P ~ 1.2e-61", DIM)
    scr.put(AXIS_ROW, 2, "-" * (COLS - 4), FG["grey"])
    scr.put(AXIS_ROW + 1, X(0) - 6, "slot center", DIM)
    scr.put(AXIS_ROW, X(0), "+", BOLD + FG["cyan"])
    scr.put(AXIS_ROW + 2, 4, f"<-- {CELL_DEX / 2 - SPAN:.1f} dex of "
                             f"NOTHING to the next k-slot -->", DIM)
    if t_now is not None:
        p = coverage(t_now)
        scr.put(3, 4, f"tolerance t = {t_now:.3f} dex   "
                      f"coverage p(t) = {p:.3f}   "
                      f"surprisal = {-math.log2(max(p, 1e-9)):.2f} "
                      f"bits", FG["yellow"])


def main():
    if FRAMES_CAP is None and not PLAIN:
        sys.stdout.write(CSI + "?1049h" + CSI + "?25l" + CSI + "2J")
    try:
        run()
    finally:
        if FRAMES_CAP is None and not PLAIN:
            sys.stdout.write(CSI + "?25h" + CSI + "?1049l")
            sys.stdout.flush()


def run():
    scr = Screen()
    logs = sorted((math.log10(v), n) for n, v in PREFACTORS.items())

    # phase 1: the prefactor cloud pops in
    for k in range(len(logs) + 1):
        scr.clear()
        axis_base(scr)
        scr.put(3, 4, "the codebook: 20 declared prefactors on the "
                      "slot", FG["cyan"])
        for (v, name) in logs[:k]:
            scr.put(AXIS_ROW - 1, X(v), "|", FG["blue"])
        if not scr.flush(0.09):
            break

    # phase 2: the coverage sweep (the detector null)
    steps = 26
    for i in range(steps + 1):
        t = 0.30 * i / steps
        scr.clear()
        axis_base(scr, t_now=t)
        for (v, name) in logs:
            scr.put(AXIS_ROW - 1, X(v), "|", FG["blue"])
        # shade covered cells
        for c in range(6, COLS - 6):
            dex = (c - 6) / (COLS - 12) * 2 * SPAN - SPAN
            if any(abs(dex - v) <= t for v, _ in logs):
                scr.put(AXIS_ROW, c, "=", FG["yellow"])
        scr.put(5, 4, "factor-2 coincidences are cheap BY DERIVATION"
                if t > 0.25 else "", DIM)
        if not scr.flush(0.10):
            break

    # phase 3: the census entries drop in
    board = []
    for name, dm, pref, net, expr in CENSUS:
        xv = math.log10(PREFACTORS[pref]) + dm
        for r in range(4, AXIS_ROW - 1):
            scr.clear()
            axis_base(scr)
            for (v, _n) in logs:
                scr.put(AXIS_ROW - 1, X(v), "|", FG["blue"])
            for i, (bn, bnet) in enumerate(board):
                col = FG["green"] if bnet <= 0.1 else (
                    FG["magenta"] if bnet < 2 else FG["red"])
                scr.put(4 + i, COLS - 34,
                        f"{bn:18} {bnet:+.2f} bits", col)
            scr.put(r, X(xv), "v", BOLD + FG["red"])
            scr.put(r + 1 if r + 1 < AXIS_ROW else r, X(xv) - 2,
                    "", "")
            scr.put(3, 4, f"{name}: mismatch {abs(dm):.4f} dex from "
                          f"prefactor {pref}", BOLD)
            if not scr.flush(0.03):
                return finale(scr, board)
        # bits meter
        s_bits = net + CENSUS_CHARGE
        for i in range(14):
            frac = (i + 1) / 14
            scr.clear()
            axis_base(scr)
            for (v, _n) in logs:
                scr.put(AXIS_ROW - 1, X(v), "|", FG["blue"])
            for j, (bn, bnet) in enumerate(board):
                col = FG["green"] if bnet <= 0.1 else (
                    FG["magenta"] if bnet < 2 else FG["red"])
                scr.put(4 + j, COLS - 34,
                        f"{bn:18} {bnet:+.2f} bits", col)
            scr.put(AXIS_ROW - 2, X(xv), "v", BOLD + FG["red"])
            scr.put(3, 4, f"{name} = {expr} off by {abs(dm):.4f} "
                          f"dex", BOLD)
            bar_s = int(max(s_bits, 0) * 4 * min(frac * 2, 1))
            scr.put(5, 4, f"surprisal  {'#' * bar_s} "
                          f"{s_bits:.2f} bits", FG["yellow"])
            if frac > 0.5:
                bar_c = int(CENSUS_CHARGE * 4 * (frac - 0.5) * 2)
                scr.put(6, 4, f"census x5  {'#' * bar_c} "
                              f"-{CENSUS_CHARGE:.2f} bits",
                        FG["grey"])
            if frac == 1.0:
                col = FG["green"] if net <= 0.1 else (
                    FG["magenta"] if net < 2 else FG["red"])
                scr.put(7, 4, f"NET        {net:+.2f} bits", BOLD
                        + col)
            if not scr.flush(0.06):
                return finale(scr, board)
        board.append((name, net))

    # phase 4: four mechanisms, one slot
    for i in range(16):
        f = (i + 1) / 16
        scr.clear()
        scr.put(1, 4, "FOUR MECHANISMS, ONE SLOT", BOLD + FG["red"])
        cy, cx = ROWS // 2, COLS // 2
        scr.put(cy, cx - 9, "[ rho ~ rho_P mu^2 ]", BOLD
                + FG["cyan"])
        corners = [(3, 6), (3, COLS - 24), (ROWS - 4, 6),
                   (ROWS - 4, COLS - 24)]
        for (r0, c0), m in zip(corners, MECHS):
            r = int(r0 + (cy - r0) * f * 0.72)
            c = int(c0 + (cx - 10 - c0) * f * 0.72)
            scr.put(r, c, m, FG["magenta"])
        scr.put(ROWS - 2, 4, "they cannot all be right - and the "
                             "slot they share was cheap (0.012 dex "
                             "at p ~ 0.05)", DIM)
        if not scr.flush(0.10):
            break

    finale(scr, board)


def finale(scr, board):
    scr.clear()
    scr.put(1, 4, "THE SCOREBOARD", BOLD + FG["cyan"])
    scr.put(3, 4, f"{'entry':20}{'mismatch':>10}{'net bits':>12}",
            DIM)
    rows = board if board else [(n, net) for n, _d, _p, net, _e
                                in CENSUS]
    for i, (name, net) in enumerate(rows):
        dm = next(abs(d) for n, d, _p, nt, _e in CENSUS if n == name)
        col = FG["green"] if net <= 0.1 else (
            FG["magenta"] if net < 2 else FG["red"])
        scr.put(5 + i, 4, f"{name:20}{dm:>9.4f}d{net:>+11.2f}", col)
    scr.put(11, 4, "none reaches the 3-bit flag", BOLD)
    scr.put(12, 4, "the two most famous horizon coincidences are "
                   "worth nothing", DIM)
    scr.put(14, 4, "evidence: P-34/R-31, p34_results.json - this "
                   "animation is illustration only", DIM)
    if FRAMES_CAP is not None:
        print(scr.render())
        return
    sys.stdout.write(CSI + "H" + scr.render())
    sys.stdout.flush()
    time.sleep(0.4 if FAST else 4.0)


if __name__ == "__main__":
    main()
