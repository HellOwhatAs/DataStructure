from typing import Iterable, Any, Optional
try:
    from ..linear.Array import Array
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.linear.Array import Array
    sys.path.pop(0)
    del sys, os

class PriorityQueue:
    def __init__(self, init: Optional[Iterable[Any]] = None):
        self.data = Array([None])
        if init is not None:
            for elem in init: self.data.push(elem)
            for idx in reversed(range(1, len(self) // 2 + 1)):
                self.__percolate_down(idx)
    
    @property
    def length(self):
        return len(self.data) - 1
    
    def __len__(self):
        return self.length
    
    def __percolate_up(self, idx: int):
        if idx == 1: return
        if self.data[idx // 2] > self.data[idx]:
            self.data[idx // 2], self.data[idx] = self.data[idx], self.data[idx // 2]
            self.__percolate_up(idx // 2)

    def __percolate_down(self, idx: int):
        if idx * 2 + 1 < len(self.data):
            left_idx, right_idx = idx * 2, idx * 2 + 1
            left_val, right_val = self.data[left_idx], self.data[right_idx]
            if self.data[idx] > min(left_val, right_val):
                if left_val > right_val:
                    self.data[right_idx], self.data[idx] = self.data[idx], self.data[right_idx]
                    self.__percolate_down(right_idx)
                else:
                    self.data[left_idx], self.data[idx] = self.data[idx], self.data[left_idx]
                    self.__percolate_down(left_idx)
        elif idx *2 < len(self.data):
            if self.data[idx] > self.data[idx * 2]:
                self.data[idx], self.data[idx * 2] = self.data[idx * 2], self.data[idx]
                self.__percolate_down(idx * 2)

    def push(self, val: Any):
        self.data.push(val)
        self.__percolate_up(len(self))
    
    def top(self):
        return self.data[1]
    
    def pop(self):
        ret = self.data[1]
        self.data[1] = self.data.pop()
        self.__percolate_down(1)
        return ret

    def empty(self):
        return len(self) == 0
    
    def __repr__(self):
        return f"{type(self).__name__}({[self.data[i] for i in range(1, len(self.data))]})"

if __name__ == '__main__':
    pq = PriorityQueue([5,4,3,2,1])
    pq.push(23)
    print(pq)
    pq.push(5)
    print(pq)
    pq.push(25)
    print(pq)
    pq.push(-120)
    print(pq)
    pq.push(23000)
    print(pq)
    pq.push(20)
    print(pq)
    while not pq.empty():
        print(pq.pop())