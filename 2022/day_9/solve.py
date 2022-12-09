from utils.common import solve_puzzle, grid_offsets
import numpy as np
from numpy.linalg import norm

dirs = {
    'R': np.array((1, 0)),
    'L': np.array((-1, 0)),
    'U': np.array((0, 1)),
    'D': np.array((0, -1)),
}


def move_tail(H, T):
    offset = H - T

    if abs(H[0] - T[0]) > 1 or abs(H[1] - T[1]) > 1:
        if H[0] == T[0] or H[1] == T[1]:
            dist = norm(offset)
            return T + offset / dist
        else:
            step = np.array((0, 0))
            step[0] = max(-1, min(1, H[0] - T[0]))
            step[1] = max(-1, min(1, H[1] - T[1]))
            return T + step
    return T


def solve_part1(data, visited):
    H, T = np.array((0, 0)), np.array((0, 0))

    head_positions = set()
    tail_positions = set()

    head_positions.add(tuple(H))
    tail_positions.add(tuple(T))

    for direct, dist in data:
        offset = dirs[direct]
        for step in range(dist):
            H += offset
            T = move_tail(H, T)
            tail_positions.add(tuple(T))

    return len(tail_positions)

def solve_part2(data, visited):
    knots = [np.array((0, 0)) for _ in range(10)]

    tail_positions = set()

    tail_positions.add(tuple(knots[-1]))

    for direct, dist in data:
        offset = dirs[direct]
        for step in range(dist):
            knots[0] += offset
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i-1], knots[i])
            tail_positions.add(tuple(knots[-1]))

    return len(tail_positions)


def solve(lines):
    data = [(x.strip().split(' ')[0], int(x.strip().split(' ')[1])) for x in lines]

    visited = set()

    part1 = solve_part1(data, visited)

    part2 = solve_part2(data, visited)

    return part1, part2


debug = True
# solve_puzzle(year=2022, day=9, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=9, solver=solve, do_sample=True, do_main=False, sample_data_path='sample2')
solve_puzzle(year=2022, day=9, solver=solve, do_sample=False, do_main=True) # Submit

# -------Sample-------
# Part 1: 88
# Part 2: 36
# -----Main input-----
# Part 1: 6470
# Part 2: 2658