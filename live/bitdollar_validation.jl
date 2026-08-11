#!/usr/bin/env julia
# bitdollar_validation.jl — validate-before-live gate for the BITDOLLAR sleeve (walk-forward / OOS / net-of-cost).
# Reuses bitdollar_target from bitdollar_live.jl. Run:  julia --project=engine live/bitdollar_validation.jl
include(joinpath(@__DIR__, "bitdollar_live.jl"))
include(joinpath(@__DIR__, "_sleeve_validation.jl"))
validate_sleeve(bitdollar_target; label = "BITDOLLAR", universe = UNIVERSE, warmup = 150, kind = :directional)
