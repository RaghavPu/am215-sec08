#!/usr/bin/env python3
# plot_finals_score_progress.py

import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt

nba_team_ids = {
    "CLE": {"team_id": 1610612739, "team_name": "Cleveland Cavaliers"},
    "GSW": {"team_id": 1610612744, "team_name": "Golden State Warriors"},
}


def get_finals_game_ids(team_id_1: int, team_id_2: int, season: str) -> pd.DataFrame:
    season_year = season.split('-')[-1]
    finals_games_file = f'finals_ids/finals_games_{season_year}.csv'
    if not os.path.isfile(finals_games_file):
        raise FileNotFoundError(f"Missing file: {finals_games_file}")
    return pd.read_csv(finals_games_file)


def get_game_score_progress(game_id: int) -> pd.DataFrame:
    score_progress_file = f'score_progress/score_progress_{game_id}.csv'
    if not os.path.isfile(score_progress_file):
        raise FileNotFoundError(f"Missing file: {score_progress_file}")
    df = pd.read_csv(score_progress_file)
    return df.dropna(subset=['SCORE'])


def plot_all_games_score_progress(finals_games: pd.DataFrame, team_code_1: str, team_code_2: str, season: str):
    plt.figure(figsize=(10, 6))
    color_cycle = itertools.cycle(plt.cm.tab10.colors)

    game_years = pd.to_datetime(finals_games['GAME_DATE']).dt.year
    start_year = int(game_years.min())
    end_year = int(game_years.max())

    team_name_1 = nba_team_ids[team_code_1]['team_name']
    team_name_2 = nba_team_ids[team_code_2]['team_name']

    if start_year == end_year:
        title = f'Score Progression of {start_year} NBA Finals Games ({team_name_1} vs {team_name_2})'
    else:
        title = f'Score Progression of {start_year}-{end_year} NBA Finals Games ({team_name_1} vs {team_name_2})'

    for _, game in finals_games.iterrows():
        game_id = int(game['GAME_ID'])
        game_date = game['GAME_DATE']

        score_progress = get_game_score_progress(game_id)
        scores = score_progress['SCORE'].astype(str).str.split('-').apply(lambda x: [int(i) for i in x])
        team1_scores = scores.apply(lambda x: x[0])
        team2_scores = scores.apply(lambda x: x[1])
        cum_time = score_progress['CUMULATIVE_TIME']

        c = next(color_cycle)
        plt.plot(cum_time, team1_scores, label=f"{team_code_1} - {game_date}", color=c, linestyle='-')
        plt.plot(cum_time, team2_scores, label=f"{team_code_2} - {game_date}", color=c, linestyle='--')

    plt.xlabel('Cumulative Time (Seconds)')
    plt.ylabel('Score')
    plt.title(title)
    plt.legend()
    plt.tight_layout()

    # --- Save instead of show ---
    os.makedirs("plots", exist_ok=True)
    out_file = f"plots/score_progress_{season}.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Saved plot to {out_file}")


def main():
    GSW_TEAM_ID = nba_team_ids["GSW"]["team_id"]
    CLE_TEAM_ID = nba_team_ids["CLE"]["team_id"]

    for season in ['2014-15', '2015-16']:
        finals_games = get_finals_game_ids(GSW_TEAM_ID, CLE_TEAM_ID, season)
        print(f"Loaded {len(finals_games)} games for season {season}")
        plot_all_games_score_progress(finals_games, "GSW", "CLE", season)


if __name__ == "__main__":
    main()
