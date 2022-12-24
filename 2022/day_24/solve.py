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


def to_array(g, w, h):
    out = []
    for y in range(h):
        line = []
        for x in range(w):
            if (x, y) in g.nodes:
                cell = [g.nodes[(x, y)]['char']] + list(sorted(list(g.nodes[(x, y)]['blizz'])))
            else:
                cell = tuple()

            line.append(tuple(cell))
        out.append(tuple(line))
    return tuple(out)


def solve_part_1(G, path, start=(1, 0), cache=None):
    g = G.graph

    # g.nodes[start]['char'] = 'E'
    # G.graph = g
    # G.draw('char')

    state = to_array(g, G.w, G.h)
    if (state, start) in cache:
        return None

    cache.add((state, start))

    path.append(start)

    if start[1] == G.h - 1:
        # g.nodes[start]['char'] = 'E'
        # G.graph = g
        # G.draw('char')
        # found = True
        # print(len(path))
        return path.copy()

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

    G.graph = next_g

    # Choose positions
    shortest = 1e9
    final_path = None
    x, y = start
    for ox, oy in grid_offsets():
        neighx, neighy = x + ox, y + oy
        neigh = (neighx, neighy)
        if neigh in next_g.nodes and len(next_g.nodes[neigh]['blizz']) == 0:
            sub_path = solve_part_1(deepcopy(G), deepcopy(path), neigh, cache)
            if not sub_path:
                continue
            if len(sub_path) < shortest:
                shortest = len(sub_path)
                final_path = sub_path

    if not final_path:
        stay = start
        if len(next_g.nodes[stay]['blizz']) == 0:
            sub_path = solve_part_1(deepcopy(G), deepcopy(path), stay, cache)
            if sub_path:
                if len(sub_path) < shortest:
                    final_path = sub_path

    return final_path


def solve(lines):
    G = read_data(lines)

    # G.draw("char")

    cache = set()

    start = (1, 0)
    path = solve_part_1(deepcopy(G), [], start, cache)

    part1 = len(path) -1

    part2 = None

    return part1, part2


debug = True
solve_puzzle(year=2022, day=24, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
# solve_puzzle(year=2022, day=24, solver=solve, do_sample=False, do_main=True)
