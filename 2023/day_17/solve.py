from utils.common import solve_puzzle, grid_offsets

YEAR = 2023
DAY = 17


def heuristic(x, end, factor=0.1):
    (x, y), cur_cost, prev_pos, s_count = x
    xe, ye = end

    dist_cost = (xe - x) + (ye - y)
    heat_cost = cur_cost / 9.0

    return dist_cost + factor * heat_cost


def in_bounds(x, y, w, h):
    return (0 <= x < w) and (0 <= y < h)


def solve_part_01(grid, part_2=False):
    w, h = len(grid[0]), len(grid)
    start = (0, 0)
    end = (w - 1, h - 1)
    stack = [(start, 0, (-1, -1), 0)]

    best_cost = 1e9
    seen = {}

    while stack:
        (x, y), cur_cost, prev_pos, s_count = stack.pop()
        key = ((x, y), prev_pos, s_count)

        if key in seen:
            if seen[key] <= cur_cost:
                continue
        seen[key] = cur_cost

        neihbours = []

        for xo, yo in grid_offsets():
            xn, yn = x + xo, y + yo
            xs, ys = x, y

            if (xn, yn) == prev_pos:
                continue

            if not in_bounds(xn, yn, w, h):
                continue

            next_cost = cur_cost + grid[yn][xn]

            s_count_cur = s_count + 1
            if xn != prev_pos[0] and yn != prev_pos[1]:
                if part_2:
                    s_count_cur = 0
                    xdir, ydir = (xn - xs), (yn - ys)
                    possible = True
                    for _ in range(3):
                        xn += xdir
                        yn += ydir
                        if not in_bounds(xn, yn, w, h):
                            possible = False
                            break
                        next_cost += grid[yn][xn]
                        s_count_cur += 1

                    if not possible:
                        continue
                    xs = xn - xdir
                    ys = yn - ydir

                else:
                    s_count_cur = 0

            if part_2:
                if s_count_cur >= 10:
                    continue
            elif s_count_cur >= 3:
                continue

            rem_dist = get_rem_dist(end, (xn, yn))

            if next_cost + rem_dist >= best_cost:
                continue

            if (xn, yn) == end:
                best_cost = min(best_cost, next_cost)
                print(f"Found end. New best cost: {best_cost}. Remaining stack: {len(stack)}")
                found_path = True
                continue

            neihbours.append(((xn, yn), next_cost, (xs, ys), s_count_cur))

        neihbours.sort(key=lambda x: heuristic(x, end, 0.1), reverse=True)
        stack += neihbours

    return best_cost


def get_rem_dist(end, x):
    rem_dist = (end[0] - x[0]) + (end[1] - x[1])
    return rem_dist


def solve(lines):
    grid = [[int(c) for c in l] for l in lines]

    part1 = None  # solve_part_01(grid)
    part2 = solve_part_01(grid, True)

    return part1, part2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
