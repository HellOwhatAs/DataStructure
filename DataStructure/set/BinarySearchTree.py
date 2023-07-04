from typing import Any, Optional

try:
    from ..tree.BinaryTree import BinaryTree
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
    from DataStructure.tree.BinaryTree import BinaryTree
    sys.path.pop(0)
    del sys, os

class BinarySearchTree(BinaryTree):
    def __init__(self, val: Optional[Any] = None, left: Optional['BinarySearchTree'] = None, right: Optional['BinarySearchTree'] = None, father: Optional['BinarySearchTree'] = None):
        if val is None: left = right = None
        if left is not None:
            if left.father is None: left.father = self
            if left.val is None: left = None
        if right is not None:
            if right.father is None: right.father = self
            if right.val is None: right = None
        super().__init__(val, left, right)
        self.left: 'BinarySearchTree|None'
        self.right: 'BinarySearchTree|None'
        self.father = father

    def pre_order(self):
        if self.val is None: return
        for elem in super().pre_order(): yield elem

    def mid_order(self):
        if self.val is None: return
        for elem in super().mid_order(): yield elem

    def post_order(self):
        if self.val is None: return
        for elem in super().post_order(): yield elem
    
    def level_order(self):
        if self.val is None: return
        for elem in super().level_order(): yield elem

    @property
    def size(self):
        if self.val is None: return 0
        return super().size

    @property
    def depth(self):
        if self.val is None: return 0
        return super().depth
    
    def search(self, val: Any):
        if val == self.val: return self
        elif val < self.val:
            if self.left is None: return self
            return self.left.search(val)
        else:
            if self.right is None: return self
            return self.right.search(val)
    
    def get_prev(self):
        if self.left is not None: return self.left.get_max()
        p = self
        while p.father is not None:
            if p.father.left is p:
                p = p.father
            else:
                return p.father
    
    def get_next(self):
        if self.right is not None: return self.right.get_min()
        p = self
        while p.father is not None:
            if p.father.right is p:
                p = p.father
            else:
                return p.father
    
    def add(self, val: Any):
        if self.val is None:
            self.val = val
            return
        node = self.search(val)
        if node.val == val: return
        elif node.val < val: node.right = type(self)(val, father = node)
        else: node.left = type(self)(val, father = node)
    
    def __assign_self(self, other: 'BinarySearchTree'):
        self.val = other.val
        if other.left is not None:
            other.left.father = self
        if other.right is not None:
            other.right.father = self
        self.left = other.left
        self.right  = other.right
    
    def __detach_self(self, replacement: Optional['BinarySearchTree'] = None):
        if self.father is None: return
        if replacement is not None: replacement.father = self.father
        if self.father.left is self:
            self.father.left = replacement
        else:
            self.father.right = replacement
        self.father = None

    def get_max(self):
        if self.val is None: return
        if self.right is None: return self
        else: return self.right.get_max()
    
    def get_min(self):
        if self.val is None: return
        if self.left is None: return self
        else: return self.left.get_min()
    
    def remove(self, val: Any):
        if self.val is None: return
        ret = self.search(val)
        if ret.val != val: return
        if ret is self:
            if self.left is self.right is None:
                self.val = None
            elif self.left is None:
                self.__assign_self(self.right)
            elif self.right is None:
                self.__assign_self(self.left)
            else:
                if ret.left.size > ret.right.size:
                    tmp = ret.left.get_max()
                    tmp.__detach_self(tmp.left)
                else:
                    tmp = ret.right.get_min()
                    tmp.__detach_self(tmp.right)
                ret.val = tmp.val
        else:
            if ret.left is ret.right is None:
                ret.__detach_self()
            elif ret.left is None:
                ret.__detach_self(ret.right)
            elif ret.right is None:
                ret.__detach_self(ret.left)
            else:
                if ret.left.size > ret.right.size:
                    tmp = ret.left.get_max()
                    tmp.__detach_self(tmp.left)
                else:
                    tmp = ret.right.get_min()
                    tmp.__detach_self(tmp.right)
                ret.val = tmp.val

if __name__ == '__main__':
    bst = BinarySearchTree()
    import random
    random.seed(0)
    items = [random.randint(-10000, 10000) for i in range(10**4)]
    random.shuffle(items)
    for elem in items:
        bst.add(elem)
    print(bst.depth)
    next_list, prev_list = [], []
    p = bst.search(-float('inf'))
    while p is not None:
        next_list.append(p.val)
        p = p.get_next()
    p = bst.search(float('inf'))
    while p is not None:
        prev_list.append(p.val)
        p = p.get_prev()
    print(next_list == list(bst.mid_order()) == sorted(set(items)))
    print(prev_list == sorted(set(items), reverse=True))