import sys
import random
import math
import numpy as np

def estimate_volume(dimension, max_points):
    inside = 0
    check_points = np.logspace(1, np.log10(max_points), num=20, dtype=int)
    estimates = np.zeros(len(check_points))
    
    for i in range(1, max_points + 1):
        point = [random.uniform(-1, 1) for _ in range(dimension)]
        if sum(x**2 for x in point) <= 1:
            inside += 1
        
        if i in check_points:
            idx = np.where(check_points == i)[0][0]
            estimates[idx] = (2**dimension) * (inside / i)
    
    return list(zip(check_points, estimates))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python hypersphere_volume.py <dimension> <max_points>")
        sys.exit(1)
    
    dimension = int(sys.argv[1])
    max_points = int(sys.argv[2])
    
    estimates = estimate_volume(dimension, max_points)
    true_volume = math.pi**(dimension/2) / math.gamma(dimension/2 + 1)
    
    for num_points, estimate in estimates:
        print(f"{dimension},{num_points},{estimate},{true_volume}")
