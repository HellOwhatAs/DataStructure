from typing import Callable, List, Optional

try:
    from .Graph import Graph
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.graph.Graph import Graph
    sys.path.pop()
    del sys, os

def __dfs(g: Graph, visited: List[bool], start: int, on_visit: Callable[[int], None]):
    if visited[start]: return
    visited[start] =  True
    on_visit(start, visited)
    for neibour, weight in g.get_neibours(start):
        __dfs(g, visited, neibour, on_visit)

def dfs(g: Graph, on_visit: Callable[[int, List[bool]], None], start: Optional[int] = None, *, on_tree_over: Optional[Callable[[List[bool]], None]] = None):
    visited = [False] * len(g)
    if start is not None: __dfs(g, visited, start, on_visit)
    for i in range(len(g)):
        if not visited[i]:
            __dfs(g, visited, i, on_visit)
            if on_tree_over is not None: on_tree_over(visited)

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

    dfs(g, lambda x, y: print(x + 1, end=' '), on_tree_over=print)

    print(g.edge_weight(2, 0))