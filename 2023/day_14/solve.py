from utils.common import solve_puzzle

from collections import Counter

YEAR = 2023
DAY = 14


def solve_part_1(objects, w, h):
    new_objects = tilt_mirror(objects, (0, -1), w, h)

    return calc_score(h, new_objects.items())


def calc_score(h, new_objects):
    return sum(h - y for (x, y), c in new_objects if c == "O")


def tilt_mirror(objects, tilt_dir, w, h):
    start_objects = Counter(objects.values())

    tx, ty = tilt_dir

    def sort_func(item):
        (xi, yi), ci = item
        if ty < 0:
            return yi
        elif ty > 0:
            return -yi
        elif tx < 0:
            return xi
        else:
            return -xi

    objects_sorted = sorted(objects.items(), key=sort_func)

    new_objects = {}
    for (x, y), c in objects_sorted:
        if c != "O":
            new_objects[(x, y)] = c
            continue

        curx, cury = x, y
        while (0 <= curx < w) and (0 <= cury < h) and (curx, cury) not in new_objects:
            curx += tx
            cury += ty

        new_objects[(curx - tx, cury - ty)] = c

    final_objects = Counter(new_objects.values())
    assert final_objects == start_objects

    return new_objects


def read_input(lines):
    objects = {}

    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c == ".":
                continue

            objects[(x, y)] = c
    return objects


def solve_part_2(objects, w, h, cycles=1000000000):
    new_objects = objects
    tilts = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    cache = {}

    i = 0
    while i < cycles:
        # Check cache
        obj_ser = tuple(new_objects.items())

        if obj_ser in cache:
            new_objects, final_idx = get_final_grid(cache, cycles, i - 1, obj_ser)
            break

        for tx, ty in tilts:
            new_objects = tilt_mirror(new_objects, (tx, ty), w, h)

        cache[obj_ser] = (new_objects, i)
        i += 1

    return calc_score(h, new_objects)


def get_final_grid(cache, max_cycles, cycle_end, first_repeating_object):
    _, cycle_start = cache[first_repeating_object]
    rem_items = max_cycles - cycle_start
    d = cycle_end - cycle_start + 1
    final_cache_idx = (rem_items % d)
    cache_list = list(cache.items())
    assert all([i == cache_list[i][1][1] for i in range(len(cache_list))])

    cache_list = cache_list[cycle_start:]
    new_objects, _ = cache_list[final_cache_idx]

    return new_objects, final_cache_idx


def solve(lines):
    objects = read_input(lines)
    w, h = len(lines[0]), len(lines)

    part1 = solve_part_1(objects, w, h)
    part2 = solve_part_2(objects, w, h)

    return part1, part2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
