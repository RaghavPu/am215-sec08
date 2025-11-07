import time
import random
from concurrent.futures import ProcessPoolExecutor

def hits(n):
    """
    Simulates n random draws to estimate pi and returns the number of hits.
    This is a CPU-intensive calculation.
    """
    c = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            c += 1
    return c

def main():
    """Runs a parallel Monte Carlo simulation using ProcessPoolExecutor."""
    TASKS, N = 8, 1_000_000
    print(f"Running {TASKS} parallel tasks of {N:,} draws each...")

    t0 = time.perf_counter()
    # The 'with' statement creates the process pool and ensures it's shut down.
    with ProcessPoolExecutor() as executor:
        # executor.map distributes the 'hits' calls across the worker processes.
        total_hits = sum(executor.map(hits, [N] * TASKS))
    t1 = time.perf_counter()

    pi_est = 4 * total_hits / (TASKS * N)
    print(f"Pi approximation: {pi_est:.6f}")
    print(f"Multiprocessing time: {t1 - t0:.3f}s")

# The if __name__ == "__main__" guard is essential for multiprocessing.
if __name__ == "__main__":
    main()
