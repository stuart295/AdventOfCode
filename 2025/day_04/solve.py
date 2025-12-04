from utils.common import solve_puzzle
import numpy as np
import cv2 as cv

YEAR = 2025
DAY = 4

def solve(lines):
    grid = np.array([[1 if c == '@' else 0 for c in line] for line in lines], dtype=np.uint8)

    # Part 1
    _, part1 = solve_part_01(grid)

    # Part 2
    part2 = 0
    while True:
        accessible, total = solve_part_01(grid)
        if total == 0:
            break

        part2 += total
        grid[accessible] = 0

    return part1, part2


def solve_part_01(grid):
    kernel = np.ones([3, 3], dtype=np.uint8)
    kernel[1, 1] = 0
    result = cv.filter2D(src=grid, ddepth=-1, kernel=kernel, borderType=cv.BORDER_CONSTANT)

    accessible = (result < 4) & (grid == 1)
    total = np.sum(accessible)
    return accessible, total


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
