from utils.exceptions import EmptyStackException
from al_struct.utils.nodes import Node


class Stack:
    """Simple stack data structure."""

    def __init__(self):
        self._top = None

    def __str__(self):
        values = []
        temp = self._top
        while temp:
            values.append(str(temp.key))
            temp = temp.next
        del temp
        return ", ".join(values)

    def __repr__(self):
        return f"PyAlStruct.Stack({str(self)})"

    def __len__(self):
        """Return len(self)"""
        size = 0
        tmep = self._top
        while tmep:
            size += 1
            tmep = tmep.next
        return size

    def __iter__(self):
        """Initialize an iterator over the linked list."""
        self._current = self._top
        return self

    def __next__(self):
        """Get the next element in the iteration."""
        if self._current:
            current = self._current
            self._current = self._current.next
            return current.key
        else:
            raise StopIteration

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        :returns: bool -- True if the stack is empty, otherwise False.
        """
        return self._top is None

    def push(self, item):
        """
        Add a new item to the top of the stack.
        :param item: The item to be added to the stack.
        """
        node = Node(item)
        node.next = self._top
        self._top = node

    def pop(self):
        """
        Removes and returns an item from the top of the stack.
        :return: The item at the top of the stack if exists.
        :raise EmptyStackException: If the stack is empty.
        """
        if not self._top:
            raise EmptyStackException()
        item = self._top.key
        temp = self._top
        self._top = self._top.next
        del temp
        return item

    def peek(self):
        """
        Return the item in the top of the stack without removing it.
        :return: The item of the node at the top of the stack.
        """
        if not self._top:
            raise EmptyStackException()
        return self._top.key

    def size(self) -> int:
        """
        Return The size of the stack.
        :return: int -- The size of the stack.
        """
        size = 0
        tmep = self._top
        while tmep:
            size += 1
            tmep = tmep.next
        return size
