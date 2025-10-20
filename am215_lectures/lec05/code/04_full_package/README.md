# Demo 4: A Full-Featured Package

## Motivation

This demo showcases a complete, professional Python package with all the features discussed in the lecture:
- Automated versioning via `setuptools-scm` and `git` tags.
- Optional dependencies for development, testing, and plotting.
- A command-line entry point (`run-blackjack-sim`).
- A compiled Cython extension (`fast_rules.pyx`) for performance.
- Bundled data files (`strategies.json`).

## Commands to Run

1.  **Initialize Git and Tag a Release:**
    `setuptools-scm` requires a `git` repository to determine the version.
    ```bash
    # You should be in /app
    cd 04_full_package

    # IMPORTANT: First, ensure a .gitignore file exists to exclude build artifacts.
    # This is crucial for setuptools-scm to generate a clean version number.
    # (The file is provided in this directory).
    git init
    git add .
    git commit -m "Initial commit"
    git tag -a v0.1.0 -m "v0.1.0"
    ```

2.  **Install the Package in Editable Mode:**
    This installs the package and all its optional dependencies.
    ```bash
    uv pip install -e '.[dev,plotting,test]'
    ```

3.  **Build the Distributable Artifacts:**
    To create a portable `manylinux` wheel, we will use a dedicated Docker build container.

    First, build the builder image:
    ```bash
    ./build.sh
    ```

    Now, run the build. This will mount the current directory into the container and run the build command, placing the artifacts in a new `dist/` directory.
    ```bash
    ./run_build.sh
    ls -l dist/
    ```

4.  **Verify the Entry Point and Version:**
    Check that the command-line script was created and that the version was correctly inferred from the `git` tag.
    ```bash
    run-blackjack-sim --help
    python3 -c "import card_games; print(f'Package version: {card_games.__version__}')"
    ```

5.  **Publish to TestPyPI (Optional):**
    This step uploads your package to a public repository so others can install it.

    *Setup on Host Machine (First time only):*
    1. Create a file at `~/.secrets/test-pypi-token`.
    2. Paste your TestPyPI API token into this file.
    The `run.sh` script will securely mount this file into the container and configure `twine` to use it.

    **Canonical Workflow (`twine`):**
    ```bash
    # Assumes `twine` was installed via the `dev` extra
    # Credentials will be picked up automatically from the environment.
    twine upload --repository testpypi dist/*
    ```

    **Streamlined Workflow (`uv`):**
    ```bash
    # uv uses its own UV_PUBLISH_* environment variables, which are also set by run.sh.
    uv publish --publish-url https://test.pypi.org/legacy/ dist/*
    ```
