from utils.common import solve_puzzle

YEAR = 2024
DAY = 7


def solve(lines):
    inputs = []
    for line in lines:
        x, y = line.split(": ")
        inputs.append([int(x), list(map(int, y.split(" ")))])

    part1 = solve_part_01(inputs)
    part2 = solve_part_02()

    return part1, part2


def find_ops(nums, target):
    if len(nums) == 1 and nums[0] != target:
        return False

    cur_num = nums[-1]

    res, rem = divmod(target, cur_num)
    t1 = None
    if rem == 0:
        t1 = res

    t2 = target - cur_num

    left_over = sum(nums[:-1])
    if t1 and t1 == left_over:
        return True

    if t2 == left_over:
        return True

    if t1 and find_ops(nums[:-1], t1):
        return True

    return find_ops(nums[:-1], t2)


def solve_part_01(inputs):
    res = 0

    for targ, nums in inputs:
        if find_ops(nums, targ):
            res += targ

    return res


def solve_part_02(inputs):
    return None


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
