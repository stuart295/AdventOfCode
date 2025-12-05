from utils.common import solve_puzzle
import numpy as np
import cv2 as cv

YEAR = 2025
DAY = 5


def solve(lines):
    fresh = []
    all_ingredients = []

    collecting_all = False
    for line in lines:
        if line.strip() == "":
            collecting_all = True
            continue

        if collecting_all:
            all_ingredients.append(int(line))
        else:
            fresh.append([int(x) for x in line.split("-")])

    part1 = solve_part_01(all_ingredients, fresh)

    part2 = solve_part_02(fresh)

    return part1, part2


def is_overlapping(s1, e1, s2, e2):
    if s2 <= s1 <= e2:
        return True

    if s2 <= e1 <= e2:
        return True

    if s1 <= s2 <= e1:
        return True

    if s1 <= e2 <= e1:
        return True

    return False

def merge_ranges(ranges):
    merged = list(ranges)

    idx = 0

    while idx < len(merged):

        cur_start, cur_end = merged[idx]
        was_merged = False
        for other_idx, (other_start, other_end) in enumerate(merged[idx+1:]):
            if is_overlapping(cur_start, cur_end, other_start, other_end):
                new_range = [min(cur_start, other_start), max(cur_end, other_end)]
                merged.pop(idx+1+other_idx)
                merged[idx] = new_range
                was_merged = True
                break

        if not was_merged:
            idx+=1

    return merged


def solve_part_02(fresh) -> int:
    prev = []
    ranges_merged = list(fresh)
    while len(ranges_merged) != len(prev):
        prev = list(ranges_merged)
        ranges_merged = merge_ranges(prev)

    result = 0
    for start, end in ranges_merged:
        result += (end+1)-start

    return result


def solve_part_01(all_ingredients, fresh) -> int:
    part1_match = []
    for ing in all_ingredients:
        for start, end in fresh:
            if start <= ing <= end:
                part1_match.append(ing)
                break

    part1 = len(part1_match)
    return part1


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
