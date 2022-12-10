from utils.common import solve_puzzle
import numpy as np
from more_itertools import chunked


def execute(data):
    X = 1
    cycle = 1
    all_x = []

    for line in data:
        if line.startswith('noop'):
            cycle += 1
            all_x.append(X)
            continue

        if line.startswith('addx'):
            cycle += 2
            for i in range(2):
                all_x.append(X)

            X += int(line.strip().split(' ')[1])

    return all_x


def solve(lines):
    X = execute(lines)

    part1 = 0
    for i in [20, 60, 100, 140, 180, 220]:
        if debug: print(f"{i}: {X[i + 1] * i}")
        part1 += X[i+1] * i

    w, h = 40, 6
    out = np.zeros((h, w))
    spos = np.array((1, 0))

    line = ''

    for i, s in enumerate(X):
        x, y = i % w, i // w
        sx, sy = s % w, s // w

        # x = i
        # sx = s

        if abs(x-sx) <= 1:
            line += '#'
        else:
            line += '.'

    lines = [''.join(x) for x in chunked(line, w) ]
    print('\n'.join(lines))

    part2 = None

    return part1, part2


debug = False
solve_puzzle(year=2022, day=10, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=10, solver=solve, do_sample=False, do_main=True, submit=False)
