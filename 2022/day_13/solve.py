import functools

from utils.common import solve_puzzle
import json


def compare(p1, p2):
    if isinstance(p1, str):
        p1 = json.loads(p1)

    if isinstance(p2, str):
        p2 = json.loads(p2)

    for i in range(len(p1)):
        if i >= len(p2):
            return 1

        d1, d2 = p1[i], p2[i]

        if isinstance(d1, int):
            if isinstance(d2, int):
                if d1 < d2: return -1
                if d2 < d1: return 1
                continue

            d1 = [d1]

        if isinstance(d2, int):
            d2 = [d2]

        res = compare(d1, d2)
        if res == 0:
            continue
        return res

    if len(p1) < len(p2):
        return -1

    return 0


def solve(lines):
    # Part 1
    pairs = '\n'.join(lines).split('\n\n')
    pairs = [x.split('\n') for x in pairs]

    ordered = []
    for i, pair in enumerate(pairs):
        if compare(*pair) <= 0:
            ordered.append(i + 1)

    part1 = sum(ordered)

    # Part 2
    pairs2 = [p for pair in pairs for p in pair]

    div1 = [[2]]
    div2 = [[6]]

    pairs2.append(div1)
    pairs2.append(div2)

    pairs2 = sorted(pairs2, key=functools.cmp_to_key(compare))

    i1 = pairs2.index(div1) + 1
    i2 = pairs2.index(div2) + 1

    part2 = i1 * i2

    return part1, part2


debug = True
solve_puzzle(year=2022, day=13, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=13, solver=solve, do_sample=False, do_main=True)
