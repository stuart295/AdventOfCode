from utils.common import solve_puzzle, grid_offsets, in_bounds

YEAR = 2024
DAY = 4


def solve_part_01(lines):
    count = 0
    target = "XMAS"

    w, h = len(lines[0]), len(lines)

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'X':
                for xo, yo in grid_offsets(diagonals=True):

                    found = True
                    for step in range(1, 4):
                        cx, cy = x + xo * step, y + yo * step
                        if not in_bounds((cx, cy), w, h):
                            found = False
                            break

                        if lines[cy][cx] != target[step]:
                            found = False
                            break

                    if found:
                        count += 1
    return count


def solve_part_02(lines):
    count = 0
    allowed = {"SAM", "MAS"}

    for y, line in enumerate(lines[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c == 'A':
                hor1 = lines[y][x] + "A" + lines[y + 2][x + 2]
                hor2 = lines[y][x + 2] + "A" + lines[y + 2][x]

                if hor1 in allowed and hor2 in allowed:
                    count += 1

    return count


def solve(lines):
    inp = [list(s) for s in lines]

    part1 = solve_part_01(inp)
    part2 = solve_part_02(inp)

    return part1, part2


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, sample_data_path="example.txt")
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
