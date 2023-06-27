from typing import Any


from DataStructure.tree.BinaryTree import BinaryTree


try:
    from ..tree.BinaryTree import BinaryTree
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.tree.BinaryTree import BinaryTree
    sys.path.pop()
    del sys, os

class AVL(BinaryTree):
    def __init__(self, val: Any, left: 'AVL|None' = None, right: 'AVL|None' = None):
        raise NotImplementedError("AVL not implemented")