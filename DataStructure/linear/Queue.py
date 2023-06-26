from typing import Iterable, Any
try:
    from .List import List
    from .Array import Array
    from ..tree.PriorityQueue import PriorityQueue
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.linear.List import List
    from DataStructure.linear.Array import Array
    from DataStructure.tree.PriorityQueue import PriorityQueue
    sys.path.pop()
    del sys, os

class Queue(List):
    def __init__(self, init: Iterable[Any] = None):
        super().__init__(init)

    def pop(self, idx: int = 0):
        if self.empty():
            raise IndexError(f"get from empty {type(self).__name__}")
        return super().pop(idx)
    
    def getfront(self):
        if self.empty():
            raise IndexError(f"get from empty {type(self).__name__}")
        return self.head.next.val
    
    def getrear(self):
        if self.empty():
            raise IndexError(f"get from empty {type(self).__name__}")
        return self.tail.val
    
class CircularQueue:
    def __init__(self, maxlength: int) -> None:
        self.maxlength = (maxlength + 1)
        self.data = Array([0] * self.maxlength)
        self.front = 0
        self.rear = 0

    def push(self, val: Any):
        if self.full():
            raise MemoryError(f"push to full {type(self).__name__}")
        self.rear = (self.rear + 1) % self.maxlength
        self.data[self.rear] = val

    def pop(self):
        if self.empty():
            raise IndexError(f"pop from empty {type(self).__name__}")
        self.front = (self.front + 1) % self.maxlength
        return self.data[self.front]
    
    def getfront(self):
        if self.empty():
            raise IndexError(f"get from empty {type(self).__name__}")
        return self.data[(self.front + 1) % self.maxlength]
    
    def getrear(self):
        if self.empty():
            raise IndexError(f"get from empty {type(self).__name__}")
        return self.data[self.rear]
    
    def __repr__(self):
        vals = []
        tmp = self.front
        while tmp != self.rear:
            tmp = (tmp + 1) % self.maxlength
            vals.append(self.data[tmp])
        return f"{type(self).__name__}({vals})"
    
    def empty(self):
        return self.front == self.rear
    
    def full(self):
        return (self.rear + 1) % self.maxlength == self.front

    def __len__(self):
        return (self.rear - self.front) % self.maxlength


if __name__ == '__main__':
    q = Queue([1,2,3,4,5])
    q.push(1145)
    print(q, q.getfront(), q.getrear())
    while not q.empty():
        print(q.pop())

    cq = CircularQueue(10)
    for i in range(10):
        for j in range(6):
            cq.push(i*100 + j)
            print(cq, len(cq))
        for j in range(5):
            cq.pop()
            print(cq, len(cq))