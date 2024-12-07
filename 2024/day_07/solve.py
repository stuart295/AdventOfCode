from utils.common import solve_puzzle

YEAR = 2024
DAY = 7


def solve(lines):
    inputs = []
    for line in lines:
        x, y = line.split(": ")
        inputs.append([int(x), list(map(int, y.split(" ")))])

    part1 = solve_parts(inputs)
    part2 = solve_parts(inputs, True)

    return part1, part2


def is_legit(target, nums, part2):
    if sum(nums) == target:
        return True

    if len(nums) <= 1:
        return False

    if is_legit(target, [nums[0] * nums[1]] + nums[2:], part2):
        return True

    if is_legit(target, [nums[0] + nums[1]] + nums[2:], part2):
        return True

    if part2 and len(nums) >= 2:
        nums[0] = int(str(nums[0]) + str(nums.pop(1)))
        if is_legit(target, nums, part2):
            return True

    return False


def solve_parts(inputs, part2=False):
    res = 0

    for targ, nums in inputs:
        if is_legit(targ, nums, part2):
            res += targ

    return res


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
