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


def find_ops(nums, target, allow_concat=False):
    if len(nums) == 1 and nums[0] != target:
        return False

    cur_num = nums[-1]

    t1 = None
    if cur_num != 0:
        res, rem = divmod(target, cur_num)

        if rem == 0:
            t1 = res

    t2 = target - cur_num

    left_over = sum(nums[:-1])
    if (t1 and t1 == left_over) or t2 == left_over:
        return True

    if t1:
        if find_ops(nums[:-1], t1):
            return True

        if allow_concat:
            for p in combinations(nums[:-1]):
                if find_ops(p, t1):
                    return True

    if find_ops(nums[:-1], t2):
        return True

    if allow_concat:
        for p in combinations(nums[:-1]):
            if find_ops(p, t2):
                return True

    if not allow_concat or len(nums) < 2:
        return False

    cur_num_concat = int(str(nums[-2]) + str(cur_num))
    if cur_num_concat == target:
        return True

    if find_ops(nums[:-2] + [cur_num_concat], target):
        return True

    return False





def solve_parts(inputs, allow_concat=False):
    res = 0

    for targ, nums in inputs:
        if find_ops(nums, targ, allow_concat):
            res += targ

    return res

def combinations(nums):
    s = "".join([str(x) for x in nums])

    new_nums = [int(s)]
    yield new_nums

    for i in range(1, len(s)):
        s1, s2 = s[:i], s[i:]
        for sub in combinations(s1):
            yield sub + [int(s2)]



# def solve_part_02(inputs):
#     res = 0
#
#     for targ, nums in inputs:
#         for p in combinations(nums):
#             if find_ops(p, targ):
#                 res += targ
#                 break
#
#     return res




solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
