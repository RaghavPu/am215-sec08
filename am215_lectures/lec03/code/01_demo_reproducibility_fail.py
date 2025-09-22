#!/usr/bin/env python3
"""
Demonstrate reproducibility failures.
This script shows what happens WITHOUT proper seed management.
"""

import numpy as np

def unstable_computation():
    """A computation that will give different results each run."""
    
    print("=== Reproducibility Failure Demo ===\n")
    
    # Problem 1: No seed management
    print("1. Random sampling without seed:")
    for i in range(3):
        values = np.random.normal(0, 1, 5)
        print(f"   Run {i+1}: mean = {values.mean():.6f}")
    
    print("\n2. Same computation, different results:")
    results = []
    for i in range(3):
        # Simulate a Monte Carlo estimation
        samples = np.random.exponential(2.0, 1000)
        estimate = samples.mean()
        results.append(estimate)
        print(f"   Run {i+1}: λ estimate = {estimate:.6f}")
    
    variation = (max(results) - min(results)) / np.mean(results) * 100
    print(f"   Variation: {variation:.2f}%")
    
    # Problem 2: Global state pollution
    print("\n3. Global random state (old NumPy style):")
    np.random.seed(42)
    print(f"   After seed(42): {np.random.random():.6f}")
    
    # Some other function uses random
    _ = np.random.random()
    
    # Now our "reproducible" code gives different results
    np.random.seed(42)
    _ = np.random.random()  # Someone else's code
    print(f"   After interference: {np.random.random():.6f}")
    print("   (Different despite same seed!)")
    
    print("\n=== Why This Matters ===")
    print("- Collaborator gets different results")
    print("- Can't debug issues")
    print("- Results change between runs")
    print("- Paper results not reproducible")

if __name__ == "__main__":
    unstable_computation()
