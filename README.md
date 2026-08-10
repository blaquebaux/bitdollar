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
**Research: first pass complete; trend+vol-target keeper prototyped, dollar-axis rejected**
(`research/`). No live driver; short (one-cycle) history. Nothing validated to the spine's bar.

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
