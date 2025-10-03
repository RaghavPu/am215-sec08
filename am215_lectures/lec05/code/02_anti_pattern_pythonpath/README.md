# Demo 2: The `PYTHONPATH` Anti-Pattern

## Motivation

This demo shows the `PYTHONPATH` environment variable hack. The `run.sh` script sets this variable before executing the Python script, which allows Python to find and import the `deck` module from the `card_games_lib` directory.

This is an **anti-pattern** because it creates a hidden dependency in the shell environment. It's not declared anywhere in the project's code, making it hard to debug and prone to causing conflicts with other projects.

## Commands to Run

From inside the container, navigate to this directory and run the wrapper script:

```bash
# You should be in /app
cd 02_anti_pattern_pythonpath

./run.sh
```

## Expected Output

The script will run successfully, but only because the `run.sh` wrapper configured the environment correctly. Running `python3 importer_script.py` directly would fail.

```
--- Demo 2: PYTHONPATH hack ---
Successfully imported 'Deck' because PYTHONPATH was set.
Created a deck with 52 cards.
```
