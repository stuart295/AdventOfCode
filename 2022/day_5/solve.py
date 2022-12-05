from more_itertools import chunked


def solve_part1(lines, instr_lines):
    stacks = setup_stacks(lines)
    follow_instructions(instr_lines, stacks)
    return ''.join([x[-1] for x in stacks if x])


def solve_part2(lines, instr_lines):
    stacks = setup_stacks(lines)
    follow_instructions_propertly(instr_lines, stacks)
    return ''.join([x[-1] for x in stacks if x])


def solve(path):
    print(f"{path:-^20}")

    lines = open(path).readlines()
    instr_lines = [line.strip() for line in lines if line.startswith('move')]

    part1 = solve_part1(lines, instr_lines)
    print(f"Part 1: {part1}")

    part2 = solve_part2(lines, instr_lines)
    print(f"Part 2: {part2}\n")


def follow_instructions(instr, stacks):
    # print_stacks(stacks)
    for in_line in instr:
        # print(in_line)
        split = in_line.split(' ')
        cnt, src, dest = int(split[1]), int(split[3]) - 1, int(split[5]) - 1
        for i in range(cnt):
            if not stacks[src]:
                continue
            moving = stacks[src].pop()
            stacks[dest].append(moving)
        # print_stacks(stacks)


def follow_instructions_propertly(instr, stacks):
    # print_stacks(stacks)
    for in_line in instr:
        # print(in_line)
        split = in_line.split(' ')
        cnt, src, dest = int(split[1]), int(split[3]) - 1, int(split[5]) - 1

        moving = []
        for i in range(cnt):
            if not stacks[src]:
                break
            moving.append(stacks[src].pop())
        stacks[dest] += moving[::-1]
        # print_stacks(stacks)


def setup_stacks(lines):
    stack_lines = []
    scount = 0
    for line in lines:
        if line.strip().startswith('1'):
            scount = len(line.strip().replace(' ', ''))
            break
        stack_lines.append(line)

    stacks = []
    for i in range(scount):
        stacks.append([])

    for line in reversed(stack_lines):
        for c, o in zip(chunked(line[:-1], 4), stacks):
            chars = ''.join(c)
            if not chars.strip():
                o.append(None)
            else:
                o.append(chars[1])
    return [[c for c in stack if c is not None] for stack in stacks]


def print_stacks(stacks):
    for i, s in enumerate(stacks):
        print(f"{i + 1}: {''.join(s)}")
    print('-' * 10)


solve('sample')
solve('input')
