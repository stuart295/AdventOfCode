from utils.common import solve_puzzle
import re

YEAR = 2024
DAY = 3

mul_reg = r"mul\((\d{1,3}),(\d{1,3})\)"


def solve(lines):
    joined = "\n".join(lines)

    part1 = sum(int(a) * int(b) for a, b in re.findall(mul_reg, joined))
    part2 = solve_part_02(joined)

    return part1, part2


def solve_part_02(instr: str):
    mults = re.finditer(mul_reg, instr)
    dos = {d.span()[0] for d in re.finditer(r"do\(\)", instr)}
    donts = {d.span()[0] for d in re.finditer(r"don't\(\)", instr)}

    enabled = True
    allowed = set()
    for i in range(len(instr)):
        if i in donts:
            enabled = False
        if i in dos:
            enabled = True

        if enabled:
            allowed.add(i)

    return sum(int(m.groups()[0]) * int(m.groups()[1]) for m in mults if m.span()[0] in allowed)


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
