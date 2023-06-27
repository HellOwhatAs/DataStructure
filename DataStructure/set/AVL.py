from typing import Any

try:
    from ..tree.BinaryTree import BinaryTree
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.tree.BinaryTree import BinaryTree
    sys.path.pop()
    del sys, os

class AVL(BinaryTree):
    raise NotImplementedError("AVL not implemented")