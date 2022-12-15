import multiprocessing

from utils.common import solve_puzzle, grid_offsets
from collections import defaultdict
from functools import lru_cache
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


@lru_cache()
def manhatten(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def is_sensed(pos, sensors, dists):
    for s in sensors:
        dist = manhatten(pos, s)
        if dist <= dists[s]:
            return True
    return False


def solve_part_1(beacons, sensors, dists, y):
    max_dist = max(dists.values())
    min_x = min(b[0] for b in beacons) - max_dist
    max_x = max(b[0] for b in beacons) + max_dist
    no_beacons = 0

    for x in range(min_x, max_x):
        if (x, y) in beacons:
            continue

        if (x, y) in sensors:
            no_beacons += 1
            continue

        if is_sensed((x, y), sensors, dists):
            no_beacons += 1

    return no_beacons


def solve_part_2(s, sensors, dists, limit, outputs, run):
    searched = set()

    sx, sy = s

    to_search = [(sx + dists[s], sy)]

    while len(to_search) > 0:
        if not run.is_set():
            return

        cur = to_search.pop()
        searched.add(cur)

        for x, y in grid_offsets(True):
            neigh = (cur[0] + x, cur[1] + y)

            nx, ny = neigh

            if 0 <= nx <= limit and 0 <= ny <= limit:
                if manhatten(neigh, s) <= dists[s]:
                    continue

                if not is_sensed(neigh, sensors, dists):
                    outputs.append(4000000 * nx + ny)
                    run.clear()
                    return

            if not neigh in searched and is_border(neigh, s, dists[s]):
                to_search.append(neigh)


def is_border(pos, s, sdist):
    outside = 0
    for x, y in grid_offsets(False):
        neigh = (pos[0] + x, pos[1] + y)
        ndist = manhatten(neigh, s)

        if ndist > sdist:
            outside += 1

    return 0 < outside < 4


def solve(lines):
    sensors, beacons, dists = read_data(lines)

    part1 = solve_part_1(beacons, sensors, dists, y=2000000)

    # Part 2 - Bad code and multiprocessing
    limit = 4000000
    # limit = 20

    jobs = []

    manager = multiprocessing.Manager()
    outputs = manager.list()
    run = manager.Event()
    run.set()

    for i, s in enumerate(sensors):
        process = multiprocessing.Process(
            target=solve_part_2,
            args=(s, sensors, dists, limit, outputs, run)
        )
        jobs.append(process)
        process.start()

    for j in jobs:
        j.join()

    part2 = outputs[0]

    return part1, part2


debug = False
# solve_puzzle(year=2022, day=15, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=15, solver=solve, do_sample=False, do_main=True)
