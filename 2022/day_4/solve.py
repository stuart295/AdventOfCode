def contained(a1, a2):
    x1, y1 = a1
    x2, y2 = a2
    return x1 <= x2 and y1 >= y2


def overlaps(a1, a2):
    x1, y1 = a1
    x2, y2 = a2
    return (x1 <= y2 and x1 >= x2) or (x2 <= y1 and x2 >= x1)


def solve(path):
    print(f"{path:-^20}")

    lines = open(path).readlines()

    contained_reg = 0
    overlap_reg = 0
    for line in lines:
        a1, a2 = line.split(",")
        a1 = [int(x) for x in a1.split("-")]
        a2 = [int(x) for x in a2.split("-")]

        if contained(a1, a2) or contained(a2, a1):
            contained_reg += 1

        if overlaps(a1, a2):
            overlap_reg += 1

    part1 = contained_reg
    print(f"Part 1: {part1}")

    part2 = overlap_reg
    print(f"Part 2: {part2}\n")


solve('sample')
solve('input')
