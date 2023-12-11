from utils.common import solve_puzzle

YEAR = 2023
DAY = 11


def expand_space(galaxies, exp_rate):
    padding = exp_rate - 1

    expanded = set(galaxies)

    galaxy_rows = {y for x, y in galaxies}
    galaxy_cols = {x for x, y in galaxies}

    max_w = max(galaxy_cols)
    max_h = max(galaxy_rows)

    # expand vert
    cur_y = 0

    while cur_y < max_h:
        if cur_y not in galaxy_rows:
            expanded = {(x, y + padding) if y > cur_y else (x, y) for x, y in expanded}
            galaxy_rows = {y + padding if y > cur_y else y for y in galaxy_rows}
            max_h += padding
            cur_y += padding + 1
        else:
            cur_y += 1

    # Expand hor
    cur_x = 0

    while cur_x < max_w:
        if cur_x not in galaxy_cols:
            expanded = {(x + padding, y) if x > cur_x else (x, y) for x, y in expanded}
            galaxy_cols = {x + padding if x > cur_x else x for x in galaxy_cols}
            max_w += padding
            cur_x += padding + 1
        else:
            cur_x += 1

    return expanded


def find_paths(galaxies):
    seen_pairs = {(g, g) for g in galaxies}

    lengths = []

    for (x, y) in galaxies:
        for x2, y2 in galaxies:
            if ((x, y), (x2, y2)) in seen_pairs or ((x2, y2), (x, y)) in seen_pairs:
                continue
            lengths.append(abs(x - x2) + abs(y - y2))
            seen_pairs.add(((x, y), (x2, y2)))

    return lengths


def solve_part_01(galaxies, exp_rate=1):
    expanded = expand_space(galaxies, exp_rate)
    lengths = find_paths(expanded)
    return sum(lengths)


def parse_inputs(lines):
    galaxies = set()

    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c == "#":
                galaxies.add((x, y))

    return galaxies


def solve(lines):
    galaxies = parse_inputs(lines)

    part1 = solve_part_01(galaxies)
    part2 = solve_part_01(galaxies, 1000000)

    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
