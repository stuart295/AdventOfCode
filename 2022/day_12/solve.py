from utils.common import solve_puzzle
from utils.grid_graph import GridGraph
import networkx as nx


def solve(lines):
    G = GridGraph(lines)

    start = [node for node in G.graph.nodes if G.graph.nodes[node]['char'] == 'S'][0]
    end = [node for node in G.graph.nodes if G.graph.nodes[node]['char'] == 'E'][0]

    g = G.graph

    for node in g.nodes:
        if g.nodes[node]['char'] == 'S':
            g.nodes[node]['height'] = 0
        elif g.nodes[node]['char'] == 'E':
            g.nodes[node]['height'] = ord('z') - ord('a')
        else:
            g.nodes[node]['height'] = ord(g.nodes[node]['char']) - ord('a')

    def weight_func(n1, n2, att):
        if g.nodes[n2]['height'] > g.nodes[n1]['height'] + 1:
            return 1e9
        return 1

    # Part 1
    part1 = nx.shortest_path_length(g, start, end, weight_func)

    # Path 2
    part2 = 1e9
    for node in g.nodes:
        if g.nodes[node]['height'] != 0:
            continue

        cur_len = nx.shortest_path_length(g, node, end, weight_func)
        part2 = min(part2, cur_len)

    return part1, part2


debug = False
solve_puzzle(year=2022, day=12, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=2022, day=12, solver=solve, do_sample=False, do_main=True)
