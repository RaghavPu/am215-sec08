# Demo 3: A Minimal, Correct Package

## Motivation

This demo shows the first step towards a modern, correct Python package. It uses two key best practices:

1.  **`src/` layout:** The package code (`card_games/`) is placed inside a `src/` directory to prevent ambiguous imports.
2.  **`pyproject.toml`:** A minimal configuration file declares the project's name, version, and build system.

This structure is the foundation of a distributable library.

## Commands to Run

From inside the container, navigate to this directory and install the package in "editable" mode.

1.  **Install the package:**
    ```bash
    # You should be in /app
    cd 03_basic_package
    uv pip install -e .
    ```

2.  **Verify the installation:**
    We `cd` to a temporary directory to prove that the package is now importable from anywhere, not just the project root.
    ```bash
    cd /tmp
    python3 -c "from card_games import Deck; print('Successfully imported Deck:', Deck())"
    cd -
    ```

## Expected Output

The installation will be quick, and the verification script will successfully import the `Deck` class, confirming that our package is correctly installed and available in the environment.
