from utils.common import solve_puzzle

YEAR = 2025
DAY = 2


def solve(lines):
    if len(lines) > 1:
        raw = ''.join(lines)
    else:
        raw = lines[0]
    ranges = raw.split(",")
    ranges = [range.split("-") for range in ranges]

    part1 = solve_part_01(ranges)
    part2 = solve_part_02(ranges)

    return part1, part2


def check_invalids(first, last, splits, invalid_ids):
    first_int = int(first)
    last_int = int(last)
    cur_num = first

    while int(cur_num) <= last_int:
        if len(cur_num) % splits != 0:
            cur_num = "1" + "0" * len(cur_num)
            cur_num = cur_num[:len(cur_num) // 2] * splits
            cur_num_int = int(cur_num)
            if first_int <= cur_num_int <= last_int:
                invalid_ids.add(cur_num_int)
            continue

        first_half = cur_num[:len(cur_num) // splits]
        first_half_int = int(first_half)
        cur_num = str(first_half_int) * splits

        cur_num_int = int(cur_num)
        if first_int <= cur_num_int <= last_int:
            invalid_ids.add(cur_num_int)

        first_half_int += 1
        cur_num = str(first_half_int) * splits


def solve_part_01(ranges: list[str]) -> int:
    invalid_ids = set()
    for first, last in ranges:
        check_invalids(first, last, 2, invalid_ids)

    return sum(invalid_ids)


def solve_part_02(ranges: list[str]) -> int:
    invalid_ids = set()

    for first, last in ranges:
        for splits in range(2, len(last) + 1):
            check_invalids(first, last, splits, invalid_ids)

    return sum(invalid_ids)


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
