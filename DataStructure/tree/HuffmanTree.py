from typing import Any, Dict, Optional
from numbers import Real

try:
    from .BinaryTree import BinaryTree
    from .PriorityQueue import PriorityQueue
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.tree.BinaryTree import BinaryTree
    from DataStructure.tree.PriorityQueue import PriorityQueue
    sys.path.pop(0)
    del sys, os

class HuffmanTree(BinaryTree):
    def __init__(self, val: Any, weight: Real, left: Optional['HuffmanTree'] = None, right: Optional['HuffmanTree'] = None):
        super().__init__(val, left, right)
        self.weight = weight
        self.left: Optional[HuffmanTree]
        self.right: Optional[HuffmanTree]

    @classmethod
    def build(cls, data: Dict[Any, Real]) -> 'HuffmanTree':
        heap = PriorityQueue([cls(k, v) for k, v in data.items()])
        while len(heap) > 1:
            a, b = heap.pop(), heap.pop()
            heap.push(cls(None, a.weight + b.weight, a, b))
        return heap.top()
    
    def __gt__(self, other: 'HuffmanTree'):
        return self.weight > other.weight

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.val}, {self.weight}, {repr(self.left)}, {repr(self.right)})"

    def getcode(self, path: str = ''):
        if self.left is self.right is None:
            yield (self.val, path)
        if self.left is not None:
            for elem in self.left.getcode(path + '0'):
                yield elem
        if self.right is not None:
            for elem in self.right.getcode(path + '1'):
                yield elem
        


if __name__ == '__main__':
    data = {
        'a': 10,
        'e': 15,
        'i': 12,
        's': 3,
        't': 4,
        ' ': 13,
        '\n': 1
    }
    hftree = HuffmanTree.build(data)
    print(hftree)
    print(list(hftree.getcode()))
    print(sum(data[k]*len(v) for k, v in hftree.getcode()))
    print(hftree.size, hftree.depth)