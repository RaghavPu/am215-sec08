import heapq
from typing import Any, List, Tuple


class PriorityQueueHeapq:
    """
    An efficient Priority Queue implementation using Python's `heapq` module.

    This implementation uses a list as a min-heap. `heapq.heappush` and
    `heapq.heappop` provide O(log n) complexity for insertion and removal of
    the minimum element, respectively.

    Attributes
    ----------
    _data : list
        The underlying list storing (priority, item) tuples, maintained as a
        min-heap by the `heapq` module.
    """

    def __init__(self) -> None:
        """
        Initializes an empty Priority Queue.
        """
        self._data: List[Tuple[float, Any]] = []

    def insert(self, item: Any, priority: float) -> None:
        """
        Adds an item with a given priority to the queue.

        Time complexity is O(log n).

        Parameters
        ----------
        item : Any
            The item to be added.
        priority : float
            The priority of the item (lower number means higher priority).
        """
        heapq.heappush(self._data, (priority, item))

    def pop_min(self) -> Any:
        """
        Removes and returns the item with the minimum priority.

        Time complexity is O(log n).

        Returns
        -------
        Any
            The item with the minimum priority.

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        if not self._data:
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._data)[1]  # (priority, item)

    def peek_min(self) -> Any:
        """
        Returns the item with the minimum priority without removing it.

        Time complexity is O(1).

        Returns
        -------
        Any
            The item with the minimum priority.

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        if not self._data:
            raise IndexError("peek from empty priority queue")
        return self._data[0][1]

    def is_empty(self) -> bool:
        """
        Checks if the priority queue is empty.

        Returns
        -------
        bool
            True if empty, False otherwise.
        """
        return len(self._data) == 0

    def size(self) -> int:
        """
        Returns the number of items in the priority queue.

        Returns
        -------
        int
            The number of items.
        """
        return len(self._data)

    def __len__(self) -> int:
        """
        Returns the number of items in the queue (for len() built-in).
        """
        return self.size()

    def __str__(self) -> str:
        """
        Returns a string representation of the priority queue.
        Note: The list is not necessarily sorted, it only has the heap property.
        """
        return f"PriorityQueueHeapq({self._data})"


if __name__ == "__main__":
    print("--- Testing PriorityQueueHeapq ---")
    pq = PriorityQueueHeapq()
    print(f"Is empty: {pq.is_empty()}")

    pq.insert("task1", 5)
    pq.insert("task2", 1)
    pq.insert("task3", 3)
    print(f"After inserts: {pq}")
    print(f"Size: {pq.size()}")
    print(f"Peek min: {pq.peek_min()}")

    print(f"Popped min: {pq.pop_min()}")
    print(f"After pop: {pq}")
    print(f"Peek min: {pq.peek_min()}")

    pq.insert("task4", 0)
    print(f"After inserting task4 with priority 0: {pq}")
    print(f"Peek min: {pq.peek_min()}")

    # The power of a heap is that popping always gives the minimum
    # in O(log n) time.
    sorted_tasks = []
    while not pq.is_empty():
        sorted_tasks.append(pq.pop_min())
    print(f"Tasks popped in order: {sorted_tasks}")

    print(f"Final queue: {pq}")
    print(f"Is empty: {pq.is_empty()}")

    try:
        pq.pop_min()
    except IndexError as e:
        print(f"Caught expected error: {e}")
