from .nodes import Node, BinaryNode, TreeNode


def compare_nodes(node1: Node | BinaryNode, node2: Node | BinaryNode | TreeNode) -> bool:
    """
    Compare two Node instances.

    :param node1: The first Node|BinaryNode instance.
    :param node2: The second Node|BinaryNode instance.
    :return: True if the nodes are equal, False otherwise.
    """
    if isinstance(node1, Node) and isinstance(node2, Node):
        return node1.data == node2.data and node1.next == node2.next
    elif isinstance(node1, BinaryNode) and isinstance(node2, BinaryNode):
        return node1.data == node2.data and node1.prev == node2.prev and node1.next == node2.next
    elif isinstance(node1, TreeNode) and isinstance(node2, TreeNode):
        return node1.key == node2.key and node1.left == node2.left and node1.right == node2.right
    raise TypeError("node1 and node2 should be of the same type from (Node, BinaryNode, TreeNode)")


__all__ = ["compare_nodes"]
