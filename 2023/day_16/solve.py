from utils.common import solve_puzzle

YEAR = 2023
DAY = 16


def solve_part_01(grid, start_pos=(0, 0), start_dir=(1, 0)):
    w, h = len(grid[0]), len(grid)
    beams = [[start_pos, start_dir]]
    energised, seen = set(), set()

    while beams:
        (x, y), (xd, yd) = beams.pop(0)

        if ((x, y), (xd, yd)) in seen:
            continue

        seen.add(((x, y), (xd, yd)))

        if not (0 <= x < w) or not (0 <= y < h):
            continue

        energised.add((x, y))

        cn = grid[y][x]

        if cn == ".":
            beams.append([(x + xd, y + yd), (xd, yd)])
        elif cn == "\\":
            if xd == 1:
                beams.append([(x, y + 1), (0, 1)])
            elif xd == -1:
                beams.append([(x, y - 1), (0, -1)])
            elif yd == 1:
                beams.append([(x + 1, y), (1, 0)])
            else:
                beams.append([(x - 1, y), (-1, 0)])
        elif cn == "/":
            if xd == 1:
                beams.append([(x, y - 1), (0, -1)])
            elif xd == -1:
                beams.append([(x, y + 1), (0, 1)])
            elif yd == 1:
                beams.append([(x - 1, y), (-1, 0)])
            else:
                beams.append([(x + 1, y), (1, 0)])
        elif cn == "|":
            if abs(xd) != 0:
                beams.append([(x, y + 1), (0, 1)])
                beams.append([(x, y - 1), (0, -1)])
            else:
                beams.append([(x + xd, y + yd), (xd, yd)])
        elif cn == "-":
            if abs(yd) != 0:
                beams.append([(x + 1, y), (1, 0)])
                beams.append([(x - 1, y), (-1, 0)])
            else:
                beams.append([(x + xd, y + yd), (xd, yd)])

    return len(energised)


def solve_part_02(grid):
    best = 0
    w, h = len(grid[0]), len(grid)

    for x in range(w):
        best = max(best, solve_part_01(grid, (x, 0), (0, 1)))
        best = max(best, solve_part_01(grid, (x, h - 1), (0, -1)))

    for y in range(h):
        best = max(best, solve_part_01(grid, (0, y), (1, 0)))
        best = max(best, solve_part_01(grid, (w - 1, y), (-1, 0)))

    return best


def solve(lines):
    grid = [list(l) for l in lines]

    part1 = solve_part_01(grid)
    part2 = solve_part_02(grid)

    return part1, part2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
