import numpy as np


dir_map = {
    'forward' : np.array([1, 0]),
    'down' : np.array([0, 1]),
    'up' : np.array([0, -1]),
}

def cmd2offset(command):
    dir, dist = command.split(' ')
    return dir_map[dir] * int(dist)


def d2_1(commands:list):
    pos = np.array([0,0])

    for command in commands:
        pos += cmd2offset(command)

    return pos[0] * pos[1]


with open('d2_1_in.txt') as f:
    result = d2_1(f.readlines())
    print(result)