import itertools
import numpy as np


class Sensor(object):
    def __init__(self, beacons):
        self.beacons = beacons
        self.position = None
        self.checked = set()
        self.rotations = list(transform(beacons))

    def transformed_beacons(self):
        return {add_offset(x, self.position) for x in self.beacons}


def read_input(path):
    beacons = []
    with open(path) as f:
        lines = f.read().splitlines()
        points = set()
        for line in lines:
            if line.startswith('--'):
                continue
            if line == '':
                beacons.append(Sensor(points))
                points = set()
                continue
            points.add(tuple(map(int, line.split(','))))

    beacons.append(Sensor(points))
    return beacons


# Terrible way to handle rotations in this case
def rotz(p, deg):
    rad = np.radians(deg)
    x, y, z = p
    return (x * np.cos(rad) - y * np.sin(rad), x * np.sin(rad) + y * np.cos(rad), z)


def roty(p, deg):
    rad = np.radians(deg)
    x, y, z = p
    return (x * np.cos(rad) + z * np.sin(rad), y, -x * np.sin(rad) + z * np.cos(rad))


def rotx(p, deg):
    rad = np.radians(deg)
    x, y, z = p
    return (x, y * np.cos(rad) - z * np.sin(rad), y * np.sin(rad) + z * np.cos(rad))


def transform(coords):
    for z_degs in range(0, 360, 90):
        for y_degs in range(0, 360, 90):
            yield [tuple(map(int, map(round, roty(rotz(x, z_degs), y_degs)))) for x in coords]

    for x_degs in [-90, 90]:
        for y_degs in range(0, 360, 90):
            yield [tuple(map(int, map(round, roty(rotx(x, x_degs), y_degs)))) for x in coords]


def add_offset(x: tuple, offset):
    return tuple((np.array(x) + offset))


def check_overlap(source, target: set):
    for coord in source:
        for t in target:
            offset = (np.array(t) - np.array(coord))
            off_source = {add_offset(x, offset) for x in source}
            if len(off_source.intersection(target)) >= 12:
                return True, off_source, offset
    return False, None, -1


def align_beacons(sensors):
    out = sensors[0].beacons
    sensors[0].position = (0, 0, 0)
    unaligned = sensors[1:]

    while len(unaligned) > 0:
        print(f"Remaining unaligned: {len(unaligned)}")
        src = unaligned.pop(0)
        found = False
        for coords in src.rotations:
            overlap, transformed, offset = check_overlap(coords, out)
            if overlap:
                src.position = offset
                out.update(transformed)

                found = True
                break

        if not found:
            unaligned.append(src)

    return out


def manhat(p1, p2):
    return sum(abs(pp1 - pp2) for pp1, pp2 in zip(p1, p2))

# sensors = read_input('test.txt')
sensors = read_input('input.txt')

aligned = align_beacons(sensors)
print(len(aligned))

largest = max([manhat(p1.position, p2.position) for p1, p2 in itertools.permutations(sensors, 2)])
print(largest)