from dataclasses import dataclass
import re


@dataclass
class Cube(object):
    from_coords: tuple
    to_coords: tuple

    def __post_init__(self):
        self.width = self.to_coords[0] - self.from_coords[0] + 1
        self.height = self.to_coords[1] - self.from_coords[1] + 1
        self.depth = self.to_coords[2] - self.from_coords[2] + 1
        self.volume = self.width * self.height * self.depth

    def point_inside(self, point: tuple):
        return all(p in range(self.from_coords[i], self.to_coords[i]+1) for i, p in enumerate(point))

    def overlaps(self, other) -> bool:
        return all(self.from_coords[axis] <= other.to_coords[axis] and self.to_coords[axis] >= other.from_coords[axis] for axis in range(3))


@dataclass
class Instruction(object):
    state: bool
    cube: Cube


def read_input(path):
    with open(path) as f:
        lines = f.read().splitlines()

    out = []
    regex = r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
    for line in lines:
        match = re.match(regex, line)
        state = match.group(1) == 'on'
        min_c = [int(match.group(2)), int(match.group(4)), int(match.group(6))]
        max_c = [int(match.group(3)), int(match.group(5)), int(match.group(7))]
        out.append(Instruction(state, Cube(tuple(min_c), tuple(max_c))))
    return out


# TODO Find more efficient method
def find_overlapping_cubes(cube, cube_list):
    return [c for c in cube_list if c.overlaps(cube)]


# TODO There's probably a better way to do this...
def subdivide_cube(cube, cutting_cube):
    sub = []
    const_min = tuple(max(x1, x2) for x1, x2 in zip(cube.from_coords, cutting_cube.from_coords))
    const_max = tuple(min(x1, x2) for x1, x2 in zip(cube.to_coords, cutting_cube.to_coords))

    cutter = Cube(const_min, const_max)

    # bottom
    bot = Cube(cube.from_coords, (cube.to_coords[0], cutter.from_coords[1] - 1, cube.to_coords[2]))
    if bot.width > 0 and bot.height > 0 and bot.depth > 0:
        sub.append(bot)

    # top
    top = Cube((cube.from_coords[0], cutter.to_coords[1] + 1, cube.from_coords[2]), cube.to_coords)
    if top.width > 0 and top.height > 0 and top.depth > 0:
        sub.append(top)

    # left
    left = Cube((cube.from_coords[0], cutter.from_coords[1], cube.from_coords[2]), (cutter.from_coords[0] - 1, cutter.to_coords[1], cube.to_coords[2]))
    if left.width > 0 and left.height > 0 and left.depth > 0:
        sub.append(left)

    # right
    right = Cube((cutter.to_coords[0] + 1, cutter.from_coords[1], cube.from_coords[2]), (cube.to_coords[0], cutter.to_coords[1], cube.to_coords[2]))
    if right.width > 0 and right.height > 0 and right.depth > 0:
        sub.append(right)

    # front
    front = Cube((cutter.from_coords[0], cutter.from_coords[1], cutter.to_coords[2] + 1), (cutter.to_coords[0], cutter.to_coords[1], cube.to_coords[2]))
    if front.width > 0 and front.height > 0 and front.depth > 0:
        sub.append(front)

    # back
    back = Cube((cutter.from_coords[0], cutter.from_coords[1], cube.from_coords[2]), (cutter.to_coords[0], cutter.to_coords[1], cutter.from_coords[2] - 1))
    if back.width > 0 and back.height > 0 and back.depth > 0:
        sub.append(back)

    return sub


def run_instruction(instr, cube_list):
    out_list = cube_list
    overlapping = find_overlapping_cubes(instr.cube, out_list)

    # No overlaps
    if not overlapping:
        if instr.state:
            out_list.append(instr.cube)
            return out_list

    # Overlaps - Subtract overlapping region and then add it back - not ideal
    for overlap in overlapping:
        out_list.remove(overlap)
        subvdived = subdivide_cube(overlap, instr.cube)

        out_list += subvdived


    if instr.state:
        out_list.append(instr.cube)
    return out_list


def solve(instructions):
    cube_list = []
    for input in instructions:
        cube_list = run_instruction(input, cube_list)
    total_volume = sum([cube.volume for cube in cube_list])
    print(total_volume)


# inputs = read_input('./test.txt')
inputs = read_input('./input.txt')


part1 = inputs[:20]

solve(part1)
solve(inputs)
