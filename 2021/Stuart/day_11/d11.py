def inc_energy_levels(state):
    to_flash = set()
    for i in range(len(state)):
        for j in range(len(state[i])):
            state[i][j] += 1
            if state[i][j] > 9:
                to_flash.add((i, j))

    return to_flash


def process_flashes(state, to_flash: set):
    flashes = 0
    while len(to_flash) > 0:
        flashes += 1
        row, col = to_flash.pop()
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i not in range(0, len(state)) or j not in range(0, len(state[0])):
                    continue

                if (i, j) == (row, col) or state[i][j] > 9:
                    continue
                state[i][j] += 1
                if state[i][j] > 9:
                    to_flash.add((i, j))
    return flashes


def reset_energy(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = state[i][j] % 10


def step(state):
    to_flash = inc_energy_levels(state)
    flash_count = process_flashes(state, to_flash)
    reset_energy(state)
    return flash_count


def read_input(path):
    input = open(path).readlines()
    return [list(map(int, x.strip())) for x in input]


def solve_1(state):
    flashes = 0
    for i in range(100):
        flashes += step(state)
    print(flashes)


def solve_2(state):
    step_num = 0
    while not all(all(x == 0 for x in row) for row in state):
        step(state)
        step_num += 1
    print(step_num)


solve_1(read_input('input.txt'))
solve_2(read_input('input.txt'))
