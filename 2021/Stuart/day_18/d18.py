import itertools
from math import floor, ceil
from binarytree import Node
import json


def create_tree(l):
    node = Node(-1)
    if isinstance(l, list):
        node.left = create_tree(l[0])
        node.right = create_tree(l[1])
    else:
        node.val = int(l)

    return node


def inorder_leaves(tree):
    out = []
    for node in tree.inorder:
        if node.val != -1:
            out.append(node)
    return out


def read_input(path):
    with open(path) as f:
        lines = f.readlines()
    lines = [json.loads(x.strip()) for x in lines]

    trees = []
    for line in lines:
        trees.append(create_tree(line))

    return trees


def merge_trees(t1, t2):
    new_root = Node(-1)
    new_root.left = t1
    new_root.right = t2
    return new_root


def is_level_4(node: Node, tree: Node):
    if len(tree.levels) < 5:
        return False

    return node.left in tree.leaves and node.right in tree.leaves and node in tree.levels[4]


def explode(node: Node, tree: Node):
    if node.val != -1:
        raise Exception("Invalid node to explode")

    leaves = inorder_leaves(tree)
    for i in range(len(leaves)):
        if leaves[i] == node.left:
            if i > 0:
                leaves[i - 1].val += node.left.val
            if i + 2 < len(leaves):
                leaves[i + 2].val += node.right.val
            break

    node.val = 0
    del node[1]
    del node[2]


def split_node(node: Node):
    if node.val == -1:
        raise Exception("Invalid node to split")
    node.left = Node(floor(node.val / 2))
    node.right = Node(ceil(node.val / 2))
    node.val = -1


def reduce_tree(tree):
    finished = False
    while not finished:
        finished = True
        # Explode
        for node in tree.inorder:
            if is_level_4(node, tree):
                explode(node, tree)
                finished = False
                break

        # Split
        if finished:
            for node in tree.inorder:
                if node.val >= 10:
                    split_node(node)
                    finished = False
                    break


def magnitude(tree: Node):
    if tree.val != -1:
        return tree.val

    return 3 * magnitude(tree.left) + 2 * magnitude(tree.right)


def snail_sum(t1, t2):
    result = merge_trees(t1, t2)
    reduce_tree(result)
    return result


# Part 1
# inputs = read_input('./test.txt')
inputs = read_input('./input.txt')

result = inputs[0]
for input in inputs[1:]:
    result = snail_sum(result, input)

print(f"Part 1: {magnitude(result)}")


# Part 2: Just gonna brute force this one
inputs = read_input('./input.txt')
# inputs = read_input('./test.txt')
largest = 0
for p1, p2 in itertools.combinations(inputs, 2):
    result1 = snail_sum(p1.clone(), p2.clone())
    result2 = snail_sum(p2.clone(), p1.clone())
    largest = max(largest, magnitude(result1), magnitude(result2))
print(f"Part 2: {largest}")
