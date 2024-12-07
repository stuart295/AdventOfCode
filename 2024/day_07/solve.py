from utils.common import solve_puzzle
from itertools import product

YEAR = 2024
DAY = 7


def solve(lines):
    inputs = []
    for line in lines:
        x, y = line.split(": ")
        inputs.append([int(x), list(map(int, y.split(" ")))])

    part1 = solve_like_a_savage(inputs, "*+")
    part2 = solve_like_a_savage(inputs, "*+|")

    return part1, part2


def solve_like_a_savage(inputs, ops):
    res = 0

    for targ, nums in inputs:
        for op_combs in product(ops, repeat=len(nums) - 1):
            val = nums[0]
            for n, o in zip(nums[1:], op_combs):
                if o == "*":
                    val *= n
                elif o == "+":
                    val += n
                else:
                    val = int(str(val) + str(n))
            if val == targ:
                res += targ
                break

    return res


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
