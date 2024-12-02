from utils.common import solve_puzzle
from collections import Counter

YEAR = 2024
DAY = 2


def solve(lines):
    lines = [[int(l) for l in line.split(" ")] for line in lines]

    part1 = solve_part_01(lines)

    part2 = solve_part_02(lines)

    return part1, part2


def is_line_safe(line) -> bool:
    inc = all(l2 > l1 for l1, l2 in zip(line, line[1:]))
    dec = all(l2 < l1 for l1, l2 in zip(line, line[1:]))
    if not (inc or dec):
        return False

    diffs = [abs(l1 - l2) for l1, l2 in zip(line, line[1:])]
    return min(diffs) >= 1 and max(diffs) <= 3


def solve_part_01(lines):
    result = 0
    for line in lines:
        result += is_line_safe(line)
    return result


def solve_part_02(lines):
    result = 0
    for line in lines:
        if is_line_safe(line):
            result += 1
        else:
            # Glorious brute forcing
            for i in range(len(line)):
                new_line = line[0:i] + line[i + 1:]
                if is_line_safe(new_line):
                    result += 1
                    break
    return result

debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
