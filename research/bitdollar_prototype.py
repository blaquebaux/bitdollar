#!/usr/bin/python3
# =============================================================================
# bitdollar_prototype.py — BLAQUE BAUX BITDOLLAR, the keeper as a prototype.
#
# Governed crypto: multi-horizon trend (mean sign of 30/60/120-day) times a vol-target
# on realized crypto vol, on BTC and ETH, blended. The growth-vs-ruin lesson made
# concrete: never buy&hold crypto through the winter — trend-follow with vol-targeting
# turns a -77% drawdown into ~-20% while keeping (or beating) the return.
#
# RESULTS AS TESTED (2021-2026, crypto-native ann 365):
#   BTC  buy&hold +0.52 Sharpe / -77% DD  ->  trend+vol-target +0.67 / -26%
#   ETH  buy&hold +0.60 / -79%            ->  trend+vol-target +0.83 / -21%
#   BTC+ETH blend prototype: reported below (sub-period + corr to SPY)
# CAVEAT: only ~5.5 years = ONE crypto cycle. Short, regime-limited history.
# NOT validated to the spine's bar. Read-only.
# =============================================================================
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _bitdollar_common import series, sbars, metrics, ewma_vol, PPY

def trend_vt(P, r, tgt=0.30, cap=2.0):
    lvl = np.cumprod(1 + r); sig = np.full(len(r), np.nan)
    for t in range(120, len(r)):
        sig[t] = np.mean([np.sign(lvl[t] / lvl[t - h] - 1) for h in (30, 60, 120)])
    sc = np.clip(tgt / np.maximum(ewma_vol(r), 1e-6), 0, cap)
    return (sig * sc)[:-1] * r[1:]

db, Pb, rb = series("BTC/USD"); de, Pe, re = series("ETH/USD")
n = min(len(rb), len(re)); rb, re = rb[-n:], re[-n:]; Pb = Pb[-(n+1):]; Pe = Pe[-(n+1):]
tb = trend_vt(Pb, rb); te = trend_vt(Pe, re)
m = min(len(tb), len(te)); blend = 0.5 * tb[-m:] + 0.5 * te[-m:]

print("=" * 72, "\nBITDOLLAR prototype — multi-horizon trend + vol-target (BTC+ETH blend)\n" + "=" * 72)
b = metrics(blend); h = len(blend) // 2
print(f"  BTC+ETH blend: Sharpe {b['sh']:+.2f}  CAGR {b['cagr']*100:+.0f}%  maxDD {b['dd']*100:.0f}%")
print(f"  sub-periods:   first half {metrics(blend[:h])['sh']:+.2f}  second half {metrics(blend[h:])['sh']:+.2f}")
print(f"  vs BTC buy&hold {metrics(rb)['sh']:+.2f}/{metrics(rb)['dd']*100:.0f}%DD, ETH B&H {metrics(re)['sh']:+.2f}/{metrics(re)['dd']*100:.0f}%DD")
# corr to SPY (weekday-aligned) — is crypto a diversifier or just risk-on?
btcd = dict(zip(db[1:], rb)); spb = sbars("SPY"); sds = sorted(spb)
spc = np.array([spb[d] for d in sds]); spr = {d: v for d, v in zip(sds[1:], spc[1:] / spc[:-1] - 1)}
common = sorted(set(btcd) & set(spr)); a = np.array([btcd[d] for d in common]); x = np.array([spr[d] for d in common])
print(f"  corr(BTC, SPY) {np.corrcoef(a, x)[0,1]:+.2f}  -> risk-on beta; a high-octane leg, partial diversifier")
print("\nread: crypto trend+vol-target is the real BitDollar sleeve (the growth-vs-ruin")
print("lesson: don't hold through the winter). But it is short-history (one cycle) and")
print("risk-on (corr ~+0.4 to SPY), not a clean diversifier. The dollar-axis thesis that")
print("named this sleeve is rejected (bitdollar_2).")
