from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Mapping, Optional


DB_PATH = Path("data/covid.sqlite")


def get_sqlite_connection(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database.

    Args:
        db_path: The path to the SQLite database file.

    Returns:
        A sqlite3.Connection object.

    Raises:
        FileNotFoundError: If the database file does not exist.
    """
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"SQLite DB not found at {path!s}")
    # Connect to the database and enable foreign key support
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def read_query(sql: str, params: Optional[Mapping[str, Any]] = None) -> list[tuple]:
    """
    Run a read-only query and return rows as tuples.
    Uses parameter binding to avoid SQL injection.

    Args:
        sql: The SQL query string to execute.
        params: A dictionary of parameters to bind to the query.

    Returns:
        A list of tuples representing the query results.
    """
    with get_sqlite_connection() as conn:
        cursor = conn.execute(sql, params or {})
        rows = cursor.fetchall()
    return rows
