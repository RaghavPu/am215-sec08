#!/usr/bin/env python3
# nba_finals_simulate_from_saved.py
# Uses results saved by calc_residuals.py

import os
import json
import numpy as np
import matplotlib.pyplot as plt


def load_season_summary(season: str):
    """Load per-season mean slopes/variances from results/{season}_summary.json."""
    path = f"results/{season}_summary.json"
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Missing {path}. Run calc_residuals.py first to generate summaries."
        )
    with open(path, "r") as f:
        s = json.load(f)
    # Expected keys: mean_gsw_slope, mean_gsw_variance, mean_cle_slope, mean_cle_variance
    return (
        float(s["mean_gsw_slope"]),
        float(s["mean_gsw_variance"]),
        float(s["mean_cle_slope"]),
        float(s["mean_cle_variance"]),
    )


def simulate_basketball_game(slope_gsw, variance_gsw, slope_cle, variance_cle,
                             duration=2880, time_step=10):
    """
    Random walk with drift (slope) + Gaussian perturbations scaled to time_step.
    - slope_* in points/second
    - variance_* is residual variance (from fitted lines)
    """
    steps = int(duration / time_step)
    gsw_scores = np.zeros(steps)
    cle_scores = np.zeros(steps)
    cumulative_time = np.arange(0, duration, time_step)

    # Distribute total variance across steps (simple heuristic), then per-step scaling
    adjusted_variance_gsw = variance_gsw / steps
    adjusted_variance_cle = variance_cle / steps

    # TODO: Generate random perturbations for GSW and CLE from the normal distribution
    gsw_noise = ___
    cle_noise = ___

    # TODO: Simulate the score progression for both teams
    for t in range(1, steps):
        gsw_scores[t] = ___
        cle_scores[t] = ___

    return cumulative_time, gsw_scores, cle_scores


def save_simulation_plot(cumulative_time, gsw_scores, cle_scores, season: str, out_dir="plots"):
    os.makedirs(out_dir, exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_time, gsw_scores, label="GSW Score", linestyle="-")
    plt.plot(cumulative_time, cle_scores, label="CLE Score", linestyle="--")
    plt.xlabel("Cumulative Time (Seconds)")
    plt.ylabel("Score")
    plt.title(f"Simulated Basketball Game: GSW vs CLE with {season} fits (from saved means)")
    plt.legend()
    plt.tight_layout()
    out_path = os.path.join(out_dir, f"simulated_{season}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved simulation plot: {out_path}")


def main():
    os.makedirs("plots", exist_ok=True)

    # Seasons that were saved by calc_residuals.py
    seasons = ["2014-15", "2015-16"]

    for season in seasons:
        # 1) Load saved mean slopes/variances
        mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var = load_season_summary(season)
        print(f"{season}: loaded means -> "
              f"GSW slope={mean_gsw_slope:.6f}, var={mean_gsw_var:.6f}; "
              f"CLE slope={mean_cle_slope:.6f}, var={mean_cle_var:.6f}")

        # 2) Simulate a game using the loaded means
        cum_t, gsw_sim, cle_sim = simulate_basketball_game(
            mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var, time_step=10
        )

        # 3) Save simulation plot
        save_simulation_plot(cum_t, gsw_sim, cle_sim, season)


if __name__ == "__main__":
    main()
