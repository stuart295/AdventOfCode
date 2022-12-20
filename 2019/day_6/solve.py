from utils.common import solve_puzzle
import networkx as nx


def build_graph(lines, directed):
    G = nx.DiGraph() if directed else nx.Graph()
    for line in lines:
        a, b = line.strip().split(')')
        G.add_edge(a, b)
    return G


def solve_part_1(lines):
    G = build_graph(lines, directed=True)
    part1 = 0
    for node in G.nodes:
        part1 += len(nx.descendants(G, node))
    return part1


def solve_part_2(lines):
    G = build_graph(lines, directed=False)
    dest = list(nx.neighbors(G, 'SAN'))[0]
    return len(nx.shortest_path(G, 'YOU', dest)) - 2


def solve(lines):
    part1 = solve_part_1(lines)
    part2 = solve_part_2(lines)

    return part1, part2


debug = True
# solve_puzzle(year=2019, day=6, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
# solve_puzzle(year=2019, day=6, solver=solve, do_sample=True, do_main=False, sample_data_path='sample2')
solve_puzzle(year=2019, day=6, solver=solve, do_sample=False, do_main=True, main_data_path='input')
