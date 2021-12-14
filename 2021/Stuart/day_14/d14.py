from collections import Counter


def read_input(path):
    with open(path) as f:
        template = f.readline().strip()
        f.readline()

        rules = {}
        line = f.readline()
        while line != '':
            pair, result = line.strip().split('->')
            rules[pair.strip()] = result.strip()
            line = f.readline()

        return rules, template


def poly2dict(poly):
    out = Counter()
    for i in range(len(poly) - 1):
        out[poly[i:i + 2]] += 1

    return out


def step(pairs, rules):
    out = Counter()
    for pair, count in pairs.items():
        if pair in rules:
            res = rules[pair]
            out[pair[0] + res] += count
            out[res + pair[1]] += count
        else:
            out[pair] += count

    return out


def calc_score(pairs, poly):
    counts = Counter()

    for pair, count in pairs.items():
        counts[pair[0]] += count
        counts[pair[1]] += count

    adj = Counter()
    adj[poly[0]] += 1
    adj[poly[-1]] += 1
    counts = Counter({ele: (count - adj[ele]) / 2.0 + adj[ele] for ele, count in counts.items()})

    sorted = counts.most_common()
    return int(sorted[0][1] - sorted[-1][1])


def solve(steps, inputs='input.txt'):
    rules, poly = read_input(inputs)
    pairs = poly2dict(poly)

    for i in range(steps):
        pairs = step(pairs, rules)

    print(calc_score(pairs, poly))

solve(10)
solve(40)
