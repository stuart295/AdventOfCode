from utils.common import solve_puzzle
import re

YEAR = 2024
DAY = 3


def solve(lines):
    joined = "\n".join(lines)

    part1 = solve_part_01(joined)
    part2 = solve_part_02(joined)

    return part1, part2


def solve_part_01(instr: str):
    result = 0
    for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", instr):
        result += int(a) * int(b)
    return result


def solve_part_02(instr: str):
    dos = re.finditer(r"do\(\)", instr)
    donts = re.finditer(r"don't\(\)", instr)
    mults = re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", instr)

    dos = {d.span()[0] for d in dos}
    donts = {d.span()[0] for d in donts}

    result = 0

    for mul in mults:
        pos = mul.span()[0]

        enabled = True
        for i in range(pos, 0, -1):
            if i in dos:
                break
            if i in donts:
                enabled = False
                break

        if enabled:
            a, b = mul.groups()
            result += int(a) * int(b)
    return result


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
