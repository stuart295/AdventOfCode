import dataclasses
import multiprocessing
import random
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
        return self.ore >= bp.geo_bot_ore_cost and self.obs >= bp.geo_bot_obs_cost



def build_geo_bot(state: State, bp: Blueprint):
    assert state.ore >= bp.geo_bot_ore_cost
    assert state.obs >= bp.geo_bot_obs_cost

    state.ore -= bp.geo_bot_ore_cost
    state.obs -= bp.geo_bot_obs_cost
    state.geo_bots += 1


def build_obs_bot(state: State, bp: Blueprint):
    assert state.ore >= bp.obs_bot_ore_cost
    assert state.clay >= bp.obs_bot_clay_cost
    state.ore -= bp.obs_bot_ore_cost
    state.clay -= bp.obs_bot_clay_cost
    state.obs_bots += 1


def build_clay_bot(state: State, bp: Blueprint):
    assert state.ore >= bp.clay_bot_ore_cost
    state.ore -= bp.clay_bot_ore_cost
    state.clay_bots += 1


def build_ore_bot(state: State, bp: Blueprint):
    assert state.ore >= bp.ore_bot_ore_cost
    state.ore -= bp.ore_bot_ore_cost
    state.ore_bots += 1


def do_nothing(state: State, bp: Blueprint):
    pass



def geo_limit(state: State, bp : Blueprint, other_cache):
    t = state.to_tuple()
    if t in other_cache:
        return other_cache[t]


    temp_state = dataclasses.replace(state)

    temp_state.ore_ore = temp_state.ore
    temp_state.clay_ore = temp_state.ore
    temp_state.obs_ore = temp_state.ore
    temp_state.obs_clay = temp_state.clay
    temp_state.geo_ore = temp_state.ore
    temp_state.geo_obs = temp_state.obs



    while temp_state.timestep > 0:
        prev = dataclasses.replace(temp_state)
        prev.ore_ore = temp_state.ore_ore
        prev.clay_ore = temp_state.clay_ore
        prev.obs_ore = temp_state.obs_ore
        prev.obs_clay = temp_state.obs_clay
        prev.geo_ore = temp_state.geo_ore
        prev.geo_obs = temp_state.geo_obs

        temp_state.step()
        temp_state.ore_ore += temp_state.ore_bots
        temp_state.clay_ore += temp_state.ore_bots
        temp_state.obs_ore += temp_state.ore_bots
        temp_state.obs_clay += temp_state.clay_bots
        temp_state.geo_ore += temp_state.ore_bots
        temp_state.geo_obs += temp_state.obs_bots


        if prev.ore_ore >= bp.ore_bot_ore_cost:
            temp_state.ore_ore -= bp.ore_bot_ore_cost
            temp_state.ore_bots += 1

        if prev.clay_ore >= bp.clay_bot_ore_cost:
            temp_state.clay_ore -= bp.clay_bot_ore_cost
            temp_state.clay_bots += 1

        if prev.obs_ore >= bp.obs_bot_ore_cost and prev.obs_clay >= bp.obs_bot_clay_cost:
            temp_state.obs_ore -= bp.obs_bot_ore_cost
            temp_state.obs_clay -= bp.obs_bot_clay_cost
            temp_state.obs_bots += 1

        if prev.geo_ore >= bp.geo_bot_ore_cost and prev.geo_obs >= bp.geo_bot_obs_cost:
            temp_state.geo_ore -= bp.geo_bot_ore_cost
            temp_state.geo_obs -= bp.geo_bot_obs_cost
            temp_state.geo_bots += 1

    other_cache[t] = temp_state.geo
    return temp_state.geo





    # return time ** 2 - (time * (time - 1)) / 2


@dataclass
class BestValue:
    value: int = -1


def get_max_geos(state, bp, step, all_best, cache, other_cache):

    prev_state = dataclasses.replace(state)

    if step:
        state.step()

    if state.timestep <= 0:
        # print(f"Leaf reached: {state.geo}", flush=True)
        return state.geo

    max_possible_geos = geo_limit(state, bp, other_cache)
    if max_possible_geos + 2 <= all_best.value:
        return -1

    # if state.score(bp) <= prev_best:
    #     return -1

    tup = state.to_tuple()
    if tup in cache:
        return cache[tup]

    # Add actions
    def get_actions(state):
        actions = []

        if state.can_build_geo_bot(bp): actions.append(build_geo_bot)
        if state.can_build_obs_bot(bp): actions.append(build_obs_bot)
        if state.can_build_clay_bot(bp): actions.append(build_clay_bot)
        if state.can_build_ore_bot(bp): actions.append(build_ore_bot)

        actions.append(do_nothing)

        if len(actions) > 1:
            random.shuffle(actions)
        return actions

    local_best = -1

    for act in get_actions(prev_state):
        # next_state = State(**dataclasses.asdict(new_state))
        next_state = dataclasses.replace(state)
        act(next_state, bp)

        cur_best = get_max_geos(next_state, bp, True, all_best, cache, other_cache)

        local_best = max(local_best, cur_best)
        all_best.value = max(all_best.value, local_best)

    cache[tup] = local_best

    # all_best.value = max(all_best.value, local_best)

    return local_best


def solve_one(bp, outputs, time=24, use_quality=True):
    local_best = BestValue()

    cache = {}
    other_cache = {}
    start_state = State(timestep=time)
    best = get_max_geos(start_state, bp, True, local_best, cache, other_cache)
    print(f"BP {bp.id}: {best}", flush=True)

    if use_quality:
        outputs.append(best * bp.id)
    else:
        outputs.append(best)

def solve(lines):
    bps = [Blueprint(line) for line in lines]

    # manager = multiprocessing.Manager()
    # outputs = manager.list()
    # jobs = []
    #
    # for bp in bps:
    #     process = multiprocessing.Process(
    #         target=solve_one,
    #         args=(bp, outputs)
    #     )
    #     jobs.append(process)
    #     process.start()
    #
    # for j in jobs:
    #     j.join()

    # part1 = sum(outputs)
    part1 = None

    # Part 2
    manager = multiprocessing.Manager()
    outputs = manager.list()
    jobs = []

    for bp in bps[:3]:
        process = multiprocessing.Process(
            target=solve_one,
            args=(bp, outputs, 32, False)
        )
        jobs.append(process)
        process.start()

    for j in jobs:
        j.join()

    part2 = outputs[0] * outputs[1] * outputs[2]

    print(part2)

    return part1, part2


debug = True
# solve_puzzle(year=2022, day=19, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=19, solver=solve, do_sample=False, do_main=True)
