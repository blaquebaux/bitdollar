#!/usr/bin/python3
# =============================================================================
# _bitdollar_common.py — shared helpers for the Blaque Baux BitDollar (crypto) sketches.
# Alpaca crypto (v1beta3, BTC/ETH from 2021, 7-day bars) + stock ETFs (UUP/SPY).
# Reads ALPACA_KEY_ID / ALPACA_SECRET_KEY from env. Read-only.
# NOTE: crypto trades 7 days/week -> annualize crypto-native series with PPY=365;
# use PPY=252 for weekday-aligned (vs UUP/SPY) analysis.
# =============================================================================
import os, json, urllib.request, math
from urllib.parse import quote
import numpy as np

H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
START, END = "2021-01-01", "2026-08-01"
PPY = 365
_cache = {}

def cbars(sym):
    if sym in _cache: return _cache[sym]
    u = ("https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols=" + quote(sym) +
         f"&timeframe=1Day&start={START}&end={END}&limit=10000")
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40)).get("bars", {}).get(sym, [])
    _cache[sym] = {b["t"][:10]: b["c"] for b in d}
    return _cache[sym]

def sbars(sym):
    if sym in _cache: return _cache[sym]
    u = (f"https://data.alpaca.markets/v2/stocks/bars?symbols={sym}&timeframe=1Day"
         f"&start={START}&end={END}&adjustment=all&feed=sip&limit=10000")
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40)).get("bars", {}).get(sym, [])
    _cache[sym] = {b["t"][:10]: b["c"] for b in d}
    return _cache[sym]

def metrics(r, ppy=PPY):
    r = np.asarray(r, float); r = r[np.isfinite(r)]
    if len(r) < 30 or r.std() == 0: return dict(sh=float('nan'), cagr=float('nan'), dd=float('nan'))
    cum = np.cumprod(1 + r)
    return dict(sh=r.mean() / r.std() * math.sqrt(ppy), cagr=cum[-1] ** (ppy / len(r)) - 1,
                dd=(cum / np.maximum.accumulate(cum) - 1).min())

def ewma_vol(r, hl=30, ppy=PPY):
    lam = 0.5 ** (1 / hl); v = r[0] ** 2; o = np.empty(len(r))
    for t in range(len(r)):
        v = r[t] ** 2 if t == 0 else lam * v + (1 - lam) * r[t] ** 2
        o[t] = math.sqrt(max(v, 1e-12)) * math.sqrt(ppy)
    return o

def series(sym):
    b = cbars(sym); ds = sorted(b); P = np.array([b[d] for d in ds]); return ds, P, P[1:] / P[:-1] - 1
