# Demo 5: Using the Package in a Downstream Project

## Motivation

This demo shows the ultimate goal of packaging: reusing your code as a dependency in a separate project. Here, we have a new analysis project that lists our `card_games` package in its `requirements.txt`.

This demonstrates how packaging enables modular, reproducible scientific workflows. The analysis script can simply `import card_games` without needing to know anything about its internal structure.

## Commands to Run

1.  **Create a Virtual Environment and Install Dependencies:**
    We create a new, isolated environment for this downstream project.
    ```bash
    # You should be in /app
    cd 05_project_using_package

    uv venv
    source .venv/bin/activate
    ```

2.  **Install Dependencies:**
    The `requirements.txt` file points to our local `card_games` package, which `pip` will build and install. This serves as a reliable fallback for the demo if publishing to TestPyPI fails.
    ```bash
    uv pip install -r requirements.txt
    ```

    Alternatively, to install the package from public indexes (assuming it was published in the previous step), you can install dependencies in two steps. Since libraries like `numpy` are on PyPI and our package is on TestPyPI, we must install from both.

    First, install the common libraries from the standard PyPI index:
    ```bash
    uv pip install -r requirements.pypi.txt
    ```
    Then, install our package from the TestPyPI index:
    ```bash
    uv pip install --index-url https://test.pypi.org/simple/ -r requirements.testpypi.txt
    ```

3.  **Run the Analysis:**
    Execute the script that uses our library to perform an extreme value analysis.
    ```bash
    python3 analyze_extremes.py
    ```

4.  **Verify the Output:**
    Check that the analysis successfully produced a plot.
    ```bash
    ls -l extreme_wealth_distribution.png
    ```

5.  **View the Plot (Optional):**
    You can use ImageMagick's `display` command to view the generated image.
    ```bash
    display extreme_wealth_distribution.png
    ```
