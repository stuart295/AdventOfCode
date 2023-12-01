from utils.common import solve_puzzle
import re

nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def solve_part_1(lines):
    total = 0
    for line in lines:
        cleaned = re.sub(r"[^\d]","", line)
        total += int(cleaned[0] + cleaned[-1])
    return total

def replace_numbers(lines):
    replaced = []
    for line in lines:
        cleaned = ""

        for j in range(0, len(line)):
            for i, num in enumerate(nums):
                if line[j:].startswith(num):
                    cleaned += str(i+1)
                    break
                elif line[j].isdigit():
                    cleaned += line[j]
                    break

        replaced.append(cleaned)

    return replaced

def solve(lines):
    part1 = solve_part_1(lines)

    cleaned = replace_numbers(lines)
    part2 = solve_part_1(cleaned)

    return part1, part2


debug = True
solve_puzzle(year=2023, day=1, solver=solve, do_sample=True, do_main=True, sample_data_path="./test")
