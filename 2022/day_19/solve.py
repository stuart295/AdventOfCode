import dataclasses
import uuid
from dataclasses import dataclass

from utils.common import solve_puzzle
import networkx as nx


class Blueprint:

    def __init__(self, line):
        # Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 4 ore and 7 obsidian.
        split = line.strip().replace(':', '').split(' ')
        self.id = int(split[1])
        self.ore_bot_ore_cost = int(split[6])
        self.clay_bot_ore_cost = int(split[12])
        self.obs_bot_ore_cost = int(split[18])
        self.obs_bot_clay_cost = int(split[21])
        self.geo_bot_ore_cost = int(split[27])
        self.geo_bot_obs_cost = int(split[30])


@dataclass
class State:
    clay: int = 0
    ore: int = 0
    obs: int = 0
    geo: int = 0
    ore_bots: int = 1
    clay_bots: int = 0
    obs_bots: int = 0
    geo_bots: int = 0
    timestep :int = 24

    def to_tuple(self):
        return (
            self.clay, self.ore, self.obs, self.geo, self.ore_bots, self.clay_bots, self.obs_bots, self.geo_bots,
            self.timestep)

    def step(self):
        self.clay += self.clay_bots
        self.ore += self.ore_bots
        self.obs += self.obs_bots
        self.geo += self.geo_bots
        self.timestep -= 1

    def can_build_ore_bot(self, bp: Blueprint):
        return self.ore >= bp.ore_bot_ore_cost

    def can_build_clay_bot(self, bp: Blueprint):
        return self.ore >= bp.clay_bot_ore_cost

    def can_build_obs_bot(self, bp: Blueprint):
        return self.ore >= bp.obs_bot_ore_cost and self.clay >= bp.obs_bot_clay_cost

    def can_build_geo_bot(self, bp: Blueprint):
        return self.ore >= bp.geo_bot_ore_cost and self.clay >= bp.geo_bot_obs_cost


def add_node(G, state, bp, step):
    # Update resources
    # new_state = dataclasses.replace(state)
    new_state = State(**dataclasses.asdict(state))
    if step:
        new_state.step()

    if new_state.timestep <= 0:
        G.add_edge(new_state.to_tuple(), 'end')
        return new_state

    # Add actions
    # ore bot
    if new_state.can_build_ore_bot(bp):
        # next_state = dataclasses.replace(new_state)
        next_state = State(**dataclasses.asdict(new_state))
        next_state.ore -= bp.ore_bot_ore_cost
        next_state.ore_bots += 1
        if not next_state.to_tuple() in G.nodes:
            n = add_node(G, next_state, bp, True)
            G.add_edge(next_state.to_tuple(), n.to_tuple())

    # clay bot
    if new_state.can_build_clay_bot(bp):
        next_state = State(**dataclasses.asdict(new_state))
        next_state.ore -= bp.clay_bot_ore_cost
        next_state.clay_bots += 1
        if not next_state.to_tuple() in G.nodes:
            n = add_node(G, next_state, bp, True)
            G.add_edge(next_state.to_tuple(), n.to_tuple())

    # obs bot
    if new_state.can_build_obs_bot(bp):
        next_state = State(**dataclasses.asdict(new_state))
        next_state.ore -= bp.obs_bot_ore_cost
        next_state.clay -= bp.obs_bot_clay_cost
        next_state.obs_bots += 1
        if not next_state.to_tuple() in G.nodes:
            n = add_node(G, next_state, bp, True)
            G.add_edge(next_state.to_tuple(), n.to_tuple())

    # geo bot
    if new_state.can_build_geo_bot(bp):
        next_state = State(**dataclasses.asdict(new_state))
        next_state.ore -= bp.geo_bot_ore_cost
        next_state.obs -= bp.geo_bot_obs_cost
        next_state.geo_bots += 1
        if not next_state.to_tuple() in G.nodes:
            n = add_node(G, next_state, bp, True)
            G.add_edge(next_state.to_tuple(), n.to_tuple())

    # nothing
    if not new_state.to_tuple() in G.nodes:
        n = add_node(G, new_state, bp, True)
        G.add_edge(new_state.to_tuple(), n.to_tuple())

    return new_state


def build_graph(bp):
    G = nx.DiGraph()

    start_state = State()

    G.add_node(start_state.to_tuple(), state=start_state, time=start_state.timestep)
    out = add_node(G, start_state, bp, True)
    G.add_edge(start_state.to_tuple(), out.to_tuple())

    return G, start_state


# def find_best(state, bp, time, step):
#     # Update resources
#     new_state = dataclasses.replace(state)
#     if step:
#         new_state.step()
#
#     if time <= 0:
#         return
#
#     # Add actions
#     # ore bot
#     if new_state.can_build_ore_bot(bp):
#         next_state = dataclasses.replace(new_state)
#         next_state.ore -= bp.ore_bot_ore_cost
#         next_state.ore_bots += 1
#         add_node(G, next_state, time, bp, False)
#
#     # clay bot
#     if new_state.can_build_clay_bot(bp):
#         next_state = dataclasses.replace(new_state)
#         next_state.ore -= bp.clay_bot_ore_cost
#         next_state.clay_bots += 1
#         add_node(G, next_state, time, bp, False)
#
#     # obs bot
#     if new_state.can_build_obs_bot(bp):
#         next_state = dataclasses.replace(new_state)
#         next_state.ore -= bp.obs_bot_ore_cost
#         next_state.clay -= bp.obs_bot_clay_cost
#         next_state.obs_bots += 1
#         add_node(G, next_state, time, bp, False)
#
#     # geo bot
#     if new_state.can_build_geo_bot(bp):
#         next_state = dataclasses.replace(new_state)
#         next_state.ore -= bp.geo_bot_ore_cost
#         next_state.obs -= bp.geo_bot_obs_cost
#         next_state.geo_bots += 1
#         add_node(G, next_state, time, bp, False)
#
#     # nothing
#     add_node(G, new_state, time - 1, bp, True)
#
#     return guid


def solve(lines):
    bps = [Blueprint(line) for line in lines]

    max_geos = []
    quality = 0
    for bp in bps:
        G, start = build_graph(bp)
        print(f"BP {bp.id}: {len(G.nodes)}", flush=True)
        cur_max = 0
        for node in G.nodes:
            cur_max = max(cur_max, G.nodes[node]['state'].geo)

        max_geos.append(cur_max)
        quality += cur_max * bp.id

    part1 = quality

    part2 = None

    return part1, part2


debug = True
solve_puzzle(year=2022, day=19, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
# solve_puzzle(year=2022, day=19, solver=solve, do_sample=False, do_main=True)
