from utils.common import solve_puzzle
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


def manhatten(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# def is_sensed(pos, sensors):
#     dists = [(s, manhatten(pos, s)) for s in sensors]
#     dists = sorted(dists, key=lambda x: x[1])
#     closest, close_dist = dists[0]
#     sensor_dist = manhatten(closest, sensors[closest])
#     return close_dist <= sensor_dist


def is_sensed(pos, sensors, dists):
    # last_dist = 1e9

    # s_dists = [(s, manhatten(pos, s)) for s in sensors]
    # s_dists = sorted(s_dists, key=lambda x: x[1])

    for s in sensors:
        sensor_dist = dists[s]

        # if sensor_dist > last_dist:
        #     return False

        # last_dist = sensor_dist

        dist = manhatten(pos, s)
        if dist <= sensor_dist:
            return True
    return False

# def is_sensed(pos, sensors, beacons, dists):
#     last_dist = 1e9
#
#     b_dists = [(b, manhatten(pos, b)) for b in beacons]
#     b_dists = sorted(b_dists, key=lambda x: x[1])
#
#     for b, b_dist in b_dists:
#         if last_dist < b_dist:
#             return False
#         last_dist = b_dist
#
#         for s in beacons[b]:
#             sensor_dist = dists[s]
#
#             dist = manhatten(pos, s)
#             if dist <= sensor_dist:
#                 return True
#     return False


def solve(lines):
    sensors, beacons, dists = read_data(lines)

    # sensed = part_1(beacons, sensors, dists, y=2000000)
    #
    # part1 = sensed
    part1 = None

    limit = 4000000
    part2 = None
    for x in range(0, limit+1):
        for y in range(0, limit+1):
            if (x, y) in beacons:
                continue

            if (x, y) in sensors:
                continue

            if is_sensed((x, y), sensors, dists):
                continue

            part2 =4000000 * x + y

    return part1, part2


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


debug = False
solve_puzzle(year=2022, day=15, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=2022, day=15, solver=solve, do_sample=False, do_main=True)
