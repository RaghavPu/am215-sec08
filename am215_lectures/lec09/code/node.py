class Node:
    """Node for a linked list."""
    def __init__(self, key, *,
                next=None,
                data=None):
        self.key = key
        self.next = next # node
        self.data = data
