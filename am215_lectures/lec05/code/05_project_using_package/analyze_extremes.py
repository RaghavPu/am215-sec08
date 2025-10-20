import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gumbel_r
from card_games.simulation import (
    run_simulation,
    Deck,
    BlackjackGame,
    blind_player_strategy,
)

# --- Analysis Parameters ---
N_BLOCKS = 100        # Number of blocks of simulations
BLOCK_SIZE = 20       # Number of simulations per block
N_ROUNDS = 100        # Number of rounds per simulation
OUTPUT_FILENAME = "extreme_wealth_distribution.png"

def run_extreme_value_analysis():
    """
    Runs many blocks of blackjack simulations to find the maximum final wealth
    in each block. This generates a distribution of extreme values, which is
    then fitted with a Gumbel distribution.
    """
    print(f"Running {N_BLOCKS} blocks of {BLOCK_SIZE} simulations each...")
    max_wealths = []
    for i in range(N_BLOCKS):
        # For progress indication
        if (i + 1) % 10 == 0:
            print(f"  ... completed block {i + 1}/{N_BLOCKS}")

        block_final_wealths = []
        for _ in range(BLOCK_SIZE):
            # Run a single full simulation trajectory
            history = run_simulation(
                n_rounds=N_ROUNDS,
                deck_factory=Deck,
                game_rules=BlackjackGame,
                player_strategy_fn=blind_player_strategy,
            )
            # Record the final wealth
            block_final_wealths.append(history[-1])
        
        # Find the maximum wealth in the block and store it
        max_wealths.append(max(block_final_wealths))

    max_wealths = np.array(max_wealths)

    # --- Fit Gumbel Distribution ---
    # The Gumbel distribution is used to model the distribution of the maximum
    # (or minimum) of a number of samples of a distribution.
    loc, scale = gumbel_r.fit(max_wealths)
    print(f"\nFitted Gumbel distribution parameters: loc={loc:.2f}, scale={scale:.2f}")

    # --- Plotting ---
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot histogram of the observed maximum wealths
    ax.hist(max_wealths, bins=20, density=True, alpha=0.6, label="Observed Max Final Wealths")

    # Plot the PDF of the fitted Gumbel distribution
    x = np.linspace(max_wealths.min(), max_wealths.max(), 200)
    ax.plot(x, gumbel_r.pdf(x, loc, scale), 'r-', lw=2, label="Fitted Gumbel PDF")

    ax.set_title(f"Distribution of Max Final Wealth (Blocks={N_BLOCKS}, Block Size={BLOCK_SIZE})")
    ax.set_xlabel("Maximum Final Player Wealth in a Block")
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(True)

    fig.savefig(OUTPUT_FILENAME, dpi=150)
    print(f"Plot saved to {OUTPUT_FILENAME}")
    plt.close(fig)


if __name__ == "__main__":
    run_extreme_value_analysis()
