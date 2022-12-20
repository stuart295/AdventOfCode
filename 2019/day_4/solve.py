from utils.common import solve_puzzle
from itertools import groupby


def count_passwords(min_val, max_val, part2=False):
    c = 0

    for i in range(min_val, max_val + 1):
        digits = list(map(int, str(i)))
        if not all(x1 <= x2 for x1, x2 in zip(digits, digits[1:])): continue

        if not part2:
            if not any(x1 == x2 for x1, x2 in zip(digits, digits[1:])): continue
        else:
            if not any(len(list(g)) == 2 for k, g in groupby(digits)): continue

        c += 1
    return c


def solve(lines):
    min_val, max_val = map(int, lines[0].strip().split('-'))

    part1 = count_passwords(min_val, max_val)
    part2 = count_passwords(min_val, max_val, part2=True)

    return part1, part2


debug = True
# solve_puzzle(year=2019, day=4, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2019, day=4, solver=solve, do_sample=False, do_main=True, main_data_path='input')
