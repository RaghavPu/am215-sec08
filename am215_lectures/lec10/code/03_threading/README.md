# 03: Threading Examples

This directory explores the `ThreadPoolExecutor`, its effectiveness for I/O-bound tasks, its limitations due to the GIL, and the dangers of shared state.

-   `threads_fetch.py`: The URL fetching task implemented with a `ThreadPoolExecutor`. Compare its runtime to `01_synchronous/sync_fetch.py` to see the dramatic speedup from overlapping I/O waits.
-   `threads_pi_gil.py`: The CPU-bound Monte Carlo simulation implemented with a `ThreadPoolExecutor`. This script demonstrates the effect of the GIL: performance will be similar to or worse than the sequential version.
-   `race_condition.py`: A classic example of a race condition where multiple threads attempt to increment a shared counter, leading to an incorrect final result.
-   `race_condition_lock.py`: The fix for the race condition using a `threading.Lock` to protect the shared counter, ensuring a correct result.
