debug = False


def solve(path):
    print(f"{path:-^20}")

    stream = open(path).readlines()[0]

    for i in range(len(stream)):
        if len(set(stream[i:i+4])) == 4:
            part1 = i+4
            break

    print(f"Part 1: {part1}")

    for i in range(len(stream)):
        if len(set(stream[i:i+14])) == 14:
            part2 = i+14
            break

    print(f"Part 2: {part2}\n")


solve('sample')
solve('input')
