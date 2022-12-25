from collections import deque
from functools import lru_cache

from utils.common import solve_puzzle, grid_offsets
from utils.grid_graph import GridGraph
from copy import deepcopy

BLIZZ = {'v': (0, 1), '<': (-1, 0), '>': (1, 0), '^': (0, -1)}


def read_data(lines):
    G = GridGraph([line.strip() for line in lines])  # Hijacking this class for convenience
    G.set_walls('#')

    blizzards = {}

    for node in G.graph.nodes:
        blizzards[node] = set()
        if G.graph.nodes[node]['char'] in BLIZZ:
            blizzards[node].add(G.graph.nodes[node]['char'])
            G.graph.nodes[node]['char'] = '.'

    return G, blizzards


def lcm(a, b):
    big, small = max(a, b), min(a, b)

    result = big
    while result % small != 0:
        result += big

    return result


@lru_cache()
def taxicab(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@lru_cache()
def is_valid(pos, w, h, start, end):
    if pos == start or pos == end:
        return True

    x, y = pos
    return 1 <= x <= (w - 2) and 1 <= y <= (h - 2)


def find_path(blizzards, w, h, start, end, cache=None, limit=500):
    to_check = deque()
    to_check.append((deepcopy(blizzards), start, 0))

    bliz_loop = lcm(w-2, h-2)

    shortest = limit

    blizz_cache = {}
    final_blizz = None

    while to_check:
        to_check = sorted(to_check, key=lambda x: taxicab(x[1], end), reverse=True)

        cur_blizzards, pos, cur_dist = to_check.pop()

        rem_dist = taxicab(pos, end)
        if cur_dist + rem_dist >= shortest:
            continue

        state = (cur_dist % bliz_loop, pos)
        if state in cache:
            continue

        cache.add(state)

        if pos == end:
            if cur_dist < shortest:
                shortest = cur_dist
                final_blizz = cur_blizzards
            continue

        cur_blizzards = update_blizzards(cur_blizzards, cur_dist % bliz_loop, blizz_cache, w, h, start, end)

        # Choose positions
        x, y = pos

        for ox, oy in grid_offsets():
            neighx, neighy = x + ox, y + oy
            neigh = (neighx, neighy)
            if is_valid(neigh, w, h, start, end) and len(cur_blizzards[neigh]) == 0:
                dist = taxicab(neigh, end)
                if cur_dist + dist < shortest:
                    to_check.append((cur_blizzards.copy(), neigh, cur_dist + 1))

        if len(cur_blizzards[pos]) == 0:
            dist = taxicab(pos, end)
            if cur_dist + dist < shortest:
                to_check.append((cur_blizzards.copy(), pos, cur_dist + 1))

    return shortest, final_blizz


def update_blizzards(blizzards, step, blizz_cache, w, h, start, end):
    if step in blizz_cache:
        return blizz_cache[step]

    new_blizz = deepcopy(blizzards)

    for node in new_blizz:
        new_blizz[node] = set()

    # Update blizzards
    for node in blizzards:
        x, y = node
        blizz = blizzards[node]
        for b in blizz:
            dir = BLIZZ[b]
            dest = (x + dir[0], y + dir[1])
            if not is_valid(dest, w, h, start, end):
                if b == 'v':
                    dest = (x, 1)
                elif b == '^':
                    dest = (x, h - 2)
                elif b == '<':
                    dest = (w - 2, y)
                elif b == '>':
                    dest = (1, y)

            new_blizz[dest].add(b)

    blizz_cache[step] = new_blizz
    return new_blizz


def solve(lines):
    G, blizzards = read_data(lines)
    cache = set()

    start = (1, 0)
    end = (G.w - 2, G.h - 1)

    # Part 1
    part1, blizzards = find_path(blizzards.copy(), G.w, G.h, start, end, cache)

    # Part 2
    cache.clear()
    trip_back_dist, blizzards = find_path(blizzards.copy(), G.w, G.h, end, start, cache)

    cache.clear()
    final_trip_dist, blizzards = find_path(blizzards.copy(), G.w, G.h, start, end, cache)

    part2 = part1 + trip_back_dist + final_trip_dist

    return part1, part2


debug = True
solve_puzzle(year=2022, day=24, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=24, solver=solve, do_sample=False, do_main=True)
