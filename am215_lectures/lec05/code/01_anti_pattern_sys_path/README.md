# Demo 1: The `sys.path` Anti-Pattern

## Motivation

This demo shows the `sys.path.append` hack. The `importer_script.py` manually adds its parent directory to Python's path to make the `card_games` library importable.

This is an **anti-pattern** because it creates a fragile, non-portable dependency on a specific local directory structure. It will break if the script is moved or if a collaborator has a different folder layout.

## Commands to Run

From inside the container, navigate to this directory and run the script:

```bash
# You should be in /app
cd 01_anti_pattern_sys_path

python3 importer_script.py
```

## Expected Output

You will see that the script successfully imports the `Deck` class and creates an instance, but it does so using a method that is not robust or reproducible.

```
--- Demo 1: sys.path hack ---
Successfully imported 'Deck' by modifying sys.path.
Created a deck with 52 cards.
```
