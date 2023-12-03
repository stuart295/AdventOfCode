from utils.common import solve_puzzle, grid_offsets


def solve_part_01(lines):
    nums = []
    num_pos = {}

    for y, row in enumerate(lines):
        cur_num = ""
        is_part = False
        digit_pos = []

        for x, c in enumerate(row):

            if not c.isdigit():
                # End of num
                if cur_num and is_part:
                    nums.append(int(cur_num))

                    num_id = len(num_pos)
                    for d in digit_pos:
                        num_pos[d] = (int(cur_num), num_id)

                cur_num = ""
                is_part = False
                digit_pos = []

                continue

            cur_num += c
            digit_pos.append((x, y))

            for xo, yo in grid_offsets(True):
                xa = x + xo
                ya = y + yo

                if not 0 <= xa < len(row):
                    continue

                if not 0 <= ya < len(lines):
                    continue

                adj_c = lines[ya][xa]

                if not adj_c.isdigit() and adj_c != ".":
                    is_part = True
                    break

        # End of num
        if cur_num and is_part:
            nums.append(int(cur_num))

            num_id = len(num_pos)
            for d in digit_pos:
                num_pos[d] = (int(cur_num), num_id)

    return sum(nums), num_pos


def solve_part_02(lines, num_pos):
    gear_ratios = []

    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c == "*":
                adj_nums = []
                unique_ids = set()

                for xo, yo in grid_offsets(True):
                    coord = (x + xo, y + yo)
                    if coord in num_pos and num_pos[coord][1] not in unique_ids:
                        adj_nums.append(num_pos[coord][0])
                        unique_ids.add(num_pos[coord][1])

                if len(adj_nums) == 2:
                    gear_ratios.append(adj_nums[0] * adj_nums[1])

    return sum(gear_ratios)


def solve(lines):
    lines = [row.strip() for row in lines]
    part1, num_pos = solve_part_01(lines)

    part2 = solve_part_02(lines, num_pos)

    return part1, part2


debug = True
# solve_puzzle(year=2023, day=3, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2023, day=3, solver=solve, do_sample=False, do_main=True)
