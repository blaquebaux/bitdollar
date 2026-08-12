# Blaque Baux BitDollar

**Crypto and the dollar.**

BitDollar is a member of the Blaque Baux family. The [core repo](https://github.com/Carter-Warrens/blaquebaux)
is the **engine and blueprint** — a governed, systematic platform (Julia) with a venue-agnostic
execution controller and a Layer-3 live-money safety gate. BitDollar points that engine in its own
direction and inherits the governance wholesale.

> **Not investment advice.** Educational/research software. Nothing here is validated. See [LICENSE](LICENSE).

```bash
git clone --recursive https://github.com/Carter-Warrens/blaquebaux-bitdollar.git
julia --project=engine -e 'using Pkg; Pkg.instantiate()'   # one-time engine setup
```

## The thesis

A crypto sleeve focused on the USD/crypto axis — BTC/ETH (via spot ETFs or Alpaca crypto) and the dollar-crypto relationship. It overlaps Brash's crypto remit but centers on the currency angle. The base ingests Deribit BTC implied vol as a risk input, and the growth-vs-ruin work governs sizing (crypto's fat tails punish over-leverage).

## Research plan (Path A — not yet built)

- BTC/ETH trend + vol-target — the honest baseline; Deribit vol as a risk input.
- Dollar-crypto axis — DXY vs crypto: a tradeable relationship, or just risk-on/off beta?
- Funding / basis carry — with the negative-skew caveat from the base's carry work.

## Research — first pass done

Full detail in [`research/README.md`](research/README.md). The scorecard:

| # | Question | Verdict |
|---|----------|---------|
| 1 | How to size crypto? | ✅ **keeper** — trend+vol-target (BTC+ETH blend +0.83 Sharpe, −18% DD vs buy&hold −77%) |
| 2 | Is the USD/crypto dollar axis tradeable? | ❌ **rejected** — BTC is risk-on (+0.37 SPY), dollar-timing loses |

**The synthesis:** the keeper is the growth-vs-ruin lesson in crypto — buy&hold eats a
~−77% drawdown, while multi-horizon trend + vol-target keeps the return at ~−20% drawdown
(BTC+ETH blend: **Sharpe +0.83, CAGR +17%, maxDD −18%**, stable across halves). But the
namesake *dollar-axis* thesis is rejected: BTC is only mildly anti-dollar (−0.16 to UUP)
and mostly risk-on beta (+0.37 to SPY); dollar-trend timing destroys returns. So the sleeve
reduces to **governed crypto trend-following** (overlapping Brash). Two honest caveats: the
history is **one crypto cycle** (2021–2026), and crypto is a **risk-on** leg, not a clean
diversifier. Funding/basis carry needs exchange data Alpaca lacks.

## Status
**Research: first pass complete; trend+vol-target keeper — standalone driver built** (`research/` +
`live/`; dollar-axis rejected). `live/bitdollar_live.jl` runs governed crypto trend standalone through
the engine's order path + Layer-3 safety gate: multi-horizon trend × vol-target on spot BTC/ETH ETFs
(IBIT/ETHA), long-only. **Dry-run by default**; graduates to paper with its own isolated keys. Short
(one-cycle) history, risk-on leg; not validated to the spine's bar.

**Validation — the edge is real, the ETF proxy is the problem.** On the equity rail (the spot ETFs
IBIT/ETHA, which only exist since 2024) the walk-forward gate FAILS (OOS Sharpe −0.69). But
[`research/bitdollar_crypto_validation.py`](research/bitdollar_crypto_validation.py) tests the *actual*
thesis on real BTC/USD + ETH/USD (Alpaca v1beta3, 2021–2026, causal, net of cost) and it **PASSES**:
governed trend **+0.72 Sharpe / −12% maxDD** vs buy-and-hold +0.29 / **−76%** — in line with the
research's +0.83. The equity-rail failure was the young ETF proxy, not the edge.

**Crypto execution is now wired** — the engine gained a v1beta3 data provider, a fractional/`gtc`
crypto-mode venue, and a fractional governed rebalance, so [`live/bitdollar_crypto_live.jl`](live/bitdollar_crypto_live.jl)
trades the validated edge on the **real BTC/USD + ETH/USD rail** through the same Layer-3 safety gate +
reconcile as the spine (fractional orders, e.g. 0.05 BTC). **Dry-run by default**; graduates to a
crypto-enabled paper account with its own isolated ledger. This is the deployable form of the edge;
the ETF-proxy driver (`bitdollar_live.jl`) remains for equity-only accounts.
```bash
BB_DRYRUN=1 julia --project=engine live/bitdollar_crypto_live.jl   # real BTC/ETH book, no orders
```
```bash
BB_DRYRUN=1 julia --project=engine live/bitdollar_live.jl
```

## About Blaque Baux

**Blaque Baux** is a quantitative research initiative and a subsidiary of **[Carter Warrens](https://carterwarrens.com)**.
[**BlaqueBaux.com**](https://blaquebaux.com) is the home for the work; the code lives here on GitHub — open to
study, test, and build bespoke strategies on top of.

Anyone can point an AI at a market. The edge is **understanding what the data actually says — and turning it
into something you can act on.** We test relentlessly and put most of it *on the record as rejected, with the
reason*; what survives is built, governed, and validated before it is ever called real. That combination —
honest research, reproducible evidence, and execution you can trust — is why Carter Warrens leads on
**strategy and implementation**, not merely uses the tools everyone now has.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/Carter-Warrens/blaquebaux) is the
base/blueprint and holds the [full family roster](https://github.com/Carter-Warrens/blaquebaux#the-blaque-baux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule -> Carter-Warrens/blaquebaux)
research/   three Path-A sketches (sizing keeper, dollar-axis rejected) + prototype + scorecard
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
