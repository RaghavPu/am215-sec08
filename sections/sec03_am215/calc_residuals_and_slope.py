#!/usr/bin/env python3
# calc_residuals.py
# Requirements: pandas, numpy, matplotlib, seaborn, scipy

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

def get_finals_game_ids(season: str) -> pd.DataFrame:
    """Load Finals games for a season like '2014-15' -> uses '2015'."""
    season_year = season.split('-')[-1]
    fp = f'finals_ids/finals_games_{season_year}.csv'
    if not os.path.isfile(fp):
        raise FileNotFoundError(f"Missing file: {fp}")
    return pd.read_csv(fp)

def get_game_score_progress(game_id: int) -> pd.DataFrame:
    """Load score progression for a specific game_id."""
    fp = f'score_progress/score_progress_{game_id}.csv'
    if not os.path.isfile(fp):
        raise FileNotFoundError(f"Missing file: {fp}")
    df = pd.read_csv(fp)
    return df.dropna(subset=['SCORE'])

# ---------------- core analysis ----------------

def calculate_residual_variance_with_slope(finals_games: pd.DataFrame, season: str):
    """
    Linear fit for each game's score progression (both teams), collect slope & residual variance.
    Returns:
      gsw_data, cle_data, all_gsw_residuals, all_cle_residuals
    """
    gsw_data, cle_data = [], []
    all_gsw_residuals, all_cle_residuals = [], []

    for _, game in finals_games.iterrows():
        game_id = game['GAME_ID']
        game_date = game['GAME_DATE']
        sp = get_game_score_progress(game_id)

        t = sp['CUMULATIVE_TIME']
        scores = sp['SCORE'].astype(str).str.split('-').apply(lambda x: [int(i) for i in x])

        # Only regulation time (<= 2880 sec = 48 min)
        mask = t <= 2880
        t = t[mask].to_numpy()
        gsw = scores.apply(lambda x: x[0])[mask].to_numpy()
        cle = scores.apply(lambda x: x[1])[mask].to_numpy()

        if t.size < 2:
            continue

        # --- TODO: fininsh erform linear regression for GSW, find the slope and the residuals 
        # residuals are the actual score minus the linear fit ---
        slope_gsw, intercept_gsw = ___
        pred_gsw = ___
        resid_gsw = ___

        # --- TODO: Perform linear regression for CLE ---
        slope_cle, intercept_cle = ___
        pred_cle = ___
        resid_cle = ___

        var_gsw = np.var(resid_gsw)
        var_cle = np.var(resid_cle)

        all_gsw_residuals.extend(resid_gsw.tolist())
        all_cle_residuals.extend(resid_cle.tolist())

        gsw_data.append({
            "game_id": int(game_id),
            "game_date": game_date,
            "slope": float(slope_gsw),      # points per second
            "variance": float(var_gsw),     # variance of residuals
        })
        cle_data.append({
            "game_id": int(game_id),
            "game_date": game_date,
            "slope": float(slope_cle),
            "variance": float(var_cle),
        })

    return gsw_data, cle_data, all_gsw_residuals, all_cle_residuals

def summarize_variances(gsw_data, cle_data, season: str):
    """Print summary stats and return means."""
    mean_gsw_slope = np.mean([g["slope"] for g in gsw_data]) if gsw_data else float('nan')
    mean_cle_slope = np.mean([g["slope"] for g in cle_data]) if cle_data else float('nan')
    mean_gsw_var   = np.mean([g["variance"] for g in gsw_data]) if gsw_data else float('nan')
    mean_cle_var   = np.mean([g["variance"] for g in cle_data]) if cle_data else float('nan')

    print(f"\n=== {season} Summary ===")
    print(f"Mean GSW slope: {mean_gsw_slope:.6f} (points/sec)")
    print(f"Mean CLE slope: {mean_cle_slope:.6f} (points/sec)")
    print(f"Mean GSW residual variance: {mean_gsw_var:.6f}")
    print(f"Mean CLE residual variance: {mean_cle_var:.6f}")

    return mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var

# -------- residual histograms with normal overlays (saved to PNG) --------
def plot_residuals_with_normal_fit(gsw_residuals, cle_residuals, mean_variance_gsw, mean_variance_cle, out_png: str):
    """
    Makes a 1x2 plot:
      - Left: GSW residuals histogram with Normal(μ̂, σ̂) overlay
      - Right: CLE residuals histogram with Normal(μ̂, σ̂) overlay
    Saves to out_png.
    """
    std_gsw = float(np.sqrt(mean_variance_gsw)) if np.isfinite(mean_variance_gsw) else np.nan
    std_cle = float(np.sqrt(mean_variance_cle)) if np.isfinite(mean_variance_cle) else np.nan

    if len(gsw_residuals) == 0 and len(cle_residuals) == 0:
        print(f"No residuals to plot for {out_png}. Skipping.")
        return

    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.figure(figsize=(12, 6))

    # --- GSW ---
    plt.subplot(1, 2, 1)
    if len(gsw_residuals) > 0:
        sns.histplot(gsw_residuals, kde=False, bins=30, stat="density", label="GSW Residuals")
        x_gsw = np.linspace(min(gsw_residuals), max(gsw_residuals), 200)
        mu_gsw = float(np.mean(gsw_residuals))
        if np.isfinite(std_gsw) and std_gsw > 0:
            plt.plot(x_gsw, norm.pdf(x_gsw, mu_gsw, std_gsw), '-', lw=2, label='Normal Fit (GSW)')
        plt.title('GSW Residuals and Normal Distribution')
        plt.xlabel('Residuals')
        plt.ylabel('Density')
        plt.legend()
    else:
        plt.text(0.5, 0.5, "No GSW residuals", ha='center', va='center')
        plt.axis('off')

    # --- CLE ---
    plt.subplot(1, 2, 2)
    if len(cle_residuals) > 0:
        sns.histplot(cle_residuals, kde=False, bins=30, stat="density", label="CLE Residuals")
        x_cle = np.linspace(min(cle_residuals), max(cle_residuals), 200)
        mu_cle = float(np.mean(cle_residuals))
        if np.isfinite(std_cle) and std_cle > 0:
            plt.plot(x_cle, norm.pdf(x_cle, mu_cle, std_cle), '-', lw=2, label='Normal Fit (CLE)')
        plt.title('CLE Residuals and Normal Distribution')
        plt.xlabel('Residuals')
        plt.ylabel('Density')
        plt.legend()
    else:
        plt.text(0.5, 0.5, "No CLE residuals", ha='center', va='center')
        plt.axis('off')

    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"Saved plot: {out_png}")

# -------- saving utilities --------
def save_results(season: str, gsw_data, cle_data, gsw_resid, cle_resid,
                 mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var):
    os.makedirs("results", exist_ok=True)

    # Per-game CSVs
    pd.DataFrame(gsw_data).to_csv(f"results/{season}_gsw_games.csv", index=False)
    pd.DataFrame(cle_data).to_csv(f"results/{season}_cle_games.csv", index=False)

    # Residual arrays
    np.save(f"results/{season}_gsw_residuals.npy", np.asarray(gsw_resid, dtype=np.float32))
    np.save(f"results/{season}_cle_residuals.npy", np.asarray(cle_resid, dtype=np.float32))

    # Summary JSON
    summary = {
        "season": season,
        "mean_gsw_slope": float(mean_gsw_slope),
        "mean_gsw_variance": float(mean_gsw_var),
        "mean_cle_slope": float(mean_cle_slope),
        "mean_cle_variance": float(mean_cle_var),
        "n_games_gsw": len(gsw_data),
        "n_games_cle": len(cle_data),
        "n_residuals_gsw": len(gsw_resid),
        "n_residuals_cle": len(cle_resid),
    }
    with open(f"results/{season}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved results to results/ for season {season}")

# ---------------- main ----------------
def main():
    os.makedirs("plots", exist_ok=True)

    for season in ['2014-15', '2015-16']:
        finals_games = get_finals_game_ids(season)
        print(f"Loaded {len(finals_games)} games for season {season}")

        # Compute slopes/variances/residuals
        gsw_data, cle_data, gsw_resid, cle_resid = calculate_residual_variance_with_slope(finals_games, season)
        mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var = summarize_variances(gsw_data, cle_data, season)

        # Plot residual histograms with normal overlays
        out_png = f"plots/residuals_normal_{season}.png"
        plot_residuals_with_normal_fit(gsw_resid, cle_resid, mean_gsw_var, mean_cle_var, out_png)

        # --- NEW: Save all results for later use ---
        save_results(season, gsw_data, cle_data, gsw_resid, cle_resid,
                     mean_gsw_slope, mean_gsw_var, mean_cle_slope, mean_cle_var)

if __name__ == "__main__":
    main()
