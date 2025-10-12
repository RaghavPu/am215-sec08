#!/usr/bin/env python3
"""
Extreme Value Distribution Analyzer.

This module provides a class for computing empirical EVDs from
batched sampling of base distributions.
"""

import numpy as np
import matplotlib.pyplot as plt
from distributions import GaussianSampler, ExponentialSampler


class EVDAnalyzer:
    """
    Analyzer for computing and studying extreme value distributions.
    
    This class performs repeated trials of sampling N values from a base
    distribution and recording the maximum in each trial.
    
    Parameters
    ----------
    distribution : BaseDistribution
        The base distribution to sample from
    N : int
        Number of samples per trial
    n_trials : int
        Number of trials (each produces one maximum)
    """
    
    def __init__(self, distribution, N, n_trials=2000):
        self.distribution = distribution
        self.N = N
        self.n_trials = n_trials
        self._maxima = None  # Will be computed lazily
    
    def compute_maxima(self):
        """
        Generate maxima from batched sampling.
        
        For each of n_trials, draw N samples and record the maximum.
        
        TODO: Implement this method.
        Steps:
          1. Sample shape (n_trials, N) from self.distribution
          2. Take the maximum along axis=1 (rowwise max)
          3. Store result in self._maxima
        
        Hint: Use self.distribution.sample(size=...) and np.max(..., axis=1)
        """
        # TODO: Implement batched sampling and max computation
        raise NotImplementedError("Students need to implement compute_maxima()")
    
    @property
    def maxima(self):
        """Lazy evaluation: compute maxima if not already done."""
        if self._maxima is None:
            self.compute_maxima()
        return self._maxima
    
    @property
    def mean_max(self):
        """Mean of the maxima."""
        return np.mean(self.maxima)
    
    @property
    def std_max(self):
        """Standard deviation of the maxima."""
        return np.std(self.maxima, ddof=1)
    
    def plot_histogram(self, bins=50, ax=None, **kwargs):
        """
        Plot histogram of maxima.
        
        Parameters
        ----------
        bins : int
            Number of histogram bins
        ax : matplotlib axis
            Axis to plot on (creates new figure if None)
        **kwargs : dict
            Additional arguments passed to plt.hist
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        ax.hist(self.maxima, bins=bins, density=True, alpha=0.7, 
                edgecolor='k', **kwargs)
        ax.axvline(self.mean_max, color='k', linestyle='--', 
                   label=f'Mean = {self.mean_max:.3f}')
        ax.set_xlabel('Maximum Value')
        ax.set_ylabel('Density')
        ax.legend()
        
        return ax
    
    def __repr__(self):
        return (f"EVDAnalyzer(distribution={self.distribution}, "
                f"N={self.N}, n_trials={self.n_trials})")


def main():
    """Demonstrate EVDAnalyzer with Gaussian and Exponential distributions."""
    
    print("=" * 60)
    print("Extreme Value Distribution Analysis")
    print("=" * 60)
    
    rng = np.random.default_rng(42)
    N = 1000
    n_trials = 4000
    
    # Gaussian base distribution
    print(f"\n1. Gaussian base distribution (N={N}, trials={n_trials})")
    gauss_dist = GaussianSampler(mu=0.0, sigma=1.0, rng=rng)
    gauss_evd = EVDAnalyzer(gauss_dist, N=N, n_trials=n_trials)
    
    print(f"   Computing maxima...")
    print(f"   Mean of maxima: {gauss_evd.mean_max:.3f}")
    print(f"   Std of maxima:  {gauss_evd.std_max:.3f}")
    
    # Exponential base distribution
    print(f"\n2. Exponential base distribution (N={N}, trials={n_trials})")
    expo_dist = ExponentialSampler(scale=1.0, rng=rng)
    expo_evd = EVDAnalyzer(expo_dist, N=N, n_trials=n_trials)
    
    print(f"   Computing maxima...")
    print(f"   Mean of maxima: {expo_evd.mean_max:.3f}")
    print(f"   Std of maxima:  {expo_evd.std_max:.3f}")
    
    # Visualizations
    print("\n3. Creating visualizations...")
    
    # Plot 1: Gaussian EVD vs base distribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    gauss_evd.plot_histogram(ax=axes[0], label='EVD (maxima)', color='skyblue')
    
    # Compare to base distribution
    base_samples = gauss_dist.sample(n_trials)
    axes[0].hist(base_samples, bins=50, density=True, alpha=0.5,
                 label='Base Gaussian', color='salmon', edgecolor='k')
    axes[0].set_title(f'Gaussian: EVD vs Base (N={N})')
    axes[0].legend()
    
    # Plot 2: Exponential EVD vs base distribution
    expo_evd.plot_histogram(ax=axes[1], label='EVD (maxima)', color='lightgreen')
    
    base_samples_exp = expo_dist.sample(n_trials)
    axes[1].hist(base_samples_exp, bins=50, density=True, alpha=0.5,
                 label='Base Exponential', color='orange', edgecolor='k')
    axes[1].set_title(f'Exponential: EVD vs Base (N={N})')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('evd_comparison.png', dpi=300)
    print(f"   Saved: evd_comparison.png")
    
    plt.show()
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

