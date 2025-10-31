# Lecture 9 Code Examples: Data Structures for Modeling & Scientific Computing

This directory contains practical code examples demonstrating various Abstract Data Types (ADTs) and their implementations using different Python data structures. The primary goal is to illustrate the performance implications of choosing appropriate data structures, particularly in the context of scientific computing where efficiency is often critical.

Each ADT is implemented in at least two ways:
1.  A "naive" implementation, often using standard Python lists in a way that highlights potential performance pitfalls.
2.  A more "ideal" implementation, leveraging Python's built-in optimized data structures or modules (like `collections.deque` or `heapq`).

A benchmarking script is provided to quantitatively compare the performance of these implementations.

## Contents

*   `queue_naive.py`: Implements a Queue ADT using a Python `list` where `pop(0)` is used for dequeuing, leading to `O(n)` complexity.
*   `queue_linked_list.py`: Implements a Queue ADT "from scratch" using a linked list with head and tail pointers to achieve `O(1)` operations.
*   `queue_deque.py`: Implements a Queue ADT using `collections.deque`, providing `O(1)` complexity for both enqueue and dequeue operations.
*   `priority_queue_naive_sorted_list.py`: Implements a Priority Queue ADT using a Python `list` that is kept sorted, resulting in `O(n)` insertion.
*   `priority_queue_heap_from_scratch.py`: Implements a Priority Queue ADT "from scratch" using an array-based binary heap, demonstrating the `O(log n)` sift-up/sift-down logic.
*   `priority_queue_heapq.py`: Implements a Priority Queue ADT using Python's `heapq` module, offering `O(log n)` for insertion and removal of the highest priority item.
*   `benchmark_adts.py`: A script to run performance comparisons between the different ADT implementations.

## How to Run the Examples

### Prerequisites

Ensure you have Python 3.8+ installed. No external libraries are strictly required for the ADT implementations themselves, but `numpy` and `matplotlib` might be useful if you extend the benchmarking script to plot results.

### Running the Benchmark

1.  Navigate to this directory in your terminal:
    ```bash
    cd am215_lectures/lec09/code/
    ```
2.  Execute the benchmark script:
    ```bash
    python benchmark_adts.py
    ```

The script will output performance metrics (typically execution times) for each implementation across different test scenarios.

## Interpreting Benchmark Results

You should observe significant performance differences between the implementations. These results highlight the interplay between **algorithmic complexity** (e.g., O(n) vs O(log n)) and **implementation language** (pure Python vs. optimized C code).

*   **Queue ADT:**
    *   The `QueueNaive` (using `list.pop(0)`) is the slowest, clearly demonstrating the performance penalty of an O(n) dequeue operation.
    *   The `QueueLinkedList` (from-scratch) and `QueueDeque` (built-in) are both much faster, showing the power of an O(1) dequeue operation.
    *   The `QueueDeque` is the fastest overall because it is implemented in highly optimized C code, whereas our linked list is pure Python.

*   **Priority Queue ADT:**
    *   The `PQHeapq` (using Python's `heapq` module) is the clear winner. It combines the best of both worlds: an efficient O(log n) heap algorithm *and* an implementation in optimized C code.
    *   A surprising result is that the `PQHeap (from-scratch)` is often *slower* than the `PQNaiveSortedList`. This is a critical lesson:
        *   The from-scratch heap has better **asymptotic complexity** (O(log n) operations). However, it is written in pure Python, so every comparison and swap is slow.
        *   The naive sorted list has worse asymptotic complexity (O(n) operations via `bisect.insort` and `pop(0)`), but these operations are implemented in fast, compiled C code.
        *   For the given data size, the massive constant-factor speedup from the C implementation outweighs the better algorithmic complexity of the pure Python heap.

These examples underscore that while choosing the right algorithm is crucial, the underlying implementation details can have a profound impact on real-world performance.
