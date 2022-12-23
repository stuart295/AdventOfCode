from utils.common import solve_puzzle, grid_offsets
from collections import Counter


def read_data(lines):
    pos = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c == '#':
                pos.add((x, y))

    return pos


def consider_north(elf, elves, proposals, move_map):
    ex, ey = elf
    if all(x not in elves for x in [(ex, ey - 1), (ex - 1, ey - 1), (ex + 1, ey - 1)]):
        proposals[(ex, ey - 1)] += 1
        move_map[(ex, ey)] = (ex, ey - 1)
        return True
    return False


def consider_south(elf, elves, proposals, move_map):
    ex, ey = elf
    if all(x not in elves for x in [(ex, ey + 1), (ex - 1, ey + 1), (ex + 1, ey + 1)]):
        proposals[(ex, ey + 1)] += 1
        move_map[(ex, ey)] = (ex, ey + 1)
        return True
    return False


def consider_west(elf, elves, proposals, move_map):
    ex, ey = elf
    if all(x not in elves for x in [(ex - 1, ey), (ex - 1, ey + 1), (ex - 1, ey - 1)]):
        proposals[(ex - 1, ey)] += 1
        move_map[(ex, ey)] = (ex - 1, ey)
        return True
    return False


def consider_east(elf, elves, proposals, move_map):
    ex, ey = elf
    if all(x not in elves for x in [(ex + 1, ey), (ex + 1, ey + 1), (ex + 1, ey - 1)]):
        proposals[(ex + 1, ey)] += 1
        move_map[(ex, ey)] = (ex + 1, ey)
        return True
    return False


def print_state(elves):
    maxx = max(x for x, y in elves) + 1
    maxy = max(y for x, y in elves) + 1
    minx = min(x for x, y in elves)
    miny = min(y for x, y in elves)

    lines = [['.' for x in range(maxx - minx)] for _ in range(maxy - miny)]

    for ex, ey in elves:
        lines[ey - miny][ex - minx] = '#'

    for line in lines:
        print(''.join(line))
    print('=' * 20)


def simulate(elves, rounds, debug=False):
    dirs = [consider_north, consider_south, consider_west, consider_east]

    round = -1
    while True:
        round += 1
        if debug: print_state(elves)
        proposals = Counter()
        move_map = {}

        skips = 0

        for ex, ey in elves:
            # Adj empty
            if all((ex + ox, ey + oy) not in elves for (ox, oy) in grid_offsets(diagonals=True)):
                skips += 1
                continue

            for direction_check in dirs:
                if direction_check((ex, ey), elves, proposals, move_map):
                    break
                # print(f"No result for {ex}, {ey}!")

        if skips == len(elves) or round >= rounds:
            return elves, round

        new_elves = set()
        for elf in elves:
            if elf not in move_map:
                new_elves.add(elf)
                continue

            dest = move_map[elf]
            if proposals[dest] <= 1:
                new_elves.add(dest)
            else:
                new_elves.add(elf)

        assert len(new_elves) == len(elves)
        elves = new_elves

        dirs = dirs[1:] + [dirs[0]]


def solve_part_1(lines):
    elves = read_data(lines)
    elves, rounds = simulate(elves, rounds=10)
    minx = min(x for x, y in elves)
    maxx = max(x for x, y in elves)
    miny = min(y for x, y in elves)
    maxy = max(y for x, y in elves)
    part1 = (maxx - minx + 1) * (maxy - miny + 1) - len(elves)
    return part1


def solve_part_2(lines):
    elves = read_data(lines)
    elves, rounds = simulate(elves, rounds=1e9)
    return rounds + 1


def solve(lines):
    part1 = solve_part_1(lines)
    part2 = solve_part_2(lines)

    return part1, part2


debug = True
solve_puzzle(year=2022, day=23, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=23, solver=solve, do_sample=False, do_main=True)
