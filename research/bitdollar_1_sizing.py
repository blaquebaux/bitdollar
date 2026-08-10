#!/usr/bin/python3
# =============================================================================
# bitdollar_1_sizing.py — BLAQUE BAUX BITDOLLAR #1 (the keeper: growth-vs-ruin in crypto).
#
# Crypto buy&hold carries ~-77% drawdowns. The base's growth-vs-ruin work says fat tails
# punish naive holding; the fix is trend + vol-target. FINDING: trend (multi-horizon
# 30/60/120 sign) times a vol-target roughly matches/beats buy&hold's return while cutting
# the drawdown from ~-77% to ~-20%. The trend does the heavy lifting (out of the 2022
# winter); the vol-target smooths it. This is the real BitDollar sleeve.
#
# RESULTS AS TESTED (2021-2026, crypto-native ann 365):
#   BTC buy&hold        +0.52 Sharpe  +15% CAGR  -77% DD
#   BTC vol-target      +0.43         +9%        -48%
#   BTC trend+vol-target+0.67         +14%       -26%
#   ETH buy&hold        +0.60  +18%  -79%  |  ETH trend+vol-target +0.83  +19%  -21%
# CAVEAT: ~5.5 years = one crypto cycle. Read-only.
# =============================================================================
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _bitdollar_common import series, metrics, ewma_vol

def voltarget(r, tgt=0.30, cap=2.0):
    sc = np.clip(tgt / np.maximum(ewma_vol(r), 1e-6), 0, cap); return sc[:-1] * r[1:]
def trend_vt(r, tgt=0.30, cap=2.0):
    lvl = np.cumprod(1 + r); sig = np.full(len(r), np.nan)
    for t in range(120, len(r)):
        sig[t] = np.mean([np.sign(lvl[t] / lvl[t - h] - 1) for h in (30, 60, 120)])
    sc = np.clip(tgt / np.maximum(ewma_vol(r), 1e-6), 0, cap); return (sig * sc)[:-1] * r[1:]

print("=" * 72, "\nBITDOLLAR #1 — sizing: buy&hold vs vol-target vs trend (growth-vs-ruin)\n" + "=" * 72)
for nm, sym in [("BTC", "BTC/USD"), ("ETH", "ETH/USD")]:
    _, P, r = series(sym)
    for lab, x in [("buy&hold", r), ("vol-target", voltarget(r)), ("trend+vol-target", trend_vt(r))]:
        m = metrics(x); print(f"  {nm} {lab:<17} Sharpe {m['sh']:+.2f}  CAGR {m['cagr']*100:+.0f}%  maxDD {m['dd']*100:.0f}%")
print("\nVERDICT: trend+vol-target is the keeper — it cuts the ~-77% buy&hold drawdown to")
print("~-20% while keeping the return. Don't hold crypto through the winter; trend-follow it.")
print("(The deployable BTC+ETH blend is in bitdollar_prototype.py.)")
