from utils.common import solve_puzzle
import networkx as nx
import uuid
from itertools import combinations

dists = {}


def read_input(lines):
    G = nx.Graph()
    for line in lines:
        split = line.split(' ')
        valve = split[1]
        rate = int(split[4].split('=')[1].replace(';', ''))

        G.add_node(valve, rate=rate)

        dests = [x.replace(',', '') for x in split[9:]]
        for d in dests:
            G.add_edge(valve, d, weight=1)

    return G


def get_dist(G, f, t):
    if (f, t) in dists:
        return dists[(f, t)]

    path = nx.shortest_path(G, f, t, weight='weight')

    d = 0
    for p1, p2 in zip(path, path[1:]):
        d += G.edges[(p1, p2)]['weight']

    dists[(f, t)] = d
    return d


def add_node(G, OG, from_node, node, remaining_nodes, time):
    src = from_node.split('_')[0] if from_node != 'start' else 'AA'

    dist = get_dist(G, src, node)
    arrive_time = time - dist - 1

    pressure = G.nodes[node]['rate'] * arrive_time

    if arrive_time <= 0:
        OG.add_edge(from_node, 'end', weight=0)
        return

    guid = str(uuid.uuid4())
    tname = f"{node}_{arrive_time}_{guid}"
    OG.add_node(tname, time=arrive_time, rate=G.nodes[node]['rate'])

    OG.add_edge(from_node, tname, weight=-pressure)

    if node != 'end':
        remaining_nodes.remove(node)

    if len(remaining_nodes) > 0:
        for n in remaining_nodes:
            add_node(G, OG, tname, n, remaining_nodes.copy(), arrive_time)
    else:
        OG.add_edge(tname, 'end', weight=0)


def simplify(G):
    nodes = list(G.nodes)
    for n in nodes:
        if G.nodes[n]['rate'] > 0 or n == 'AA': continue
        remove_node(G, n)


def remove_node(G, n):
    if n not in G.nodes: return

    cons = G.neighbors(n)

    for c1 in cons:
        for c2 in cons:
            if c1 == c2: continue

            weight = G.edges[(c1, n)]['weight'] + G.edges[(c2, n)]['weight']
            G.add_edge(c1, c2, weight=weight)
    G.remove_node(n)


def calc_pressure(G, actions):
    pressure = 0
    for a in actions:
        split = a.split('_')
        if len(split) == 1: continue
        node, time, uid = split
        rate = G.nodes[node]['rate']
        pressure += rate * int(time)
    return pressure


def solve_part_1(G, time=30):
    opt_G = nx.DiGraph()
    cur_node = 'AA'
    remaining_nodes = [n for n in G.nodes if n != cur_node]
    for n in remaining_nodes:
        add_node(G, opt_G, cur_node, n, remaining_nodes.copy(), time)
    actions = nx.shortest_path(opt_G, 'AA', 'end', weight='weight', method='bellman-ford')
    return calc_pressure(G, actions=actions)


def solve(lines):
    G = read_input(lines)

    simplify(G)

    # Part 1
    pressure = solve_part_1(G)

    part1 = pressure

    # Part 2
    best = 0

    for comb in combinations([n for n in G.nodes if n != 'AA'], r=len(G.nodes) // 2):
        G1 = G.copy()

        for r in comb:
            remove_node(G1, r)

        G2 = G.copy()
        for n in G1.nodes:
            if n != 'AA':
                remove_node(G2, n)

        p1 = solve_part_1(G1, time=26)
        p2 = solve_part_1(G2, time=26)
        best = max(best, p1 + p2)

    part2 = best

    return part1, part2


debug = True
solve_puzzle(year=2022, day=16, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=16, solver=solve, do_sample=False, do_main=True)
