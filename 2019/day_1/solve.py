from utils.common import solve_puzzle


def calc_fuel(m):
    total = 0
    rem = m
    while True:
        fuel = (rem//3) - 2
        if fuel > 0:
            total += fuel
        else:
            break
        rem = fuel

    return total

def solve(lines):
    mass = list(map(int, lines))
    fuel = map(lambda m: (m//3) -2, mass)
    part1 = sum(fuel)

    part2 = sum(map(calc_fuel, mass))

    return part1, part2


debug = True

solve_puzzle(year=2019, day=1, solver=solve, do_sample=False, do_main=True, main_data_path='input')
# solve_puzzle(year=2022, day=-1, solver=solve, do_sample=False, do_main=True)
