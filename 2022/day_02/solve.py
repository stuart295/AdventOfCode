values = {"X": 1, "Y": 2, "Z": 3}
op_vals = {"A" : 0, "B": 1, "C": 2}
move_map = {"X": "A", "Y": "B", "Z": "C"}

lose_reactions = {"A": "Z", "B": "X", "C": "Y"}
win_reactions = {"A": "Y", "B": "Z", "C": "X"}
draw_reactions = {"A": "X", "B": "Y", "C": "Z"}


def outcome(op, player):
    trans = move_map[player]
    diff = op_vals[trans] - op_vals[op]

    if diff == 0: return 3
    if diff == 1 or diff == -2: return 6
    return 0


def solve(path):
    print(f"{path:-^20}")
    lines = open(path).readlines()
    rounds = [x.strip().split(' ') for x in lines]
    print(f"Part 1: {calc_score(rounds)}")

    rounds = translate(rounds)
    print(f"Part 2: {calc_score(rounds)}")


def translate(rounds):
    out = []
    for op, outcome in rounds:
        if outcome == "X":
            out.append([op, lose_reactions[op]])
        elif outcome == "Y":
            out.append([op, draw_reactions[op]])
        elif outcome == "Z":
            out.append([op, win_reactions[op]])
    return out


def calc_score(rounds):
    score = 0
    for op, player in rounds:
        score += outcome(op, player)
        score += values[player]

    return score


solve('sample')
solve('input')
