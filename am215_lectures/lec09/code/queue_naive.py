import collections
from typing import Any, List, Optional


class QueueNaive:
    """
    A naive implementation of a Queue ADT using a Python list.

    This implementation uses `list.append()` for enqueueing and `list.pop(0)`
    for dequeuing. While `append()` is O(1) amortized, `pop(0)` requires
    shifting all subsequent elements, making it an O(n) operation. This
    demonstrates a common performance pitfall.

    Attributes
    ----------
    _data : list
        The underlying list storing the queue elements.
    """

    def __init__(self) -> None:
        """
        Initializes an empty Queue.
        """
        self._data: List[Any] = []

    def enqueue(self, item: Any) -> None:
        """
        Adds an item to the back of the queue.

        This operation has an amortized time complexity of O(1).

        Parameters
        ----------
        item : Any
            The item to be added to the queue.
        """
        self._data.append(item)

    def dequeue(self) -> Any:
        """
        Removes and returns the item from the front of the queue.

        This operation has a time complexity of O(n) because all subsequent
        elements in the list must be shifted.

        Returns
        -------
        Any
            The item removed from the front of the queue.

        Raises
        ------
        IndexError
            If the queue is empty.
        """
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)

    def peek(self) -> Any:
        """
        Returns the item at the front of the queue without removing it.

        This operation has a time complexity of O(1).

        Returns
        -------
        Any
            The item at the front of the queue.

        Raises
        ------
        IndexError
            If the queue is empty.
        """
        if not self._data:
            raise IndexError("peek from empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.

        This operation has a time complexity of O(1).

        Returns
        -------
        bool
            True if the queue is empty, False otherwise.
        """
        return len(self._data) == 0

    def size(self) -> int:
        """
        Returns the number of items in the queue.

        This operation has a time complexity of O(1).

        Returns
        -------
        int
            The number of items in the queue.
        """
        return len(self._data)

    def __len__(self) -> int:
        """
        Returns the number of items in the queue (for len() built-in).
        """
        return self.size()

    def __str__(self) -> str:
        """
        Returns a string representation of the queue.
        """
        return f"QueueNaive({self._data})"

    def __repr__(self) -> str:
        """
        Returns a developer-friendly string representation of the queue.
        """
        return self.__str__()


if __name__ == "__main__":
    print("--- Testing QueueNaive ---")
    q = QueueNaive()
    print(f"Is empty: {q.is_empty()}")
    print(f"Size: {q.size()}")

    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    print(f"After enqueuing 10, 20, 30: {q}")
    print(f"Size: {q.size()}")
    print(f"Peek: {q.peek()}")

    print(f"Dequeued: {q.dequeue()}")
    print(f"After dequeue: {q}")
    print(f"Size: {q.size()}")

    q.enqueue(40)
    print(f"After enqueuing 40: {q}")

    while not q.is_empty():
        print(f"Dequeued: {q.dequeue()}")
    print(f"Final queue: {q}")
    print(f"Is empty: {q.is_empty()}")

    try:
        q.dequeue()
    except IndexError as e:
        print(f"Caught expected error: {e}")

    try:
        q.peek()
    except IndexError as e:
        print(f"Caught expected error: {e}")
