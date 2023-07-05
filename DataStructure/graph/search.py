from typing import Callable, List, Optional, Union, overload

try:
    from .Graph import Graph, DirectedGraph
    from ..linear.Queue import Queue
    from ..tree.PriorityQueue import PriorityQueue
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.graph.Graph import Graph, DirectedGraph
    from DataStructure.linear.Queue import Queue
    from DataStructure.tree.PriorityQueue import PriorityQueue
    sys.path.pop(0)
    del sys, os

def __dfs(g: Union[Graph, DirectedGraph], visited: List[bool], start: int, on_visit: Callable[[int], None]):
    if visited[start]: return
    visited[start] =  True
    on_visit(start, visited)
    for neibour, weight in g.get_neibours(start):
        __dfs(g, visited, neibour, on_visit)

def dfs(g: Union[Graph, DirectedGraph], on_visit: Callable[[int, List[bool]], None], start: Optional[int] = None,
        *, on_tree_over: Optional[Callable[[List[bool]], bool]] = None):
    visited = [False] * len(g)
    if start is not None:
        __dfs(g, visited, start, on_visit)
        if on_tree_over is not None:
            if on_tree_over(visited): return
    for i in range(len(g)):
        if not visited[i]:
            __dfs(g, visited, i, on_visit)
            if on_tree_over is not None:
                if on_tree_over(visited): return

def __bfs(g: Union[Graph, DirectedGraph], visited: List[bool], start: int, on_visit: Callable[[int], None]):
    q = Queue()
    q.push(start)
    while not q.empty():
        node = q.pop()
        if visited[node]: continue
        on_visit(node, visited)
        visited[node] = True
        for neibour, weight in g.get_neibours(node):
            if not visited[neibour]: q.push(neibour)

def bfs(g: Union[Graph, DirectedGraph], on_visit: Callable[[int, List[bool]], None], start: Optional[int] = None,
        *, on_tree_over: Optional[Callable[[List[bool]], bool]] = None):
    visited = [False] * len(g)
    if start is not None:
        __bfs(g, visited, start, on_visit)
        if on_tree_over is not None:
            if on_tree_over(visited): return
    for i in range(len(g)):
        if not visited[i]:
            __bfs(g, visited, i, on_visit)
            if on_tree_over is not None:
                if on_tree_over(visited): return

@overload
def euler_path(g: DirectedGraph, start: Optional[int] = None):...

def __directed_euler_path_dfs(curr: int, heap_g: List[PriorityQueue]):
    while not heap_g[curr].empty():
        tmp, weight = heap_g[curr].pop()
        if weight > 1: heap_g[curr].push((tmp, weight - 1))
        for _ in __directed_euler_path_dfs(tmp, heap_g): yield _
    yield curr

def __directed_euler_path(g: DirectedGraph, start: Optional[int] = None):
    unbalanced = sorted([(i, tmp) for i in range(len(g)) if (tmp := g.degree(i, 'in') - g.degree(i, 'out')) != 0], key=lambda x: x[1])
    if len(unbalanced) == 1 or len(unbalanced) > 2: raise TypeError(f"{g} does not exists euler path")
    if start is None:
        if len(unbalanced) == 0: start = 0
        else: start = unbalanced[0][0]
    ret = list(__directed_euler_path_dfs(start, [PriorityQueue(g.get_neibours(i)) for i in range(len(g))]))
    ret.reverse()
    return ret

@overload
def euler_path(g: Graph, start: Optional[int] = None):...

def __euler_path(g: Graph, start: Optional[int] = None):
    raise NotImplementedError('euler path undirected graph not implemented')

def euler_path(g: Union[Graph, DirectedGraph], start: Optional[int] = None):
    if isinstance(g, DirectedGraph): return __directed_euler_path(g, start)
    return __euler_path(g, start)

if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.graph.Graph import DirectedAdjListGraph
    sys.path.pop(0)
    del sys, os

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

    dfs(g, lambda x, y: print(x + 1, end=' '), start=4, on_tree_over=print)
    bfs(g, lambda x, y: print(x + 1, end=' '), start=4, on_tree_over=print)

    g2 = DirectedAdjListGraph(6)
    for edge in (
        (0, 1), (1, 2), (2, 3), (3, 1), (1, 4), (4, 3), (3, 5), (5, 4), (4, 2), (2, 0)
    ):g2.add_edge(*edge)
    print(euler_path(g2))