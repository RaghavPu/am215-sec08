#!/usr/bin/env python3
"""
Base distribution classes for sampling.

This module demonstrates object-oriented design for statistical sampling,
using abstract base classes and concrete implementations.
"""

from abc import ABC, abstractmethod
import numpy as np


class BaseDistribution(ABC):
    """
    Abstract base class for probability distributions.
    
    Subclasses must implement the sample() method.
    """
    
    @abstractmethod
    def sample(self, size):
        """
        Draw samples from the distribution.
        
        Parameters
        ----------
        size : int or tuple of ints
            Shape of the output array.
            
        Returns
        -------
        samples : ndarray
            Random samples from the distribution.
        """
        pass
    
    @abstractmethod
    def __repr__(self):
        """String representation of the distribution."""
        pass


class GaussianSampler(BaseDistribution):
    """
    Sampler for Gaussian (Normal) distribution.
    
    Parameters
    ----------
    mu : float
        Mean of the distribution (default: 0.0)
    sigma : float
        Standard deviation (default: 1.0)
    rng : np.random.Generator
        Random number generator instance
    """
    
    def __init__(self, mu=0.0, sigma=1.0, rng=None):
        self.mu = mu
        self.sigma = sigma
        self.rng = rng if rng is not None else np.random.default_rng()
    
    def sample(self, size):
        """Draw samples from Gaussian distribution."""
        return self.rng.normal(loc=self.mu, scale=self.sigma, size=size)
    
    def __repr__(self):
        """String representation of the sampler."""
        return f"GaussianSampler(mu={self.mu}, sigma={self.sigma})"


class ExponentialSampler(BaseDistribution):
    """
    Sampler for Exponential distribution.
    
    Parameters
    ----------
    scale : float
        Scale parameter (mean = scale, default: 1.0)
    rng : np.random.Generator
        Random number generator instance
    """
    
    def __init__(self, scale=1.0, rng=None):
        self.scale = scale
        self.rng = rng if rng is not None else np.random.default_rng()
    
    def sample(self, size):
        """Draw samples from Exponential distribution."""
        return self.rng.exponential(scale=self.scale, size=size)
    
    def __repr__(self):
        return f"ExponentialSampler(scale={self.scale})"


if __name__ == "__main__":
    # Test the samplers
    rng = np.random.default_rng(42)
    
    gauss = GaussianSampler(mu=0.0, sigma=1.0, rng=rng)
    expo = ExponentialSampler(scale=1.0, rng=rng)
    
    print("Testing samplers:")
    print(f"  {gauss}")
    print(f"  {expo}")
    
    gauss_samples = gauss.sample(size=5)
    expo_samples = expo.sample(size=5)
    
    print(f"\nGaussian samples (n=5): {gauss_samples}")
    print(f"Exponential samples (n=5): {expo_samples}")
    print("\nIf you see samples above, TODOs in distributions.py are complete!")

