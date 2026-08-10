# Blaque Baux BitDollar — research

First-pass Path-A research on the crypto sleeve. Alpaca crypto (BTC/ETH, 7-day bars from
2021) + stock ETFs (UUP/SPY). Read-only. Crypto-native series annualize at 365; the
dollar-axis (weekday-aligned) at 252.

```bash
export $(grep -v '^#' ~/.config/blaquebaux/alpaca.env | xargs)   # or source it
python research/bitdollar_1_sizing.py       # the keeper
python research/bitdollar_2_dollar_axis.py  # the rejected namesake thesis
```

## Scorecard

| # | Question | Result | Verdict |
|---|----------|--------|---------|
| 1 | How to size crypto (buy&hold vs trend+vol-target)? | B&H +0.52/−77% → **trend+vt +0.67/−26%** (BTC); ETH → +0.83/−21% | ✅ the keeper |
| 2 | Is the USD/crypto dollar axis tradeable? | corr −0.16 to UUP, +0.37 to SPY; timing loses (0.00 vs +0.50) | ❌ rejected |
| — | Diversifier value? | corr +0.37 to SPY (risk-on) | 🟡 partial |
| — | Funding/basis carry? | needs exchange data | ⚪ data gap |

## The synthesis

- **#1 is the keeper — the growth-vs-ruin lesson in crypto.** Buy-and-holding crypto means
  eating a ~−77% drawdown. Multi-horizon trend (30/60/120-day sign) times a vol-target
  matches or beats the buy&hold return while cutting the drawdown to ~−20%. The **trend**
  does the heavy lifting (it takes you out of the 2022 winter); the vol-target smooths it.
  The deployable **BTC+ETH blend** (`bitdollar_prototype.py`): **Sharpe +0.83, CAGR +17%,
  maxDD −18%**, sub-period stable (+0.59 / +1.02).

- **#2 rejects the namesake thesis.** The "BitDollar" idea — trade crypto against the dollar
  — does not hold. BTC is only mildly anti-dollar (−0.16 to UUP) and is predominantly
  **risk-on** (+0.37 to SPY); timing "long BTC when the dollar falls" destroys returns
  (Sharpe 0.00 vs +0.50 buy&hold). The relationship is real but too weak and unstable to
  trade; crypto is driven by its own risk-on dynamics, not the dollar.

**So the sleeve reduces to governed crypto trend-following** — real, but it overlaps Brash's
crypto remit, and the distinctive dollar angle that named it is a null. Two honest caveats:
the history is **one crypto cycle** (2021–2026 only), and crypto is a **risk-on** leg
(+0.37 to SPY), so it's a high-octane return source, not a clean diversifier like Bore/Bounce.

## Files
- `_bitdollar_common.py` — shared crypto/stock fetch + metrics (365/252 annualization).
- `bitdollar_1_sizing.py` — buy&hold vs vol-target vs trend+vol-target (the keeper).
- `bitdollar_2_dollar_axis.py` — the rejected USD/crypto dollar-axis thesis.
- `bitdollar_prototype.py` — the deployable BTC+ETH trend+vol-target blend.
