from typing import Generator, Tuple, Literal, Optional, overload
from abc import ABC, abstractmethod
from numbers import Real
from math import inf, isinf

class Graph(ABC):
    
    @property
    def directed(self):
        return False
    
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

    @abstractmethod
    def edges(self) -> Generator[Tuple[int, int, Real], None, None]:...

    def graphviz(self):
        return '\n'.join(('graph{', *(f'{node};' for node in range(len(self))), *(f'{s} -- {t} [label={w}];' for s, t, w in self.edges()), '}'))
    
    @overload
    def renderHTML(self, filename: str, *, engine: Literal['circo', 'dot', 'fdp', 'sfdp', 'neato', 'osage', 'patchwork', 'twopi'] = 'dot') -> None:...
    @overload
    def renderHTML(self, *, engine: Literal['circo', 'dot', 'fdp', 'sfdp', 'neato', 'osage', 'patchwork', 'twopi'] = 'dot') -> str:...
    def renderHTML(self, filename: Optional[str] = None, *, engine: Literal['circo', 'dot', 'fdp', 'sfdp', 'neato', 'osage', 'patchwork', 'twopi'] = 'dot'):
        htmlcode = '''
        <!DOCTYPE html>
        <meta charset="utf-8">
        <body>
        <script src="https://cdn.jsdelivr.net/npm/d3@7.8.5/dist/d3.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@hpcc-js/wasm@2.13.0/dist/graphviz.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/d3-graphviz@5.0.2/build/d3-graphviz.min.js"></script>
        <div id="graph" style="text-align: center; width: 100%;"></div>
        <script>
        d3.select("#graph").graphviz().width('100%').height('95vh').fit(true).engine('{engine}')
        .renderDot({dotcode});
        </script>
        '''.format(dotcode = repr(self.graphviz()), engine = engine)
        if filename is None: return htmlcode
        with open(filename, 'w', encoding='utf-8') as f: f.write(htmlcode)

class DirectedGraph(Graph):
    
    @property
    def directed(self):
        return True
    
    @abstractmethod
    def degree(self, node: int, degree_type: Literal['in', 'out']) -> int:...

    def graphviz(self):
        return '\n'.join(('digraph{', *(f'{node};' for node in range(len(self))), *(f'{s} -> {t} [label={w}];' for s, t, w in self.edges()), '}'))

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
    
    def edges(self) -> Generator[Tuple[int, int, Real], None, None]:
        for start in range(self.n):
            for end in range(start, self.n):
                if not isinf(self.mat[start][end]):
                    yield start, end, self.mat[start][end]
        

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

    def edges(self) -> Generator[Tuple[int, int, Real], None, None]:
        for start in range(self.n):
            for end in range(self.n):
                if not isinf(self.mat[start][end]):
                    yield start, end, self.mat[start][end]

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
    
    def edges(self) -> Generator[Tuple[int, int, Real], None, None]:
        for start in range(self.n):
            for end in self.list[start]:
                if end >= start:
                    yield start, end, self.list[start][end]

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

    def edges(self) -> Generator[Tuple[int, int, Real], None, None]:
        for start in range(self.n):
            for end in self.list[start]:
                yield start, end, self.list[start][end]

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

    for edge in g.edges():
        print(edge)
    
    g.renderHTML('./out.html', engine='circo')