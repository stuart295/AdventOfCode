import numpy as np


dir_map = {
    'down' : np.array([0, 0, 1]),
    'up' : np.array([0, 0, -1]),
}

def cmd2offset(command, state):
    dir, dist = command.split(' ')
    dist = int(dist)

    if dir == 'forward':
        return np.array([dist, dist * state[2], 0])

    return dir_map[dir] * int(dist)



def d2_2(commands:list):
    state = np.array([0,0,0])

    for command in commands:
        state += cmd2offset(command, state)

    return state[0] * state[1]



with open('d2_2_in.txt') as f:
    result = d2_2(f.readlines())
    print(result)