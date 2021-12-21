import itertools
from functools import lru_cache


def move(from_pos, die, score):
    end = (from_pos + sum(die))
    if end > 10:
        end = ((end - 1) % 10) + 1
    return end, score + end


def solve1():
    p1 = 7
    p2 = 3
    p1_score = 0
    p2_score = 0
    d = 1
    rolls = 0
    while p1_score < 1000 and p2_score < 1000:
        p1, p1_score = move(p1, [d, d + 1, d + 2], p1_score)
        rolls += 3
        if p1_score >= 1000: break
        d += 3

        p2, p2_score = move(p2, [d, d + 1, d + 2], p2_score)
        rolls += 3
        d += 3

    res = min(p1_score, p2_score)
    print(f"Rolls: {rolls}")
    print(f"Losing score: {res}")
    print(f"Output: {res * rolls}")


@lru_cache(maxsize=None)
def solve2(p1, p2, p1_score, p2_score):
    p1_wins, p2_wins = 0, 0
    for d1 in itertools.product([1, 2, 3], repeat=3):
        p1_cur, p1_score_cur = move(p1, d1, p1_score)
        if p1_score_cur >= 21:
            p1_wins += 1
            continue

        for d2 in itertools.product([1, 2, 3], repeat=3):
            p2_cur, p2_score_cur = move(p2, d2, p2_score)
            if p2_score_cur >= 21:
                p2_wins += 1
                continue

            w1, w2 = solve2(p1_cur, p2_cur, p1_score_cur, p2_score_cur)
            p1_wins += w1
            p2_wins += w2

    return p1_wins, p2_wins


solve1()

wins = solve2(7, 3, 0, 0)

print('Part 2')
print(max(wins))
