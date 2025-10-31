import bisect
from typing import Any, List, Tuple


class PriorityQueueNaiveSortedList:
    """
    A naive Priority Queue implementation using a sorted Python list.

    This implementation maintains a list sorted by priority. Insertion uses
    `bisect.insort` to find the correct position and insert, which is an O(n)
    operation for a list. Popping the minimum priority item is O(n) as it
    removes from the beginning of the list.

    Attributes
    ----------
    _data : list
        The underlying list storing (priority, item) tuples.
    """

    def __init__(self) -> None:
        """
        Initializes an empty Priority Queue.
        """
        self._data: List[Tuple[float, Any]] = []

    def insert(self, item: Any, priority: float) -> None:
        """
        Adds an item with a given priority to the queue.

        Maintains sort order. Time complexity is O(n) due to list insertion.

        Parameters
        ----------
        item : Any
            The item to be added.
        priority : float
            The priority of the item (lower number means higher priority).
        """
        bisect.insort(self._data, (priority, item))

    def pop_min(self) -> Any:
        """
        Removes and returns the item with the minimum priority.

        Time complexity is O(n) because it removes from the start of the list.

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
        return self._data.pop(0)[1]  # (priority, item)

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
        """
        return f"PriorityQueueNaiveSortedList({self._data})"


if __name__ == "__main__":
    print("--- Testing PriorityQueueNaiveSortedList ---")
    pq = PriorityQueueNaiveSortedList()
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

    while not pq.is_empty():
        print(f"Popped min: {pq.pop_min()}")

    print(f"Final queue: {pq}")
    print(f"Is empty: {pq.is_empty()}")

    try:
        pq.pop_min()
    except IndexError as e:
        print(f"Caught expected error: {e}")
