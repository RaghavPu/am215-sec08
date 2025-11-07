# Code Examples for Lecture 10: Concurrency in Python

This directory contains the code examples for Lecture 10, demonstrating the principles of synchronous execution, multiprocessing, threading, and asyncio. Each example is designed to be run from the command line and corresponds to a specific concept covered in the lecture slides.

## Dependencies

Some of the examples require third-party libraries. You can install them using the provided `requirements.txt` file:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Directory Structure

The examples are organized into subdirectories that follow the lecture's progression. This structure helps isolate the concepts and provides a clear path from baseline sequential code to advanced concurrency models.

-   `01_synchronous/`: Baseline sequential scripts for performance comparison.
-   `02_multiprocessing/`: Demonstrates true parallelism for CPU-bound tasks.
-   `03_threading/`: Shows concurrency for I/O-bound tasks, the impact of the GIL, and race conditions.
-   `04_asyncio/`: Illustrates lightweight concurrency for massive I/O.
-   `05_hybrid_pipeline/`: A sophisticated example combining `asyncio` and `threading` for a scientific pipeline.

## How to Run the Examples

All scripts are self-contained and can be run directly from your terminal. Navigate to the appropriate subdirectory and execute the Python script.

```bash
# Example for running a multiprocessing script
cd 02_multiprocessing/
python mp_pi.py
```

Pay attention to the console output, as most scripts print their execution time, allowing you to directly compare the performance of different concurrency models.
