from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd
import polars as pl

from analysis import (
    pandas_mem_bytes,
    polars_mem_bytes,
    print_comparison,
    time_block,
)
from db import get_sqlite_connection
from features import pandas_per_capita_rolling, polars_per_capita_rolling

SQL_PATH = Path("query.sql")


def load_sql() -> str:
    """Loads the SQL query from the .sql file."""
    return SQL_PATH.read_text(encoding="utf-8")


def main(start: str, end: str):
    """Main function to run and compare the Pandas and Polars pipelines."""
    sql = load_sql()
    params = {"start_date": start, "end_date": end}

    with get_sqlite_connection() as conn:
        # 1) Run the full Pandas pipeline and time it
        df_pd_initial = pd.read_sql_query(sql, conn, params=params)
        pd_feat, pd_time = time_block(pandas_per_capita_rolling, df_pd_initial)
        pd_mem = pandas_mem_bytes(pd_feat)

        # 2) Run the Polars compute step on the same initial data
        pl_feat, pl_time = time_block(polars_per_capita_rolling, pl.from_pandas(df_pd_initial))
        pl_mem = polars_mem_bytes(pl_feat)

    print("--- Pandas Head ---")
    print(pd_feat.head(8).to_string(index=False))
    print("\n--- Polars Head ---")
    print(pl_feat.head(8))

    print_comparison((pd_time, pd_mem), (pl_time, pl_mem))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Compare Pandas and Polars for a feature engineering task."
    )
    ap.add_argument(
        "--start", default="2021-01-01", help="Start date for the query (YYYY-MM-DD)."
    )
    ap.add_argument(
        "--end", default="2021-12-31", help="End date for the query (YYYY-MM-DD)."
    )
    args = ap.parse_args()
    main(args.start, args.end)
