#!/usr/bin/env julia
# ============================================================================
# bitdollar_live.jl — BLAQUE BAUX BITDOLLAR live driver (governed crypto trend).
#
# Runs on the engine (engine/ submodule) — same governed order path + Layer-3 safety gate as the spine.
# SIGNAL (research keeper): governed crypto trend-following. Multi-horizon trend (30/60/120-day sign,
# long-only) times a vol-target on a BTC+ETH blend — the trend takes you OUT of crypto winters, the
# vol-target smooths it. Buy&hold ate a ~-77% drawdown; this cut it to ~-18% at Sharpe +0.83. The
# namesake "trade crypto vs the dollar" angle was a NULL (BTC is risk-on, not anti-dollar).
#
# Traded via SPOT crypto ETFs on the equity rail: IBIT (BTC) + ETHA (ETH). CAVEATS (honest): the ETFs
# are young (since 2024), history is one crypto cycle, and crypto is a RISK-ON leg (+0.37 to SPY) — a
# high-octane return source, not a clean diversifier.
#
# MODES: dry-run by default via the wrapper (BB_DRYRUN=1). Real money needs BB_LIVE_CONFIRM. Kill
# switch: ~/.config/blaquebaux/HALT.  Run: julia --project=engine live/bitdollar_live.jl.  Not validated to the spine's bar.
# ============================================================================
using Dates, Printf, Statistics

const REPO   = normpath(joinpath(@__DIR__, ".."))
const ENGINE = joinpath(REPO, "engine")
for m in ("module_7_execution/module_7_execution.jl","module_10_feedback/module_10_feedback.jl",
          "module_13_portfolio/module_13_portfolio.jl","module_1_data/equity_panel.jl",
          "module_1_data/alpaca_panel.jl","module_8_governance/safety_gate.jl")
    include(joinpath(ENGINE, "src", m))
end
using .ExecutionLayer, .FeedbackLayer, .PortfolioOptModule, .EquityPanel, .AlpacaPanel, .SafetyGate
include(joinpath(ENGINE, "scripts/live_execution.jl"))
include(joinpath(@__DIR__, "_sleeve_main.jl"))

const ASSETS = ["IBIT", "ETHA"]                    # spot BTC + spot ETH ETFs
const UNIVERSE = ASSETS
const LIVE_SENTINEL = "I_UNDERSTAND_THIS_IS_REAL_MONEY"
const VOL_TARGET = 0.15                            # governed (modest) crypto exposure
const CAP_GROSS = 1.0

function ewma_vol_ann(r; hl = 20)
    isempty(r) && return NaN; lam = 0.5^(1/hl); v = float(r[1])^2
    for t in eachindex(r); v = t == 1 ? float(r[t])^2 : lam*v + (1-lam)*float(r[t])^2; end
    sqrt(max(v, 1e-12)) * sqrt(252)
end

"Multi-horizon crypto trend x vol-target, long-only, blended and gross-capped. (Shared by bitdollar/brash.)"
function crypto_trend_target(panel, cap; vol_target, cap_gross)
    syms = panel.symbols; R = panel.returns; T = size(R, 1)
    col(s) = R[:, findfirst(==(s), syms)]; px(s) = panel.prices[findfirst(==(s), syms)]
    net = Dict{String,Float64}(); price = Dict{String,Float64}()
    for a in ASSETS
        r = col(a); frac = mean([(prod(1 .+ r[T-h+1:T]) - 1) > 0 ? 1.0 : 0.0 for h in (30, 60, 120)])
        net[a] = frac * (vol_target / max(ewma_vol_ann(r; hl = 20), 1e-6)) / length(ASSETS); price[a] = px(a)
    end
    g = sum(abs, values(net)); g > cap_gross && for a in keys(net); net[a] *= cap_gross / g; end
    (targets = Dict(a => round(Float64, net[a] * cap / price[a]) for a in ASSETS), prices = price, net = net, gross = sum(abs, values(net)))
end
bitdollar_target(panel, cap) = crypto_trend_target(panel, cap; vol_target = VOL_TARGET, cap_gross = CAP_GROSS)

if abspath(PROGRAM_FILE) == @__FILE__
    sleeve_main(bitdollar_target; label = "bitdollar", signal_id = "bitdollar", regime = "crypto-trend",
        lookback = 220, LIVE_SENTINEL = LIVE_SENTINEL, UNIVERSE = UNIVERSE, REPO = REPO)
end
