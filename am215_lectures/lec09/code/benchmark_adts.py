import random
import time
from typing import Any, Type

from queue_deque import QueueDeque
from queue_linked_list import QueueLinkedList
from queue_naive import QueueNaive
from priority_queue_heap_from_scratch import PriorityQueueHeap
from priority_queue_heapq import PriorityQueueHeapq
from priority_queue_naive_sorted_list import PriorityQueueNaiveSortedList


def benchmark_queue(queue_class: Type[Any], n_items: int) -> float:
    """
    Benchmarks a Queue implementation.

    The benchmark consists of enqueueing and then dequeueing a specified
    number of items.

    Parameters
    ----------
    queue_class : Type[Any]
        The queue class to benchmark (e.g., QueueNaive).
    n_items : int
        The number of items to enqueue and dequeue.

    Returns
    -------
    float
        The total time taken for the benchmark in seconds.
    """
    q = queue_class()
    start_time = time.perf_counter()

    for i in range(n_items):
        q.enqueue(i)

    for _ in range(n_items):
        q.dequeue()

    end_time = time.perf_counter()
    return end_time - start_time


def benchmark_pq(pq_class: Type[Any], n_items: int) -> float:
    """
    Benchmarks a Priority Queue implementation.

    The benchmark consists of inserting a specified number of items with
    random priorities, and then popping all items.

    Parameters
    ----------
    pq_class : Type[Any]
        The priority queue class to benchmark.
    n_items : int
        The number of items to insert and pop.

    Returns
    -------
    float
        The total time taken for the benchmark in seconds.
    """
    pq = pq_class()
    # Generate random priorities to avoid best/worst-case scenarios for sorted list
    priorities = [random.random() for _ in range(n_items)]
    start_time = time.perf_counter()

    for i in range(n_items):
        pq.insert(f"item_{i}", priorities[i])

    for _ in range(n_items):
        pq.pop_min()

    end_time = time.perf_counter()
    return end_time - start_time


def main():
    """
    Runs and prints the benchmark results for Queue and Priority Queue ADTs.
    """
    N_ITEMS_QUEUE = 50_000
    N_ITEMS_PQ = 10_000

    print("--- Benchmarking Queue ADT Implementations ---")
    print(f"Number of items: {N_ITEMS_QUEUE:,}")

    q_implementations = {
        "QueueNaive (list)": QueueNaive,
        "QueueLinkedList (from-scratch)": QueueLinkedList,
        "QueueDeque (collections.deque)": QueueDeque,
    }

    results_q = {}
    for name, impl in q_implementations.items():
        time_taken = benchmark_queue(impl, N_ITEMS_QUEUE)
        results_q[name] = time_taken
        print(f"{name:<32} {time_taken:.6f} seconds")

    if (
        "QueueNaive (list)" in results_q
        and results_q["QueueNaive (list)"] > 0
        and "QueueDeque (collections.deque)" in results_q
        and results_q["QueueDeque (collections.deque)"] > 0
    ):
        speedup = (
            results_q["QueueNaive (list)"] / results_q["QueueDeque (collections.deque)"]
        )
        print(f"\nSpeedup (deque vs naive): {speedup:.2f}x")

    print("\n" + "-" * 50 + "\n")

    print("--- Benchmarking Priority Queue ADT Implementations ---")
    print(f"Number of items: {N_ITEMS_PQ:,}")

    pq_implementations = {
        "PQNaiveSortedList (list)": PriorityQueueNaiveSortedList,
        "PQHeap (from-scratch)": PriorityQueueHeap,
        "PQHeapq (heapq)": PriorityQueueHeapq,
    }

    results_pq = {}
    for name, impl in pq_implementations.items():
        time_taken = benchmark_pq(impl, N_ITEMS_PQ)
        results_pq[name] = time_taken
        print(f"{name:<32} {time_taken:.6f} seconds")

    if (
        "PQNaiveSortedList (list)" in results_pq
        and results_pq["PQNaiveSortedList (list)"] > 0
        and "PQHeapq (heapq)" in results_pq
        and results_pq["PQHeapq (heapq)"] > 0
    ):
        speedup = (
            results_pq["PQNaiveSortedList (list)"] / results_pq["PQHeapq (heapq)"]
        )
        print(f"\nSpeedup (heapq vs naive): {speedup:.2f}x")


if __name__ == "__main__":
    main()
