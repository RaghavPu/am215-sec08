from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

# Define paths
DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "covid.sqlite"


def create_population_data() -> pd.DataFrame:
    """Creates a dummy population DataFrame."""
    data = {
        "region": ["North", "North", "South", "South", "West"],
        "subregion": ["A", "B", "C", "D", "E"],
        "population": [1_500_000, 2_300_000, 800_000, 3_100_000, 1_200_000],
    }
    return pd.DataFrame(data)


def create_covid_data(pop_df: pd.DataFrame) -> pd.DataFrame:
    """Creates a dummy time-series DataFrame for COVID cases."""
    dates = pd.to_datetime(pd.date_range(start="2021-01-01", end="2021-12-31", freq="D"))
    rng = np.random.default_rng(seed=42)

    all_data = []
    for _, row in pop_df.iterrows():
        # Generate some noisy case data based on population
        base_cases = row["population"] * 0.0001
        noise = rng.integers(-50, 50, size=len(dates))
        trend = np.linspace(0, 100, len(dates))
        cases = np.maximum(0, base_cases + noise + trend).astype(int)

        region_df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "region": row["region"],
                "subregion": row["subregion"],
                "cases": cases,
            }
        )
        all_data.append(region_df)

    return pd.concat(all_data, ignore_index=True)


def main():
    """Generates dummy data and saves it to a SQLite database and Parquet files."""
    print("Creating dummy data for the demo...")

    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)

    # Create dataframes
    pop_df = create_population_data()
    covid_df = create_covid_data(pop_df)

    # Write to Parquet files for the DuckDB bonus script
    pop_df.to_parquet(DATA_DIR / "population.parquet", index=False)
    covid_df.to_parquet(DATA_DIR / "covid.parquet", index=False)

    # Write to SQLite database, replacing tables if they exist
    with sqlite3.connect(DB_PATH) as conn:
        pop_df.to_sql("population", conn, if_exists="replace", index=False)
        covid_df.to_sql("covid", conn, if_exists="replace", index=False)

        # For robustness, add a composite primary key on the population table
        try:
            conn.execute(
                "CREATE UNIQUE INDEX idx_pop_region_subregion ON population (region, subregion);"
            )
        except sqlite3.OperationalError:
            # Index might already exist if script is re-run, which is fine.
            pass

    print(f"Successfully created dummy database at '{DB_PATH}'")
    print(f"Successfully created Parquet files in '{DATA_DIR}/'")
    print(f" - Population table/file: {len(pop_df)} rows")
    print(f" - Covid table/file: {len(covid_df)} rows")


if __name__ == "__main__":
    main()
