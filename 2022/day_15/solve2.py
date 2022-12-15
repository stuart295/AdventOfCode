import multiprocessing

from utils.common import solve_puzzle, grid_offsets
from collections import defaultdict
from functools import lru_cache
import numpy as np
from scipy.spatial.distance import cityblock


def read_data(lines):
    sensors = {}
    beacons = defaultdict(set)
    dists = {}

    for line in lines:
        cur = line.replace(',', '').replace(':', '').strip().split(' ')
        cur_s = (int(cur[2].split('=')[1]), int(cur[3].split('=')[1]))
        cur_b = (int(cur[8].split('=')[1]), int(cur[9].split('=')[1]))
        sensors[cur_s] = cur_b
        beacons[cur_b].add(cur_s)
        dists[cur_s] = manhatten(cur_s, cur_b)

    return sensors, beacons, dists


def manhatten(p1, p2):
    return cityblock(p1, p2)
    # return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# def is_sensed(pos, sensors, dists):
#     last_dist = 1e9
#
#     s_dists = [(s, manhatten(pos, s)) for s in sensors]
#     s_dists = sorted(s_dists, key=lambda x: x[1])
#
#     for s, dist in s_dists:
#         if dist > last_dist:
#             return False
#
#         sensor_dist = dists[s]
#
#
#
#         last_dist = sensor_dist
#
#         if dist <= sensor_dist:
#             return True
#     return False


def is_sensed(pos, sensors, dists):
    for s in sensors:
        sensor_dist = dists[s]

        dist = manhatten(pos, s)
        if dist <= sensor_dist:
            return True
    return False


def part_1(beacons, sensors, dists, y):
    max_dist = max(dists.values())
    min_x = min(b[0] for b in beacons) - max_dist
    max_x = max(b[0] for b in beacons) + max_dist
    no_beacons = 0
    temp = ''
    for x in range(min_x, max_x):
        if (x, y) in beacons:
            temp += 'B'
            continue

        if (x, y) in sensors:
            temp += 'S'
            no_beacons += 1
            continue

        if is_sensed((x, y), sensors, dists):
            no_beacons += 1
            temp += '#'
        else:
            temp += '.'

    if debug: print(temp)

    return no_beacons


def solve_row(beacons, sensors, dists, dy, skip, limit):
    for y in range(dy, limit + 1, skip):
        max_dist = max(dists.values())
        min_x = min(b[0] for b in beacons) - max_dist
        min_x = max(0, min_x)

        max_x = max(b[0] for b in beacons) + max_dist
        max_x = min(limit + 1, max_x)

        for x in range(min_x, max_x):
            if (x, y) in beacons:
                continue

            if (x, y) in sensors:
                continue

            if is_sensed((x, y), sensors, dists):
                continue

            print(4000000 * x + y, flush=True)
            return


def solve_part2(sensors, beacons, dists, limit):
    jobs = []

    for i in range(12):
        process = multiprocessing.Process(
            target=solve_row,
            args=(beacons, sensors, dists, i, 12, limit)
        )
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()


def searchable(pos, searched, s, dists):
    return pos not in searched and manhatten(pos, s) > dists[s]


def solve_part2_2(s, sensors, dists, limit):
    searched = set()

    # to_search = []
    sx, sy = s

    to_search = [(sx + dists[s], sy)]

    while len(to_search) > 0:
        cur = to_search.pop()
        searched.add(cur)

        for x, y in grid_offsets(True):
            neigh = (cur[0] + x, cur[1] + y)

            nx, ny = neigh

            if nx >= 0 and nx <= limit and ny >= 0 and ny <= limit:
                if manhatten(neigh, s) <= dists[s]:
                    continue

                if not is_sensed(neigh, sensors, dists):
                    print(4000000 * nx + ny, flush=True)

            if not neigh in searched and is_border(neigh, s, dists[s]):
                to_search.append(neigh)

    print(f"{s}: Done.", flush=True)


def is_border(pos, s, sdist):
    outside = 0
    for x, y in grid_offsets(False):
        neigh = (pos[0] + x, pos[1] + y)
        ndist = manhatten(neigh, s)

        if ndist > sdist:
            outside += 1

    return outside > 0 and outside < 4


def solve(lines):
    sensors, beacons, dists = read_data(lines)

    # sensed_areas = get_sensed_positions(sensors, dists)

    # sensed = part_1(beacons, sensors, dists, y=2000000)
    #
    # part1 = sensed
    part1 = None

    limit = 4000000
    # limit = 20
    part2 = None
    # for x in range(0, limit+1):
    #     for y in range(0, limit+1):
    #         if (x, y) in beacons:
    #             continue
    #
    #         if (x, y) in sensors:
    #             continue
    #
    #         if is_sensed((x, y), sensors, dists):
    #             continue
    #
    #         part2 = 4000000 * x + y
    #         break
    #
    #     if part2:
    #         break

    jobs = []

    for i, s in enumerate(sensors):
        process = multiprocessing.Process(
            target=solve_part2_2,
            args=(s, sensors, dists, limit)
        )
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    # for s in sensors:
    #     solve_part2_2(sensors, beacons, dists, limit)

    return part1, part2


debug = True
# solve_puzzle(year=2022, day=15, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=15, solver=solve, do_sample=False, do_main=True)
