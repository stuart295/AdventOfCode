# First time using this library, so may be messy
import networkx as nx
from networkx.algorithms.shortest_paths.astar import astar_path
import numpy as np

# Should prob use the np.tile function instead
def tilemap(lines, size):
    orig = np.array(lines)
    grid = [[orig]]

    for row in range(size):
        if row > 0:
            grid.append([])
        for col in range(size):
            if row == 0 and col == 0:
                continue

            prev = grid[row - 1][col] if row > 0 else grid[row][col - 1]
            cur = (prev % 9) + 1

            grid[row].append(cur)

    return np.concatenate([np.concatenate(row, axis=1) for row in grid], axis=0).tolist()


def read_input(path, tile=False):
    with open(path) as f:
        lines = f.readlines()

    lines = [list(map(int, list(x.strip()))) for x in lines]

    if tile:
        lines = tilemap(lines, 5)

    h, w = len(lines), len(lines[0])

    graph = nx.grid_2d_graph(h, w, create_using=nx.DiGraph)
    for row in range(h):
        for col in range(w):
            risk = int(lines[row][col])
            graph.nodes[row, col]['risk'] = risk
            for _, __, data in graph.in_edges((row, col), data=True):
                data['risk'] = risk

    return graph, h, w


def manhatten_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_path(graph, start, target):
    shortest = astar_path(graph, start, target, manhatten_dist, 'risk')
    risk = sum([graph.nodes[c]['risk'] for c in shortest[1:]])
    return risk


def solve(tile):
    g, h, w = read_input('./input.txt', tile=tile)
    cost = find_path(g, start=(0, 0), target=(h - 1, w - 1))
    print(cost)


solve(False)
solve(True)
