from typing import Iterable, Any

class Node:
    def __init__(self, val: Any, next: 'Node|None'):
        self.val = val
        self.next = next

class List:
    def __init__(self, init: Iterable[Any] = None):
        self.head = Node(0, None)
        self.tail = self.head
        if init:
            for i in init: self.push(i)

    def push(self, val: Any):
        self.tail.next = Node(val, None)
        self.tail = self.tail.next
        self.head.val += 1

    def pop(self, idx: int = None):
        if idx is None: idx = self.head.val - 1
        p = self.head
        for _ in range(idx): p = p.next
        if p.next is self.tail: self.tail = p
        ret = p.next.val
        p.next = p.next.next
        self.head.val -= 1
        return ret
    
    def __repr__(self):
        vals = []
        p = self.head
        while p.next is not None:
            p = p.next
            vals.append(p.val)
        return f"{type(self).__name__}({vals})"
    
    def __getitem__(self, idx: int):
        if idx < 0 or idx >= self.length: raise IndexError(f"{type(self).__name__} index out of range")
        p = self.head.next
        for _ in range(idx): p = p.next
        return p.val
    
    def __setitem__(self, idx: int, val: Any):
        p = self.head.next
        for _ in range(idx): p = p.next
        p.val = val

    def clear(self):
        self.head.next = None
        self.head.val = 0

    @property
    def length(self):
        return self.head.val

    def __len__(self):
        return self.length
    
    def insert(self, idx: int, val: Any):
        p = self.head
        for _ in range(idx): p = p.next
        p.next = Node(val, p.next)
        self.head.val += 1
        
    def empty(self):
        return self.length == 0

    def reverse(self):
        if self.empty(): return
        new_list = None
        self.tail = self.head.next
        while self.head.next is not None:
            tmp = self.head.next.next
            self.head.next.next = new_list
            new_list = self.head.next
            self.head.next = tmp
        self.head.next = new_list


if __name__ == '__main__':
    l = List([1,2,3,4])
    print(l)
    l.reverse()
    l.push(1234)
    print(l)
    print(l.pop())
    print(l)
    print(l[2])
    l[2] = -10
    print(l)
    print(l.length)
    l.insert(1, 100000)
    print(l)
    print(l.length)
    print(l.pop(0))
    print(l)
    print(l.pop(2))
    print(l)
    l.reverse()
    print(l)