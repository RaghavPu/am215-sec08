from typing import Any, Optional


class _Node:
    """A private node class for the linked list implementation."""

    def __init__(self, item: Any, next_node: Optional["_Node"] = None):
        self.item = item
        self.next = next_node


class QueueLinkedList:
    """
    A from-scratch Queue implementation using a linked list.

    This implementation uses a singly linked list with pointers to both the
    head and tail of the list. This allows for O(1) time complexity for both
    enqueue (adding to the tail) and dequeue (removing from the head) operations.

    Attributes
    ----------
    _head : _Node, optional
        The first node in the queue.
    _tail : _Node, optional
        The last node in the queue.
    _size : int
        The number of items in the queue.
    """

    def __init__(self) -> None:
        """Initializes an empty Queue."""
        self._head: Optional[_Node] = None
        self._tail: Optional[_Node] = None
        self._size: int = 0

    def enqueue(self, item: Any) -> None:
        """
        Adds an item to the back of the queue. O(1) complexity.
        """
        new_node = _Node(item)
        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            # self._tail is guaranteed not to be None here
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the item from the front of the queue. O(1) complexity.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        # self._head is guaranteed not to be None here
        item = self._head.item
        self._head = self._head.next
        self._size -= 1
        if self.is_empty():
            self._tail = None  # Important: reset tail if queue becomes empty
        return item

    def peek(self) -> Any:
        """
        Returns the item at the front of the queue without removing it. O(1) complexity.
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")
        # self._head is guaranteed not to be None here
        return self._head.item

    def is_empty(self) -> bool:
        """Checks if the queue is empty."""
        return self._size == 0

    def size(self) -> int:
        """Returns the number of items in the queue."""
        return self._size

    def __len__(self) -> int:
        """Returns the number of items in the queue (for len() built-in)."""
        return self.size()

    def __str__(self) -> str:
        """Returns a string representation of the queue."""
        items = []
        current = self._head
        while current:
            items.append(repr(current.item))
            current = current.next
        return f"QueueLinkedList([{', '.join(items)}])"

    def __repr__(self) -> str:
        """Returns a developer-friendly string representation of the queue."""
        return self.__str__()


if __name__ == "__main__":
    print("--- Testing QueueLinkedList ---")
    q = QueueLinkedList()
    print(f"Is empty: {q.is_empty()}")

    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    print(f"After enqueuing 10, 20, 30: {q}")
    print(f"Size: {q.size()}")
    print(f"Peek: {q.peek()}")

    print(f"Dequeued: {q.dequeue()}")
    print(f"After dequeue: {q}")

    while not q.is_empty():
        print(f"Dequeued: {q.dequeue()}")

    print(f"Final queue: {q}")
    try:
        q.dequeue()
    except IndexError as e:
        print(f"Caught expected error: {e}")
