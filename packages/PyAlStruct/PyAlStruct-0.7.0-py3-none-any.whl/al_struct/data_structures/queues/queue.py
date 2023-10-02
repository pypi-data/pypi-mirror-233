from utils.exceptions import EmptyQueueException
from al_struct.utils.nodes import Node


class Queue:
    """Simple queue data structure."""

    def __init__(self):
        self._front = None
        self._back = None

    def __str__(self):
        values = []
        temp = self._front
        while temp:
            values.append(str(temp.key))
            temp = temp.next
        del temp
        return " | ".join(values)

    def __repr__(self):
        return f"PyAlStruct.Queue({str(self)})"

    def __len__(self):
        """Return len(self)"""
        size = 0
        tmep = self._front
        while tmep:
            size += 1
            tmep = tmep.next
        return size

    def __iter__(self):
        """Initialize an iterator over the linked list."""
        self._current = self._front
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
        Check if the queue is empty.
        :returns: bool -- True if the queue is empty, otherwise False.
        """
        return self._front is None

    def enqueue(self, item):
        """
        Add a new node with item to the back of the queue.
        :param item: The item to be added to the queue.
        """
        node = Node(item)
        if self._front is None:
            self._front = node
            self._back = node
            return
        self._back.next = node
        self._back = node

    def dequeue(self):
        """
        Removes and returns an item from the front of the queue.
        :return: The item at the front of the queue if exists.
        :raise EmptyQueueException: If the stack is empty.
        """
        if self._front is None:
            raise EmptyQueueException()
        if self._front == self._back:
            self._front = None
        data = self._front.data
        temp = self._front
        self._front = self._front.next
        del temp
        return data

    def size(self):
        """
        Return The size of the queue.
        :return: int -- The size of the queue.
        """
        size = 0
        tmep = self._front
        while tmep:
            size += 1
            tmep = tmep.next
        return size
