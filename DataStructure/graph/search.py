from typing import Callable, List, Optional

try:
    from .Graph import Graph
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.graph.Graph import Graph
    sys.path.pop()
    del sys, os

def __dfs(g: Graph, visited: List[bool], start: int, f: Callable[[int], None]):
    if visited[start]: return
    visited[start] =  True
    f(start, visited)
    for neibour, weight in g.get_neibours(start):
        __dfs(g, visited, neibour, f)

def dfs(g: Graph, f: Callable[[int, List[bool]], None], start: Optional[int] = None, *, newtree: Optional[Callable[[List[bool]], None]] = None):
    visited = [False] * len(g)
    if start is not None: __dfs(g, visited, start, f)
    for i in range(len(g)):
        if not visited[i]:
            __dfs(g, visited, i, f)
            if newtree is not None: newtree(visited)

if __name__ == '__main__':

    from Graph import DirectedAdjListGraph
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

    dfs(g, lambda x, y: print(x + 1, end=' '), newtree=print)