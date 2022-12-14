from utils.common import solve_puzzle


def is_free(pt, all_rock, all_sand, floor=None):
    if floor and pt[1] >= floor:
        return False

    return pt not in all_rock and pt not in all_sand


def simulate(rock, sandpoint, is_floor=False):
    low_rock = max(y for x, y in rock)

    floor = None
    if is_floor:
        low_rock = low_rock + 2
        floor = low_rock

    all_sand = set()

    while True:
        sx, sy = sandpoint

        while True:
            if is_free((sx, sy + 1), rock, all_sand, floor):
                sy += 1
            elif is_free((sx - 1, sy + 1), rock, all_sand, floor):
                sx, sy = sx - 1, sy + 1
            elif is_free((sx + 1, sy + 1), rock, all_sand, floor):
                sx, sy = sx + 1, sy + 1
            else:
                all_sand.add((sx, sy))
                if (sx, sy) == sandpoint:
                    return all_sand
                break

            if sy >= low_rock:
                return all_sand


def load_rocks(lines):
    rock = set()
    for line in lines:
        verts = line.strip().split(' -> ')
        verts = [x.split(',') for x in verts]
        for s1, s2 in zip(verts, verts[1:]):
            x1, y1 = [int(x) for x in s1]
            x2, y2 = [int(x) for x in s2]

            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    rock.add((x, y))
    return rock


def solve(lines):
    rock = load_rocks(lines)

    final_sand = simulate(rock, (500, 0))
    part1 = len(final_sand)

    final_sand_2 = simulate(rock, (500, 0), is_floor=True)
    part2 = len(final_sand_2)

    return part1, part2


debug = True
solve_puzzle(year=2022, day=14, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=14, solver=solve, do_sample=False, do_main=True)
