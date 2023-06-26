try:
    from ..linear.Array import Array
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.linear.Array import Array
    sys.path.pop()
    del sys, os

class PriorityQueue:
    def __init__(self):
        self.data = Array()