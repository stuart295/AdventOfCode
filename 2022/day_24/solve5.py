from collections import deque
import networkx as nx
from networkx import NetworkXNoPath, NodeNotFound

from utils.common import solve_puzzle, grid_offsets
from utils.grid_graph import GridGraph
from copy import deepcopy

BLIZZ = {'v': (0, 1), '<': (-1, 0), '>': (1, 0), '^': (0, -1)}


def set_z(G, dim):
    remap = {}
    for node in G.nodes:
        remap[node] = (node[0], node[1], dim)
    return nx.relabel_nodes(G, remap)


# def to_array(g, w, h, z):
#     out = []
#     for y in range(h):
#         line = []
#         for x in range(w):
#             if (x, y) in [(gx, gy) for gx, gy, gz in g.nodes]:
#                 cell = [g.nodes[(x, y, z)]['char']] + list(sorted(list(g.nodes[(x, y, z)]['blizz'])))
#             else:
#                 cell = tuple()
#
#             line.append(tuple(cell))
#         out.append(tuple(line))
#     return tuple(out)
def to_array(g, w, h, z):
    sorted_nodes = sorted([(gx, gy) for gx, gy, gz in g.nodes])
    out = list(sorted_nodes)
    for x, y in sorted_nodes:
        out.append(''.join(list(sorted(list(g.nodes[(x, y, z)]['blizz'])))))

    return tuple(out)


def read_data(lines):
    G = GridGraph([line.strip() for line in lines])
    G.set_walls('#')
    G.graph = G.graph.to_directed()

    G.graph.remove_edges_from(list(G.graph.edges()))

    print("Initilizing blizzards...")
    # init blizzards
    for node in G.graph.nodes:
        G.graph.nodes[node]['blizz'] = set()
        if G.graph.nodes[node]['char'] in BLIZZ:
            G.graph.nodes[node]['blizz'].add(G.graph.nodes[node]['char'])
            G.graph.nodes[node]['char'] = '.'

    # Expand dims
    G.graph = set_z(G.graph, 0)

    # start_state = to_array(G.graph, G.w, G.h, 0)
    start_state = to_array(G.graph, G.w, G.h, 0)

    # Add graph through time
    prev_g = G.graph
    depth = 0

    print("Expanding depth...")
    while True:
        depth += 1
        new_g = deepcopy(prev_g)
        new_g = update_blizzards(new_g, G.w, G.h)
        new_g = set_z(new_g, depth)

        # if depth == 2:
        #     print_layer(new_g, G.w, G.h, z)

        # new_state = to_array(new_g, G.w, G.h, depth)
        new_state = to_array(new_g, G.w, G.h, depth)
        if new_state == start_state:
            break

        G.graph = nx.compose(new_g, G.graph)
        prev_g = new_g

    print("Removing blizzard nodes...")
    remove_blizz_nodes(G)

    print("Adding edges...")
    for z in range(0, depth):
        for x, y in [(gx, gy) for gx, gy, gz in G.graph.nodes if gz == z]:
            G.graph.add_edge((x, y, z), (x, y, z + 1))
            for ox, oy in grid_offsets():
                other = (x + ox, y + oy, z + 1)
                if other in G.graph.nodes:
                    G.graph.add_edge((x, y, z), other)

    # Connect last state to first state
    for x, y, z in [(gx, gy, gz) for gx, gy, gz in G.graph.nodes if gz == depth]:
        G.graph.add_edge((x, y, z), (x, y, 0))
        for ox, oy in grid_offsets():
            other = (x + ox, y + oy, 0)
            if other in G.graph.nodes:
                G.graph.add_edge((x, y, z), other)  # Check

    return G


def remove_blizz_nodes(G):
    to_remove = set()
    for n in G.graph.nodes:
        if G.graph.nodes[n]['blizz']:
            to_remove.add(n)
    for n in to_remove:
        G.graph.remove_node(n)


def taxicab(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def update_blizzards(g, w, h):
    next_g = deepcopy(g)
    for node in next_g.nodes:
        next_g.nodes[node]['blizz'] = set()

    # Update blizzards
    for node in g.nodes:
        x, y, z = node
        blizz = g.nodes[node]['blizz']
        for b in blizz:
            dir = BLIZZ[b]
            dest = (x + dir[0], y + dir[1], z)
            if dest not in next_g.nodes:
                if b == 'v':
                    dest = (x, 1, z)
                elif b == '^':
                    dest = (x, h - 2, z)
                elif b == '<':
                    dest = (w - 2, y, z)
                elif b == '>':
                    dest = (1, y, z)

            next_g.nodes[dest]['blizz'].add(b)
    return next_g


def solve(lines):
    G = read_data(lines)

    # print_layer(G.graph, G.w, G.h, 0)

    start = (1, 0)
    end = (G.w - 2, G.h - 1)
    max_t = max(z for x, y, z in G.graph.nodes)

    shortest = 1e9
    # best_path = None

    from_point = start + (0,)

    # cur = (6, 5, 6)

    # path = nx.shortest_path(G.graph, from_point, cur)
    # print(path)
    # print(len(path))

    # print("==========")
    # for n in G.graph.successors(cur):
    #     print(n)
    # print("==========")

    print(f"States loop at {max_t}")

    for t in range(0, max_t + 1):
        # path_len = nx.shortest_path_length(G.graph, start + (0,), end + (t,))
        to_point = end + (t,)
        # if debug: print(f"{from_point} -> {to_point}")
        try:
            path = nx.shortest_path(G.graph, from_point, to_point)
            # path = nx.shortest_path(G.graph, from_point, to_point, method='bellman-ford')
            if len(path) < shortest:
                shortest = len(path)
                # best_path = path
        except NetworkXNoPath as e:
            print(f'No path for t == {t}')
            continue
        except NodeNotFound as e:
            print(f'Destination blocked at t == {t}')
            continue

    part1 = shortest - 1
    # part1 = None

    part2 = None

    return part1, part2


def print_layer(g, w, h, depth):
    for y in range(h):
        line = ''
        for x in range(w):
            if (x, y) in [(gx, gy) for gx, gy, gz in g.nodes if gz == depth]:
                line += g.nodes[(x, y, depth)]['char']
            else:
                line += ' '
        print(line)


debug = True
# solve_puzzle(year=2022, day=24, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=24, solver=solve, do_sample=False, do_main=True)
