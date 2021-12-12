from collections import Counter


class Node(object):

    def __init__(self, code: str):
        self.neighbours = set()
        self.code = code
        self.small = code[0].islower()

    def add_neihbour(self, n2):
        self.neighbours.add(n2)
        n2.neighbours.add(self)

    def __repr__(self):
        return self.code


def read_inputs(p):
    nodes = {}
    with open(p) as f:
        lines = f.readlines()

    for line in lines:
        c1, c2 = line.strip().split('-')

        n1 = nodes[c1] if c1 in nodes else Node(c1)
        n2 = nodes[c2] if c2 in nodes else Node(c2)
        n1.add_neihbour(n2)

        nodes[c1] = n1
        nodes[c2] = n2

    return nodes


def find_path(start, explored, special_cave=None):
    paths = set()

    if start.small:
        explored[start] += 1

    for neighbour in start.neighbours:
        if neighbour in explored:
            if neighbour != special_cave or explored[neighbour] >= 2:
                continue
        if neighbour.code == 'end':
            paths.add(f"{start.code},{neighbour.code}")
        else:
            n_paths = find_path(neighbour, explored.copy(), special_cave)

            for n_path in n_paths:
                paths.add(f"{start.code},{n_path}")

    return paths


def find_path_count(nodes):
    explored_small = Counter()
    paths = find_path(nodes['start'], explored_small)
    return len(paths)


def find_path_count_2(nodes):
    small_caves = [v for k, v in nodes.items() if k != 'start' and k != 'end' and v.small]
    paths = set()
    for small in small_caves:
        explored_small = Counter()
        unique_paths  = find_path(nodes['start'], explored_small, small)
        paths.update(unique_paths)

    return len(paths)


nodes = read_inputs('./input.txt')
# nodes = read_inputs('./test.txt')
print(find_path_count(nodes))
print(find_path_count_2(nodes))

# Comment: Not my proudest solution...