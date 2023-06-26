from DataStructure.tree.HuffmanTree import HuffmanTree
from DataStructure.tree.BinaryTree import BinaryTree

hftree = HuffmanTree.build({
    'a': 10,
    'e': 15,
    'i': 12,
    's': 3,
    't': 4,
    ' ': 13,
    '\n': 1
})
print(hftree)
print(list(hftree.getcode()))
print(hftree.size, hftree.depth)

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