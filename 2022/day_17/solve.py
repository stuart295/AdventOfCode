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


def draw(rocks, cur_r, pos, height, width, filename=None):
    print('=' * 20)

    f = None
    if filename:
        f = open(filename, 'w')

    for h in range(height + 5, -1, -1):
        line = ''
        for x in range(width):
            if (x, h) in rocks:
                line += '#'
            elif (x, h) in {tuple(p + pos) for p in cur_r}:
                line += '@'
            else:
                line += '.'

        if f:
            f.write(line + '\n')
        else:
            print(line)

    if f:
        f.close()


cache = {}


def play_game(wind, start_wind_idx, start_rock_idx, max_steps, chamber_width, start_rocks, h_thresh):
    key = (wind, start_wind_idx, start_rock_idx, chamber_width, start_rocks, max_steps)
    if key in cache:
        return cache[key]

    rocks = set(start_rocks)

    rock_idx = start_rock_idx
    wind_idx = start_wind_idx

    max_heights = [0 for _ in range(chamber_width)]

    if rocks:
        for rx, ry in rocks:
            max_heights[rx] = max(max_heights[rx], ry + 1)

    for step in range(max_steps):
        cur_rock = rock_types[rock_idx]
        rock_idx = (rock_idx + 1) % len(rock_types)

        pos = np.array([2, max(max_heights) + 3])

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
            if debug: draw(rocks, cur_rock, pos, max(max_heights), chamber_width)

            if collides:
                for p in cur_rock:
                    pp = pos + p
                    px, py = pp
                    rocks.add(tuple(pp))

                    max_heights[px] = max(max_heights[px], py + 1)

                # Epoch check
                min_h, max_h = min(max_heights), max(max_heights)

                min_p = min(y for x, y in cur_rock + pos)
                max_p = max(y for x, y in cur_rock + pos)

                can_break = False
                for ty in range(min_p - 1, max_p + 1):
                    filled = [False for _ in range(chamber_width)]

                    for x in range(chamber_width):
                        if (x, ty) in rocks or (x, ty + 1) in rocks:
                            filled[x] = True

                    if all(filled):
                        can_break = True
                        break

                if max_h > h_thresh and can_break:
                    # draw(rocks, cur_rock, pos, max(max_heights) + 1, chamber_width, filename=str(step))
                    rem_rocks = []
                    for x in range(chamber_width):
                        for y in range(min_p - 1, max_h):
                            if (x, y) in rocks:
                                rem_rocks.append((x, y - (min_p - 1)))

                    rem_rocks = sorted(rem_rocks, key=lambda x: x[0] * 1000 + x[1])

                    h_off = max(y for x, y in rem_rocks) + 1
                    out = max_h - h_off, wind_idx, rock_idx, step, rem_rocks
                    cache[key] = out
                    return out
                break

            pos = new_pos

    # draw(rocks, [], [], max(max_heights) + 1, chamber_width, filename=str(max_steps))
    return max(max_heights), wind_idx, rock_idx, max_steps, []


def simulate(wind, steps=2022, chamber_width=7):
    rock_idx = 0
    wind_idx = 0

    highest = 0

    rem_steps = steps
    wind_tup = tuple(wind)

    start_rocks = []

    while rem_steps > 0:
        print(f"Remaining steps: {rem_steps}")

        h_thresh = 500000

        max_steps = 5000000
        if rem_steps < max_steps:
            max_steps = min(rem_steps, 10000)
            h_thresh = 1000

        h, wind_idx, rock_idx, s, start_rocks = play_game(wind_tup, wind_idx, rock_idx, max_steps,
                                                          chamber_width, tuple(start_rocks), h_thresh)

        highest += h
        rem_steps -= s + 1

    return highest


def solve(lines):
    wind = list(lines[0].strip())

    highest = simulate(wind)

    part1 = highest

    highest = simulate(wind, steps=1000000000000)
    part2 = highest
    return part1, part2


debug = False
# solve_puzzle(year=2022, day=17, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=17, solver=solve, do_sample=False, do_main=True)
