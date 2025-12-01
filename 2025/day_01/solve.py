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

        if dist > 0:
            remaining_distance = dist
            if pos != 0:
                if direction == 'L':
                    remaining_distance = dist - pos
                elif direction == 'R':
                    remaining_distance = dist - (100 - pos)

                if remaining_distance >= 0:
                    part2 += 1

            if remaining_distance > 0:
                part2 += remaining_distance // 100


        pos = (pos + dir_const * dist) % 100
        if pos == 0:
            part1 += 1

    return part1, part2


with open("test.txt", 'r') as f:
    test_lines = f.readlines()

with open("input.txt", 'r') as f:
    lines = f.readlines()

p1, p2 = solve(test_lines)
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")

p1, p2 = solve(lines)

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")


# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
