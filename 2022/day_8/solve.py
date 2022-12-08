from utils.common import solve_puzzle


def solve_part1(grid):
    visible = 0
    for i in range(len(grid)):
        if i in [0, len(grid) - 1]:
            visible += len(grid[i])
            continue

        for j in range(len(grid[i])):
            if j in [0, len(grid[i]) - 1]:
                visible += 1
                continue

            height = grid[i][j]

            found = False
            for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                i_, j_ = i, j
                while True:
                    i_ += offset[0]
                    j_ += offset[1]
                    if i_ < 0 or i_ >= len(grid):
                        visible += 1
                        found = True
                        break

                    if j_ < 0 or j_ >= len(grid[i_]):
                        visible += 1
                        found = True
                        break

                    if grid[i_][j_] >= height:
                        break

                if found:
                    break

    return visible


def solve_part2(grid):
    best_score = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            height = grid[i][j]
            cur_score = 0

            scores = []
            for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                i_, j_ = i, j
                dir_score = 0
                while True:
                    i_ += offset[0]
                    j_ += offset[1]
                    if i_ < 0 or i_ >= len(grid):
                        break

                    if j_ < 0 or j_ >= len(grid[i_]):
                        break

                    dir_score += 1
                    if grid[i_][j_] >= height:
                        break


                scores.append(dir_score)
            cur_score = scores[0] * scores[1] * scores[2] * scores[3]
            best_score = max(best_score, cur_score)

    return best_score


def solve(lines):

    grid = []
    for line in lines:
        grid.append([int(x) for x in list(line.strip())])

    part1 = solve_part1(grid)

    part2 = solve_part2(grid)

    return part1, part2


debug = False
solve_puzzle(year=2022, day=8, solver=solve, do_sample=True, do_main=not debug)
