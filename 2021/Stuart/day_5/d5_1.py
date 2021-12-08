from collections import Counter
import numpy as np


def solve(lines, allow_diags=False):
    floor_map = Counter()
    high_counts = 0

    for line in lines:
        p1, p2 = line.strip().split(' -> ')
        p1 = np.array(list(map(int, p1.split(','))))
        p2 = np.array(list(map(int, p2.split(','))))

        if p1[0] != p2[0] and p1[1] != p2[1] and not allow_diags:
            continue

        step = np.array([p2[0] - p1[0], p2[1] - p1[1]])

        for i in range(2):
            if abs(step[i]) > 0:
                step[i] /= abs(step[i])

        curp = np.array(p1)

        dist = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))
        for i in range(dist+1):
            t = tuple(curp)
            floor_map[t] += 1
            if floor_map[t] == 2:
                high_counts += 1
            curp += step

    return high_counts


with open('d5_1_in.txt') as f:
    lines = f.readlines()
    print(solve(lines))
    print(solve(lines, allow_diags=True))