"""termplot -- dependency-free terminal plotting (Python 3 stdlib only).

Conventions:
  * No third-party imports; safe on hosts without pip.
  * Every public function RETURNS a string (nothing is printed).
  * Output is plain monospace text; pass color=True for minimal ANSI accents.

Public API: plot_xy, staircase, heatmap, bars.
"""

_DOTS = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))  # [py%4][px%2]
_EIGHTHS = "▏▎▍▌▋▊▉"  # 1/8 .. 7/8 blocks
_BOLD, _DIM, _RESET = "\x1b[1m", "\x1b[2m", "\x1b[0m"


def _fmt(v):
    if float(v).is_integer() and abs(v) < 1e6:
        return str(int(v))
    return "%.4g" % v


def _span(lo, hi):
    if hi > lo:
        return lo, hi
    pad = abs(lo) * 0.5 or 0.5
    return lo - pad, lo + pad


def _empty(title, kind):
    head = (title + "\n") if title else ""
    return head + "(%s: no data)" % kind


class _Canvas:
    """Braille pixel canvas: width x height char cells = 2w x 4h pixels."""

    def __init__(self, width, height):
        self.w, self.h = width, height
        self.pw, self.ph = 2 * width, 4 * height
        self.cells = [[0] * width for _ in range(height)]

    def set(self, px, py):
        if 0 <= px < self.pw and 0 <= py < self.ph:
            self.cells[py // 4][px // 2] |= _DOTS[py % 4][px % 2]

    def line(self, x0, y0, x1, y1, thick=False):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx - dy
        while True:
            self.set(x0, y0)
            if thick:
                self.set(x0, y0 - 1)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def rows(self):
        return ["".join(chr(0x2800 + c) for c in row) for row in self.cells]


def _render_frame(cv, xlo, xhi, ylo, yhi, title, xlabel, ylabel,
                  marker_rows, color):
    """Compose axes, tick labels, and right-margin marker labels."""
    lo_s, hi_s = _fmt(ylo), _fmt(yhi)
    gut = max(len(lo_s), len(hi_s), len(ylabel))
    out = []
    if title:
        t = (_BOLD + title + _RESET) if color else title
        pad = max(0, (gut + 1 + cv.w - len(title)) // 2)
        out.append(" " * pad + t)
    if ylabel:
        out.append(ylabel.rjust(gut))
    for i, row in enumerate(cv.rows()):
        left = hi_s if i == 0 else (lo_s if i == cv.h - 1 else "")
        tick = "┤" if i in (0, cv.h - 1) else "│"
        tail = ""
        if i in marker_rows:
            lbl = " ┈ " + marker_rows[i]
            tail = (_DIM + lbl + _RESET) if color else lbl
        out.append(left.rjust(gut) + tick + row + tail)
    out.append(" " * gut + "└" + "─" * cv.w)
    xl, xh = _fmt(xlo), _fmt(xhi)
    out.append(" " * (gut + 1) + xl + xh.rjust(cv.w - len(xl)))
    if xlabel:
        out.append(" " * (gut + 1) + xlabel.center(cv.w).rstrip())
    return "\n".join(out)


def _setup(points, width, height, markers):
    pts = [(float(x), float(y)) for x, y in points]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if markers:
        ys = ys + [float(v) for v in markers.values()]
    xlo, xhi = _span(min(xs), max(xs))
    ylo, yhi = _span(min(ys), max(ys))
    cv = _Canvas(width, height)
    px = lambda x: round((x - xlo) / (xhi - xlo) * (cv.pw - 1))
    py = lambda y: round((yhi - y) / (yhi - ylo) * (cv.ph - 1))
    marker_rows = {}
    for lbl, v in (markers or {}).items():
        r = py(float(v))
        for x in range(0, cv.pw, 4):  # faint dotted row
            cv.set(x, r)
        row = r // 4
        marker_rows[row] = (marker_rows[row] + ", " + str(lbl)
                            if row in marker_rows else str(lbl))
    return pts, cv, px, py, (xlo, xhi, ylo, yhi), marker_rows


def plot_xy(points, width=72, height=20, title="", xlabel="", ylabel="",
            markers=None, color=False):
    """Braille scatter plot of (x, y) pairs; markers={label: yvalue}."""
    if not points:
        return _empty(title, "plot_xy")
    pts, cv, px, py, box, mrows = _setup(points, width, height, markers)
    for x, y in pts:
        cv.set(px(x), py(y))
    return _render_frame(cv, *box, title, xlabel, ylabel, mrows, color)


def staircase(points, width=72, height=20, title="", xlabel="", ylabel="",
              markers=None, color=False):
    """Step plot for monotone data; flat plateau runs are drawn doubled."""
    if not points:
        return _empty(title, "staircase")
    pts, cv, px, py, box, mrows = _setup(sorted(points), width, height, markers)
    xlo, xhi, ylo, yhi = box
    eps = (yhi - ylo) / cv.ph          # one pixel of y
    min_run = (xhi - xlo) * 0.02       # plateaus wider than 2% get bold
    i, n = 0, len(pts)
    while i < n - 1:
        j = i
        while j < n - 1 and abs(pts[j + 1][1] - pts[i][1]) <= eps:
            j += 1
        if j > i and pts[j][0] - pts[i][0] >= min_run:  # plateau run
            r = py(pts[i][1])
            cv.line(px(pts[i][0]), r, px(pts[j][0]), r, thick=True)
            i = j
        else:
            a, b = pts[i], pts[i + 1]
            cv.line(px(a[0]), py(a[1]), px(b[0]), py(a[1]))  # tread
            cv.line(px(b[0]), py(a[1]), px(b[0]), py(b[1]))  # riser
            i += 1
    return _render_frame(cv, *box, title, xlabel, ylabel, mrows, color)


def heatmap(grid, row_labels=None, col_labels=None, title="", legend=True,
            color=False):
    """Shade a 2D grid with ' ░▒▓█'; labels optional."""
    grid = [list(map(float, row)) for row in grid]
    if not grid or not grid[0]:
        return _empty(title, "heatmap")
    ramp = " ░▒▓█"
    flat = [v for row in grid for v in row]
    lo, hi = min(flat), max(flat)
    ncol = max(len(r) for r in grid)
    rl = [str(x) for x in (row_labels or [""] * len(grid))]
    cl = [str(x) for x in (col_labels or [])]
    gut = max([len(s) for s in rl] + [0])
    cw = max([2] + [len(s) + 1 for s in cl])
    out = []
    if title:
        out.append((_BOLD + title + _RESET) if color else title)
    if cl:
        out.append(" " * (gut + 1) + "".join(s.center(cw) for s in cl))
    for r, row in enumerate(grid):
        cells = ""
        for v in row:
            k = int((v - lo) / (hi - lo) * (len(ramp) - 1) + 0.5) if hi > lo \
                else len(ramp) // 2
            cells += ramp[k] * cw
        out.append((rl[r] if r < len(rl) else "").rjust(gut) + " " + cells)
    if legend:
        out.append("%s min %s [%s] max %s" % (" " * gut, _fmt(lo), ramp,
                                              _fmt(hi)))
    return "\n".join(out)


def bars(labels, values, width=60, title="", color=False):
    """Horizontal bar chart with value annotations."""
    values = [float(v) for v in values]
    if not values:
        return _empty(title, "bars")
    labels = [str(x) for x in labels] + [""] * (len(values) - len(labels))
    gut = max(len(s) for s in labels)
    top = max([v for v in values if v > 0] + [0]) or 1.0
    out = []
    if title:
        out.append((_BOLD + title + _RESET) if color else title)
    for lbl, v in zip(labels, values):
        n8 = max(0, round(v / top * width * 8))
        bar = "█" * (n8 // 8) + (_EIGHTHS[n8 % 8 - 1] if n8 % 8 else "")
        if color and bar:
            bar = "\x1b[36m" + bar + _RESET
        pad = width - (n8 // 8) - (1 if n8 % 8 else 0)
        out.append("%s │%s%s %s" % (lbl.rjust(gut), bar, " " * pad,
                                         _fmt(v)))
    return "\n".join(out)
