#!/usr/bin/env python3
"""
Monte Carlo simulation of a 2D random walk.
This script is the central example for the reproducibility lecture.
"""

import sys
import numpy as np
from scipy.stats import rayleigh
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# --- Environment Reporting ---
def log_environment():
    """Prints key environment details."""
    print("--- Environment ---")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"NumPy version: {np.__version__}")
    try:
        import scipy
        print(f"SciPy version: {scipy.__version__}")
    except ImportError:
        print("SciPy not found")
    print("-------------------")

# --- Simulation ---
def simulate_walks(n_walks, n_steps, rng):
    """Simulates multiple 2D random walks."""
    steps = rng.integers(0, 4, size=(n_walks, n_steps))
    # 0: up, 1: down, 2: left, 3: right
    dx = (steps == 3).astype(int) - (steps == 2).astype(int)
    dy = (steps == 0).astype(int) - (steps == 1).astype(int)
    
    x = np.cumsum(dx, axis=1)
    y = np.cumsum(dy, axis=1)
    
    final_distances = np.sqrt(x[:, -1]**2 + y[:, -1]**2)
    return final_distances

# --- Analysis ---
def analyze_results(distances, output_png="walk_analysis.png"):
    """Analyzes and plots the simulation results."""
    mean_dist = np.mean(distances)
    std_dist = np.std(distances)
    
    print("\n--- Analysis ---")
    print(f"Mean final distance: {mean_dist:.4f}")
    print(f"Std dev of distance: {std_dist:.4f}")
    
    # Compare to Rayleigh distribution
    scale_mle = np.sqrt(np.mean(distances**2) / 2)
    print(f"Rayleigh scale (MLE): {scale_mle:.4f}")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.hist(distances, bins=30, density=True, alpha=0.7, label='Simulated Distances')
    
    x = np.linspace(0, np.max(distances), 200)
    plt.plot(x, rayleigh.pdf(x, scale=scale_mle), 'r-', lw=2, label=f'Rayleigh PDF (scale={scale_mle:.2f})')
    
    plt.title('Distribution of Final Distances in 2D Random Walk')
    plt.xlabel('Final Distance from Origin')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_png)
    print(f"Plot saved to {output_png}")
    print("------------------")

def main():
    """Main function to run the simulation and analysis."""
    log_environment()
    
    # For reproducibility, we use a seeded generator
    # The seed is hardcoded here for demonstration purposes.
    SEED = 42
    rng = np.random.default_rng(SEED)
    print(f"\nUsing random seed: {SEED}")
    
    N_WALKS = 1000
    N_STEPS = 100
    print(f"Simulating {N_WALKS} walks of {N_STEPS} steps each...")
    
    distances = simulate_walks(N_WALKS, N_STEPS, rng)
    analyze_results(distances)

if __name__ == "__main__":
    main()
