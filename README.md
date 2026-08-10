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

Nothing above is implemented or validated. This is the map, not the territory.

## Status
**Scaffold.** Engine wired as a submodule; strategy research not yet conducted.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/Carter-Warrens/blaquebaux) is the
base/blueprint and holds the [full family roster](https://github.com/Carter-Warrens/blaquebaux#the-blaque-baux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule -> Carter-Warrens/blaquebaux)
research/   Path-A strategy sketches (to come)
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
