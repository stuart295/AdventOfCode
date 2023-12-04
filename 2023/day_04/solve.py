from utils.common import solve_puzzle
import re


def clean_lines(lines):
    cards, mine = [], []

    for line in lines:
        cleaned = re.sub(" +", " ", line).strip()

        c, m = cleaned.split(":")[1].strip().split("|")
        cards.append(c.strip().split(" "))
        mine.append(m.strip().split(" "))

    return cards, mine


def solve_part_01(cards, my_nums):
    points = 0

    for card, my_num in zip(cards, my_nums):
        matches = [num for num in my_num if num in card]
        match_cnt = len(matches)
        if match_cnt > 0:
            points += 1 * pow(2, match_cnt - 1)

    return points


def solve_part_02(cards, my_nums):
    total_cards = {i + 1: 1 for i in range(len(cards))}

    for i, (card, my_num) in enumerate(zip(cards, my_nums)):
        card_num = i + 1
        matches = [num for num in my_num if num in card]
        match_cnt = len(matches)

        for j in range(card_num + 1, card_num + 1 + match_cnt):
            total_cards[j] += total_cards[card_num]

    return sum(total_cards.values())


def solve(lines):
    cards, my_nums = clean_lines(lines)

    part1 = solve_part_01(cards, my_nums)
    part2 = solve_part_02(cards, my_nums)

    return part1, part2


debug = True
solve_puzzle(year=2023, day=4, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2023, day=4, solver=solve, do_sample=False, do_main=True)
