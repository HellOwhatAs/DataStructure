from typing import Iterable, Any
try:
    from .Array import Array
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.linear.Array import Array
    sys.path.pop()
    del sys, os

class Stack(Array):
    def __init__(self, init: Iterable[Any] = None):
        super().__init__(init)
    def top(self):
        return self.data[self.length - 1]
    
if __name__ == '__main__':
    s = Stack()
    for i in range(10):
        s.push(i)
    print(s)
    while not s.empty():
        print(s.pop())