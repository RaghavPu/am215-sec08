from __future__ import annotations

import time

import pandas as pd
import polars as pl


def time_block(fn, *args, **kwargs):
    """Measures the execution time of a function."""
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    dt = time.perf_counter() - t0
    return result, dt


def pandas_mem_bytes(df: pd.DataFrame) -> int:
    """Returns the memory usage of a Pandas DataFrame in bytes."""
    return int(df.memory_usage(deep=True).sum())


def polars_mem_bytes(df: pl.DataFrame) -> int:
    """Returns the estimated memory usage of a Polars DataFrame in bytes."""
    try:
        return int(df.estimated_size())
    except Exception:
        # Fallback for older Polars versions or other issues
        return int(df.to_pandas().memory_usage(deep=True).sum())


def pretty_bytes(n: int) -> str:
    """Converts a number of bytes into a human-readable string (KB, MB, GB)."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def print_comparison(
    pandas_stats: tuple[float, int], polars_stats: tuple[float, int]
):
    """Prints a formatted comparison of Pandas and Polars performance."""
    pt, pm = pandas_stats
    lt, lm = polars_stats
    print("\n=== Compute Comparison (7-day per‑capita) ===")
    print(f"Pandas → time: {pt:.3f}s, mem: {pretty_bytes(pm)}")
    print(f"Polars → time: {lt:.3f}s, mem: {pretty_bytes(lm)}")
