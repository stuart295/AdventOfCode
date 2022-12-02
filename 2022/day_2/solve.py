values = {"X": 1, "Y": 2, "Z":3}

lose_reactions = {"A": "Z", "B": "X", "C": "Y"}
win_reactions = {"A": "Y", "B": "Z", "C": "X"}
draw_reactions = {"A": "X", "B": "Y", "C": "Z"}

def outcome(op, player):
    if op == "A": # Rock
        if player == "Y": return 6 # paper
        if player == "Z": return 0 # rock
    if op == "B": # paper
        if player == "Z": return 6 # scissors
        if player == "X": return 0 # rock
    if op == "C": # scissors
        if player == "X": return 6 # rock
        if player == "Y": return 0 # paper
    return 3

def solve(path):
    lines = open(path).readlines()
    rounds = [x.strip().split(' ') for x in lines]
    print(calc_score(rounds))

    rounds = translate(rounds)
    print(calc_score(rounds))

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




