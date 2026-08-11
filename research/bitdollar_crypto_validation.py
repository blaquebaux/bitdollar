#!/usr/bin/python3
# ============================================================================
# bitdollar_crypto_validation.py — validate the crypto-trend thesis on the REAL crypto rail.
#
# The live driver (bitdollar_live.jl / brash_live.jl) trades SPOT ETF PROXIES (IBIT/ETHA) because the
# engine's order path is equity-only, and the equity-rail validation gate FAILED there (OOS Sharpe
# -0.69) — but those ETFs only exist since 2024, a short, different window. This tests the ACTUAL thesis
# on real BTC/USD + ETH/USD daily bars (Alpaca v1beta3, 2021-2026), causal and net of cost, the same
# signal the driver runs: multi-horizon trend (30/60/120-day sign, long-only) x vol-target, 50/50 blend.
# Crypto trades daily -> annualize with 365.
#
# THE BAR: governed (15% vol-target) OOS net Sharpe >= 0.40 and maxDD shallower than buy&hold.
# Read-only. Keys from env only.  Run:  python research/bitdollar_crypto_validation.py
# ============================================================================
import os, json, math, urllib.request, urllib.parse
import numpy as np
H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}

def crypto_closes(sym):
    u = ("https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols=" + urllib.parse.quote(sym) +
         "&timeframe=1Day&start=2021-01-01&end=2026-08-01&limit=10000")
    b = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40)).get("bars", {}).get(sym, [])
    return {x["t"][:10]: x["c"] for x in b}

BTC, ETH = crypto_closes("BTC/USD"), crypto_closes("ETH/USD")
ds = sorted(set(BTC) & set(ETH))
P = np.array([[BTC[d], ETH[d]] for d in ds], float); R = P[1:] / P[:-1] - 1; T, N = R.shape

def ewma_vol_ann(r, hl=20):
    lam = 0.5 ** (1/hl); v = r[0]**2
    for x in r: v = lam*v + (1-lam)*x**2
    return math.sqrt(max(v, 1e-12)) * math.sqrt(365)

def book(vt, cap_gross, cost=10/1e4):                          # causal walk-forward, net of cost
    wp = np.zeros(N); pnl = []
    for t in range(120, T-1):
        frac = np.array([np.mean([1.0 if (np.prod(1+R[t-h+1:t+1, i])-1) > 0 else 0.0 for h in (30, 60, 120)]) for i in range(N)])
        vol = np.array([ewma_vol_ann(R[:t+1, i]) for i in range(N)])
        w = frac * (vt / np.maximum(vol, 1e-6)) / N
        g = np.abs(w).sum();  w = w * (cap_gross/g) if g > cap_gross else w
        pnl.append(float(w @ R[t+1]) - np.abs(w - wp).sum() * cost); wp = w
    return np.array(pnl)

def met(p):
    p = p[np.isfinite(p)]; s = p.std(); sh = p.mean()/s*math.sqrt(365) if s > 0 else float('nan')
    lvl = np.cumprod(1+p); dd = (lvl/np.maximum.accumulate(lvl)-1).min(); return sh, lvl[-1]**(365/len(p))-1, dd

gov = met(book(0.15, 1.0)); agg = met(book(0.25, 1.5)); bh = met(R[120:].mean(1))
print("="*76, "\nBITDOLLAR/BRASH — crypto-trend validation on the REAL rail (BTC/USD + ETH/USD)\n"+"="*76)
print(f"\n  window {ds[121]} .. {ds[-1]}   ({T-121} days, net 10 bps/side, ann 365)")
print(f"  {'book':32s} {'Sharpe':>7s} {'CAGR':>7s} {'maxDD':>7s}")
print(f"  {'governed trend (15% vol-target)':32s} {gov[0]:+7.2f} {gov[1]*100:+6.0f}% {gov[2]*100:+6.0f}%")
print(f"  {'aggressive trend (brash, 25%/1.5x)':32s} {agg[0]:+7.2f} {agg[1]*100:+6.0f}% {agg[2]*100:+6.0f}%")
print(f"  {'buy & hold (EW BTC+ETH)':32s} {bh[0]:+7.2f} {bh[1]*100:+6.0f}% {bh[2]*100:+6.0f}%")

ok_sh = gov[0] >= 0.40; ok_dd = gov[2] >= bh[2]
print("\n  THE BAR (real crypto rail):")
print(f"    [{'PASS' if ok_sh else 'FAIL'}] governed OOS net Sharpe >= 0.40        {gov[0]:+.2f}")
print(f"    [{'PASS' if ok_dd else 'FAIL'}] drawdown shallower than buy & hold      {gov[2]*100:+.0f}% vs {bh[2]*100:+.0f}%")
print("\n  VERDICT:", "PASS — the thesis holds on real BTC/ETH; the equity-rail FAIL was the ETF proxy, not the edge."
      if (ok_sh and ok_dd) else "MIXED — does not clear even on the real rail.")
print("\n  NOTE: the live drivers trade spot ETFs (IBIT/ETHA) because the engine is equity-only. To trade")
print("  the validated edge, crypto order support (v1beta3) would need wiring into the venue layer.")
