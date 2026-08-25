#!/usr/bin/env python3
"""P-17 registered computation: the three mechanical machines run at
1e6 pairs each (seed and angles pinned at registration), scored
against their exact curves with derived binomial bands.

  rotor      the best honest local machine: zigzag E = 2 theta/pi - 1,
             CHSH exactly 2 at the pinned angles.
  toner-bacon one bit buys the singlet: E = -cos theta exactly.
  detection  Bob detects with probability |b.lambda|: post-selected
             E = -cos theta at mean efficiency 3/4.
"""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p17_registration.json").read_text())
M = REG["mc"]["pairs"]
ANGLES = REG["mc"]["angles"]
SEED = REG["mc"]["seed"]
NSIG = REG["tolerances"]["mc_sigma"]


def sphere(rng):
    while True:
        x, y, z = rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)
        n = math.sqrt(x * x + y * y + z * z)
        if n > 1e-9:
            return x / n, y / n, z / n


def rotor_E(theta, rng, m=M):
    acc = 0
    for _ in range(m):
        mu = rng.random() * 2 * math.pi
        acc += (1 if math.cos(mu) > 0 else -1) * (-1 if math.cos(mu - theta) > 0 else 1)
    return acc / m


def tb_E(theta, rng, m=M):
    ca, sa = 1.0, 0.0                      # a = x-axis
    cb, sb = math.cos(theta), math.sin(theta)
    acc = 0
    for _ in range(m):
        l1 = sphere(rng)
        l2 = sphere(rng)
        a_l1 = ca * l1[0] + sa * l1[1]
        a_l2 = ca * l2[0] + sa * l2[1]
        A = -1 if a_l1 > 0 else 1
        c = (1 if a_l1 > 0 else -1) * (1 if a_l2 > 0 else -1)
        b_dot = cb * (l1[0] + c * l2[0]) + sb * (l1[1] + c * l2[1])
        B = 1 if b_dot > 0 else -1
        acc += A * B
    return acc / m


def det_E(theta, rng, m=M):
    cb, sb = math.cos(theta), math.sin(theta)
    acc = ndet = 0
    for _ in range(m):
        l = sphere(rng)
        u = cb * l[0] + sb * l[1]          # b . lambda
        if rng.random() >= abs(u):
            continue                        # Bob's detector stays silent
        ndet += 1
        A = -1 if l[0] > 0 else 1          # a = x-axis, Alice always answers
        B = 1 if u > 0 else -1
        acc += A * B
    return acc / ndet, ndet


def main():
    rng = random.Random(SEED)
    out = {"clauses": {}, "detail": {}}

    # (a) rotor: zigzag at angles, CHSH at the pinned settings
    ok_a, rows = True, []
    for th in ANGLES:
        e = rotor_E(th, rng)
        z = 2 * th / math.pi - 1
        sig = math.sqrt(max(1e-12, 1 - z * z) / M)
        ok_a = ok_a and abs(e - z) < NSIG * sig
        rows.append(f"theta={th}: {e:.4f} vs zigzag {z:.4f} ({abs(e-z)/sig:.2f} sig)")
    aa = REG["chsh_angles"]["a"]
    bb = REG["chsh_angles"]["b"]
    s_acc = s_var = 0.0
    for x in (0, 1):
        for y in (0, 1):
            th = abs(aa[x] - bb[y])
            e = rotor_E(th, rng)
            zg = 2 * th / math.pi - 1
            s_acc += e * (1 if (x, y) != (1, 1) else -1)
            s_var += max(1e-12, 1 - zg * zg) / M
    sig_s = math.sqrt(s_var)
    ok_a = ok_a and abs(abs(s_acc) - 2.0) < NSIG * sig_s
    out["clauses"]["a_rotor"] = bool(ok_a)
    out["detail"]["rotor"] = rows + [f"S = {abs(s_acc):.5f} vs 2 ({abs(abs(s_acc)-2)/sig_s:.2f} sig)"]

    # (b) Toner-Bacon: one bit, exact singlet curve
    ok_b, rows_b = True, []
    for th in ANGLES:
        e = tb_E(th, rng)
        q = -math.cos(th)
        sig = math.sqrt(max(1e-12, 1 - q * q) / M)
        ok_b = ok_b and abs(e - q) < NSIG * sig
        rows_b.append(f"theta={th}: {e:.4f} vs -cos {q:.4f} ({abs(e-q)/sig:.2f} sig)")
    out["clauses"]["b_toner_bacon"] = bool(ok_b)
    out["detail"]["toner_bacon"] = rows_b

    # (c) detection machine: faked cosine, priced at 25% of detections
    ok_c, rows_c = True, []
    for th in ANGLES:
        e, ndet = det_E(th, rng)
        q = -math.cos(th)
        sig = math.sqrt(max(1e-12, 1 - q * q) / ndet)
        eta = ndet / M
        sig_eta = math.sqrt(0.5 * 0.5 / M)
        ok_c = (ok_c and abs(e - q) < NSIG * sig
                and abs(eta - 0.5) < NSIG * sig_eta)
        rows_c.append(f"theta={th}: {e:.4f} vs {q:.4f} ({abs(e-q)/sig:.2f} sig), "
                      f"eta_B = {eta:.4f} ({abs(eta-0.5)/sig_eta:.2f} sig)")
    out["clauses"]["c_detection"] = bool(ok_c)
    out["detail"]["detection"] = rows_c

    changes = not (ok_a and ok_b and ok_c)
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p17_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    for k in ("rotor", "toner_bacon", "detection"):
        print(f"  {k}: " + "; ".join(out["detail"][k]))
    print(f"changes-my-mind fired: {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
