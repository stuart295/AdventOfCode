from utils.common import solve_puzzle
import numpy as np

YEAR = 2023
DAY = 18

dir_vecs = {
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, -1]),
    "D": np.array([0, 1]),
}


def find_intersections(scan_line, edges):
    intersections = []
    for i, edge in enumerate(edges):
        (sx1, sy), (sx2, _) = scan_line
        (ox1, oy1), (ox2, oy2) = edge

        # Other line is vertical
        if ox1 == ox2:
            if min(oy1, oy2) <= sy <= max(oy1, oy2):
                if (ox1, sy) == (ox1, oy1) or (ox1, sy) == (ox1, oy2):
                    continue

                intersections.append(edge)
        elif oy1 == sy:
            intersections.append(edge)

    return intersections


def get_dir(edge):
    d = np.array(edge[1]) - np.array(edge[0])
    return d / np.linalg.norm(d)


def fill_holes(edges, maxx, maxy, minx, miny):
    result = 0
    global ax

    vertex_ys = {pt[1] for edge in edges for pt in edge}
    # vertex_ys = list(sorted(vertex_ys))

    prev_width = None

    for y in range(miny, maxy + 1):

        if y not in vertex_ys and prev_width is not None:
            result += prev_width
            continue

        prev_width = 0

        scan_line = ((minx, y), (maxx, y))

        intersects = find_intersections(scan_line, edges)
        intersects = list(sorted(intersects, key=lambda x: min(x[0][0], x[1][0])))

        leading = None
        for (ox1, y1), (ox2, y2) in intersects:
            edge_idx = edges.index(((ox1, y1), (ox2, y2)))
            prev_edge = edges[edge_idx - 1] if edge_idx > 0 else edges[-1]
            next_edge = edges[(edge_idx + 1) % len(edges)]

            x1 = min(ox1, ox2)
            x2 = max(ox1, ox2)

            # Horizontal edge
            if y1 == y2:
                dir1 = get_dir(prev_edge)
                dir2 = get_dir(next_edge)
                if not np.array_equal(dir1, dir2):
                    if leading is not None:
                        continue
                    prev_width += x2 + 1 - x1
                    continue
                else:
                    if leading is not None:
                        prev_width += x2 + 1 - leading

                        leading = None
                        continue
                    else:
                        leading = x1
                        continue
            # Vertical line
            elif leading is not None:
                prev_width += x1 + 1 - leading
                leading = None
                continue
            else:
                leading = x1
                continue

        result += prev_width
        if y in vertex_ys:
            prev_width = None

    return result


def solve_part_01(inputs):
    cur_pos = np.array([0, 0])
    edges = []

    maxx, minx = 0, 0
    maxy, miny = 0, 0

    for direction, dist, col in inputs:
        next_pos = cur_pos + dir_vecs[direction] * dist
        maxx, maxy = max(maxx, next_pos[0]), max(maxy, next_pos[1])
        minx, miny = min(minx, next_pos[0]), min(miny, next_pos[1])

        edges.append((tuple(map(int, cur_pos)), tuple(map(int, next_pos))))
        cur_pos = next_pos

    # Fill holes
    return fill_holes(edges, maxx, maxy, minx, miny)


def decode_hex(hex_vals):
    new_inputs = []

    dir_mappings = "RDLU"

    for h in hex_vals:
        direct = int(h[5])
        direct = dir_mappings[direct]
        dist = h[:5]
        dist = int(dist, 16)
        new_inputs.append((direct, dist, None))

    return new_inputs


def solve(lines):
    split = [l.split(" ") for l in lines]
    inputs = [(direction, int(dist), color[2:-1]) for direction, dist, color in split]

    part1 = solve_part_01(inputs)

    new_inputs = decode_hex([x[2] for x in inputs])
    part2 = solve_part_01(new_inputs)

    return part1, part2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
