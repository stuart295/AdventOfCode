from utils.common import solve_puzzle
import numpy as np

YEAR = 2025
DAY = 3

def solve(lines):
    part1 = solve_battery_settings(lines, 2)
    part2 = solve_battery_settings(lines, 12)

    return part1, part2


def solve_battery_settings(lines, required_batteries) -> int:
    result = 0
    for line in lines:
        jolts = [int(s) for s in line]
        digits = []

        for jolt_cnt in range(required_batteries):
            padding = -(required_batteries-jolt_cnt-1)
            if padding < 0:
                cur_idx = np.argmax(jolts[:padding])
            else:
                cur_idx = np.argmax(jolts)

            digits.append(str(jolts[cur_idx]))
            jolts[cur_idx] = -999
            jolts = jolts[cur_idx+1:]

        result += int(''.join(digits))
    return result

solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
