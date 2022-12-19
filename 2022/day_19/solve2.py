import dataclasses
import uuid
from dataclasses import dataclass

from ortools.sat.python import cp_model

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
    timestep: int = 24

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
            n = add_node(G, next_state, bp, False)
            G.add_edge(next_state.to_tuple(), n.to_tuple())

    # clay bot
    if new_state.can_build_clay_bot(bp):
        next_state = State(**dataclasses.asdict(new_state))
        next_state.ore -= bp.clay_bot_ore_cost
        next_state.clay_bots += 1
        if not next_state.to_tuple() in G.nodes:
            n = add_node(G, next_state, bp, False)
            G.add_edge(next_state.to_tuple(), n.to_tuple())

    # obs bot
    if new_state.can_build_obs_bot(bp):
        next_state = State(**dataclasses.asdict(new_state))
        next_state.ore -= bp.obs_bot_ore_cost
        next_state.clay -= bp.obs_bot_clay_cost
        next_state.obs_bots += 1
        if not next_state.to_tuple() in G.nodes:
            n = add_node(G, next_state, bp, False)
            G.add_edge(next_state.to_tuple(), n.to_tuple())

    # geo bot
    if new_state.can_build_geo_bot(bp):
        next_state = State(**dataclasses.asdict(new_state))
        next_state.ore -= bp.geo_bot_ore_cost
        next_state.obs -= bp.geo_bot_obs_cost
        next_state.geo_bots += 1
        if not next_state.to_tuple() in G.nodes:
            n = add_node(G, next_state, bp, False)
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

def calc_max_ore_bots(cost, time):
    bots = 1
    ore = 0
    for t in range(time):
        ore += bots
        while ore >= cost:
            bots += 1
            ore -= cost
    return bots

def solve_constraints(bp: Blueprint, time: int = 24):
    bound = 10000000000
    # solver = pywraplp.Solver('Maximize geodes', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    model = cp_model.CpModel()
    # solver = pywraplp.Solver.CreateSolver('SCIP')
    ore_bots = model.NewIntVar(1, time, 'ore_bots')
    clay_bots = model.NewIntVar(0, time, 'clay_bots')
    obs_bots = model.NewIntVar(0, time, 'obs_bots')
    geo_bots = model.NewIntVar(0, time, 'geo_bots')

    model.Add(ore_bots <= calc_max_ore_bots(bp.ore_bot_ore_cost, time))

    model.Add(ore_bots + clay_bots + obs_bots + geo_bots < time)

    ore = model.NewIntVar(0, bound, 'ore')
    clay = model.NewIntVar(0, bound, 'clay')
    obs = model.NewIntVar(0, bound, 'obs')
    geo = model.NewIntVar(0, bound, 'geo')

    # timesteps = model.NewIntVar(0, time, 'time')

    max_ore = model.NewIntVar(0, bound, 'max ore')
    max_clay = model.NewIntVar(0, bound, 'max clay')
    max_obs = model.NewIntVar(0, bound, 'max obs')
    max_geo = model.NewIntVar(0, bound, 'max geo')

    model.AddMultiplicationEquality(max_ore, [ore_bots, time])
    model.AddMultiplicationEquality(max_clay, [clay_bots, time])
    model.AddMultiplicationEquality(max_obs, [obs_bots, time])
    model.AddMultiplicationEquality(max_geo, [geo_bots, time])

    model.Add(ore <= max_ore)
    model.Add(clay <= max_clay)
    model.Add(obs <= max_obs)
    model.Add(geo <= max_geo)

    available_ore = model.NewIntVar(0, bound, 'total ore')
    model.Add(
        available_ore == ore - ore_bots * bp.ore_bot_ore_cost - clay_bots * bp.clay_bot_ore_cost - obs_bots * bp.obs_bot_ore_cost - geo_bots * bp.geo_bot_ore_cost)

    available_clay = model.NewIntVar(0, bound, 'total clay')
    model.Add(available_clay == clay - obs_bots * bp.obs_bot_clay_cost)

    available_obs = model.NewIntVar(0, bound, 'total obs')
    model.Add(available_obs == obs - geo_bots * bp.geo_bot_obs_cost)

    # Bot limits given resources
    max_ore_bots = model.NewIntVar(0, bound, 'max_ore_bots')
    model.AddDivisionEquality(max_ore_bots, available_ore, bp.ore_bot_ore_cost)

    max_clay_bots = model.NewIntVar(0, bound, 'max_clay_bots')
    model.AddDivisionEquality(max_clay_bots, available_ore, bp.clay_bot_ore_cost)

    max_obs_bots_ore = model.NewIntVar(0, bound, 'max_obs_bots_ore')
    model.AddDivisionEquality(max_obs_bots_ore, available_ore, bp.obs_bot_ore_cost)

    max_obs_bots_clay = model.NewIntVar(0, bound, 'max_obs_bots_clay')
    model.AddDivisionEquality(max_obs_bots_clay, available_clay, bp.obs_bot_clay_cost)

    max_geo_bots_ore = model.NewIntVar(0, bound, 'max_geo_bots_ore')
    model.AddDivisionEquality(max_geo_bots_ore, available_ore, bp.geo_bot_ore_cost)

    max_geo_bots_obs = model.NewIntVar(0, bound, 'max_geo_bots_obs')
    model.AddDivisionEquality(max_geo_bots_obs, available_obs, bp.geo_bot_obs_cost)

    model.Add(ore_bots <= max_ore_bots)
    model.Add(clay_bots <= max_clay_bots)
    model.Add(obs_bots <= max_obs_bots_ore)
    model.Add(obs_bots <= max_obs_bots_clay)
    model.Add(geo_bots <= max_geo_bots_ore)
    model.Add(geo_bots <= max_geo_bots_obs)

    model.Maximize(geo)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(status)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Value: {solver.Value(geo)}")
        return solver.Value(geo)
    else:
        print('No solution found.')
        return -1


def solve(lines):
    bps = [Blueprint(line) for line in lines]

    max_geos = []
    quality = 0
    for bp in bps:
        # G, start = build_graph(bp)
        # print(f"BP {bp.id}: {len(G.nodes)}", flush=True)
        # cur_max = 0
        # for node in G.nodes:
        #     cur_max = max(cur_max, G.nodes[node]['state'].geo)
        best = solve_constraints(bp, 24)

        max_geos.append(best)
        quality += best * bp.id

    part1 = quality

    part2 = None

    return part1, part2


debug = True
solve_puzzle(year=2022, day=19, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
# solve_puzzle(year=2022, day=19, solver=solve, do_sample=False, do_main=True)
