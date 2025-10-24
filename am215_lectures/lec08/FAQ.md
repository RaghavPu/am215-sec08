# Lecture 8 FAQ - Working with Large Datasets

This document contains answers to common questions that may arise from the "Working with Large Datasets" lecture. It is designed to supplement the lecture by providing deeper explanations and exploring advanced topics.

---

### Storage Formats: The Columnar Revolution

#### Why is Parquet so much better than CSV for analytics?
While CSV is simple and human-readable, it is fundamentally inefficient for analytical work. The performance difference comes down to its **row-oriented** nature versus Parquet's **column-oriented** layout.

-   **Scanning:** Imagine a query that needs to calculate the average of one column in a 100-column table.
    -   With a CSV file, you must read every single byte of the file from start to finish, parsing each row to find the value in the desired column. This is incredibly I/O-intensive.
    -   With a Parquet file, you can read *only the bytes for that one column*, skipping the other 99 columns entirely. This can result in a 100x reduction in I/O.
-   **Type Inference:** A CSV file has no schema. When you run `pd.read_csv()`, Pandas has to spend time and memory scanning the data to guess the data types (`int`, `float`, `str`). This is slow and can be incorrect (e.g., is a zip code a number or a string?). Parquet stores the schema in the file's metadata, so loading is faster and types are guaranteed.
-   **Compression:** Because data in a column is all of the same type (e.g., all integers or all strings), it is highly compressible. Parquet uses efficient, type-aware compression algorithms (like dictionary encoding for strings or delta encoding for sorted integers) that are far more effective than generic text compression on a CSV.

#### What's the difference between Parquet, Feather, and Arrow? When would I use each?
This is a key distinction between in-memory formats and on-disk formats.

-   **Apache Arrow:** This is an **in-memory** specification. It defines a standardized, language-agnostic way to represent columnar data in RAM. Its primary purpose is to enable zero-copy data sharing between different tools (like Polars, DuckDB, and Pandas 2.0+). You don't typically "save" an Arrow object directly, but you use libraries that are built on it.

-   **Parquet:** This is a rich, **on-disk** format designed for long-term, archival storage. It has excellent compression, supports complex nested data types, and stores detailed metadata. It is the industry standard for storing large analytical datasets. **Use Parquet for your final, stored datasets.**

-   **Feather:** This is a simple, lightweight **on-disk** format that is essentially the Arrow in-memory format written directly to disk. It's extremely fast to read and write but lacks the advanced compression and metadata features of Parquet. **Use Feather for temporary storage or for passing data between processes (Inter-Process Communication) where speed is the top priority.**

#### How does "zero-copy" actually work with Arrow?
"Zero-copy" is a bit of a misnomer; it's more accurately "low-copy." The key idea is to avoid the expensive process of **serialization and deserialization**.

Without Arrow, if you wanted to move a DataFrame from Polars to Pandas, the process would be:
1.  **Serialize:** Polars would have to convert its internal data structures into a common intermediate format (like Python objects).
2.  **Copy:** This intermediate data would be copied in memory.
3.  **Deserialize:** Pandas would then have to parse this intermediate format and convert it into its own internal data structures.

This process is slow and memory-intensive.

With Arrow, both Polars and Pandas (with PyArrow backing) understand the same in-memory data layout. When you move data between them, they can simply pass a **pointer** to the underlying block of memory. No conversion is needed. The data itself doesn't move; both libraries just get a new "view" of the same data. This is why it's so fast—it eliminates the costly serialization and deserialization steps.

---

### Compute Engines: Pandas, Polars, and Dask

#### If Polars is so fast, why would I ever use Pandas?
While Polars has a significant performance advantage, Pandas remains a vital tool for several reasons:

1.  **Ecosystem Maturity:** Pandas has been the standard for over a decade and has a massive ecosystem of third-party libraries built on top of it. Many visualization libraries (`seaborn`), statistical modeling libraries, and domain-specific tools integrate directly and seamlessly with Pandas DataFrames.
2.  **Existing Codebases:** The vast majority of existing data science code in the world is written with Pandas. Being able to read, maintain, and contribute to this code is a critical skill.
3.  **Flexibility and Features:** Pandas has a wider range of features for certain niche tasks, especially around time-series analysis with complex frequency offsets and specific indexing needs.
4.  **Learning Curve:** The imperative, eager-execution model of Pandas is often more intuitive for beginners than Polars' lazy, expression-based API.

**Recommendation:** Use Polars for new, performance-critical data wrangling pipelines. Continue to use Pandas when you need its vast ecosystem or when working with existing code. The two can coexist happily in the same project.

#### What is "lazy execution" in Polars and why does it matter?
**Lazy execution** means that when you write a line of Polars code, it doesn't run immediately. Instead, Polars builds up a logical **query plan** of all the operations you want to perform. The computation is only triggered when you explicitly ask for the result (e.g., by calling `.collect()` or `.head()`).

This is powerful because it allows Polars to use a **query optimizer**. Before executing, the optimizer analyzes the entire query plan and looks for ways to make it faster and more memory-efficient.

For example, consider this query:
```python
df.filter(pl.col("value") > 100).select(["id", "name"]).limit(5)
```
-   An **eager** engine (like Pandas) would execute this step-by-step:
    1.  Create a full new DataFrame with all rows where `value > 100`.
    2.  Create another new DataFrame by selecting two columns from the result.
    3.  Create a final DataFrame with the first 5 rows.
-   A **lazy** engine (like Polars) optimizes the plan:
    1.  It sees you only need 5 rows in the end (`limit(5)`).
    2.  It realizes it doesn't need to scan the whole `value` column. It can stop as soon as it finds 5 matching rows.
    3.  It also knows it only needs to read the `id`, `name`, and `value` columns from the source, not all columns.

This optimization, called **predicate pushdown**, dramatically reduces I/O and memory usage.

#### When should I reach for Dask? Is it just for "big data"?
Dask is designed to scale Python code, but it's not just for massive, multi-terabyte datasets on a cluster. It's useful in two main scenarios:

1.  **Larger-than-RAM Data (Out-of-Core):** If you have a single dataset that is too large to fit into your machine's RAM (e.g., a 50 GB file on a laptop with 16 GB of RAM), Dask can process it. It breaks the Dask DataFrame into many smaller Pandas DataFrames (chunks) and processes them sequentially, spilling to disk as needed. This allows you to work with the data on a single machine without crashing.

2.  **Parallelizing Computations (Distributed):** If you have a task that is "pleasantly parallel" (can be broken into independent sub-tasks), Dask can distribute that work across all the cores of your machine or even across multiple machines in a cluster. This can provide significant speedups even for datasets that fit comfortably in memory.

**The Catch:** Dask has overhead. It needs to manage a scheduler and workers, which adds complexity. If your data fits in memory and your problem can be solved efficiently on a single machine, **Polars is almost always a better and simpler choice.** Reach for Dask only when your data is truly too big for one machine's RAM or when you have a computationally intensive, parallelizable task that can benefit from being distributed.

---

### The SQL Layer: SQLite vs. DuckDB

#### Why use SQL at all if Polars is so fast? Can't I just filter in Python?
This comes down to a core principle: **push computation to the data**. The most efficient way to handle large data is to avoid loading data you don't need in the first place.

Even if Polars is extremely fast at filtering a DataFrame that's already in memory, it first has to *get* that data into memory. If your raw data is a 100 GB Parquet file on disk and your query only needs 500 MB of it, it's far more efficient to let a SQL engine read only the required 500 MB from disk.

-   **SQL:** Reduces the data *before* it is loaded into a Python process. This minimizes I/O and dramatically reduces the memory footprint of your Python script.
-   **Polars/Pandas:** Computes on data *after* it has been loaded into memory.

Using a SQL engine like DuckDB to pre-filter, aggregate, and join your data on disk is the most effective memory optimization you can make.

#### What's the real difference between SQLite and DuckDB? They both seem like in-process databases.
While both are "in-process" (they run inside your Python application without a separate server), they are designed for fundamentally different workloads, which is reflected in their architecture.

-   **SQLite** is an **OLTP (Online Transaction Processing)** database. It is **row-oriented**.
    -   It's optimized for writing and retrieving individual rows quickly.
    -   It provides strong ACID guarantees, making it excellent for transactional workloads where data integrity is paramount.
    -   **ACID** stands for **A**tomicity, **C**onsistency, **I**solation, and **D**urability. These properties guarantee that database transactions are processed reliably. For example, atomicity ensures that a transaction either completes fully or not at all, preventing partial updates that could corrupt the data.
    -   Think of it as a tool for building a robust, structured, and reliable dataset.

-   **DuckDB** is an **OLAP (Online Analytical Processing)** database. It is **column-oriented**.
    -   It's optimized for fast analytical queries that scan and aggregate large amounts of data (e.g., `SUM`, `AVG`).
    -   Its key feature is the ability to run complex SQL queries *directly on external files* (Parquet, CSV) without needing to import them first.
    -   Think of it as a high-performance query engine for analysis, not a database for managing transactional data.

#### How do I choose between SQLite and DuckDB for a project?
They are complementary tools, not competitors.

-   Use **SQLite** when you want to create and manage a curated, structured, relational dataset that you control. It's perfect for the "golden" dataset that serves as the single source of truth for a project. The database file itself becomes a versionable, reproducible artifact.

-   Use **DuckDB** when you need to perform fast, ad-hoc analysis on raw data files (like Parquet or CSV) that live on your disk. It's the perfect tool for the exploration and pre-processing phase, where you want to use the power of SQL to quickly slice, dice, and aggregate large files before loading them into a DataFrame.

---

### The Data Pipeline in Practice

#### Why is using `params` in `pd.read_sql` so important? Can't I just use an f-string?
Using f-strings to insert values into a SQL query is one of the most common and dangerous security vulnerabilities, known as **SQL Injection**.

An f-string constructs the final SQL query string *before* sending it to the database. If any part of that string comes from user input, a malicious user can craft that input to change the structure of the query itself.

**The Vulnerable Code:**
```python
user_input = "2021-01-01'; DROP TABLE population; --"
query = f"SELECT * FROM covid WHERE date >= '{user_input}';"
# The final query becomes:
# "SELECT * FROM covid WHERE date >= '2021-01-01'; DROP TABLE population; --';"
conn.executescript(query) # This would delete your table!
```

When you use the `params` argument, you are sending the query template and the values to the database *separately*. The database driver is then responsible for safely inserting the values. It treats the values as data only, never as executable code, completely preventing this entire class of attack. **Always use parameterization.**

#### In the demo, why did you convert from Pandas to Polars instead of reading from SQL directly into Polars?
This was a deliberate choice to ensure a **fair and focused comparison of the compute engines**.

The goal of the demo is to compare the performance of Pandas vs. Polars for the *feature engineering* step (the rolling average calculation). To do this fairly, both engines must start with the exact same data in memory.

By loading the data into Pandas first (`pd.read_sql`) and then converting it to a Polars DataFrame (`pl.from_pandas`), we guarantee that the input is identical. This isolates the performance measurement to just the compute step.

While there are ways to read from a database directly into Polars (e.g., using the `connectorx` library or DuckDB's scanner), these methods can have different performance characteristics and dependencies. The demo's approach keeps the dependencies minimal and the comparison clean.

#### How do I test a function that reads from a database?
As we saw in Lecture 6, unit tests should be fast, reliable, and isolated from external systems. A test that connects to a real database file on disk is an **integration test**, not a unit test.

To unit-test a function that relies on data from a database, you should use **mocking**.
1.  **Isolate Data Access:** Create a dedicated function for data access (e.g., `load_data_from_db()`).
2.  **Mock the Function:** In your test, use `pytest-mock`'s `mocker` fixture to "patch" this function, replacing it with a mock that returns a pre-defined, fake Pandas DataFrame.
3.  **Test Your Logic:** Your analysis function now receives the fake DataFrame, allowing you to test its logic in complete isolation from the database.

```python
# test_analysis.py
def test_feature_engineering(mocker):
    # 1. Create fake data
    fake_df = pd.DataFrame(...)
    # 2. Patch the data access function
    mocker.patch("my_project.db.load_data_from_db", return_value=fake_df)

    # 3. Run the function under test
    result = create_features()
    assert "new_feature" in result.columns
```
For integration tests, you can use an in-memory SQLite database (`sqlite3.connect(":memory:")`) to create a temporary, clean database for each test run.

#### Why store SQL in `.sql` files? Isn't a multi-line string in Python easier?
Storing SQL in dedicated `.sql` files is a critical best practice for creating a maintainable and reproducible data pipeline.

-   **Separation of Concerns:** It cleanly separates your data logic (SQL) from your application logic (Python).
-   **Readability & Tooling:** Your IDE can provide syntax highlighting, formatting, and linting for `.sql` files, making them much easier to read and write than a Python string.
-   **Collaboration:** A data analyst who knows SQL but not Python can easily review and edit the query logic.
-   **Versioning:** Committing a `get_covid_data.sql` file to `git` provides a clear, auditable history of how your dataset was defined and how it changed over time.

Hiding complex SQL inside Python scripts or Jupyter notebooks makes it hard to find, hard to review, and nearly impossible to version control effectively.
