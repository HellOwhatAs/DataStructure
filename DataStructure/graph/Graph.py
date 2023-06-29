from typing import Generator, Tuple
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
    def remove_edge(self, start: int, end: int):...

    @abstractmethod
    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:...

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

    def remove_edge(self, start: int, end: int):
        self.mat[start][end] = self.mat[end][start] = None

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for idx in range(self.n):
            if idx == node: continue
            if not isinf(self.mat[node][idx]):
                yield idx, self.mat[node][idx]

class DirectedAdjMatrixGraph(Graph):
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        self.mat = [[inf] * self.n for _ in range(self.n)]
    
    def __len__(self):
        return self.n

    def add_edge(self, start: int, end: int, weight: Real = 1):
        self.mat[start][end] = weight

    def exist_edge(self, start: int, end: int):
        return not isinf(self.mat[start][end])

    def remove_edge(self, start: int, end: int):
        self.mat[start][end] = None

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for idx in range(self.n):
            if idx == node: continue
            if not isinf(self.mat[node][idx]):
                yield idx, self.mat[node][idx]

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
    
    def remove_edge(self, start: int, end: int):
        self.list[start].pop(end)
        self.list[end].pop(start)

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for k, v in self.list[node].items():
            yield k, v

class DirectedAdjListGraph(Graph):
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        self.list = [{} for _ in range(self.n)]
    
    def __len__(self):
        return self.n

    def add_edge(self, start: int, end: int, weight: Real = 1):
        self.list[start][end] = weight

    def exist_edge(self, start: int, end: int):
        return end in self.list[start]
    
    def remove_edge(self, start: int, end: int):
        self.list[start].pop(end)

    def get_neibours(self, node: int) -> Generator[Tuple[int, Real], None, None]:
        for k, v in self.list[node].items():
            yield k, v