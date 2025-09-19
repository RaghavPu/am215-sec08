#!/usr/bin/env python3
"""
Demonstrate proper reproducibility practices.
This script shows the RIGHT way to handle randomness.
"""

import numpy as np

def stable_computation():
    """A computation that gives reproducible results."""
    
    print("=== Reproducibility Success Demo ===\n")
    
    # Solution: Use Generator with explicit seed
    print("1. Random sampling WITH proper seed:")
    for i in range(3):
        rng = np.random.default_rng(42)  # Same seed each time
        values = rng.normal(0, 1, 5)
        print(f"   Run {i+1}: mean = {values.mean():.6f}")
    
    print("\n2. Same computation, SAME results:")
    results = []
    for i in range(3):
        rng = np.random.default_rng(123)  # Consistent seed
        samples = rng.exponential(2.0, 1000)
        estimate = samples.mean()
        results.append(estimate)
        print(f"   Run {i+1}: λ estimate = {estimate:.6f}")
    
    variation = (max(results) - min(results)) / np.mean(results) * 100
    print(f"   Variation: {variation:.2f}%")
    
    # Solution: Independent generators don't interfere
    print("\n3. Independent random streams:")
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(99)  # Someone else's generator
    
    print(f"   Generator 1: {rng1.random():.6f}")
    _ = rng2.random()  # Someone else uses their generator
    print(f"   Generator 1 again: {rng1.random():.6f}")
    print("   (Unaffected by other generators!)")
    
    # Best practice: Pass RNG to functions
    print("\n4. Best practice - passing RNG:")
    
    def monte_carlo_pi(n_samples, rng=None):
        """Estimate π using Monte Carlo."""
        if rng is None:
            rng = np.random.default_rng()
        
        x = rng.uniform(-1, 1, n_samples)
        y = rng.uniform(-1, 1, n_samples)
        inside = np.sum(x**2 + y**2 <= 1)
        return 4 * inside / n_samples
    
    # Reproducible calls
    rng = np.random.default_rng(42)
    pi1 = monte_carlo_pi(10000, rng)
    
    rng = np.random.default_rng(42)  # Reset
    pi2 = monte_carlo_pi(10000, rng)
    
    print(f"   π estimate 1: {pi1:.6f}")
    print(f"   π estimate 2: {pi2:.6f}")
    print(f"   Identical: {pi1 == pi2}")
    
    print("\n=== Key Takeaways ===")
    print("✓ Use np.random.default_rng(seed)")
    print("✓ Never use global np.random.seed()")
    print("✓ Pass RNG objects to functions")
    print("✓ Document your seeds")

if __name__ == "__main__":
    stable_computation()
