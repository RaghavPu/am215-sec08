#!/usr/bin/env python3
# nba_finals_series_sim.py
# Simulate ensembles of NBA Finals best-of-7 series using saved slope/variance values.

import os
import json
import numpy as np
from simulate_game import simulate_basketball_game

# ----------- Load season summary results -----------

def load_season_summary(season: str):
    """Load per-season mean slopes/variances from results/{season}_summary.json."""
    path = f"results/{season}_summary.json"
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Missing {path}. Run calc_residuals.py first to generate summaries."
        )
    with open(path, "r") as f:
        s = json.load(f)
    return (
        float(s["mean_gsw_slope"]),
        float(s["mean_gsw_variance"]),
        float(s["mean_cle_slope"]),
        float(s["mean_cle_variance"]),
    )


# ----------- Series simulation -----------
def simulate_7_game_series(slope_gsw, variance_gsw, slope_cle, variance_cle):
    """Simulates a best-of-7 series between GSW and CLE."""
    gsw_wins, cle_wins = 0, 0

    for _ in range(7):
        _, gsw_final, cle_final = simulate_basketball_game(slope_gsw, variance_gsw, slope_cle, variance_cle)
        if gsw_final[-1] > cle_final[-1]:
            gsw_wins += 1
        else:
            cle_wins += 1

        if gsw_wins == 4:
            return "GSW"
        if cle_wins == 4:
            return "CLE"

    return "GSW" if gsw_wins > cle_wins else "CLE"


def simulate_ensemble_of_series(num_series, slope_gsw, variance_gsw, slope_cle, variance_cle):
    """Simulates multiple best-of-7 series and counts how often each team wins."""
    gsw_wins, cle_wins = 0, 0
    for _ in range(num_series):
        winner = simulate_7_game_series(slope_gsw, variance_gsw, slope_cle, variance_cle)
        if winner == "GSW":
            gsw_wins += 1
        else:
            cle_wins += 1
    return gsw_wins, cle_wins

# ----------- Main -----------

def main():
    num_series = 1000
    for season in ["2014-15", "2015-16"]:
        mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var = load_season_summary(season)
        gsw_wins, cle_wins = simulate_ensemble_of_series(
            num_series, mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var
        )
        print(f"\n=== Simulation results for {season} Finals ===")
        print(f"GSW won {gsw_wins} out of {num_series} series ({gsw_wins/num_series:.1%})")
        print(f"CLE won {cle_wins} out of {num_series} series ({cle_wins/num_series:.1%})")

if __name__ == "__main__":
    main()
