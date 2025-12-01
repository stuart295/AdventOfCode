from utils.common import solve_puzzle

YEAR = 2025
DAY = 1

def solve(lines):
    pos = 50
    part1 = 0
    part2 = 0
    for line in lines:
        direction, dist = line[0], int(line[1:])
        dir_const = 1
        if direction == 'L':
            dir_const = -1

        # Part 2
        remaining_distance = dist

        # Move towards origin
        if pos != 0:
            if direction == 'L':
                remaining_distance = dist - pos
            elif direction == 'R':
                remaining_distance = dist - (100 - pos)

            if remaining_distance >= 0:
                part2 += 1

        # Calculate additional loops
        if remaining_distance > 0:
            part2 += remaining_distance // 100

        # Part 1
        pos = (pos + dir_const * dist) % 100
        if pos == 0:
            part1 += 1

    return part1, part2


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
