import multiprocessing

import numpy as np

from utils.common import solve_puzzle, grid_offsets
from collections import defaultdict
from functools import lru_cache


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
    sx, sy = s

    prev_x, prev_y = grid_offsets()[-1]
    prev_x = sx + prev_x * (dists[s] + 1)
    prev_y = sy + prev_y * (dists[s] + 1)

    checked = set()

    for cx, cy in ((sx + x * (dists[s] + 1), sy + y * (dists[s] + 1)) for x, y in grid_offsets()):
        if not run.is_set():
            if debug: print(f"{s}: Done", flush=True)
            return

        off_x = np.clip(cx - prev_x, -1, 1)
        off_y = np.clip(cy - prev_y, -1, 1)
        cur_x, cur_y = prev_x, prev_y

        for _ in range(abs(prev_x - cx)):
            if (cur_x, cur_y) not in checked:
                checked.add((cur_x, cur_y))

                if 0 <= cur_x <= limit and 0 <= cur_y <= limit:
                    if manhatten((cur_x, cur_y), s) <= dists[s]:
                        continue

                    if not is_sensed((cur_x, cur_y), sensors, dists):
                        freq = 4000000 * cur_x + cur_y
                        outputs.append(freq)
                        run.clear()
                        if debug: print(f"{s}: Done. Result = {freq}", flush=True)
                        return
            cur_x += off_x
            cur_y += off_y

        prev_x, prev_y = cx, cy

    if debug: print(f"{s}: Done", flush=True)


def solve(lines):
    sensors, beacons, dists = read_data(lines)

    # Part 1
    part1 = solve_part_1(beacons, sensors, dists, y=2000000)

    # Part 2
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


debug = True
# solve_puzzle(year=2022, day=15, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=15, solver=solve, do_sample=False, do_main=True)
