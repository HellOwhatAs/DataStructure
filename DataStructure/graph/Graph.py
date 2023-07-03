from typing import Generator, Tuple, Literal
from abc import ABC, abstractmethod
from numbers import Real
from math import inf, isinf

class Graph(ABC):
    @abstractmethod
    def __init__(self, num_nodes: int):...

    @abstractmethod
    def __len__(self):...

    @abstractmethod
    def add_edge(self, start: int, end: int, weight: Real = 1):...

    @abstractmethod
    def exist_edge(self, start: int, end: int):...

    @abstractmethod
    def edge_weight(self, start: int, end: int) -> Real:...

    @abstractmethod
    def remove_edge(self, start: int, end: int):...

    @abstractmethod
    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:...

    @abstractmethod
    def degree(self, node: int) -> int:...

class DirectedGraph(Graph):
    @abstractmethod
    def degree(self, node: int, degree_type: Literal['in', 'out']) -> int:...

class AdjMatrixGraph(Graph):
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        self.mat = [[inf] * self.n for _ in range(self.n)]
    
    def __len__(self):
        return self.n

    def add_edge(self, start: int, end: int, weight: Real = 1):
        self.mat[end][start] = self.mat[start][end] = weight

    def exist_edge(self, start: int, end: int):
        return not isinf(self.mat[start][end])

    def edge_weight(self, start: int, end: int) -> Real:
        return self.mat[start][end]

    def remove_edge(self, start: int, end: int):
        self.mat[start][end] = self.mat[end][start] = None

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for idx in range(self.n):
            if idx == node: continue
            if not isinf(self.mat[node][idx]):
                yield idx, self.mat[node][idx]

    def degree(self, node: int) -> int:
        return sum((not isinf(elem)) for elem in self.mat[node]) + (not isinf(self.mat[node][node]))
        

class DirectedAdjMatrixGraph(DirectedGraph):
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        self.mat = [[inf] * self.n for _ in range(self.n)]
    
    def __len__(self):
        return self.n

    def add_edge(self, start: int, end: int, weight: Real = 1):
        self.mat[start][end] = weight

    def exist_edge(self, start: int, end: int):
        return not isinf(self.mat[start][end])

    def edge_weight(self, start: int, end: int) -> Real:
        return self.mat[start][end]

    def remove_edge(self, start: int, end: int):
        self.mat[start][end] = None

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for idx in range(self.n):
            if idx == node: continue
            if not isinf(self.mat[node][idx]):
                yield idx, self.mat[node][idx]
    
    def degree(self, node: int, degree_type: Literal['in', 'out']) -> int:
        if degree_type == 'in':
            return sum((not isinf(self.mat[i][node])) for i in range(self.n))
        elif degree_type == 'out':
            return sum((not isinf(elem)) for elem in self.mat[node])
        else: raise TypeError("Invalid degree_type")

class AdjListGraph(Graph):
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        self.list = [{} for _ in range(self.n)]
    
    def __len__(self):
        return self.n

    def add_edge(self, start: int, end: int, weight: Real = 1):
        self.list[end][start] = self.list[start][end] = weight

    def exist_edge(self, start: int, end: int):
        return end in self.list[start]

    def edge_weight(self, start: int, end: int) -> Real:
        return self.list[start][end] if end in self.list[start] else inf
    
    def remove_edge(self, start: int, end: int):
        self.list[start].pop(end)
        self.list[end].pop(start)

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for k, v in self.list[node].items():
            yield k, v

    def degree(self, node: int) -> int:
        return len(self.list[node]) + (node in self.list[node])

class DirectedAdjListGraph(DirectedGraph):
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        self.list = [{} for _ in range(self.n)]
    
    def __len__(self):
        return self.n

    def add_edge(self, start: int, end: int, weight: Real = 1):
        self.list[start][end] = weight

    def exist_edge(self, start: int, end: int):
        return end in self.list[start]
    
    def edge_weight(self, start: int, end: int) -> Real:
        return self.list[start][end] if end in self.list[start] else inf
    
    def remove_edge(self, start: int, end: int):
        self.list[start].pop(end)

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for k, v in self.list[node].items():
            yield k, v

    def degree(self, node: int, degree_type: Literal['in', 'out']) -> int:
        if degree_type == 'in':
            return sum((node in l) for l in self.list)
        elif degree_type == 'out':
            return len(self.list[node])
        else: raise TypeError("Invalid degree_type")

if __name__ == '__main__':
    g = DirectedAdjListGraph(7)
    for edge in (
        (1, 2),
        (2, 3), (2, 4),
        (3, 1),
        (4, 1), (4, 3),
        (5, 6), (5, 7),
        (6, 2),
        (7, 4), (7, 6)
    ):
        g.add_edge(edge[0]-1, edge[1]-1)

    for i in range(len(g)):
        print(i + 1, g.degree(i, 'in'), g.degree(i, 'out'))