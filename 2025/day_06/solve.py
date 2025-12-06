import re

from utils.common import solve_puzzle
import numpy as np

YEAR = 2025
DAY = 6


def solve(lines):
    part1 = solve_part_1(lines)
    part2 = solve_part_2(lines)

    return part1, part2


def aggregate(nums, op):
    if op == "+":
        return np.sum(nums)
    else:
        return np.prod(nums)


def solve_part_2(lines):
    ops = re.sub('\s+', ' ', lines[-1]).split(" ")
    chars = [list(line) for line in lines[:-1]]

    cols = max(len(line) for line in chars)
    result = 0

    nums = []
    cur_op_idx = 0

    for col in range(cols):
        num_str = "".join([row[col] for row in chars]).strip()
        if num_str == "":
            result += aggregate(nums, ops[cur_op_idx])
            cur_op_idx += 1
            nums = []
        else:
            nums.append(int(num_str))

    result += aggregate(nums, ops[cur_op_idx])
    return result


def solve_part_1(lines) -> int:
    ops = re.sub('\s+', ' ', lines[-1].strip()).split(" ")
    nums = [[int(x) for x in re.sub('\s+', ' ', line.strip()).split(" ")] for line in lines[:-1]]
    nums = np.array(nums)

    part1 = 0
    for col in range(nums.shape[1]):
        part1 += aggregate(nums[:, col], ops[col])
    return part1


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, autoclean=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True, autoclean=False)
