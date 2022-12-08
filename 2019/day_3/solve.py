from utils.common import solve_puzzle
import numpy as np


def add_wire(w, dirs, positions, intersects):
    cur_pt = np.array((0,0))

    new_positions = dict()

    steps = 0
    for instr in w:
        direct, dist = instr[0], int(instr[1:])
        offset = dirs[direct]
        for i in range(dist):
            steps += 1
            cur_pt += offset
            t = tuple(cur_pt)
            if t in positions:
                intersects.add(t)
            new_positions[t] = new_positions.get(t) or steps
    return new_positions


def solve(lines):
    w1 = lines[0].strip().split(',')
    w2 = lines[1].strip().split(',')


    dirs = {
        'R' : np.array((1, 0)),
        'L' : np.array((-1, 0)),
        'U' : np.array((0, 1)),
        'D' : np.array((0, -1)),
    }

    intersects = set()

    positions_1 = add_wire(w1,  dirs, set(), intersects)
    positions_2 = add_wire(w2,  dirs, positions_1, intersects)

    closest = 1e9
    min_steps = 1e9

    for x, y in intersects:
        dist = abs(x) + abs(y)
        closest = min(closest, dist)

        min_steps = min(min_steps, positions_1[(x,y)] + positions_2[(x,y)])

    part1 = closest

    part2 = min_steps


    return part1, part2


debug = True

solve_puzzle(year=2019, day=3, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2019, day=3, solver=solve, do_sample=False, do_main=True,  main_data_path='input')
