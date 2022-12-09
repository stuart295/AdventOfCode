from utils.common import solve_puzzle, DIR_MAP
import numpy as np


def move_tail(H, T):
    if abs(H[0] - T[0]) > 1 or abs(H[1] - T[1]) > 1:
        step = np.array((0, 0))
        step[0] = max(-1, min(1, H[0] - T[0]))
        step[1] = max(-1, min(1, H[1] - T[1]))
        return T + step
    return T


def move_rope(data, rope_length=2):
    knots = [np.array((0, 0)) for _ in range(rope_length)]

    tail_positions = set()
    tail_positions.add(tuple(knots[-1]))

    for direct, dist in data:
        offset = DIR_MAP[direct]
        for step in range(dist):
            knots[0] += offset
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i - 1], knots[i])
            tail_positions.add(tuple(knots[-1]))

    return len(tail_positions)


def solve(lines):
    data = [x.strip().split(' ') for x in lines]
    data = [(x, int(y)) for x, y in data]

    part1 = move_rope(data, 2)
    part2 = move_rope(data, 10)

    return part1, part2


debug = True
# solve_puzzle(year=2022, day=9, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=9, solver=solve, do_sample=True, do_main=False, sample_data_path='sample2')
solve_puzzle(year=2022, day=9, solver=solve, do_sample=False, do_main=True)  # Submit
