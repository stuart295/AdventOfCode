from utils.common import solve_puzzle
from collections import defaultdict

YEAR = 2024
DAY = 5


def solve(lines):
    rules, updates = parse_input(lines)

    part1 = solve_part_01(rules, updates)
    part2 = solve_part_02(rules, updates)

    return part1, part2


def parse_input(lines):
    rules = defaultdict(list)
    updates = []

    for line in lines:
        if "|" in line:
            a, b = line.split("|")
            rules[int(a)].append(int(b))
        elif "," in line:
            updates.append([int(x) for x in line.split(",")])

    return rules, updates


def is_ordered(update, rules):
    for i, c in enumerate(update):
        if c in rules and any(x in update[:i] for x in rules[c]):
            return False

    return True


def solve_part_01(rules, updates):
    correct = []
    for update in updates:
        if is_ordered(update, rules):
            correct.append(update[len(update) // 2])

    return sum(correct)


def solve_part_02(rules, updates):
    results = []
    for update in updates:
        if is_ordered(update, rules):
            continue

        fixed = list(update)

        i = 0
        while i < len(fixed):
            c = fixed[i]

            if c not in rules:
                i += 1
                continue

            to_move = []

            for x in rules[c]:
                if x in fixed[:i - len(to_move)]:
                    to_move.append(x)
                    fixed.remove(x)

            if not to_move:
                i += 1
                continue

            fixed = fixed[:i - len(to_move) + 1] + to_move + fixed[i - len(to_move) + 1:]
            i = i - len(to_move) + 2

        results.append(fixed[len(fixed) // 2])

    return sum(results)


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
