#!/usr/bin/env python3
"""
Analyze how mean and standard deviation of maxima scale with sample size N.

Theory predicts that for Gaussian samples, the mean of maxima scales
approximately as σ√(log N).
"""

import numpy as np
import matplotlib.pyplot as plt
from distributions import GaussianSampler
from evd_analyzer import EVDAnalyzer


def analyze_scaling(distribution, Ns, n_trials=1500):
    """
    Compute mean and std of maxima for different sample sizes.
    
    Parameters
    ----------
    distribution : BaseDistribution
        Base distribution to sample from
    Ns : array-like
        Array of sample sizes to test
    n_trials : int
        Number of trials for each N
        
    Returns
    -------
    means : ndarray
        Mean of maxima for each N
    stds : ndarray
        Standard deviation of maxima for each N
    """
    means = []
    stds = []
    
    print(f"Analyzing scaling for {len(Ns)} different sample sizes...")
    print(f"(Each with {n_trials} trials)\n")
    
    for i, N in enumerate(Ns):
        print(f"  [{i+1}/{len(Ns)}] N = {N:>8,} ...", end=" ")
        
        analyzer = EVDAnalyzer(distribution, N=N, n_trials=n_trials)
        
        means.append(analyzer.mean_max)
        stds.append(analyzer.std_max)
        
        print(f"mean = {analyzer.mean_max:.3f}, std = {analyzer.std_max:.3f}")
    
    return np.array(means), np.array(stds)


def plot_scaling(Ns, means, stds, distribution_name=""):
    """Create three plots showing scaling behavior."""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # Plot 1: Mean vs N (log scale)
    axes[0].plot(Ns, means, 'o-', markersize=6)
    axes[0].set_xscale('log')
    axes[0].set_xlabel('Sample size N (log scale)')
    axes[0].set_ylabel('Mean of maxima')
    axes[0].set_title(f'{distribution_name}: Mean vs N')
    axes[0].grid(alpha=0.3)
    
    # Plot 2: Std vs N (log scale)
    axes[1].plot(Ns, stds, 'o-', markersize=6, color='orange')
    axes[1].set_xscale('log')
    axes[1].set_xlabel('Sample size N (log scale)')
    axes[1].set_ylabel('Std of maxima')
    axes[1].set_title(f'{distribution_name}: Std vs N')
    axes[1].grid(alpha=0.3)
    
    # Plot 3: Mean vs sqrt(log(N)) with linear fit
    x = np.sqrt(np.log(Ns))
    y = means
    
    # Linear fit: y = a*x + b
    A = np.vstack([x, np.ones_like(x)]).T
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]
    
    axes[2].plot(x, y, 'o', markersize=6, label='Empirical')
    
    # Plot fit line
    x_fit = np.linspace(x.min(), x.max(), 100)
    y_fit = a * x_fit + b
    axes[2].plot(x_fit, y_fit, '-', linewidth=2, 
                 label=f'Fit: {a:.3f}√(log N) + {b:.3f}')
    
    axes[2].set_xlabel(r'$\sqrt{\log N}$')
    axes[2].set_ylabel('Mean of maxima')
    axes[2].set_title(f'{distribution_name}: Mean ~ √(log N)')
    axes[2].legend()
    axes[2].grid(alpha=0.3)
    
    plt.tight_layout()
    
    return fig, (a, b)


def main():
    """Main analysis routine."""
    
    print("=" * 70)
    print("Scaling Analysis: How mean and std of maxima depend on sample size")
    print("=" * 70)
    print()
    
    # Setup
    rng = np.random.default_rng(42)
    gauss = GaussianSampler(mu=0.0, sigma=1.0, rng=rng)
    
    # Sample sizes from ~10 to ~1,000,000
    Ns = np.unique(np.round(np.logspace(1, 6, 10)).astype(int))
    n_trials = 1500
    
    print(f"Distribution: {gauss}")
    print(f"Sample sizes: {len(Ns)} values from {Ns[0]:,} to {Ns[-1]:,}")
    print(f"Trials per size: {n_trials:,}")
    print()
    
    # Run analysis
    means, stds = analyze_scaling(gauss, Ns, n_trials=n_trials)
    
    # Create plots
    print("\nCreating plots...")
    fig, (a, b) = plot_scaling(Ns, means, stds, distribution_name="Gaussian")
    
    print(f"\nFitted scaling: mean ≈ {a:.3f} * sqrt(log N) + {b:.3f}")
    print("(For standard Gaussian, theory predicts a ≈ √2 ≈ 1.414)")
    
    # Save figure
    output_file = 'scaling_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {output_file}")
    
    plt.show()
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary:")
    print("  - Mean of maxima grows logarithmically with N")
    print("  - Mean ~ sqrt(log N) fits well (see right plot)")
    print("  - Std remains roughly constant (slowly varying)")
    print("=" * 70)


if __name__ == "__main__":
    main()

