import numpy as np

from utils.common import solve_puzzle, grid_offsets


def grid_offsets_3d():
    for xoff, yoff in grid_offsets():
        yield xoff, yoff, 0

    yield 0, 0, 1
    yield 0, 0, -1


def is_inside(pos, cubes, air_pockets):
    mins = np.min(np.array([np.array(x) for x in cubes]), axis=0)
    maxs = np.max(np.array([np.array(x) for x in cubes]), axis=0)

    to_check = [pos]

    checked = set()

    while to_check:
        cur = to_check.pop()
        x, y, z = cur

        checked.add(cur)

        for ox, oy, oz in grid_offsets_3d():
            nx, ny, nz = x + ox, y + oy, z + oz
            if (nx, ny, nz) in checked: continue
            if (nx, ny, nz) in air_pockets: return True, checked | air_pockets
            if (nx, ny, nz) in cubes: continue

            if nx < mins[0] or nx > maxs[0]: return False, air_pockets
            if ny < mins[1] or ny > maxs[1]: return False, air_pockets
            if nz < mins[2] or nz > maxs[2]: return False, air_pockets

            to_check.append((nx, ny, nz))

    return True, checked | air_pockets


def solve(lines):
    cubes = [line.strip().split(',') for line in lines]

    cubes = {(int(x), int(y), int(z)) for x, y, z in cubes}

    surface = 0
    outside_surface = 0
    inside_pockets = set()

    for x, y, z in cubes:
        for xoff, yoff, zoff in grid_offsets_3d():
            space = (x + xoff, y + yoff, z + zoff)

            if space not in cubes:
                surface += 1

                ins, inside_pockets = is_inside(space, cubes, inside_pockets)

                if not ins:
                    outside_surface += 1

    part1 = surface

    part2 = outside_surface

    return part1, part2


debug = True
solve_puzzle(year=2022, day=18, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=18, solver=solve, do_sample=False, do_main=True)
