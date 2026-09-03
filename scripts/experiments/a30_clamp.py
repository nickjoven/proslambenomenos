#!/usr/bin/env python3
"""A-30 discriminator (derive-layer measurement, no registration; output in a30_clamp.txt): the ring at gamma 0.5, window [30, 80] (slow mode alive).
Variant A: the real rotor. Variant B: from Delta = 30 on, site b is clamped to
uniform rotation at the mean rotor speed measured in variant A's window
(v_b := Omega_bar, theta_b advances linearly) - the ring's slow strain is
untouched, the rotor's ripple removed. Variant C: clamped from the EVENT
(Delta = 0) so the ring's relaxation develops under a rippleless drive.
Reads the drive-locked A1, A2 and the excess over the root band."""
import sys, math, cmath, time
sys.path.insert(0, "scripts/experiments")
from p35_ring import fold_fc, ground_state
from p46_derive import evanescent
from p49_derive import analyse, N, B, SITES

def run(gamma, f, dt, win, clamp_from=None, Om_clamp=None):
    A, th = ground_state(N, True, 0); v = [0.0]*N
    D0 = [th[(j+1)%N]-th[j]-A[j] for j in range(N)]
    sinD = [math.sin(x) for x in D0]
    n_ramp = int(round(200.0/dt)); per = int(round(1.0/dt))
    event = None; n_total = int(round(1500.0/dt)); TH=[]; V=[]; cmin, cmax = 1.0, -1.0
    om_acc = 0.0; om_n = 0
    s = 0
    while s < n_total:
        fnow = f*min(1.0,(s+1)/n_ramp)
        clamped = (event is not None and clamp_from is not None and (s-event)*dt >= clamp_from)
        for j in range(N):
            if clamped and j == B:
                v[j] = Om_clamp
            else:
                v[j] += dt*(sinD[j]-sinD[j-1]-gamma*v[j]+(fnow if j==B else 0.0))
        for j in range(N): th[j] += dt*v[j]
        sinD = [math.sin(th[(j+1)%N]-th[j]-A[j]) for j in range(N)]
        s += 1
        if event is None:
            if s % per == 0:
                D = [th[(j+1)%N]-th[j]-A[j] for j in range(N)]
                if max(abs(D[j]-D0[j]) for j in range(N)) > 1.5*math.pi:
                    event = s; n_total = s + int(round(win[1]/dt)) + 1
            continue
        Delta = (s-event)*dt
        if win[0] <= Delta < win[1]:
            TH.append([th[(B+d)%N] for d in SITES]); V.append([v[(B+d)%N] for d in SITES])
            om_acc += v[B]; om_n += 1
            if s % per == 0:
                for j in range(N):
                    if min(abs(j-B), N-abs(j-B)) >= 1 and j != B-1:
                        c = math.cos(th[(j+1)%N]-th[j]-A[j]); cmin, cmax = min(cmin,c), max(cmax,c)
    return {"event_t": event*dt, "TH": TH, "V": V, "cmin": cmin, "cmax": cmax, "Om_mean": om_acc/om_n}

gamma = 0.5; f = fold_fc(N,-math.pi)+0.005; dt = 0.001; win = (30.0, 80.0)
t0=time.time()
ra = run(gamma, f, dt, win); Om = ra["Om_mean"]; a = analyse(ra, gamma, dt)
print("A real rotor: Om %.4f x1 rms %.3f excess %+.2f%% A1 %.4e ratio21 %.4e band [%.4e,%.4e] (%.0f s)" % (a["Omega"], a["x1_rms"], 100*a["ratio21_fund_over_top"], a["sites"]["1"]["fund_amp"], a["ratio21_fund_only"], *a["w_band"], time.time()-t0), flush=True)
# the rotor's ripple in A: rms of v_b about its mean over the window
vb = [row[0] for row in ra["V"]]; m = sum(vb)/len(vb); rip = math.sqrt(sum((x-m)**2 for x in vb)/len(vb))
print("   rotor velocity ripple rms %.4f (%.1f%% of Omega)" % (rip, 100*rip/m))
for label, cf in (("B clamp from 30", 30.0), ("C clamp from 0", 0.0)):
    t0=time.time(); r = run(gamma, f, dt, win, clamp_from=cf, Om_clamp=Om); b = analyse(r, gamma, dt)
    print("%s: Om %.4f x1 rms %.3f excess %+.2f%% A1 %.4e ratio21 %.4e band [%.4e,%.4e] (%.0f s)" % (label, b["Omega"], b["x1_rms"], 100*b["ratio21_fund_over_top"], b["sites"]["1"]["fund_amp"], b["ratio21_fund_only"], *b["w_band"], time.time()-t0), flush=True)
