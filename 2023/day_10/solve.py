import math

import matplotlib.pyplot as plt

from utils.common import solve_puzzle, grid_offsets
import networkx as nx
from utils.grid_graph import GridGraph

YEAR = 2023
DAY = 10

allowed_connections = {
    ("|L", 0, -1),
    ("|J", 0, -1),
    ("|7", 0, 1),
    ("|F", 0, 1),
    ("|S", 0, 1),
    ("|S", 0, -1),
    ("||", 0, -1),
    ("-L", -1, 0),
    ("-F", -1, 0),
    ("-J", 1, 0),
    ("-7", 1, 0),
    ("-S", 1, 0),
    ("-S", -1, 0),
    ("--", 1, 0),
    ("LS", 1, 0),
    ("LS", 0, 1),
    ("LJ", 1, 0),
    ("L7", 1, 0),
    ("L7", 0, 1),
    ("LF", 0, 1),
    ("JS", -1, 0),
    ("JS", 0, 1),
    ("JF", 0, 1),
    ("JF", -1, 0),
    ("J7", 0, 1),
    ("F7", 1, 0),
    ("FJ", 1, 0),
    ("FS", 1, 0),
    ("FS", 0, -1),
    ("7S", 0, -1),
    ("7S", -1, 0),

}


def find_start_pos(inp):
    for y, line in enumerate(inp):
        for x, c in enumerate(line):
            if c == "S":
                return x, y

    raise Exception("Start pos not found!")


def build_graph(inp):
    inp_rev = inp[::-1]
    G = GridGraph(inp_rev)

    start_pos = None
    for node in G.graph.nodes():
        x, y = node
        c = G.graph.nodes[node]["char"]
        if c == "S":
            start_pos = x, y

        to_remove = []
        for adj in G.graph.neighbors(node):
            if node == adj: continue
            xa, ya = adj
            ca = G.graph.nodes[adj]["char"]
            dx, dy = (xa - x, ya - y)
            if not ((c + ca, dx, dy) in allowed_connections or (ca + c, -dx, -dy) in allowed_connections):
                to_remove.append((node, adj))

        for a, b in to_remove:
            G.graph.remove_edge(a, b)

    return G, start_pos


def find_start(start, G, from_node, prev_node, visited):
    lengths = []

    for adj in G.graph.neighbors(from_node):
        if adj == prev_node: continue

        if adj == start:
            lengths.append(1)
            continue

        cur_visited = set(visited)
        if adj in cur_visited:
            continue

        cur_visited.add(adj)

        sub_lengths = find_start(start, G, adj, from_node, cur_visited)
        if sub_lengths:
            lengths.append(1 + max(sub_lengths))

    return lengths

def solve_part_01(G, start):
    cycles = [cycle for cycle in nx.simple_cycles(G.graph.to_directed())]

    s_cycles = [c for c in cycles if start in c]

    largest = max(math.ceil(len(c)/2) for c in s_cycles)

    return largest, [c for c in s_cycles if math.ceil(len(c)/2) == largest][0]


def flood_fill(from_node, G, loop, visited, off_map):
    to_visit = [from_node]
    area = []

    while to_visit:
        cur_node = to_visit.pop()

        if cur_node in off_map:
            area.append(cur_node)
            off_map.update(area)
            return []

        if cur_node in visited:
            continue

        visited.add(cur_node)

        if cur_node in loop:
            continue

        x, y = cur_node

        # Check for being on an extended edge
        on_edge = False
        for xa, ya in grid_offsets():
            n1 = (x+xa, y+ya)
            n2 = (x-xa, y-ya)

            if n1 in loop and n2 in loop and (n1, n2) in G.graph.edges:
                on_edge = True
                break

        if on_edge:
            continue

        area.append(cur_node)

        # Edge reached
        if x <= 0 or x >= G.w-1 or y <= 0 or y >= G.h-1:
            off_map.update(area)
            return []

        for xa, ya in grid_offsets():
            to_visit.append((x+xa, y+ya))

    return area

def solve_part_02(G, loop):
    expand_grid(G)
    loop_set = {(x * 2, y * 2) for x, y in loop}

    w, h = G.w, G.h

    visited = set()
    off_map = set()

    area = []

    for y in range(h):
        for x in range(w):
            area += flood_fill((x,y), G, loop_set, visited, off_map)

    area_reduced = []
    for x,y in area:
        xr, yr = x/2, y/2

        if xr != int(xr) or yr != int(yr):
            continue

        if (xr, yr) in loop:
            continue

        area_reduced.append((xr, yr))

    return len(area_reduced)


def expand_grid(G):
    nodes = list(G.graph.nodes)

    G_exp = nx.Graph()

    edges = []

    for node in nodes:
        edges += [(node, adj) for adj in G.graph.neighbors(node)]

        new_node = (node[0]*2, node[1]*2)
        G_exp.add_node(new_node)
        G_exp.nodes[new_node]["char"] = G.graph.nodes[node]["char"]


    for (x,y), (xa,ya) in edges:
        G_exp.add_edge((x*2,y*2), (xa*2,ya*2))

    G.graph = G_exp
    G.w *= 2
    G.h *= 2

def solve(lines):
    G, start = build_graph(lines)

    part1, loop = solve_part_01(G, start)

    to_remove = [n for n in G.graph.nodes if n not in loop]
    for n in to_remove:
        G.graph.remove_node(n)

    part2 = solve_part_02(G, loop)

    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, sample_data_path="test3.txt")
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
