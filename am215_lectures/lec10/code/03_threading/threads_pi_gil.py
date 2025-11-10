import time
import random
from concurrent.futures import ThreadPoolExecutor

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
    """
    Runs a concurrent Monte Carlo simulation using ThreadPoolExecutor to
    demonstrate the effect of the GIL on CPU-bound tasks.
    """
    TASKS, N = 8, 1_000_000
    print(f"Running {TASKS} concurrent tasks of {N:,} draws each with threads...")

    t0 = time.perf_counter()
    # Swapping ProcessPoolExecutor for ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=TASKS) as executor:
        total_hits = sum(executor.map(hits, [N] * TASKS))
    t1 = time.perf_counter()

    pi_est = 4 * total_hits / (TASKS * N)
    print(f"Pi approximation: {pi_est:.6f}")
    print(f"Threading (CPU-bound) time: {t1 - t0:.3f}s")
    print("Note: Performance is similar to sequential due to the GIL.")

if __name__ == "__main__":
    main()
