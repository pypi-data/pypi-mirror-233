from al_struct.utils.nodes import TreeNode


class BinarySearchTree:
    """Binary search tree key structure."""
    def __init__(self):
        """Initialize an empty binary search tree."""
        self._root = None
        self._number_of_nodes = 0

    @property
    def number_of_nodes(self) -> int:
        """
        Returns total number of nodes in the tree.
        :return: int -- The number of nodes in the tree.
        """
        return self._number_of_nodes

    @property
    def number_of_leafs(self) -> int:
        """
        Returns the number of leafs in the tree.
        :return: int -- The number of leafs in the tree.
        """
        def _number_of_leafs(node):
            if node is None:
                return 0
            if node.left is None and node.right is None:
                return 1
            return _number_of_leafs(node.left) + _number_of_leafs(node.right)
        return _number_of_leafs(self._root)

    @property
    def height(self) -> int:
        """
        Returns the height of the tree.
        :return: int -- The height of the tree.
        """
        def _height(node):
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
        return _height(self._root)

    @property
    def min(self):
        """
        Returns the minimum value in the tree.
        """
        temp = self._root
        while temp.left:
            temp = temp.left
        return temp.key

    @property
    def max(self):
        """
        Returns the maximum value in the tree.
        """
        temp = self._root
        while temp.right:
            temp = temp.right
        return temp.key

    def is_empty(self) -> bool:
        """
        Check if the tree is empty.
        :returns: bool -- True if the tree is empty, otherwise False.
        """
        return self._root is None

    def pre_order(self):
        """
        Perform a preorder traversal of the binary search tree.
        """
        def _pre_order(node):
            print(node.key, end=', ')
            _pre_order(node.left)
            _pre_order(node.right)
        if not self.is_empty():
            _pre_order(self._root)
            print("end")

    def in_order(self):
        """
        Perform an inorder traversal of the binary search tree.
        """
        def _in_order(node):
            _in_order(node.left)
            print(node.key, end=', ')
            _in_order(node.right)
        if not self.is_empty():
            _in_order(self._root)
            print("end")

    def post_order(self):
        """
        Perform a postorder traversal of the binary search tree.
        """
        def _post_order(node):
            _post_order(node.left)
            _post_order(node.right)
            print(node.key, end=', ')
        if not self.is_empty():
            _post_order(self._root)
            print("end")

    def insert(self, key):
        """
        Insert new key to the tree if it's not exist.
        :param key: the key to be inserted.
        """
        def _insert(root, key):
            if root is None:
                return TreeNode(key)
            if key < root.key:
                return _insert(root.left, key)
            elif key > root.key:
                return _insert(root.right, key)
        self._root = _insert(self._root, key)
        self._number_of_nodes += 1

    def get(self, key) -> 'TreeNode':
        """
        Return the node that contains key if exist in the tree.
        :param key: The key to search for.
        :return: TreeNode -- The node that contains key if exists, otherwise None.
        """
        def _search(root, key):
            if root is None:
                return None
            if root.key == key:
                return root
            if key < root.key:
                return _search(root.left, key)
            return _search(root.right, key)
        return _search(self._root, key)

    def search(self, key) -> bool:
        """
        Search for a key in the tree.
        :param key: The key to search for.
        :return: bool -- True if key exists in the tree, otherwise False.
        """
        def _search(root, key):
            if root is None:
                return False
            if root.key == key:
                return True
            if key < root.key:
                return _search(root.left, key)
            return _search(root.right, key)
        if self.is_empty():
            return False
        return _search(self._root, key)

    def delete(self, key):
        """
        Delete a key from the tree.
        :param key: The key to be added.
        """
        def _min_value_node(node):
            while node.left is not None:
                node = node.left
            return node

        def _delete(root, key):
            if root is None:
                return root
            if key < root.key:
                root.left = _delete(root.left, key)
            elif key > root.key:
                root.right = _delete(root.right, key)
            else:
                if root.left is None:
                    return root.right
                elif root.right is None:
                    return root.left
                root.key = _min_value_node(root.right).key
                root.right = _delete(root.right, root.key)
            return root

        if not self.is_empty():
            self._root = _delete(self._root, key)
            self._number_of_nodes -= 1
