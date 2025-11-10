# 05: Hybrid Asyncio + Threading Pipeline

This directory contains a sophisticated example demonstrating a hybrid concurrency model that combines `asyncio` for high-throughput I/O with `threading` for CPU-bound processing.

## Purpose

This example simulates a common scientific computing pipeline:

1.  **Concurrent Data Fetching:** An `asyncio` event loop, using `aiohttp`, fetches numerous binary data files from a web service concurrently. This is a classic I/O-bound task where `asyncio` excels.
2.  **CPU-Bound Analysis:** For each file downloaded, a CPU-intensive analysis is performed using NumPy. Because this computation is long-running, it would block the `asyncio` event loop if run directly.
3.  **Offloading to Threads:** To prevent blocking, the CPU-bound NumPy function is offloaded to a separate thread using `asyncio.to_thread()`. Because NumPy releases the Global Interpreter Lock (GIL) during most of its computations, this work can run in parallel on a multi-core system.

## Key Concepts Illustrated

-   **Hybrid Architecture:** Combining `asyncio` (for I/O) and `threading` (for CPU-bound work) to build highly efficient and responsive applications.
-   **`asyncio.to_thread()`:** The modern, high-level way to run a synchronous, blocking function in a separate thread without blocking the `asyncio` event loop.
-   **GIL Release:** Demonstrates a scenario where `threading` is effective for CPU-bound work because the underlying library (NumPy) releases the GIL, allowing for true parallelism.
-   **Self-Contained Simulation:** The script includes a simple `aiohttp` web server to serve randomly generated binary data, making the example fully self-contained and runnable without external dependencies beyond the required Python packages.

## How to Run

Ensure you have the necessary dependencies installed by running the command from the repository root:

```bash
uv pip install -r am215_lectures/lec10/code/requirements.txt
```

Then, simply run the script. It will start its own local web server, run the pipeline, print the results, and shut down.

```bash
python am215_lectures/lec10/code/05_hybrid_pipeline/hybrid_pipeline.py
```
