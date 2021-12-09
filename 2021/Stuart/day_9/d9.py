import math


def iterate_adjacent(row, col, width, height):
    for i in range(4):
        other_row = row + int(math.sin(i * math.pi / 2.0))
        other_col = col + int(math.cos(i * math.pi / 2.0))

        if not other_row in range(width) or other_col not in range(height):
            continue

        yield (other_row, other_col)


def is_low_point(inputs, row, col):
    cur_h = inputs[row][col]
    for other_row, other_col in iterate_adjacent(row, col, len(inputs), len(inputs[0])):
        other_h = inputs[other_row][other_col]
        if other_h <= cur_h:
            return False
    return True


def find_low_points(inputs):
    total_risk = 0
    low_points = []
    for i in range(len(inputs)):
        for j in range(len(inputs[0])):
            if is_low_point(inputs, i, j):
                total_risk += inputs[i][j] + 1
                low_points.append((i, j))

    return total_risk, low_points


def calc_basin_size(inputs, low_point):
    visited = set()
    to_visit = [low_point]

    while len(to_visit) > 0:
        cur_point = to_visit.pop()
        visited.add(cur_point)

        for adj_row, adj_col in iterate_adjacent(cur_point[0], cur_point[1], len(inputs), len(inputs[0])):
            if (adj_row, adj_col) in visited or inputs[adj_row][adj_col] >= 9:
                continue

            to_visit.append((adj_row, adj_col))

    return len(visited)


def find_risky_basins(inputs, low_points):
    basins = []

    for low_point in low_points:
        basins.append(calc_basin_size(inputs, low_point))

    largest = sorted(basins, reverse=True)[:3]
    return largest[0] * largest[1] * largest[2]


with open('./input.txt') as f:
    inputs = f.readlines()
    inputs = [list(map(int, list(x.strip()))) for x in inputs]
    risk, low_points = find_low_points(inputs)
    print(risk)
    print(find_risky_basins(inputs, low_points))
