from typing import Iterable, Any

class Array:
    def __init__(self, init: Iterable[Any] = None):
        self.data = [i for i in init] if init else []
        self.length = len(self.data)
        self.data.extend([0] * max(20, self.length))
        self.maxlength = len(self.data)

    def __getitem__(self, idx: int):
        return self.data[idx]
    
    def __setitem__(self, idx: int, val: Any):
        self.data[idx] = val

    def __repr__(self):
        return f"{type(self).__name__}({(self.data[:self.length])})"
    
    def clear(self):
        self.length = 0

    def push(self, val: Any):
        if self.length == self.maxlength:
            self.data.extend([0]*self.length)
            self.maxlength = len(self.data)
        self.data[self.length] = val
        self.length += 1

    def pop(self, idx: int = None):
        if idx is None:
            self.length -= 1
            return self.data[self.length]
        ret = self.data[idx]
        self.data[idx: self.length - 1] = self.data[idx + 1: self.length]
        self.length -= 1
        return ret
    
    def insert(self, idx: int, val: Any):
        if self.length == self.maxlength:
            self.data.extend([0]*self.length)
            self.maxlength = len(self.data)
        self.data[idx + 1: self.length + 1] = self.data[idx: self.length]
        self.data[idx] = val
        self.length += 1
        
    def empty(self):
        return self.length == 0

    def __len__(self):
        return self.length
    
if __name__ == '__main__':

    a = Array([1,2,3,4])
    print(a[1])
    a[1] = 100
    print(a)
    a.push(123)
    print(a)
    a.insert(0, 114)
    print(a)
    print(a.pop(1))
    print(a)
    print(a.pop())
    print(a)
    a.clear()
    print(a)