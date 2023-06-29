from typing import Any, List, Dict, Optional, overload
try:
    from ..linear.Queue import Queue
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.linear.Queue import Queue
    sys.path.pop()
    del sys, os

class BinaryTree:
    def __init__(self, val: Any, left: Optional['BinaryTree'] = None, right: Optional['BinaryTree'] = None):
        self.val = val
        self.left, self.right = left, right
    
    @overload
    @classmethod
    def build(cls,* , pre_order: List[Any], mid_order: List[Any]) -> 'BinaryTree':...
    @classmethod
    def __build_via_pre_mid(cls, pre_order: List[Any], mid_order: List[Any], pre_start: int, mid_start: int, length: int, mid_idxer: Dict[Any, int]):
        if length == 0: return None
        val = pre_order[pre_start]
        root_idx = mid_idxer[val]
        left = cls.__build_via_pre_mid(pre_order, mid_order, pre_start + 1, mid_start, root_idx - mid_start, mid_idxer)
        right = cls.__build_via_pre_mid(pre_order, mid_order, pre_start + 1 + root_idx - mid_start, root_idx + 1, length + mid_start - (root_idx + 1), mid_idxer)
        return cls(val, left, right)
        

    @overload
    @classmethod
    def build(cls,* , mid_order: List[Any], post_order: List[Any]) -> 'BinaryTree':...
    @classmethod
    def __build_via_mid_post(cls, mid_order: List[Any], post_order: List[Any], mid_start: int, post_start: int, length: int, mid_idxer: Dict[Any, int]):
        if length == 0: return None
        val = post_order[post_start + length - 1]
        root_idx = mid_idxer[val]
        left = cls.__build_via_mid_post(mid_order, post_order, mid_start, post_start, root_idx - mid_start, mid_idxer)
        right = cls.__build_via_mid_post(mid_order, post_order, root_idx + 1, post_start - 1 - (mid_start - (root_idx + 1)), mid_start + length - (root_idx + 1), mid_idxer)
        return cls(val, left, right)

    @overload
    @classmethod
    def build(cls,* , mid_order: List[Any], level_order: List[Any]) -> 'BinaryTree':...
    @classmethod
    def __build_via_mid_level(cls, sub_mid_order: List[Any], sub_level_order: List[Any], sub_mid_idxer: Dict[Any, int]):
        if len(sub_mid_order) == 0: return None
        val = sub_level_order[0]
        root_idx = sub_mid_idxer[val]
        left_mid, right_mid = sub_mid_order[:root_idx], sub_mid_order[root_idx + 1:]
        left_mid_idxer, right_mid_idxer = {elem:i for i, elem in enumerate(left_mid)}, {elem:i for i, elem in enumerate(right_mid)}
        left_level, right_level = [], []
        for elem in sub_level_order:
            if elem in left_mid_idxer: left_level.append(elem)
            elif elem in right_mid_idxer: right_level.append(elem)
        left = cls.__build_via_mid_level(left_mid, left_level, left_mid_idxer)
        right = cls.__build_via_mid_level(right_mid, right_level, right_mid_idxer)
        return cls(val, left, right)


    @classmethod
    def build(cls,* , pre_order: Optional[List[Any]] = None, mid_order: Optional[List[Any]] = None, post_order: Optional[List[Any]] = None, level_order: Optional[List[Any]] = None):
        if mid_order is not None and pre_order is not None and post_order is level_order is None:
            assert len(mid_order) == len(pre_order)
            return cls.__build_via_pre_mid(pre_order, mid_order, 0, 0, len(mid_order), {elem: i for i, elem in enumerate(mid_order)})
        if mid_order is not None and post_order is not None and pre_order is level_order is None:
            assert len(mid_order) == len(post_order)
            return cls.__build_via_mid_post(mid_order, post_order, 0, 0, len(mid_order), {elem: i for i, elem in enumerate(mid_order)})
        if mid_order is not None and level_order is not None and post_order is pre_order is None:
            return cls.__build_via_mid_level(mid_order, level_order, {elem: i for i, elem in enumerate(mid_order)})
        else:
            raise TypeError("no matching function to call")
    
    @property
    def size(self):
        size = 1
        if self.left is not None:
            size += self.left.size
        if self.right is not None:
            size += self.right.size
        return size
    
    @property
    def depth(self):
        depth = 0
        if self.left is not None:
            depth = max(depth, self.left.depth)
        if self.right is not None:
            depth = max(depth, self.right.depth)
        return depth + 1

    def pre_order(self):
        yield self.val
        if self.left is not None:
            for elem in self.left.pre_order():
                yield elem
        if self.right is not None:
            for elem in self.right.pre_order():
                yield elem
    
    def mid_order(self):
        if self.left is not None:
            for elem in self.left.mid_order():
                yield elem
        yield self.val
        if self.right is not None:
            for elem in self.right.mid_order():
                yield elem

    def post_order(self):
        if self.left is not None:
            for elem in self.left.post_order():
                yield elem
        if self.right is not None:
            for elem in self.right.post_order():
                yield elem
        yield self.val
    
    def level_order(self):
        q = Queue()
        q.push(self)
        while not q.empty():
            elem: 'BinaryTree' = q.pop()
            yield elem.val
            if elem.left is not None:
                q.push(elem.left)
            if elem.right is not None:
                q.push(elem.right)
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.val}, {repr(self.left)}, {repr(self.right)})"

    def __eq__(self, other: 'BinaryTree') -> bool:
        return self.val == other.val and self.left == other.left and self.right == other.right


if __name__ == '__main__':
    btree = BinaryTree('A',
        BinaryTree(
            'L',
            BinaryTree('B'),
            BinaryTree('E')
        ),
        BinaryTree('C', None, BinaryTree('D'))
    )
    print(list(btree.pre_order()))
    print(list(btree.mid_order()))
    print(list(btree.post_order()))
    print(list(btree.level_order()))
    print(btree.depth, btree.size)
    print(btree)

    btree = BinaryTree.build(
        pre_order=list("ALBECDWX"),
        mid_order=list("BLEACWXD")
    )

    btree2 = BinaryTree.build(
        post_order=['B', 'E', 'L', 'X', 'W', 'D', 'C', 'A'],
        mid_order=['B', 'L', 'E', 'A', 'C', 'W', 'X', 'D']
    )

    print(btree == btree2)

    print(list(btree.mid_order()))
    print(list(btree.level_order()))

    btree3 = BinaryTree.build(
        mid_order=['B', 'L', 'E', 'A', 'C', 'W', 'X', 'D'],
        level_order=['A', 'L', 'C', 'B', 'E', 'D', 'W', 'X']
    )

    print(btree == btree2 == btree3)