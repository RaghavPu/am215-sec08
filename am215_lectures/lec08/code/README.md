# AM215 SQL Demo (SQLite → Pandas & Polars, plus DuckDB bonus)

This demo shows a reproducible pipeline:

1) **SQLite**: run a parameterized SQL JOIN (COVID + population) on `(region, subregion)`
2) **Pandas**/**Polars**: compute a **7-day rolling per‑capita rate**
3) Compare time and memory
4) (Bonus) **DuckDB**: query Parquet directly

## Prereqs
- Python 3.10+
- `pip install -r requirements.txt`
- `data/covid.sqlite` present with tables:
  - `covid(date TEXT, region TEXT, subregion TEXT, cases INTEGER, ...)`
  - `population(region TEXT, subregion TEXT, population INTEGER, ...)`

> Dates should be ISO strings like `YYYY-MM-DD`. Ensure `(region, subregion)` pairs match across tables.

### Minimal example to create a DB (optional sketch)
If you don't have `covid.sqlite`, you can create it from CSV/Parquet in your own prep script. The demo assumes it already exists.

## Run
```bash
python demo.py --start 2021-01-01 --end 2021-12-31
```

Optional:

```bash
python duckdb_bonus.py --start 2021-01-01 --end 2021-12-31
```

## Output

* Console table comparing **Pandas vs Polars**: wall time and approximate memory
* A quick head of the engineered features

## Notes

* Rolling window is **7 rows per group** (daily data assumed). If you need calendar-aware rolling (exact 7 days with gaps), adjust in `features.py`.
* The **DuckDB** script shows SQL on Parquet without loading into SQLite.
* We load SQL results to **Pandas** and then convert to **Polars** to keep dependencies minimal and ensure a fair compute comparison. (Direct DB → Polars connectors vary by environment.)
