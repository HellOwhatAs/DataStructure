from typing import Any, Dict, Optional
from numbers import Real
import heapq

try:
    from .BinaryTree import BinaryTree
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.tree.BinaryTree import BinaryTree
    sys.path.pop()
    del sys, os

class HuffmanTree(BinaryTree):
    def __init__(self, val: Any, weight: Real, left: Optional['HuffmanTree'] = None, right: Optional['HuffmanTree'] = None):
        super().__init__(val, left, right)
        self.weight = weight
        self.left: 'HuffmanTree|None'
        self.right: 'HuffmanTree|None'

    @classmethod
    def build(cls, data: Dict[Any, Real]):
        heap = [cls(k, v) for k, v in data.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            a, b = heapq.heappop(heap), heapq.heappop(heap)
            heapq.heappush(heap, cls(None, a.weight + b.weight, a, b))
        return heap[0]
    
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
    hftree = HuffmanTree.build({
        'a': 10,
        'e': 15,
        'i': 12,
        's': 3,
        't': 4,
        ' ': 13,
        '\n': 1
    })
    print(hftree)
    print(list(hftree.getcode()))
    print(hftree.size, hftree.depth)