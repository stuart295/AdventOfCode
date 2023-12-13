from utils.common import solve_puzzle

YEAR = 2023
DAY = 13


def count_reflections(pattern):
    for i, line in enumerate(pattern):
        if i == len(pattern) - 1:
            break

        s1 = len(pattern[:i + 1])
        s2 = len(pattern[:i:-1])

        if s1 <= s2:
            if pattern[:i + 1] == pattern[i + s1:i:-1]:
                return s1
        else:
            if pattern[i + 1 - s2:i + 1] == pattern[:i:-1]:
                return s1

    return 0


def rot(pattern):
    return [[line[i] for line in pattern[::-1]] for i in range(len(pattern[0]))]


def solve_part_01(patterns):
    score = 0

    for pattern in patterns:
        # Horizontal
        cur_score = count_reflections(pattern)
        if cur_score:
            score += cur_score * 100
        else:
            # Vertical line
            rotated = rot(pattern)
            cur_score = count_reflections(rotated)

            assert cur_score > 0
            score += cur_score

    return score


def read_patterns(lines):
    patterns = []
    cur_pattern = []

    for line in lines:
        if line.strip() == "":
            patterns.append(cur_pattern)
            cur_pattern = []
        else:
            cur_pattern.append(list(line))
    return patterns + [cur_pattern]


def find_diffs(p1, p2):
    diffs = []

    for y, (l1, l2) in enumerate(zip(p1, p2)):
        for x, (c1, c2) in enumerate(zip(l1, l2)):
            if c1 != c2:
                diffs.append((x, y))

    return diffs


def fix_smudge(pattern):
    fixed = [[x for x in line] for line in pattern]
    
    for i, line in enumerate(fixed):
        if i == len(fixed) - 1:
            break

        s1 = len(fixed[:i + 1])
        s2 = len(fixed[:i:-1])
        offset = 0

        if s1 <= s2:
            p1 = fixed[:i + 1]
            p2 = fixed[i + s1:i:-1]
        else:
            p1 = fixed[i + 1 - s2:i + 1]
            p2 = fixed[:i:-1]
            offset = i + 1 - s2

        diffs = find_diffs(p1, p2)
        if len(diffs) == 1:
            x, y = diffs[0]
            fixed[y + offset][x] = "." if fixed[y + offset][x] == "#" else "#"
            assert p1 == p2
            return s1

    return 0


def solve_part_02(patterns):
    score = 0

    for pattern in patterns:
        cur = fix_smudge(pattern)
        if cur > 0:
            score += 100 * cur
        else:
            rotated = rot(pattern)
            cur = fix_smudge(rotated)
            assert cur > 0
            score += cur

    return score


def solve(lines):
    patterns = read_patterns(lines)

    part1 = solve_part_01(patterns)
    part2 = solve_part_02(patterns)

    return part1, part2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
