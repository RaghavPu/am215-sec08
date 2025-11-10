#!/usr/bin/env python3
# vim: foldmethod=marker
# File       : linked_list.py
# Description: Linked list implementation
# Copyright 2022 Harvard University. All Rights Reserved.

import copy


# Node {{{1
class Node:
    def __init__(self, key, *, data=None, next=None):
        self.key = key
        self.data = data
        self.next = next


# LinkedList {{{1
class LinkedList:
    # List creation {{{2
    def __init__(self, key, data, *, reverse=False):
        """
        Construct a linked list.

        Parameter:
        ----------
        key : list-like
            List of keys used to identify nodes
        data : list-like
            List of data objects to be associated with nodes
        reverse : bool
            Create linked list in reverse order

        """
        start = Node(key[0], data=data[0])  # create root node
        end = start
        for k, d in zip(key[1:], data[1:]):
            if reverse:
                end = self._prepend(end, Node(k, data=d))
            else:
                end = self._append(end, Node(k, data=d))
        self.root = start if not reverse else end

    @staticmethod
    def _append(anchor, node):
        anchor.next = node
        return node

    @staticmethod
    def _prepend(anchor, node):
        node.next = anchor
        return node

    # Sequence properties {{{2
    def __getitem__(self, key):
        _, node = self._getitem(key)
        return node

    def __len__(self):
        node = self.root
        count = 0
        while node != None:
            count += 1
            node = node.next
        return count

    def _getitem(self, key):
        """
        Private method to retrieve a list element given a key.

        Parameters
        ----------
        key :
            Key for node identification

        Returns
        -------
        Tuple with reference to predecessor node and reference to node with
        given key

        """
        node = self.root
        prev = node
        while node != None:
            if node.key == key:
                return (prev, node)
            prev = node
            node = node.next
        raise KeyError(f"Key '{key}' not found")

    def __str__(self):
        node = self.root
        pretty = ""
        while node != None:
            pretty += f"node: {hex(id(node))} : key={node.key} : data={node.data}\n"
            node = node.next
        return pretty

    # Node insertion {{{2
    def insert(self, key, node, *, before=False):
        """Key based node insertion [at worst O(n)]."""
        p = self[key]  # search for key explicitly -> O(n)
        if before:  # insert before
            tmp = copy.copy(p)  # beware!
            p.key = node.key
            p.data = node.data
            node = tmp
            p.next = node
        else:  # insert after
            assert p is not None
            node.next = p.next
            p.next = node
        return node

    # Node removal {{{2
    def remove(self, key):
        """Key based node removal [at worst O(n)]."""
        if self.root.key == key:
            del_node = self.root
            self.root = self.root.next
        else:
            # search for key explicitly -> O(n)
            prev, del_node = self._getitem(key)
            prev.next = del_node.next
        del del_node

    # # Iterator {{{2
    # def __iter__(self):
    #     return LinkedListForwardIterator(self.root)


# LinkedListForwardIterator {{{1
class LinkedListForwardIterator:
    def __init__(self, start):
        self.node = start  # required state to keep track of the iteration

    def __next__(self):
        if self.node is None:
            raise StopIteration
        curr_node = self.node
        self.node = self.node.next  # modify state of iterator instance
        return curr_node

    def __iter__(self):
        return self  # iter() applied on an iterator must return the iterator itself


# main() {{{1
def main():
    # Create some dummy data class
    class Data:
        def __init__(self, data):
            self.data = data

        def __str__(self):
            return f'<value={self.data} {hex(id(self))}>'

    data = [Data(d) for d in list('ABCDE')]
    keys = [f'ID_{k}' for k in range(len(data))]

    # create a list
    linked_list = LinkedList(keys, data)
    print(len(linked_list))  # __len__
    print(linked_list['ID_0'])  # __getitem__ (key/index is not an integer!)

    # # Iterate over list {{{2
    # for node in linked_list:
    #     print(node)
    # # 2}}}

    # Insertion / removal examples {{{2
    # insert a new node with different key type
    linked_list.insert(keys[1], Node(10, data='Data can be arbitrary'))

    # remove the node again
    linked_list.remove(10)
    linked_list.remove('ID_0')
    # 2}}}


if __name__ == "__main__":
    main()
