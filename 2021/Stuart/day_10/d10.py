
score_lookup = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

score_lookup_2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

char_pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}


def find_illegal_char(chunk):
    if len(chunk) < 1:
        return None, ''

    start = chunk[0]

    if start in score_lookup:
        return start, ''

    remaining = chunk[1:]

    while len(remaining) > 0:
        next = remaining[0]

        if next == char_pairs[start]:
            return None, remaining[1:]

        # Illegal chars
        if next in score_lookup:
            return next, remaining[1:]

        # Recursively process chunk
        illegal, remaining = find_illegal_char(remaining)

        if illegal:
            return illegal, remaining

    return None, ''


def find_error_score(lines):
    score = 0
    incomplete = []

    for line in lines:
        remaining = line
        illegal = None
        while len(remaining) > 0:
            illegal, remaining = find_illegal_char(remaining)
            if illegal is not None:
                score += score_lookup[illegal]
                break

        if illegal is None:
            incomplete.append(line)

    return score, incomplete


def find_missing(chunk):
    if len(chunk) < 1:
        return [], ''

    start = chunk[0]
    remaining = chunk[1:]

    missing = []

    while len(remaining) > 0:
        next = remaining[0]

        if next == char_pairs[start]:
            return [], remaining[1:]

        # Recursively process chunk
        add_missing, remaining = find_missing(remaining)
        missing += add_missing

    return missing + [char_pairs[start]], ""


def calc_missing_score(missing):
    score = 0

    for i, c in enumerate(missing):
        score = score * 5 + score_lookup_2[c]

    return score


def find_incomp_score(lines):
    scores = []

    for line in lines:
        missing, _ = find_missing(line)
        scores.append(calc_missing_score(missing))

    scores = sorted(scores)

    return scores[int(len(scores) / 2)]


with open('input.txt') as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]
    error_score, incomplete = find_error_score(lines)
    print(error_score)
    print(find_incomp_score(incomplete))
