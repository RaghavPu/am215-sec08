# Lecture 7 Code Example: Complete Mini-Project

This directory contains a small, complete Python project that demonstrates how to integrate all the code quality tools discussed in the lecture: `ruff`, `ty`, `pytest`, `sphinx`, and `nox`.

## Project Structure

-   `pyproject.toml`: The central configuration file for the project and all tools.
-   `src/my_package/`: The Python source code for the package.
-   `tests/`: The test suite.
-   `docs/`: The documentation source files.
-   `noxfile.py`: A script for automating local quality checks.

## How to Use This Example

### 1. Setup

First, set up a virtual environment and install the project with all its development dependencies. From inside the `02_complete_project` directory:

```bash
# Create and activate a virtual environment using uv
uv venv
source .venv/bin/activate

# Install dependencies using uv
# 'test' for pytest, 'dev' for nox.
# The 'demo' group installs ruff, ty, and sphinx so you can run them manually.
uv pip install -e '.[test,dev,demo]'
```

### 2. Demonstrating the Tools

The source code in `src/my_package/main.py` contains deliberate errors that our tools will catch.

#### `ruff` (Linter and Formatter)

Run `ruff` to check for linting errors. It will find the unused `os` import and the dangerous mutable default argument in `append_to`.

```bash
ruff check src/
```

You can also use `ruff` to check formatting. (Note: The code is already formatted, so this command will pass silently).

```bash
ruff format --check src/
```

#### `ty` (Type Checker)

Run `ty` to check for static type errors. It will find that the `get_user_id` function incorrectly returns a string instead of an integer.

```bash
ty src/
```

#### `pytest` (Testing)

Run `pytest` to execute the test suite.

```bash
pytest
```

#### `sphinx` (Documentation)

Run `sphinx-build` to generate the HTML documentation. For a better development experience, use `sphinx-autobuild` which starts a live-reloading web server.

```bash
# This will build the docs, start a server, and open it in your browser.
# It will automatically rebuild when you change source files.
sphinx-autobuild docs/source docs/_build/html
```

Press `Ctrl+C` to stop the server.

### 3. Automating Local Checks with `nox`

The `noxfile.py` automates all the steps above. It runs each check in a clean, isolated environment, just like a CI server would.

To run all the quality checks with a single command, simply run `nox`:

```bash
nox
```

You can also run a specific session, for example, just the linter:

```bash
nox -s lint
```
