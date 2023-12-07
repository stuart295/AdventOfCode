from utils.common import solve_puzzle
from functools import lru_cache

YEAR = 2023
DAY = 5

map_conn = {}

def parse_input(lines):
    seeds = [int(x) for x in lines[0].split(":")[1].strip().split(" ")]
    maps = {}

    cur_map = None
    cur_map_name = None

    for line in lines[2:]:
        if not line:
            continue

        # Title line
        if not line[0].isdigit():
            if cur_map:
                maps[cur_map_name] = cur_map
            cur_map_name = line.split("-")[0]
            map_conn[cur_map_name] = line.split("-")[2].split(" ")[0]
            cur_map = []
            continue

        cur_map.append([int(x) for x in line.split(" ")])

    if cur_map:
        maps[cur_map_name] = cur_map
    return seeds, maps


def apply_map(val, cur_map):
    for dest, src, length in cur_map:
        if src <= val <= src + length:
            return dest + (val - src)

    return val


def apply_maps(seed, maps):
    cur_map_name = "seed"
    seed_map = {"seed": seed}

    val = seed

    while cur_map_name != "location":
        cur_map = maps[cur_map_name]
        val = apply_map(val, cur_map)

        cur_map_name = map_conn[cur_map_name]
        seed_map[cur_map_name] = val

    return seed_map

def solve_p1(seeds, maps):
    locations = []

    for seed in seeds:
        mapped_seed = apply_maps(seed, maps)
        locations.append(mapped_seed["location"])

    return min(locations)

def solve_p2(seeds, maps):
    locations = []

    for i in range(0, len(seeds), 2):
        seed_start = seeds[i]
        seed_end = seeds[i+1]

        for seed in range(seed_start, seed_start + seed_end):
            mapped_seed = apply_maps(seed, maps)
            locations.append(mapped_seed["location"])

    return min(locations)


def solve(lines):
    seeds, maps = parse_input(lines)

    # print(seeds)
    # print(maps)
    # print(map_conn)

    part1 = solve_p1(seeds, maps)

    part2 = solve_p2(seeds, maps)

    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
