from utils.common import solve_puzzle


def shift_pos(cur_pos, num, orig):
    return (cur_pos + num) % (len(orig) - 1)


def dump(orig_list, positions):
    ordered = [(i, x) for i, x in enumerate(orig_list)]
    ordered = sorted(ordered, key=lambda x: positions.index(x[0]))
    ordered = [x[1] for x in ordered]
    print(', '.join(list(map(str, ordered))))


def mix(orig, positions):
    for orig_pos, num in enumerate(orig):
        cur_pos = positions.index(orig_pos)
        new_pos = shift_pos(cur_pos, num, orig)

        if new_pos > cur_pos:
            positions = positions[:cur_pos] + positions[cur_pos + 1:new_pos + 1] + [positions[cur_pos]] + positions[
                                                                                                          new_pos + 1:]
        else:
            positions = positions[:new_pos] + [positions[cur_pos]] + positions[new_pos:cur_pos] + positions[
                                                                                                  cur_pos + 1:]

    return positions


def solve_part_1(orig):
    positions = list(range(len(orig)))

    positions = mix(orig, positions)

    result = 0
    zero_orig = orig.index(0)
    cur_idx = positions.index(zero_orig)

    for i in range(3):
        cur_idx = (cur_idx + 1000) % len(orig)
        result += orig[positions[cur_idx]]

    return result


def solve_part_2(orig):
    key = 811589153
    decrypted = [x * key for x in orig]

    positions = list(range(len(decrypted)))

    for i in range(10):
        positions = mix(decrypted, positions)

    result = 0
    zero_orig = decrypted.index(0)
    cur_idx = positions.index(zero_orig)

    for i in range(3):
        cur_idx = (cur_idx + 1000) % len(decrypted)
        result += decrypted[positions[cur_idx]]

    return result


def solve(lines):
    orig = list(map(int, lines))
    part1 = solve_part_1(orig)

    part2 = solve_part_2(orig)

    return part1, part2


debug = True
solve_puzzle(year=2022, day=20, solver=solve, do_sample=True, do_main=False, sample_data_path='sample')
solve_puzzle(year=2022, day=20, solver=solve, do_sample=False, do_main=True)
