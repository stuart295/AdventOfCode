from utils.common import solve_puzzle
from collections import Counter
import functools

YEAR = 2023
DAY = 7

card_map = {
    "T": "A",
    "Q": "B",
    "K": "C",
    "A": "D",
    "J": "1",
}


def get_hand_rank(clean_hand):
    counts = Counter(clean_hand)

    jokers = counts.get("1", 0)

    ordered = counts.most_common()

    card, count = ordered[0]
    card_2, count2 = ordered[1] if len(ordered) >= 2 else (None, 0)

    if count == 5:
        # Normal
        return 7

    if count == 4:
        # If any jokers, upgrade to 5
        if jokers > 0:
            return 7

        # Normal: 4 + 1
        return 6

    if count == 3:
        if count2 == 2:
            # Either of them are jokers, Upgrade to 5
            if jokers > 0:
                return 7

            # Normal: 3 + 2
            return 5

        # One joker: Upgrade to 4+1
        if jokers > 0:
            return 6

        # Normal: 3 + 1 + 1
        return 4

    if count == 2:
        if count2 == 2:
            # Either of them are jokers, upgrade to 4 + 1
            if card == "1" or card_2 == "1":
                return 6

            # 1 joker, upgrade to 3+2
            if jokers > 0:
                return 5

            # Normal 2 + 2 + 1
            return 3

        # Pair of jokers or one other joker: Upgrade to 3 + 1 + 1
        if jokers > 0:
            return 4

        # Normal: 2 + 1 + 1 + 1
        return 2

    # Any joker: Upgrade to 2 + 1 + 1 + 1
    if jokers > 0:
        return 2

    # Normal 1 x 5
    return 1

def get_hand_score(clean_hand):
    rank = get_hand_rank(clean_hand)
    base14 = f"{rank}{''.join(clean_hand)}"
    return int(base14, 27)


def process_input(lines):
    hands, bids, scores = [], [], []

    for line in lines:
        hand, bid = line.split(" ")
        bids.append(int(bid))

        clean_hand = [card_map.get(x, x) for x in hand]

        hands.append(clean_hand)

        scores.append(get_hand_score(clean_hand))

    return hands, bids, scores


def compare_func(pair_a, pair_b):
    a, _ = pair_a
    b, __ = pair_b

    ra = get_hand_rank(a)
    rb = get_hand_rank(b)

    # Ranks differ
    if ra < rb:
        return -1
    if ra > rb:
        return 1

    # Ranks same
    for ca, cb in zip(a, b):
        if ca > cb:
            return 1
        if ca < cb:
            return -1

    return 0


def solve_part_1(bids, cards):
    ranked = sorted(zip(cards, bids), key=functools.cmp_to_key(compare_func))
    return sum([(i+1)*bid for i, (_, bid) in enumerate(ranked)])



def solve(lines):
    hands, bids, scores = process_input(lines)

    part1 = None

    part2 = solve_part_1(bids, hands)
    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
