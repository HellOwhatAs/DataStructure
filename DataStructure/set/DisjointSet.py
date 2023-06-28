try:
    from ..linear.Array import Array
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.linear.Array import Array
    sys.path.pop()
    del sys, os

class DisjointSet:
    def __init__(self, n_elem: int) -> None:
        self.data = Array([-1] * n_elem)
    
    def find(self, idx: int):
        if self.data[idx] < 0: return idx
        self.data[idx] = self.find(self.data[idx])
        return self.data[idx]

    def union(self, a: int, b: int):
        if self.find(a) == self.find(b): return
        fa, fb = self.find(a), self.find(b)
        if self.data[fa] < self.data[fb]:
            self.data[fa] += self.data[fb]
            self.data[fb] = fa
        else:
            self.data[fb] += self.data[fa]
            self.data[fa] = fb

if __name__ == '__main__':
    s = DisjointSet(10)
    s.union(1, 2)
    print(s.data)