from utils.common import solve_puzzle
from collections import Counter

YEAR = 2023
DAY = 7

card_map = {
    "T": "A",
    "J": "B",
    "Q": "C",
    "K": "D",
    "A": "E"
}


def get_hand_rank(clean_hand):
    counts = Counter(clean_hand)

    for _, count in counts.most_common(1):
        if count == 5: return 7
        if count == 4: return 6
        if count == 3:
            if counts.most_common(2)[1][1] == 2:
                return 5
            return 4
        if count == 2:
            if counts.most_common(2)[1][1] == 2:
                return 3
            return 2
        return 1


def get_hand_score(clean_hand):
    rank = get_hand_rank(clean_hand)
    base15 = f"{rank}{''.join(clean_hand)}"
    return int(base15, 15)


def process_input(lines):
    hands, bids, scores = [], [], []

    for line in lines:
        hand, bid = line.split(" ")
        bids.append(int(bid))

        clean_hand = [card_map.get(x, x) for x in hand]
        hands.append(''.join(clean_hand))
        scores.append(get_hand_score(clean_hand))

    return hands, bids, scores


def solve_part_1(bids, scores):
    ranked = sorted(zip(scores, bids), key=lambda x: x[0])
    return sum([(i+1)*bid for i, (score, bid) in enumerate(ranked)])



def solve(lines):
    hands, bids, scores = process_input(lines)
    # print(hands)
    # print(bids)
    # print(scores)

    part1 = solve_part_1(bids, scores)

    part2 = None

    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
