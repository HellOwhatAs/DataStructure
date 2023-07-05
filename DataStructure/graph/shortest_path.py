from typing import Union, List, Optional, overload
from math import inf, isinf
from copy import deepcopy

try:
    from .search import top_sort
    from .Graph import Graph, DirectedGraph
    from ..linear.Queue import Queue
    from ..tree.PriorityQueue import PriorityQueue
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.graph.search import top_sort
    from DataStructure.graph.Graph import Graph, DirectedGraph
    from DataStructure.linear.Queue import Queue
    from DataStructure.tree.PriorityQueue import PriorityQueue
    sys.path.pop(0)
    del sys, os

@overload
def extract_path(prev: List[Optional[int]], target: int):
    '''extract single source path to target'''
@overload
def extract_path(prev: List[List[Optional[int]]], source: int, target: int):
    '''extract floyd path from source to target'''
def extract_path(prev, *args):
    path = []
    if len(args) == 1 and isinstance(args[0], int) and isinstance(prev, List):
        target, = args
        while target is not None:
            path.append(target)
            target = prev[target]
    elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(prev, List) and all(isinstance(elem, List) for elem in prev):
        source, target = args
        while target != source and target is not None:
            path.append(target)
            target = prev[source][target]
        path.append(source)
    else: raise TypeError("no matching function to call")
    path.reverse()
    return path

def unweighted(g: Union[Graph, DirectedGraph], source: int, target: Optional[int] = None):
    prev: List[Optional[int]]
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
    if target is None: return dist, prev
    return dist[target], extract_path(prev, target)

def dijkstra(g: Union[Graph, DirectedGraph], source: int, target: Optional[int] = None):
    prev: List[Optional[int]]
    dist, prev = [inf] * len(g), [None] * len(g)
    dist[source] = 0
    pq = PriorityQueue([(0, source)])
    while not pq.empty():
        d, node = pq.pop()
        if d > dist[node]: continue
        for neibour, weight in g.get_neibours(node):
            if dist[neibour] > dist[node] + weight:
                dist[neibour] = dist[node] + weight
                prev[neibour] = node
                pq.push((dist[neibour], neibour))
    if target is None: return dist, prev
    return dist[target], extract_path(prev, target)

def bellman_ford(g: Union[Graph, DirectedGraph], source: int, target: Optional[int] = None):
    prev: List[Optional[int]]
    dist, prev = [inf] * len(g), [None] * len(g)
    dist[source] = 0
    for _ in range(len(g)):
        flag = True
        for s, t, w in g.edges():
            if dist[s] + w < dist[t]:
                dist[t] = dist[s] + w
                prev[t] = s
                flag = False
        if flag: break
    else: raise TypeError('exists negative circle in graph', {'dist': dist, 'prev': prev})
    if target is None: return dist, prev
    return dist[target], extract_path(prev, target)

def acyclic(g: DirectedGraph, source: int, target: Optional[int] = None):
    prev: List[Optional[int]]
    dist, prev = [inf] * len(g), [None] * len(g)
    dist[source] = 0
    for node in top_sort(g):
        for neibour, weight in g.get_neibours(node):
            if dist[neibour] > dist[node] + weight:
                dist[neibour] = dist[node] + weight
                prev[neibour] = node
    if target is None: return dist, prev
    return dist[target], extract_path(prev, target)

def floyd(g: Union[Graph, DirectedGraph]):
    dist = [[(0 if i == j else (g.edge_weight(i, j) if g.exist_edge(i, j) else inf)) for j in range(len(g))] for i in range(len(g))]
    prev = [[(i if i != j and g.exist_edge(i, j) else None) for j in range(len(g))] for i in range(len(g))]
    for k in range(len(g)):
        for i in range(len(g)):
            for j in range(len(g)):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]
    return dist, prev

if __name__ == '__main__':
    from Graph import DirectedAdjListGraph
    g = DirectedAdjListGraph(7)
    for edge in (
        (0, 1, 2), (0, 3, 1),
        (1, 3, 3), (1, 4, 10),
        (2, 0, 4), (2, 5, 5),
        (3, 2, 2), (3, 4, 2), (3, 5, 8), (3, 6, 4),
        (4, 6, 6),

        (6, 5, 1)
    ): g.add_edge(*edge)

    print(g.graphviz())

    dist, path = unweighted(g, 2, 4)
    print(dist, path)
    
    dist, path = dijkstra(g, 2, 4)
    print(dist, path)

    dist, path = bellman_ford(g, 2, 4)
    print(dist, path)

    dist, prev = floyd(g)
    print(dist[2][4], extract_path(prev, 2, 4))

    dag = deepcopy(g)
    dag.remove_edge(6, 5), dag.remove_edge(3, 2), dag.remove_edge(3, 5)
    dag.add_edge(5, 6, 1)

    print(dag.graphviz())

    dist, path = acyclic(dag, 0, 4)
    print(dist, path)