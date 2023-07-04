from typing import Any

try:
    from ..tree.BinaryTree import BinaryTree
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.tree.BinaryTree import BinaryTree
    sys.path.pop(0)
    del sys, os

class AVL(BinaryTree):
    raise NotImplementedError("AVL not implemented")