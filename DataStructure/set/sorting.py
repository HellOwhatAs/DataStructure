from typing import List
from copy import deepcopy
try:
    from .binary_search import binary_search
    from ..tree.PriorityQueue import PriorityQueue
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.set.binary_search import binary_search
    from DataStructure.tree.PriorityQueue import PriorityQueue
    sys.path.pop()
    del sys, os

def InsertSort(a: List, *, inplace: bool = False):
    if not inplace: a = deepcopy(a)
    for j in range(1, len(a)):
        tmp = a[j]
        for k in reversed(range(j)):
            if a[k] <= tmp:
                a[k + 1] = tmp
                break
            a[k + 1] = a[k]
        else: a[0] = tmp
    return a

def BinaryInsertSort(a: List, *, inplace: bool = False):
    if not inplace: a = deepcopy(a)
    for j in range(1, len(a)):
        tmp = a[j]
        idx = binary_search(a, tmp, 0, j)
        a[idx + 1: j + 1] = a[idx: j]
        a[idx] = tmp
    return a

def ShellSort(a: List):
    raise NotImplementedError("ShellSort not implemented")

def SelectSort(a: List, *, inplace: bool = False):
    if not inplace: a = deepcopy(a)
    for i in range(len(a)):
        min_val, min_idx = float('inf'), None
        for j in range(i, len(a)):
            if a[j] < min_val:
                min_val, min_idx = a[j], j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

class __RefPriorityQueue(PriorityQueue):
    class OffsetArray:
        def __init__(self, array, offset: int = 0):
            self.array = array
            self.offset = offset
            self.end = len(array)
        def __getitem__(self, idx: int):
            return self.array[idx + self.offset]
        def __setitem__(self, idx: int, val):
            self.array[idx + self.offset] = val
        def __len__(self):
            return self.end - self.offset
        def pop(self):
            self.end -= 1
            return self.array[self.end]
    def __init__(self, array) -> None:
        self.data = self.OffsetArray(array, -1)
        for idx in reversed(range(1, len(self) // 2 + 1)):
            super()._PriorityQueue__percolate_down(idx)

def HeapSort(a: List, *, inplace: bool = False):
    if not inplace:
        pq = PriorityQueue(a)
        return [pq.pop() for _ in range(len(pq))]
    pq = __RefPriorityQueue(a)
    while not pq.empty():
        pq.data.array[pq.data.end] = pq.pop()
    a.reverse()
    return a

def BubbleSort(a: List, *, inplace: bool = False):
    if not inplace: a = deepcopy(a)
    for _ in range(1, len(a)):
        flag = True
        for i in range(1, len(a)):
            if a[i-1] > a[i]:
                flag = False
                a[i-1], a[i] = a[i], a[i-1]
        if flag: break
    return a

def QuickSort(a: List, *, inplace: bool = False):
    if not inplace: a = deepcopy(a)
    raise NotImplementedError("ShellSort not implemented")

if __name__ == '__main__':
    import random
    l = list(range(100))
    random.shuffle(l)
    print(BubbleSort(l, inplace=True) == sorted(l))
    print(l)