from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import polars as pl

# Define paths to the Parquet files
COVID_PATH = Path("data/covid.parquet")
POP_PATH = Path("data/population.parquet")


def main(start: str, end: str):
    """
    Demonstrates running a SQL query directly on Parquet files using DuckDB.
    """
    if not COVID_PATH.exists() or not POP_PATH.exists():
        raise FileNotFoundError(
            "Place covid.parquet and population.parquet at data/ for this demo."
        )

    # DuckDB can query files directly without a persistent database
    query = """
        SELECT r.date, r.region, r.subregion, r.cases, p.population
        FROM read_parquet(?) AS r
        JOIN read_parquet(?) AS p
          ON r.region = p.region AND r.subregion = p.subregion
        WHERE r.date BETWEEN ? AND ?
        ORDER BY r.region, r.subregion, r.date
    """
    params = [str(COVID_PATH), str(POP_PATH), start, end]

    # Execute the query and return a Polars DataFrame directly (zero-copy)
    df_pl = duckdb.execute(query, params).pl()

    print("--- DuckDB → Polars Head (Zero-Copy) ---")
    print(df_pl.head())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Demonstrate DuckDB querying Parquet files."
    )
    ap.add_argument(
        "--start", default="2021-01-01", help="Start date for the query (YYYY-MM-DD)."
    )
    ap.add_argument(
        "--end", default="2021-12-31", help="End date for the query (YYYY-MM-DD)."
    )
    args = ap.parse_args()
    main(args.start, args.end)
