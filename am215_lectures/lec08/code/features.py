from __future__ import annotations

import pandas as pd
import polars as pl

# ----------------------------
# Pandas Feature Engineering
# ----------------------------


def pandas_per_capita_rolling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes per-capita cases and a 7-day rolling mean using Pandas.

    Args:
        df: DataFrame with columns: date, region, subregion, cases, population.

    Returns:
        A new DataFrame with 'per_capita' and 'roll7_per_capita' columns.
    """
    out = df.copy()
    # Ensure date column is in datetime format for proper sorting
    out["date"] = pd.to_datetime(out["date"], utc=False)
    # Sort values to ensure rolling window is applied correctly over time
    out = out.sort_values(["region", "subregion", "date"])
    # Calculate per-capita cases, handling division by zero
    out["per_capita"] = out["cases"] / out["population"].replace({0: pd.NA})
    # Compute 7-day rolling mean of per-capita cases for each group
    out["roll7_per_capita"] = (
        out.groupby(["region", "subregion"], sort=False)["per_capita"]
        .rolling(7)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )
    return out


# ----------------------------
# Polars Feature Engineering
# ----------------------------


def polars_per_capita_rolling(df_pl: pl.DataFrame) -> pl.DataFrame:
    """
    Computes per-capita cases and a 7-row rolling mean using Polars.

    Args:
        df_pl: Polars DataFrame with columns: date, region, subregion, cases, population.

    Returns:
        A new DataFrame with 'per_capita' and 'roll7_per_capita' columns.
    """
    # Chain operations using Polars' expression-based API
    df = df_pl.with_columns(
        [
            # Convert date string to Polars Date type
            pl.col("date").str.strptime(pl.Date, strict=False),
            # Calculate per-capita cases
            (pl.col("cases") / pl.col("population").cast(pl.Float64)).alias(
                "per_capita"
            ),
        ]
    ).sort(["region", "subregion", "date"])  # Ensure order for rolling window

    # Apply a 7-row rolling mean over each group
    df = df.with_columns(
        [
            pl.col("per_capita")
            .group_by(["region", "subregion"])
            .rolling_mean(window_size=7)
            .alias("roll7_per_capita")
        ]
    )
    return df
