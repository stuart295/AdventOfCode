from networkx import DiGraph

from utils.common import solve_puzzle


def build_graph(lines):
    G = DiGraph()
    idx = 0
    G.add_node(idx, name='/', dir=True, size=0)
    idx += 1
    cur_node = 0
    root_node = 0

    for line in lines:
        line_clean = line.strip()
        split = line_clean.split(' ')

        if split[0] == '$':
            if split[1] == 'cd':
                if split[2] == '..':
                    cur_node = list(G.predecessors(cur_node))[0]
                elif split[2] == '/':
                    cur_node = root_node
                else:
                    cur_node = [x for x in G.successors(cur_node) if G.nodes[x]['name'] == split[2]][0]

        else:
            if split[0] == 'dir':
                G.add_node(idx, name=split[1], dir=True, size=0)
                G.add_edge(cur_node, idx)
                idx += 1
            elif split[0].isnumeric():
                G.add_node(idx, name=split[1], dir=False, size=int(split[0]))
                G.add_edge(cur_node, idx)
                idx += 1
    return G


def calc_size(G, cur_node):
    if G.nodes[cur_node]['dir']:
        for child in G.successors(cur_node):
            G.nodes[cur_node]['size'] += calc_size(G, child)

    return G.nodes[cur_node]['size']


def solve_part1(G, cur_node, max_size):
    if not G.nodes[cur_node]['dir']: return 0

    size = G.nodes[cur_node]['size'] if G.nodes[cur_node]['size'] <= max_size else 0

    for child in G.successors(cur_node):
        size += solve_part1(G, child, max_size)
    return size


def solve_part2(G, req=30000000, sys=70000000):
    total = G.nodes[0]['size']
    unused = sys - total
    rem = req - unused

    candidates = [i for i in G if G.nodes[i]['dir'] and G.nodes[i]['size'] >= rem]
    candidates = sorted(candidates, key=lambda i: G.nodes[i]['size'])
    sol = list(candidates)[0]
    return G.nodes[sol]['size']


def solve(lines):
    G = build_graph(lines)

    calc_size(G, 0)

    part1 = solve_part1(G, 0, 100000)
    part2 = solve_part2(G)

    return part1, part2


debug = False

solve_puzzle(year=2022, day=7, solver=solve, do_sample=True, do_main=not debug, sample_data_path='sample')

