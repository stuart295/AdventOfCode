from utils.common import solve_puzzle
import numpy as np

rock_types = [
    np.array([[0, 0], [1, 0], [2, 0], [3, 0]]),
    np.array([[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]]),
    np.array([[2, 0], [2, 1], [2, 2], [0, 0], [1, 0]]),
    np.array([[0, 0], [0, 1], [0, 2], [0, 3]]),
    np.array([[0, 0], [1, 0], [0, 1], [1, 1]]),
]


def draw(rocks, cur_r, pos, height, width):
    print('=' * 20)

    for h in range(height + 5, -1, -1):
        line = ''
        for x in range(width):
            if (x, h) in rocks:
                line += '#'
            elif (x, h) in {tuple(p + pos) for p in cur_r}:
                line += '@'
            else:
                line += '.'

        print(line)


def simulate(wind, steps=2022, chamber_width=7):
    rocks = set()

    rock_idx = 0
    wind_idx = 0

    highest = 0

    for step in range(steps):
        cur_rock = rock_types[rock_idx]
        pos = np.array([2, highest + 3])


        while True:
            cur_w = wind[wind_idx]
            wind_idx = (wind_idx + 1) % len(wind)

            # Horizontal movements
            dir = np.array([-1, 0]) if cur_w == '<' else np.array([1, 0])

            new_pos = pos + dir

            collides = False

            for piece in cur_rock:
                pp = piece + new_pos
                if pp[0] < 0 or pp[0] >= chamber_width or tuple(pp) in rocks:
                    collides = True
                    break

            if not collides:
                pos = new_pos



            # Vertical
            collides = False

            new_pos = pos + np.array([0, -1])
            for piece in cur_rock:
                pp = piece + new_pos
                if pp[1] < 0 or tuple(pp) in rocks:
                    collides = True
                    break

            if debug: draw(rocks, cur_rock, pos, highest, chamber_width)

            if collides:
                for p in cur_rock:
                    highest = max(highest, (pos + p)[1] +1 )
                    rocks.add(tuple(pos + p))
                break
            pos = new_pos




        rock_idx = (rock_idx + 1) % len(rock_types)

    return rocks, highest


def solve(lines):
    wind = list(lines[0].strip())

    rocks, highest = simulate(wind)

    part1 = highest

    rocks, highest = simulate(wind, steps=1000000000000)
    part2 = highest

    return part1, part2


debug = False
solve_puzzle(year=2022, day=17, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
# solve_puzzle(year=2022, day=17, solver=solve, do_sample=False, do_main=True)
