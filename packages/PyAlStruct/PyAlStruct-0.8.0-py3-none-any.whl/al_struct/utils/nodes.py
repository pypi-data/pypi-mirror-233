class Node:
    """Basic node for linked data structures."""

    def __init__(self, data=None, next_node: 'Node' = None):
        """
        Initialize a new node.
        :param data: The data to be stored in the node.
        :param next_node: The next node in the linked structure.
        """
        self._data = data
        self._next = next_node

    def __eq__(self, other: 'Node'):
        if isinstance(other, Node):
            return self.data == other.data and self.next == other.next
        return False

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def next(self) -> 'Node':
        return self._next

    @next.setter
    def next(self, ptr: 'Node'):
        if not isinstance(ptr, (Node, type(None))):
            raise TypeError("The pointer should be a Node or None")
        self._next = ptr


class BinaryNode:
    """Node for double side linked data structures"""
    def __init__(self, data=None, prev_node: 'BinaryNode' = None, next_node: 'BinaryNode' = None):
        """
        Initialize a new node.
        :param data: The data to be stored in the node.
        :param prev_node: The previous node
        :param next_node: The next node
        """
        self._data = data
        self._prev = prev_node
        self._next = next_node

    def __eq__(self, other: 'BinaryNode'):
        if isinstance(other, BinaryNode):
            return self.data == other.data and self.prev == other.prev and self.next == other.next
        return False

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def prev(self) -> 'BinaryNode':
        return self._prev

    @prev.setter
    def prev(self, ptr: 'BinaryNode'):
        if not isinstance(ptr, (BinaryNode, type(None))):
            raise TypeError("The pointer should be a BinaryNode or None")
        self._prev = ptr

    @property
    def next(self) -> 'BinaryNode':
        return self._next

    @next.setter
    def next(self, ptr: 'BinaryNode'):
        if not isinstance(ptr, (BinaryNode, type(None))):
            raise TypeError("The pointer should be a BinaryNode or None")
        self._next = ptr


class TreeNode:
    """Node for binary tree based linked data structures"""

    def __init__(self, key=None, left_node: 'TreeNode' = None, right_node: 'TreeNode' = None):
        """
        Initialize a new node.
        :param key: The data to be stored in the node.
        :param left_node: The previous node
        :param right_node: The next node
        """
        self._key = key
        self._left = left_node
        self._right = right_node

    def __eq__(self, other: 'TreeNode'):
        if isinstance(other, TreeNode):
            return self.key == other.key and self.left == other.left and self.right == other.right
        return False

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, data):
        self._key = data

    @property
    def left(self) -> 'TreeNode':
        return self._left

    @left.setter
    def left(self, ptr: 'TreeNode'):
        if not isinstance(ptr, (TreeNode, type(None))):
            raise TypeError("The pointer should be a TreeNode or None")
        self._left = ptr

    @property
    def right(self) -> 'TreeNode':
        return self._right

    @right.setter
    def right(self, ptr: 'TreeNode'):
        if not isinstance(ptr, (TreeNode, type(None))):
            raise TypeError("The pointer should be a TreeNode or None")
        self._right = ptr
