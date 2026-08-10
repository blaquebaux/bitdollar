#!/usr/bin/python3
# =============================================================================
# bitdollar_2_dollar_axis.py — BLAQUE BAUX BITDOLLAR #2 (the namesake thesis, rejected).
#
# The distinctive "BitDollar" idea: crypto trades against the dollar, so the USD/crypto
# axis is a signal. FINDING: rejected. BTC is only mildly anti-dollar (corr ~-0.16 to UUP)
# and is predominantly RISK-ON (corr ~+0.37 to SPY). Timing "long BTC when the dollar
# falls" destroys returns (Sharpe ~0.00, -4% CAGR vs +0.50 buy&hold) — being out of BTC
# during dollar strength misses too much. The dollar relationship is real but too weak
# and unstable to trade; crypto is driven by its own risk-on dynamics, not the dollar.
#
# RESULTS AS TESTED (2021-2026, weekday-aligned, ann 252):
#   corr(BTC, UUP)  -0.16   corr(BTC, SPY)  +0.37
#   long BTC when dollar falling: Sharpe +0.00, CAGR -4%   (vs BTC weekday buy&hold +0.50)
# Read-only.
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _bitdollar_common import cbars, sbars, metrics

btc = cbars("BTC/USD"); uup = sbars("UUP"); spy = sbars("SPY")
wd = sorted(set(btc) & set(uup) & set(spy))
Pb = np.array([btc[d] for d in wd]); U = np.array([uup[d] for d in wd]); Sp = np.array([spy[d] for d in wd])
rb = Pb[1:] / Pb[:-1] - 1; ru = U[1:] / U[:-1] - 1; rs = Sp[1:] / Sp[:-1] - 1
print("=" * 72, "\nBITDOLLAR #2 — the dollar axis (rejected)\n" + "=" * 72)
print(f"  corr(BTC, UUP dollar) {np.corrcoef(rb, ru)[0,1]:+.2f}   corr(BTC, SPY) {np.corrcoef(rb, rs)[0,1]:+.2f}")
lvlU = np.cumprod(1 + ru); dtr = np.full(len(ru), np.nan)
for t in range(60, len(ru)): dtr[t] = lvlU[t] / lvlU[t - 60] - 1
timed = (dtr < 0).astype(float)[:-1] * rb[1:]
print(f"  long BTC when dollar falling: Sharpe {metrics(timed,252)['sh']:+.2f}  CAGR {metrics(timed,252)['cagr']*100:+.0f}%  "
      f"(vs BTC weekday buy&hold {metrics(rb,252)['sh']:+.2f})")
print("\nVERDICT: rejected. BTC is mildly anti-dollar but mostly risk-on beta; dollar-trend")
print("timing loses. The sleeve's edge is crypto trend+vol-target (#1), not the dollar axis.")
print("(Perp funding / basis carry — the other crypto angle — needs exchange data Alpaca lacks.)")
