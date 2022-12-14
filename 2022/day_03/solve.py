from more_itertools import chunked


def priority(item):
    if item.isupper():
        return ord(item) - ord('A') + 27
    else:
        return ord(item) - ord('a') + 1


def solve1(rs):
    s = 0

    for r in rs:
        r1 = set(r[:len(r) // 2])
        r2 = set(r[len(r) // 2:])
        for item in r1 & r2:
            s += priority(item)
    return s


def solve2(rs):
    s = 0

    for group in chunked(rs, 3):
        common = set(group[0].strip())
        for r in group[1:]:
            common &= set(r.strip())
        s += priority(list(common)[0])

    return s


def solve(path):
    print(f"{path:-^20}")

    rs = open(path).readlines()

    part1 = solve1(rs)
    print(f"Part 1: {part1}")

    part2 = solve2(rs)
    print(f"Part 2: {part2}\n")


solve('sample')
solve('input')
