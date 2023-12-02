from utils.common import solve_puzzle
from collections import defaultdict

targets = {"red": 12, "green": 13, "blue": 14}


def clean_input(lines):
    cleaned = []
    for line in lines:
        games = []
        split = line.split(":")[1].split(";")
        for all_games in split:
            round = defaultdict(int)
            for color_sets in all_games.split(","):
                num, col = color_sets.strip().split(" ")
                round[col] = int(num)
            games.append(dict(round))
        cleaned.append(games)
    return cleaned


def solve_part_1(cleaned):
    ids = []

    for i, games in enumerate(cleaned):
        if any(game.get(col, 0) > targets[col] for game in games for col in targets):
            continue
        ids.append(i + 1)
    return sum(ids)


def solve_part_2(cleaned):
    result = 0

    for i, games in enumerate(cleaned):
        min_cubes = defaultdict(int)
        for game in games:
            for col in targets:
                min_cubes[col] = max(min_cubes.get(col, 0), game.get(col, 0))

        result += min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
    return result


def solve(lines):
    cleaned = clean_input(lines)

    part1 = solve_part_1(cleaned)
    part2 = solve_part_2(cleaned)

    return part1, part2


debug = True
solve_puzzle(year=2023, day=2, solver=solve, do_sample=True, do_main=True)
# solve_puzzle(year=2022, day=-1, solver=solve, do_sample=False, do_main=True)
