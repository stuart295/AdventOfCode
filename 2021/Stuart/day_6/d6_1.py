from collections import Counter


def solve(inputs, days=80):
    times = list(map(int, inputs.strip().split(',')))

    times = Counter(times)

    for day in range(days):
        result = Counter()

        result[8] = times[0]
        result[6] = times[0]

        for i in range(0, 8):
            result[i] += times[i + 1]

        times = result

    return sum(list(times.values()))


with open('d6_1_in.txt') as f:
    lines = f.readline()
    print(solve(lines, days=80))
    print(solve(lines, days=256))
