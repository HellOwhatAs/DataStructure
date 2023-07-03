try:
    from .Graph import Graph
    from ..set.DisjointSet import DisjointSet
    from ..tree.PriorityQueue import PriorityQueue
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.graph.Graph import Graph
    from DataStructure.set.DisjointSet import DisjointSet
    from DataStructure.tree.PriorityQueue import PriorityQueue
    sys.path.pop()
    del sys, os

def kruskal(g: Graph):
    djs = DisjointSet(len(g))
    pq = PriorityQueue((weight, start, end) for start, end, weight in g.edges())
    ret = type(g)(len(g))
    count = 0
    while count < len(g) - 1:
        weight, start, end = pq.pop()
        if djs.find(start) != djs.find(end):
            djs.union(start, end)
            ret.add_edge(start, end, weight)
            count += 1
    return ret

if __name__ == '__main__':
    from Graph import AdjListGraph
    g = AdjListGraph(6)
    for edge in (
        (1, 2, 6), (1, 3, 1), (1, 4, 5),
        (2, 3, 5), (2, 5, 3),
        (3, 4, 5), (3, 5, 6), (3, 6, 4),
        (4, 6, 2),
        (5, 6, 6)
    ):
        g.add_edge(edge[0] - 1, edge[1] - 1, edge[2])
    print(list(g.edges()))

    g2 = kruskal(g)
    print(list(g2.edges()))