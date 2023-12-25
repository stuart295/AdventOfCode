from networkx import minimum_edge_cut, connected_components

from utils.common import solve_puzzle
import networkx as nx

YEAR = 2023
DAY = 25


def parse_input(lines):
    G = nx.Graph()

    for line in lines:
        left, right = line.split(": ")
        right_split = right.split(" ")

        for r in right_split:
            G.add_edge(left, r)

    return G


def solve(lines):
    G = parse_input(lines)

    wire_cuts = minimum_edge_cut(G)

    for e1, e2 in wire_cuts:
        G.remove_edge(e1, e2)

    groups = list(connected_components(G))

    part1 = len(groups[0]) * len(groups[1])
    part2 = None

    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, sample_data_path="test.txt")
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
