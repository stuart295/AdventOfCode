from collections import deque

from utils.common import solve_puzzle, grid_offsets
from utils.grid_graph import GridGraph
from copy import deepcopy

BLIZZ = {'v': (0, 1), '<': (-1, 0), '>': (1, 0), '^': (0, -1)}


def read_data(lines):
    G = GridGraph([line.strip() for line in lines])
    G.set_walls('#')

    for node in G.graph.nodes:
        G.graph.nodes[node]['blizz'] = set()
        if G.graph.nodes[node]['char'] in BLIZZ:
            G.graph.nodes[node]['blizz'].add(G.graph.nodes[node]['char'])
            G.graph.nodes[node]['char'] = '.'

    return G


# def to_array(g, w, h):
#     out = []
#     for y in range(h):
#         line = []
#         for x in range(w):
#             if (x, y) in g.nodes:
#                 cell = [g.nodes[(x, y)]['char']] + list(sorted(list(g.nodes[(x, y)]['blizz'])))
#             else:
#                 cell = tuple()
#
#             line.append(tuple(cell))
#         out.append(tuple(line))
#     return tuple(out)

def to_array(g, w, h):
    sorted_nodes = sorted(g.nodes)
    out = list(sorted_nodes)
    for x, y in sorted_nodes:
        out.append(''.join(list(sorted(g.nodes[(x, y)]['blizz']))))

    return tuple(out)


def taxicab(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def solve_part_1(G, _, start=(1, 0), cache=None, limit=930):
    # g.nodes[start]['char'] = 'E'
    # G.graph = g
    # G.draw('char')

    to_check = deque()
    to_check.append((deepcopy(G.graph), start, 0))

    bliz_loop = (G.w - 2) * (G.h - 2) // 2

    end = (G.w - 2, G.h - 1)

    shortest = limit

    while to_check:
        g, pos, cur_dist = to_check.pop()

        rem_dist = taxicab(pos, end)
        if cur_dist + rem_dist >= shortest:
            continue

        # state = to_array(g, G.w, G.h)
        state = (cur_dist % bliz_loop, pos)
        if state in cache:
            continue

        cache.add(state)

        cur_dist += 1

        if pos == end:
            print(f'End reached: {cur_dist}', flush=True)
            if cur_dist < shortest:
                shortest = cur_dist
            continue

        next_g = update_blizzards(G, g)

        # Choose positions
        x, y = pos
        options = []

        for ox, oy in grid_offsets():
            neighx, neighy = x + ox, y + oy
            neigh = (neighx, neighy)
            if neigh in next_g.nodes and len(next_g.nodes[neigh]['blizz']) == 0:
                dist = taxicab(neigh, end)
                if cur_dist + dist < shortest:
                    options.append((dist, next_g, neigh, cur_dist))

        if len(next_g.nodes[pos]['blizz']) == 0:
            dist = taxicab(pos, end)
            if cur_dist + dist < shortest:
                options.append((dist, next_g, pos, cur_dist))

        options = sorted(options, key=lambda x: x[0], reverse=True)
        for o in options:
            to_check.append(o[1:])

    return shortest


def update_blizzards(G, g):
    next_g = deepcopy(g)
    for node in next_g.nodes:
        next_g.nodes[node]['blizz'] = set()
    # Update blizzards
    for node in g.nodes:
        x, y = node
        blizz = g.nodes[node]['blizz']
        for b in blizz:
            dir = BLIZZ[b]
            dest = (x + dir[0], y + dir[1])
            if dest not in next_g.nodes:
                if b == 'v':
                    dest = (x, 1)
                elif b == '^':
                    dest = (x, G.h - 2)
                elif b == '<':
                    dest = (G.w - 2, y)
                elif b == '>':
                    dest = (1, y)

            next_g.nodes[dest]['blizz'].add(b)
    return next_g


def solve(lines):
    G = read_data(lines)

    # G.draw("char")

    cache = set()

    start = (1, 0)
    shortest = solve_part_1(G, [], start, cache)

    part1 = shortest - 1

    part2 = None

    return part1, part2


debug = True
# solve_puzzle(year=2022, day=24, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=24, solver=solve, do_sample=False, do_main=True)
