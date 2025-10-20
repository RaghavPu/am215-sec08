#!/usr/bin/env python3
"""
Gumbel distribution fitting and visualization.

Demonstrates universality: different base distributions lead to the same
EVD shape after standardization.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from distributions import GaussianSampler, ExponentialSampler
from evd_analyzer import EVDAnalyzer


class GumbelFitter:
    """
    Fit Gumbel distribution to data and provide utilities.
    
    Parameters
    ----------
    data : array-like
        Data to fit (typically maxima from repeated sampling)
    fit_type : str
        Either 'right' (gumbel_r, for maxima) or 'left' (gumbel_l, for minima)
    """
    
    def __init__(self, data, fit_type='right'):
        self.data = np.asarray(data)
        self.fit_type = fit_type
        
        # Fit using scipy
        if fit_type == 'right':
            self.loc, self.scale = stats.gumbel_r.fit(data)
            self._dist = stats.gumbel_r(loc=self.loc, scale=self.scale)
        elif fit_type == 'left':
            self.loc, self.scale = stats.gumbel_l.fit(data)
            self._dist = stats.gumbel_l(loc=self.loc, scale=self.scale)
        else:
            raise ValueError("fit_type must be 'right' or 'left'")
    
    def pdf(self, x):
        """Evaluate Gumbel PDF at points x."""
        return self._dist.pdf(x)
    
    def cdf(self, x):
        """Evaluate Gumbel CDF at points x."""
        return self._dist.cdf(x)
    
    def plot_fit(self, ax=None, bins=50, data_label='Data', fit_label='Gumbel Fit'):
        """
        Plot histogram of data with fitted Gumbel overlay.
        
        TODO: Complete this method
        Steps:
          1. Create histogram of self.data (density=True, alpha=0.6)
          2. Create x values spanning data range with some padding
          3. Evaluate self.pdf(x) and plot as a line
        
        Hint: Use ax.hist(..., density=True) and ax.plot(x, self.pdf(x))
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        # TODO: Implement the visualization
        raise NotImplementedError("Students need to implement plot_fit()")
    
    def __repr__(self):
        return f"GumbelFitter(loc={self.loc:.3f}, scale={self.scale:.3f}, type='{self.fit_type}')"


def standardize(data):
    """Convert data to z-scores (mean=0, std=1)."""
    return (data - np.mean(data)) / np.std(data, ddof=1)


def demonstrate_universality():
    """
    Show that Gaussian and Exponential maxima have the same EVD shape
    after standardization.
    """
    print("=" * 70)
    print("Demonstrating Universality of Extreme Value Distributions")
    print("=" * 70)
    print()
    
    rng = np.random.default_rng(42)
    N = 2000
    n_trials = 4000
    
    print(f"Setup: N={N} samples per trial, {n_trials} trials\n")
    
    # Generate maxima from two different base distributions
    print("1. Generating maxima from Gaussian distribution...")
    gauss = GaussianSampler(mu=0.0, sigma=1.0, rng=rng)
    gauss_evd = EVDAnalyzer(gauss, N=N, n_trials=n_trials)
    gauss_maxima = gauss_evd.maxima
    print(f"   Mean: {gauss_evd.mean_max:.3f}, Std: {gauss_evd.std_max:.3f}")
    
    print("\n2. Generating maxima from Exponential distribution...")
    expo = ExponentialSampler(scale=1.0, rng=rng)
    expo_evd = EVDAnalyzer(expo, N=N, n_trials=n_trials)
    expo_maxima = expo_evd.maxima
    print(f"   Mean: {expo_evd.mean_max:.3f}, Std: {expo_evd.std_max:.3f}")
    
    # Standardize
    print("\n3. Standardizing to z-scores...")
    z_gauss = standardize(gauss_maxima)
    z_expo = standardize(expo_maxima)
    
    # Plot 1: Universality (z-score collapse)
    print("\n4. Plotting z-score distributions (should overlap)...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    axes[0].hist(z_gauss, bins=40, density=True, alpha=0.6, 
                 edgecolor='k', label='Gaussian base', color='skyblue')
    axes[0].hist(z_expo, bins=40, density=True, alpha=0.6, 
                 edgecolor='k', label='Exponential base', color='lightcoral')
    axes[0].set_xlabel('Z-score')
    axes[0].set_ylabel('Density')
    axes[0].set_title('Universality: Z-score Collapse')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Plot 2: Fitted Gumbel distributions (on raw scale)
    print("5. Fitting Gumbel distributions to raw maxima...")
    gumbel_gauss = GumbelFitter(gauss_maxima, fit_type='right')
    gumbel_expo = GumbelFitter(expo_maxima, fit_type='right')
    
    print(f"   Gaussian maxima: {gumbel_gauss}")
    print(f"   Exponential maxima: {gumbel_expo}")
    
    # Plot both on same axes
    x_min = min(gauss_maxima.min(), expo_maxima.min())
    x_max = max(gauss_maxima.max(), expo_maxima.max())
    x = np.linspace(x_min, x_max, 400)
    
    axes[1].hist(gauss_maxima, bins=40, density=True, alpha=0.4, 
                 edgecolor='k', label='Gaussian maxima', color='skyblue')
    axes[1].hist(expo_maxima, bins=40, density=True, alpha=0.4, 
                 edgecolor='k', label='Exponential maxima', color='lightcoral')
    
    axes[1].plot(x, gumbel_gauss.pdf(x), linewidth=2, 
                 label='Gumbel fit (Gauss)', color='blue')
    axes[1].plot(x, gumbel_expo.pdf(x), linewidth=2, 
                 label='Gumbel fit (Expo)', color='red')
    
    axes[1].set_xlabel('Maximum value (raw scale)')
    axes[1].set_ylabel('Density')
    axes[1].set_title('Gumbel Fits to Different Base Distributions')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    
    output_file = 'gumbel_universality.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {output_file}")
    
    plt.show()
    
    print("\n" + "=" * 70)
    print("Key Observations:")
    print("  - After standardization, different bases → same EVD shape")
    print("  - Gumbel distribution fits both well (Fisher-Tippett theorem)")
    print("  - This is universality: coarse-grained behavior independent of details")
    print("=" * 70)


def main():
    demonstrate_universality()


if __name__ == "__main__":
    main()

