from functools import lru_cache

from utils.common import solve_puzzle
import numpy as np

rock_types = [
    np.array([[0, 0], [1, 0], [2, 0], [3, 0]]),
    np.array([[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]]),
    np.array([[2, 0], [2, 1], [2, 2], [0, 0], [1, 0]]),
    np.array([[0, 0], [0, 1], [0, 2], [0, 3]]),
    np.array([[0, 0], [1, 0], [0, 1], [1, 1]]),
]

rock_widths = [
    4,
    3,
    3,
    1,
    2
]

wind_dirs = {
    '<': np.array([-1, 0]),
    '>': np.array([1, 0]),
}


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


@lru_cache
def play_game(wind, start_wind_idx, start_rock_idx, max_steps, chamber_width, start_rocks, h_thresh):
    rocks = set(start_rocks)

    rock_idx = start_rock_idx
    wind_idx = start_wind_idx

    # highest = max(x[1]+1 for x in rocks) if len(rocks) > 0 else 0

    max_heights = [-1 for _ in range(chamber_width)]
    for r in rocks:
        max_heights[r[0]] = max(max_heights[r[0]], r[1])

    h_off = max(0, max(max_heights))

    for step in range(max_steps):
        cur_rock = rock_types[rock_idx]
        rwidth = rock_widths[rock_idx]
        rock_idx = (rock_idx + 1) % len(rock_types)

        pos = np.array([2, max(max_heights) + 1])
        if step == 0: draw(rocks, cur_rock, pos, max(max_heights) + 1, chamber_width)

        for i in range(3):
            pos += wind_dirs[wind[wind_idx]]
            pos[0] = np.clip(pos[0], 0, chamber_width - rwidth)
            wind_idx = (wind_idx + 1) % len(wind)

        while True:
            # Horizontal movements
            dir = wind_dirs[wind[wind_idx]]
            wind_idx = (wind_idx + 1) % len(wind)

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

            # debug = True
            if debug: draw(rocks, cur_rock, pos, max(max_heights) + 1, chamber_width)

            if collides:
                for p in cur_rock:
                    pp = pos + p
                    px, py = pp
                    # highest = max(highest, pp[1] + 1)
                    rocks.add(tuple(pp))

                    max_heights[px] = max(max_heights[px], py)

                thresh = 4
                min_h, max_h = min(max_heights), max(max_heights)

                if max_h > h_thresh and max_h - min_h < thresh:
                # if max_h > h_thresh and max_h == min_h:
                    # draw(rocks, cur_rock, pos, max_h + 1, chamber_width)
                    rem_rocks = []
                    for x in range(chamber_width):
                        for y in range(min_h, max_h + 1):
                            if (x, y) in rocks:
                                rem_rocks.append((x, y - min_h))

                    rem_rocks = sorted(rem_rocks, key=lambda x: x[0] * 1000 + x[1])

                    return max_h + 1 - h_off, wind_idx, rock_idx, step, rem_rocks
                break

            pos = new_pos

    min_h, max_h = min(max_heights), max(max_heights)

    rem_rocks = []
    for x in range(chamber_width):
        for y in range(min_h, max_h + 1):
            if (x, y) in rocks:
                rem_rocks.append((x, y - min_h))

    rem_rocks = sorted(rem_rocks, key=lambda x: x[0] * 1000 + x[1])

    return max_h + 1 - h_off, wind_idx, rock_idx, max_steps, rem_rocks


def simulate(wind, steps=2022, chamber_width=7):
    rock_idx = 0
    wind_idx = 0

    highest = 0

    rem_steps = steps
    wind_tup = tuple(wind)

    start_rocks = []

    while rem_steps > 0:
        print(f"Remaining steps: {rem_steps}")

        max_steps = 2000000
        h_thresh = 100000

        if rem_steps < max_steps:
            max_steps = 100000
            h_thresh = 1000

        if rem_steps < max_steps:
            max_steps = 10000
            h_thresh = 100

        if rem_steps < max_steps:
            max_steps = rem_steps
            h_thresh = 100

        # max_steps = rem_steps
        # h_thresh = 1000

        h, wind_idx, rock_idx, s, start_rocks = play_game(wind_tup, wind_idx, rock_idx, max_steps,
                                                          chamber_width, tuple(start_rocks), h_thresh)

        highest += h
        rem_steps -= s

    return highest


def solve(lines):
    wind = list(lines[0].strip())

    highest = simulate(wind)

    part1 = highest

    highest = simulate(wind, steps=1000000000000)
    part2 = highest
    # part2 = None
    return part1, part2


debug = False
solve_puzzle(year=2022, day=17, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
# solve_puzzle(year=2022, day=17, solver=solve, do_sample=False, do_main=True)
