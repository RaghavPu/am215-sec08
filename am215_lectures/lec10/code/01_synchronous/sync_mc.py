import time
import random

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
    """Runs a sequential Monte Carlo simulation to estimate Pi."""
    TASKS, N = 8, 1_000_000
    print(f"Running {TASKS} sequential tasks of {N:,} draws each...")

    t0 = time.perf_counter()
    total_hits = sum(hits(N) for _ in range(TASKS))
    t1 = time.perf_counter()

    pi_est = 4 * total_hits / (TASKS * N)
    print(f"Pi approximation: {pi_est:.6f}")
    print(f"Sequential time: {t1 - t0:.3f}s")

if __name__ == "__main__":
    main()
