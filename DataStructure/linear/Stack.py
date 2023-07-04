from typing import Iterable, Any, Optional
try:
    from .Array import Array
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.linear.Array import Array
    sys.path.pop(0)
    del sys, os

class Stack(Array):
    def __init__(self, init: Optional[Iterable[Any]] = None):
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