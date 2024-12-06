from utils.common import solve_puzzle, in_bounds

YEAR = 2024
DAY = 6

DIR_MAP = {
    ">": 0,
    "v": 1,
    "<": 2,
    "^": 3,
}

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_input(lines):
    guard = (0, 0)
    guard_dir = 0
    obst = set()
    for y, line in enumerate(lines):
        for x, l in enumerate(list(line)):
            if l == "#":
                obst.add((x, y))
            elif l in DIR_MAP:
                guard = (x, y)
                guard_dir = DIR_MAP[l]

    w, h = len(lines[0]), len(lines)
    return w, h, guard, guard_dir, obst


def solve(lines):
    inputs = parse_input(lines)

    part1 = solve_part_01(*inputs)
    part2 = solve_part_02(*inputs)

    return len(part1), part2


def solve_part_01(w, h, guard, guard_dir, obst_set):
    uni_pos = {guard}

    guard_posts = set()

    gx, gy = guard

    while True:
        dx, dy = DIRS[guard_dir]
        nx, ny = gx + dx, gy + dy
        if (nx, ny) in obst_set:
            guard_dir = (guard_dir + 1) % 4
        elif not in_bounds((nx, ny), w, h):
            return uni_pos
        else:
            gx, gy = nx, ny
            uni_pos.add((gx, gy))

            post = (gx, gy, guard_dir)
            if post in guard_posts:
                return None
            guard_posts.add(post)


def solve_part_02(w, h, guard, guard_dir, obst_set):
    # Sometimes brute forcing is just faster... # TODO solve properly
    cnts = 0

    route = solve_part_01(w, h, guard, guard_dir, obst_set)

    for x, y in route:
        if (x, y) == guard:
            continue

        new_set = set(obst_set)
        new_set.add((x, y))

        if not solve_part_01(w, h, guard, guard_dir, new_set):
            cnts += 1

    return cnts


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
