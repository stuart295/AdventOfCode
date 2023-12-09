from utils.common import solve_puzzle

YEAR = 2023
DAY = 9


def find_diffs(inp):
    cur_seq = list(inp)
    sequences = [cur_seq]

    while not all(x == 0 for x in cur_seq):
        cur_seq = [b - a for a, b in zip(cur_seq, cur_seq[1:])]
        sequences.append(cur_seq)

    return sequences


def extrapolate(sequences):
    val = 0

    for seq in sequences[::-1]:
        val += seq[-1]
    return val


def extrapolate_back(sequences):
    val = 0

    for seq in sequences[::-1]:
        val = seq[0] - val
    return val


def solve_part_01(inputs):
    total = 0

    for inp in inputs:
        sequences = find_diffs(inp)
        total += extrapolate(sequences)

    return total


def solve_part_02(inputs):
    total = 0

    for inp in inputs:
        sequences = find_diffs(inp)
        total += extrapolate_back(sequences)

    return total


def solve(lines):
    inputs = [[int(x) for x in line.split(" ")] for line in lines]
    part1 = solve_part_01(inputs)
    part2 = solve_part_02(inputs)

    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
