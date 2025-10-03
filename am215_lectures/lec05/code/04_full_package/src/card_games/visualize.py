import matplotlib.pyplot as plt


def plot_wealth_trajectories(results, output_filename):
    """
    Plots the wealth trajectories from one or more simulation runs.

    Args:
        results (dict): A dictionary where keys are simulation names (str)
                        and values are lists of lists of wealth history.
        output_filename (str): The path to save the output plot.
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)
    fig.suptitle("Player Wealth Trajectory in Blackjack Simulation", fontsize=16)

    # Separate scenarios into blind and informed
    blind_scenarios = {k: v for k, v in results.items() if "Blind" in k}
    informed_scenarios = {k: v for k, v in results.items() if "Informed" in k}

    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = prop_cycle.by_key()["color"]

    # Plot blind scenarios on the first subplot
    ax1 = axes[0]
    for i, (name, trajectories) in enumerate(blind_scenarios.items()):
        color = colors[i % len(colors)]
        for j, history in enumerate(trajectories):
            label = name if j == 0 else None
            ax1.plot(history, label=label, color=color, lw=1.5, alpha=0.3)
    ax1.set_title("Blind Strategy")
    ax1.set_ylabel("Player Wealth")
    ax1.legend()
    ax1.grid(True)

    # Plot informed scenarios on the second subplot
    ax2 = axes[1]
    for i, (name, trajectories) in enumerate(informed_scenarios.items()):
        color = colors[i % len(colors)]
        for j, history in enumerate(trajectories):
            label = name if j == 0 else None
            ax2.plot(history, label=label, color=color, lw=1.5, alpha=0.3)
    ax2.set_title("Informed Strategy")
    ax2.set_ylabel("Player Wealth")
    ax2.set_xlabel("Round Number")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(output_filename, dpi=300)
    plt.close(fig)
