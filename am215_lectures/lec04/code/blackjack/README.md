# Blackjack Simulation Module

This module provides a simple object-oriented framework to simulate games of Blackjack. It is designed to be extensible, allowing for different game rules and player strategies to be easily implemented and compared.

## Files

-   `__init__.py`: Marks the directory as a Python package.
-   `deck.py`: Contains the `Card` and `Deck` classes. The `Deck` class is a custom container that implements Python's sequence protocol.
-   `game.py`: Contains the `BlackjackGame` and `JokerBlackjackGame` classes. This demonstrates using classes and inheritance to encapsulate different sets of game rules.
-   `simulation.py`: The main executable script. It defines player/dealer strategies, runs multiple simulation trajectories for different scenarios, and calls the visualization function.
-   `visualize.py`: Contains the `plot_wealth_trajectories` function, which uses `matplotlib` to generate a plot comparing the outcomes of the different simulations.
-   `notes.md`: A document discussing potential performance bottlenecks in the simulation and suggesting remedies for optimization.

## How to Use

This simulation requires `matplotlib` for visualization. It is recommended to use a virtual environment to manage dependencies.

1.  **Create a virtual environment and install dependencies:**
    We recommend using `uv` to create the environment and install packages. From the `am215_lectures/lec04/code/blackjack/` directory, run:
    ```bash
    # Create and activate a virtual environment
    uv venv
    source .venv/bin/activate

    # Install dependencies
    uv pip install -r requirements.txt
    ```

2.  **Run the simulation:**
    From the root directory of the repository, run the simulation script as a module:
    ```bash
    python -m am215_lectures.lec04.code.blackjack.simulation
    ```
    This will execute the main simulation loop, which runs several scenarios (Standard vs. Joker game, Blind vs. Informed strategy) and saves the resulting plot as `blackjack_comparison.png` in the root directory.
