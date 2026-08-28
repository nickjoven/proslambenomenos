#!/usr/bin/env python3
"""Minimal 3D -> 2D projection kernel for the repo's figure pages:
camera (position, look-at, up), perspective and orthographic
projection returning (x, y, depth), painter's sort for segments and
polylines, and wireframe / parametric-surface helpers emitting SVG.

This is the projection layer for visual perspectives: one object,
several cameras. It enters kernels/ as new infrastructure for the
figure tier (the SVG figure pattern it feeds is landed in
p7_plots.py / p16_plots.py / p24_plots.py via kernels/figpage.py);
nothing in the claims/verify tier depends on it.

Selftest anchors:
  - a unit cube's projected vertices against hand-computed values
    (eye (0,0,5), look-at origin, up y, focal 1: the z = +1 face maps
    to +-0.25, the z = -1 face to +-1/6, depths 4 and 6).
  - collinearity is preserved: three collinear 3D points project to
    collinear image points (residual < 1e-12).
  - the CROSS-RATIO of four collinear points is preserved under
    perspective projection to 1e-12 - the projective invariant where
    harmonic ranges actually live (the repo's Otto/golden-spiral
    audit context: a harmonic range (A, B; C, D) = -1 survives any
    camera, while ratios of lengths do not).
  - painter's sort orders interpenetrating segments far-to-near by
    mean depth.

stdlib only.
"""
import math


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def _norm(a):
    n = math.sqrt(_dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


def camera(eye, look_at, up=(0.0, 0.0, 1.0)):
    """Right-handed view basis: returns (eye, right, true_up, forward)
    with forward pointing from the eye toward look_at."""
    f = _norm(_sub(look_at, eye))
    r = _norm(_cross(f, up))
    u = _cross(r, f)
    return (eye, r, u, f)


def project(cam, p, mode="persp", d=1.0):
    """Project 3D point p through the camera. Returns (x, y, depth):
    image coordinates and the distance along the view axis (larger =
    farther). mode 'persp': pinhole with focal length d (x, y scaled
    by d/depth); mode 'ortho': parallel projection, x, y unscaled."""
    eye, r, u, f = cam
    rel = _sub(p, eye)
    x = _dot(rel, r)
    y = _dot(rel, u)
    z = _dot(rel, f)
    if mode == "ortho":
        return (x, y, z)
    return (d * x / z, d * y / z, z)


def painter_sort(items, depth_of):
    """Painter's algorithm: sort drawable items far-to-near so nearer
    items are emitted later and overpaint. depth_of maps an item to
    its sort depth (mean of vertex depths is the repo convention)."""
    return sorted(items, key=depth_of, reverse=True)


def seg_depth(seg2d):
    """Mean depth of a projected segment [(x, y, depth), ...]."""
    return sum(p[2] for p in seg2d) / len(seg2d)


def project_polyline(cam, pts, mode="persp", d=1.0):
    """Project a 3D polyline; returns [(x, y, depth), ...]."""
    return [project(cam, p, mode, d) for p in pts]


def surface_mesh(fn, u0, u1, nu, v0, v1, nv):
    """Quads of the parametric surface fn(u, v) -> (x, y, z):
    [(p00, p10, p11, p01), ...], row-major."""
    P = [[fn(u0 + (u1 - u0) * i / nu, v0 + (v1 - v0) * j / nv)
          for j in range(nv + 1)] for i in range(nu + 1)]
    quads = []
    for i in range(nu):
        for j in range(nv):
            quads.append((P[i][j], P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]))
    return quads


def _map2d(pt, scale, cx, cy):
    return (cx + scale * pt[0], cy - scale * pt[1])


def wireframe_svg(cam, segments, scale, cx, cy, cls="wire", mode="persp",
                  d=1.0, fmt="{:.1f}"):
    """Project 3D segments [(p0, p1), ...], painter-sort them, and
    emit SVG <line> elements (far first)."""
    projected = [ (project(cam, a, mode, d), project(cam, b, mode, d))
                  for (a, b) in segments ]
    out = []
    for pa, pb in painter_sort(projected, lambda s: seg_depth(s)):
        x1, y1 = _map2d(pa, scale, cx, cy)
        x2, y2 = _map2d(pb, scale, cx, cy)
        out.append(f'<line x1="{fmt.format(x1)}" y1="{fmt.format(y1)}" '
                   f'x2="{fmt.format(x2)}" y2="{fmt.format(y2)}" class="{cls}"/>')
    return "".join(out)


def surface_svg(cam, quads, scale, cx, cy, cls="face", mode="persp",
                d=1.0, fmt="{:.1f}", class_of=None):
    """Project surface quads, painter-sort by mean depth, and emit SVG
    <polygon> elements (far first). class_of(quad) may vary the class
    per quad (e.g. two-tone shading by normal direction)."""
    drawn = []
    for q in quads:
        pq = [project(cam, p, mode, d) for p in q]
        drawn.append((sum(p[2] for p in pq) / 4.0, pq, q))
    out = []
    for depth, pq, q in sorted(drawn, key=lambda t: t[0], reverse=True):
        pts = " ".join(f"{fmt.format(x)},{fmt.format(y)}"
                       for x, y in (_map2d(p, scale, cx, cy) for p in pq))
        c = class_of(q) if class_of else cls
        out.append(f'<polygon points="{pts}" class="{c}"/>')
    return "".join(out)


def polyline_svg(cam, pts, scale, cx, cy, cls="curve", mode="persp",
                 d=1.0, fmt="{:.1f}", close=False):
    """Project a 3D polyline and emit one SVG <polyline>/<polygon>."""
    pj = project_polyline(cam, pts, mode, d)
    body = " ".join(f"{fmt.format(x)},{fmt.format(y)}"
                    for x, y in (_map2d(p, scale, cx, cy) for p in pj))
    tag = "polygon" if close else "polyline"
    return f'<{tag} points="{body}" class="{cls}"/>'


def cross_ratio(a, b, c, d):
    """Cross-ratio (a, b; c, d) of four collinear scalars:
    ((a-c)(b-d)) / ((b-c)(a-d))."""
    return ((a - c) * (b - d)) / ((b - c) * (a - d))


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True
    cam = camera((0.0, 0.0, 5.0), (0.0, 0.0, 0.0), up=(0.0, 1.0, 0.0))

    # anchor 1: unit cube, hand-computed image points and depths
    # eye (0,0,5) looking down -z: a vertex (sx, sy, +1) sits at depth
    # 4 and maps to (sx/4, sy/4); (sx, sy, -1) at depth 6 -> (sx/6, sy/6)
    worst = 0.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz, dep in ((1, 4.0), (-1, 6.0)):
                x, y, z = project(cam, (sx, sy, sz))
                worst = max(worst, abs(x - sx / dep), abs(y - sy / dep),
                            abs(z - dep))
    ok &= worst < 1e-12
    print(f"unit cube vs hand-computed projections: worst dev {worst:.1e} "
          f"{'ok' if worst < 1e-12 else 'FAIL'}")

    # ... and the orthographic camera keeps the square undistorted
    xo, yo, zo = project(cam, (1.0, -1.0, 1.0), mode="ortho")
    good = (xo, yo, zo) == (1.0, -1.0, 4.0)
    ok &= good
    print(f"ortho: (1,-1,1) -> ({xo:g}, {yo:g}, depth {zo:g}) "
          f"{'ok' if good else 'FAIL'}")

    # anchor 2: collinearity preserved under perspective
    cam2 = camera((3.0, -2.0, 4.0), (0.3, 0.1, -0.2), up=(0.1, 0.9, 0.2))
    A, dvec = (0.3, -0.5, 0.2), (0.4, 0.7, -0.3)
    ts = [-0.8, 0.15, 0.6, 1.3]
    pts = [project(cam2, (A[0] + t * dvec[0], A[1] + t * dvec[1],
                          A[2] + t * dvec[2])) for t in ts]
    (x1, y1, _), (x2, y2, _), (x3, y3, _) = pts[0], pts[1], pts[2]
    coll = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
    ok &= coll < 1e-12
    print(f"collinearity residual: {coll:.1e} {'ok' if coll < 1e-12 else 'FAIL'}")

    # anchor 3: the cross-ratio of four collinear points is invariant
    # under perspective projection (harmonic ranges live here)
    cr3d = cross_ratio(*ts)
    us = [(p[0] - pts[0][0]) / (pts[3][0] - pts[0][0]) for p in pts]
    cr2d = cross_ratio(*us)
    dev = abs(cr2d - cr3d)
    ok &= dev < 1e-12
    print(f"cross-ratio: 3D {cr3d:.15f} vs image {cr2d:.15f} "
          f"(dev {dev:.1e}) {'ok' if dev < 1e-12 else 'FAIL'}")
    # ... including the harmonic case (A, B; C, D) = -1: t = 0, 2, 1, inf
    # via the finite quadruple (0, 2, 1, 4) -> cr = ((0-1)(2-4))/((2-1)(0-4))
    th = [0.0, 2.0, 1.0, 4.0]
    ph = [project(cam2, (A[0] + t * dvec[0], A[1] + t * dvec[1],
                         A[2] + t * dvec[2])) for t in th]
    uh = [(p[0] - ph[0][0]) / (ph[3][0] - ph[0][0]) for p in ph]
    devh = abs(cross_ratio(*uh) - cross_ratio(*th))
    ok &= devh < 1e-12
    print(f"harmonic-range case dev: {devh:.1e} {'ok' if devh < 1e-12 else 'FAIL'}")

    # anchor 4: painter's sort on interpenetrating segments - the
    # segment whose mean depth is larger is drawn first
    s_far = [project(cam, p) for p in ((-1.0, 0.0, -2.0), (1.0, 0.0, 1.0))]
    s_near = [project(cam, p) for p in ((-1.0, 0.1, 1.5), (1.0, 0.1, -0.5))]
    order = painter_sort([s_near, s_far], seg_depth)
    good = order[0] is s_far and seg_depth(s_far) > seg_depth(s_near)
    ok &= good
    print(f"painter's sort: far (depth {seg_depth(s_far):.2f}) before near "
          f"(depth {seg_depth(s_near):.2f}) {'ok' if good else 'FAIL'}")

    # smoke: SVG emitters produce well-formed elements
    cube = [(sx, sy, sz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    edges = [(a, b) for i, a in enumerate(cube) for b in cube[i + 1:]
             if sum(x != y for x, y in zip(a, b)) == 1]
    svg = wireframe_svg(cam, edges, 100, 200, 200)
    quads = surface_mesh(lambda u, v: (u, v, u * v), -1, 1, 4, -1, 1, 4)
    svg2 = surface_svg(cam, quads, 100, 200, 200)
    good = svg.count("<line") == 12 and svg2.count("<polygon") == 16
    ok &= good
    print(f"svg emitters: {svg.count('<line')} cube edges, "
          f"{svg2.count('<polygon')} surface quads {'ok' if good else 'FAIL'}")

    print("project selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
