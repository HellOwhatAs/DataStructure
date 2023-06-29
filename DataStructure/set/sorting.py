from typing import List, Optional
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

def ShellSort(a: List, *, inplace: bool = False):
    if not inplace: a = deepcopy(a)
    step = len(a) // 2
    while step:
        for i in range(step):
            for j in range(i + step, len(a), step):
                tmp = a[j]
                for k in range(j - step, -1, -step):
                    if a[k] <= tmp:
                        a[k + step] = tmp
                        break
                    a[k + step] = a[k]
                else: a[i] = tmp
        step //= 2
    return a

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

def __divide(a: List, start: int, end: int):
    if end - start + 1 <= 1: return start
    pivot = a[start]
    activate = True
    while start < end:
        if activate:
            if a[end] > pivot: end -= 1
            else:
                a[start] = a[end]
                start += 1
                activate = False
        else:
            if a[start] < pivot: start += 1
            else:
                a[end] = a[start]
                end -= 1
                activate = True
    a[start] = pivot
    return start

def QuickSort(a: List, start: int = 0, end: Optional[int] = None, *, inplace: bool = False):
    if end is None: end = len(a) - 1
    if not inplace:
        a = a[start: end + 1]
        if len(a) <= 1: return a
        pivot = a[0]
        return QuickSort([i for i in a if i < pivot]) + [pivot] * (a.count(pivot)) + QuickSort([i for i in a if i > pivot])
    else:
        if end - start + 1 <= 1: return a
        mid = __divide(a, start, end)
        QuickSort(a, start, mid - 1, inplace=True)
        QuickSort(a, mid + 1, end, inplace=True)
        return a

def __merge(a: List, b: List):
    ret = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            ret.append(a[i])
            i += 1
        else:
            ret.append(b[j])
            j += 1
    while i < len(a):
        ret.append(a[i])
        i += 1
    while j < len(b):
        ret.append(b[j])
        j += 1
    return ret

def MergeSort(a: List):
    if len(a) <= 1: return a
    mid = len(a) // 2
    return __merge(MergeSort(a[:mid]), MergeSort(a[mid:]))

def __non_neg_bucketsort(a: List, *, num_buckets: int = 10):
    div = 1
    buckets = [[] for _ in range(num_buckets)]
    while True:
        for elem in a:
            buckets[(elem // div) % num_buckets].append(elem)
        a = sum(buckets, [])
        count = 0
        for bucket in buckets:
            if bucket:
                bucket.clear()
                count += 1
        if count == 1: break
        div *= num_buckets
    return a

def BucketSort(a: List, *, num_buckets: int = 10):
    negs, a1 = [], []
    for elem in a:
        if elem < 0: negs.append(-elem)
        else: a1.append(elem)

    a2 = __non_neg_bucketsort(a1, num_buckets = num_buckets)

    if negs:
        ret = [-elem for elem in reversed(__non_neg_bucketsort(negs, num_buckets = num_buckets))]
        ret.extend(a2)
        return ret
    return a2

if __name__ == '__main__':
    import random
    l = list(range(-5, 5))
    l = [*l] * 3
    random.shuffle(l)
    print(l)
    print(ShellSort(l, inplace=True) == sorted(l))
    print(l)