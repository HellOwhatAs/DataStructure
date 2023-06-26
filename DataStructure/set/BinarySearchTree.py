from typing import Any

try:
    from ..tree.BinaryTree import BinaryTree
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.tree.BinaryTree import BinaryTree
    sys.path.pop()
    del sys, os

class BinarySearchTree(BinaryTree):
    def __init__(self, val: Any, left: 'BinarySearchTree|None' = None, right: 'BinarySearchTree|None' = None):
        super().__init__(val, left, right)
        self.left: 'BinarySearchTree|None'
        self.right: 'BinarySearchTree|None'
    
    def search(self, val: Any):
        if val == self.val: return self
        elif val < self.val:
            if self.left is None: return self
            return self.left.search(val)
        else:
            if self.right is None: return self
            return self.right.search(val)
    
    def push(self, val: Any):
        node = self.search(val)
        if node.val == val: return
        elif node.val < val: node.right = type(self)(val)
        else: node.left = type(self)(val)

if __name__ == '__main__':
    bst = BinarySearchTree(10)
    for i in range(10):
        bst.push(i)
    print(bst)
    print(list(bst.mid_order()))