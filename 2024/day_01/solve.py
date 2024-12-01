from utils.common import solve_puzzle
from collections import Counter

YEAR = 2024
DAY = 1


def solve(lines):
    l1, l2 = convert_to_lists(lines)

    part1 = solve_part_01(l1, l2)
    part2 = solve_part_02(l1, l2)

    return part1, part2


def solve_part_02(l1, l2):
    occurrences = Counter(l2)
    part2 = sum(a * occurrences.get(a, 0) for a in l1)
    return part2


def solve_part_01(l1, l2):
    l1 = sorted(l1)
    l2 = sorted(l2)
    total_dists = sum(abs(a - b) for a, b in zip(l1, l2))
    return total_dists


def convert_to_lists(lines):
    l1, l2 = [], []
    for line in lines:
        a, b = [int(x) for x in line.split("   ")]
        l1.append(a)
        l2.append(b)
    return l1, l2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
