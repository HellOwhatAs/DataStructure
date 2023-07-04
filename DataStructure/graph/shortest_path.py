from typing import Union, List, Optional
from math import inf, isinf
from numbers import Real

try:
    from .Graph import Graph, DirectedGraph
    from ..linear.Queue import Queue
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.graph.Graph import Graph, DirectedGraph
    from DataStructure.linear.Queue import Queue
    sys.path.pop(0)
    del sys, os

def extract_path(prev: List[Optional[int]], target: int):
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    path.reverse()
    return path

def unweighted(g: Union[Graph, DirectedGraph], source: int):
    dist, prev = [inf] * len(g), [None] * len(g)
    dist[source] = 0
    q = Queue([source])
    while not q.empty():
        node = q.pop()
        for neibour, _ in g.get_neibours(node):
            if not isinf(dist[neibour]): continue
            dist[neibour] = dist[node] + 1
            prev[neibour] = node
            q.push(neibour)
    return dist, prev

if __name__ == '__main__':
    from Graph import DirectedAdjListGraph
    g = DirectedAdjListGraph(7)
    for edge in (
        (0, 1), (0, 3),
        (1, 3), (1, 4),
        (2, 0), (2, 5),
        (3, 2), (3, 4), (3, 5), (3, 6),
        (4, 6),

        (6, 5)
    ):
        g.add_edge(*edge)
    dist, prev = unweighted(g, 2)
    print(dist[4])
    print(extract_path(prev, 4))