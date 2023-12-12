import itertools
import operator
import re
from collections import Counter
from functools import lru_cache, reduce
from itertools import combinations, combinations_with_replacement, product, permutations

from joblib import Parallel, delayed

from utils.common import solve_puzzle

YEAR = 2023
DAY = 12


def parse_input(lines):
    groups, counts = [], []

    for line in lines:
        g, c = line.split(" ")
        counts.append([int(x) for x in c.split(",")])
        groups.append(g)

    return groups, counts


def unfold(groups, counts):
    groups2, counts2 = [], []

    for g, c in zip(groups, counts):
        groups2.append("?".join(g for _ in range(5)))
        counts2.append(c * 5)

    return groups2, counts2


@lru_cache(maxsize=None)
def get_combs(group, count):
    cur_count = count[0]

    total = 0

    hs_pos = None

    for idx in range(len(group) - cur_count + 1):
        region = group[idx:idx + cur_count]

        # Only a valid island if it has "?" or "#"
        has_dot = "." in region

        # Over extended
        over_ext = group[idx + cur_count] == "#" if idx + cur_count < len(group) else False

        # Following a #
        prev_c = group[idx - 1] == "#" if idx > 0 else False

        if not (has_dot or over_ext or prev_c):
            if len(count) == 1:
                if "#" not in group[idx + cur_count + 1:]:
                    total += 1
            else:
                total += get_combs(group[idx + cur_count + 1:], count[1:])

        if hs_pos is not None and hs_pos < idx:
            break

        if hs_pos is None and "#" in region:
            hs_pos = idx + region.index("#")

    return total


def solve_part_01(groups, counts):
    totals = []

    for i, (group, count) in enumerate(zip(groups, counts)):
        totals.append(get_combs(group, tuple(count)))
    return totals


def solve(lines):
    groups, counts = parse_input(lines)

    comb_counts = solve_part_01(groups, counts)
    part1 = sum(comb_counts)

    groups, counts = unfold(groups, counts)
    comb_counts = solve_part_01(groups, counts)
    part2 = sum(comb_counts)

    return part1, part2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, sample_data_path="test.txt")
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
