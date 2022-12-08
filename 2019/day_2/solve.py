from utils.common import solve_puzzle

def run_code(data):
    pos = 0
    while data[pos] != 99:
        if data[pos] == 1:
            val = data[data[pos+1]] + data[data[pos+2]]
            data[data[pos + 3]] = val
        else:
            # if data[pos + 1] >= len(data) or data[pos + 2] >= len(data) or data[pos + 3] >= len(data):
            #     break

            val = data[data[pos + 1]] * data[data[pos + 2]]
            data[data[pos + 3]] = val
        pos += 4

def solve(lines):

    data = list(map(int,lines[0].strip().split(',')))

    cur_date = data.copy()
    cur_date[1] = 12
    cur_date[2] = 2

    run_code(cur_date)

    part1 = cur_date[0]

    target = 19690720

    part2 = None

    for i in range(100):
        for j in range(100):
            cur_data = data.copy()
            cur_data[1] = i
            cur_data[2] = j
            run_code(cur_data)
            if cur_data[0] == target:
                part2 = 100* i+j
                break

        if part2 is not None:
            break

    return part1, part2


debug = True

solve_puzzle(year=2019, day=2, solver=solve, do_sample=False, do_main=True, main_data_path='input')
# solve_puzzle(year=2022, day=-1, solver=solve, do_sample=False, do_main=True)
