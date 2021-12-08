from math import ceil, floor
from statistics import median, mean


def solve_median(inputs):
    m = median(inputs)
    fuel = sum(abs(m - x) for x in inputs)
    return fuel


def triangular_fuel(m, x):
    dist = abs(m - x)
    return (dist * (dist + 1)) / 2.0


def solve_mean(inputs):
    m1 = ceil(mean(inputs))
    m2 = floor(mean(inputs))

    f1 = sum(triangular_fuel(m1, x) for x in inputs)
    f2 = sum(triangular_fuel(m2, x) for x in inputs)

    return min(f1, f2)


with open('d7_1_in.txt') as f:
    # with open('test.txt') as f:
    inputs = list(map(int, f.readline().strip().split(',')))
    print(solve_median(inputs))
    print(solve_mean(inputs))
