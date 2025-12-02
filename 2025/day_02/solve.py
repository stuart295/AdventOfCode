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


def solve_part_01(ranges: list[str]) -> int:
    part1 = 0

    for first, last in ranges:
        first_int = int(first)
        last_int = int(last)

        cur_num = first

        if len(cur_num) % 2 == 0:
            first_half = cur_num[:len(cur_num) // 2]
            first_half_int = int(first_half)
            cur_num = str(first_half_int) * 2
            if first_int <= int(cur_num) <= last_int:
                part1 += int(cur_num)

        while int(cur_num) <= last_int:
            if len(cur_num) % 2 != 0:
                cur_num = "1" + "0" * len(cur_num)
                cur_num = cur_num[:len(cur_num) // 2] * 2
                cur_num_int = int(cur_num)
                if first_int <= cur_num_int <= last_int:
                    part1 += cur_num_int
                continue

            first_half = cur_num[:len(cur_num) // 2]
            first_half_int = int(first_half) + 1
            cur_num = str(first_half_int) * 2

            cur_num_int = int(cur_num)
            if first_int <= cur_num_int <= last_int:
                part1 += cur_num_int
    return part1

def check_invalids(first, last, splits, invalid_ids):
    first_int = int(first)
    last_int = int(last)
    cur_num = first

    if len(cur_num) % splits == 0 and splits <= len(cur_num):
        first_half = cur_num[:len(cur_num) // splits]
        first_half_int = int(first_half)
        cur_num = str(first_half_int) * splits
        if first_int <= int(cur_num) <= last_int and cur_num not in invalid_ids:
            invalid_ids.add(int(cur_num))
            # print(cur_num)

    while int(cur_num) <= last_int:
        if len(cur_num) % splits != 0:
            cur_num = "1" + "0" * len(cur_num)
            cur_num = cur_num[:len(cur_num) // 2] * splits
            cur_num_int = int(cur_num)
            if first_int <= cur_num_int <= last_int:
                invalid_ids.add(int(cur_num))
            continue

        if splits > len(cur_num):
            cur_num = "1" + "0" * len(cur_num)
            cur_num = cur_num[:len(cur_num) // 2] * splits
            cur_num_int = int(cur_num)
            if first_int <= cur_num_int <= last_int:
                invalid_ids.add(int(cur_num))
                # print(cur_num)
            continue

        first_half = cur_num[:len(cur_num) // splits]
        first_half_int = int(first_half) + 1
        cur_num = str(first_half_int) * splits

        cur_num_int = int(cur_num)
        if first_int <= cur_num_int <= last_int:
            invalid_ids.add(int(cur_num))
            # print(cur_num)


def solve_part_02(ranges: list[str]) -> int:
    invalid_ids = set()

    for first, last in ranges:
        for splits in range(2, len(last)+1):
            check_invalids(first, last, splits, invalid_ids)
    # print(sorted(list(invalid_ids)))
    return sum(invalid_ids)


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
