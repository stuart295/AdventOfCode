import re
from functools import lru_cache

from utils.common import solve_puzzle, in_bounds
import numpy as np

YEAR = 2025
DAY = 7


def solve_part_01(start, lines):
    splits = 0

    beams = [start]
    seen = set()

    while beams:
        cur_row, cur_col = beams.pop()
        next_row = cur_row +1
        if next_row >= len(lines):
            continue

        if lines[next_row][cur_col] == '.':
            beams.append((next_row, cur_col))
            continue

        # Splitter
        left_added, right_added = False, False
        left_beam = (next_row, cur_col-1)
        right_beam = (next_row, cur_col+1)
        if left_beam not in seen and in_bounds(left_beam, len(lines), len(lines[0])):
            beams.append(left_beam)
            seen.add(left_beam)
            left_added = True

        if right_beam not in seen and in_bounds(right_beam, len(lines), len(lines[0])):
            seen.add(right_beam)
            beams.append(right_beam)
            right_added = True

        if left_added or right_added:
            splits += 1

    return splits

@lru_cache
def solve_part_02(start, lines):
    timelines = 0
    h, w = len(lines), len(lines[0])
    cur_row, cur_col = tuple(start)

    while True:

        cur_row += 1
        if cur_row >= len(lines):
            return 1

        if lines[cur_row][cur_col] == '.':
            continue

        # Splitter
        left_beam = (cur_row, cur_col-1)
        right_beam = (cur_row, cur_col+1)
        if in_bounds(left_beam, h, w):
            timelines += solve_part_02(left_beam, lines)

        if in_bounds(right_beam, h, w):
            timelines += solve_part_02(right_beam, lines)

        return timelines

def solve(lines):

    start = None
    for i, row in enumerate(lines):
        for j, c in enumerate(row):
            if c == 'S':
                start = (i, j)

    part1 = solve_part_01(start, lines)
    part2 = solve_part_02(start, tuple(lines))

    return part1, part2


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, autoclean=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True, autoclean=False)
