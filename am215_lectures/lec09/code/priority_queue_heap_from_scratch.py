from typing import Any, List, Tuple


class PriorityQueueHeap:
    """
    A from-scratch Priority Queue implementation using a binary heap.

    This implementation manually manages a list as a min-heap, demonstrating
    the underlying algorithms used by Python's `heapq` module. Insert and
    pop_min operations have O(log n) complexity.

    Attributes
    ----------
    _data : list
        The underlying list storing (priority, item) tuples as a min-heap.
    """

    def __init__(self) -> None:
        """Initializes an empty Priority Queue."""
        self._data: List[Tuple[float, Any]] = []

    def insert(self, item: Any, priority: float) -> None:
        """Adds an item with a given priority to the queue. O(log n) complexity."""
        self._data.append((priority, item))
        self._sift_up(len(self._data) - 1)

    def pop_min(self) -> Any:
        """
        Removes and returns the item with the minimum priority. O(log n) complexity.
        """
        if self.is_empty():
            raise IndexError("pop from empty priority queue")

        self._swap(0, len(self._data) - 1)
        _priority, item = self._data.pop()
        if not self.is_empty():
            self._sift_down(0)
        return item

    def peek_min(self) -> Any:
        """
        Returns the item with the minimum priority without removing it. O(1) complexity.
        """
        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        return self._data[0][1]

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _sift_up(self, i: int) -> None:
        """Move an element up the heap to its correct position."""
        parent_idx = self._parent(i)
        while i > 0 and self._data[i][0] < self._data[parent_idx][0]:
            self._swap(i, parent_idx)
            i = parent_idx
            parent_idx = self._parent(i)

    def _sift_down(self, i: int) -> None:
        """Move an element down the heap to its correct position."""
        min_index = i
        left = self._left_child(i)
        if left < len(self._data) and self._data[left][0] < self._data[min_index][0]:
            min_index = left

        right = self._right_child(i)
        if right < len(self._data) and self._data[right][0] < self._data[min_index][0]:
            min_index = right

        if i != min_index:
            self._swap(i, min_index)
            self._sift_down(min_index)

    def is_empty(self) -> bool:
        """Checks if the queue is empty."""
        return len(self._data) == 0

    def size(self) -> int:
        """Returns the number of items in the priority queue."""
        return len(self._data)

    def __len__(self) -> int:
        """Returns the number of items in the queue (for len() built-in)."""
        return self.size()

    def __str__(self) -> str:
        """Returns a string representation of the priority queue."""
        return f"PriorityQueueHeap({self._data})"


if __name__ == "__main__":
    print("--- Testing PriorityQueueHeap (from scratch) ---")
    pq = PriorityQueueHeap()
    pq.insert("task1", 5)
    pq.insert("task2", 1)
    pq.insert("task3", 3)
    print(f"After inserts: {pq}")
    print(f"Peek min: {pq.peek_min()}")
    print(f"Popped min: {pq.pop_min()}")
    print(f"After pop: {pq}")
    pq.insert("task4", 0)
    print(f"After inserting task4 with priority 0: {pq}")
    sorted_tasks = []
    while not pq.is_empty():
        sorted_tasks.append(pq.pop_min())
    print(f"Tasks popped in order: {sorted_tasks}")
