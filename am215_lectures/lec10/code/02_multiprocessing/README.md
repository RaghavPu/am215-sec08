# 02: Multiprocessing Examples

This directory demonstrates how to use `ProcessPoolExecutor` to achieve true parallelism for CPU-bound work, bypassing the GIL.

-   `mp_pi.py`: The Monte Carlo Pi simulation parallelized using `ProcessPoolExecutor`. Compare its runtime to `01_synchronous/sync_mc.py` to see the speedup from using multiple CPU cores.
