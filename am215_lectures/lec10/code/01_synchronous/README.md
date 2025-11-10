# 01: Synchronous Examples

This directory contains the sequential "baseline" scripts. Run these first to establish a performance benchmark to which the concurrent versions can be compared.

-   `sync_tasks.py`: A simple demonstration of two sequential tasks that each `sleep` for 1 second. Total time is ~2 seconds. This corresponds to the "Synchronous Execution" slide.
-   `sync_mc.py`: A sequential Monte Carlo simulation to estimate Pi. This is a **CPU-bound** baseline.
-   `sync_fetch.py`: A sequential script that downloads a series of URLs one by one. This is an **I/O-bound** baseline.
