# I changed my approach 3 times while solving this, so its a bit of a mess

import math
import numpy as np

def calc_y(vy0, t):
    return -0.5*(t)**2 + (vy0 + 0.5)*(t)

def step(p, v):
    out_p = p + v
    out_v = v - np.array([1, 1])
    out_v[0] = max(out_v[0], 0)
    return out_p, out_v


def calc_vx(targ_x):
    return -1 + math.sqrt(1 + 2 * targ_x)


def calc_heighest(vy0):
    return 0.5 * vy0 * (vy0+1)


def in_target(pos, x_targ, y_targ):
    return pos[0] in range(x_targ[0], x_targ[1]+1) and pos[1] in range(y_targ[0], y_targ[1]+1)


def calc_vy0(targ_y, targ_t):
    return math.floor((targ_y/targ_t) + 0.5*targ_t)


def simulate(vy0, y_targ):
    max_y = 0
    y = 0
    t = 1
    while y >= y_targ[0]:
        y = calc_y(vy0, t)
        max_y = max(max_y, y)
        if y in range(y_targ[0], y_targ[1]+1):
            return max_y, t
        t += 1

    return None, t


def simulate2(vx0, vy0, xtarg, ytarg):
    p = np.array([0, 0])
    v = np.array([vx0, vy0])

    while True:
        p, v = step(p, v)
        if in_target(p, xtarg, ytarg):
            return True, p
        elif p[0] > xtarg[1] or p[1] < ytarg[0]:
            return False, None


def solve1( y_targ):
    t0 = 1

    max_y = 0
    vels = set()
    for t in range(t0, 100000):
        for y in range(y_targ[0], y_targ[1] + 1):
            vy0 = calc_vy0(y, t)
            final_y = calc_y(vy0, t)
            if final_y in range(y_targ[0], y_targ[1]+1):
                h = calc_heighest(vy0)
                max_y = max(max_y, round(h))
                vels.add(vy0)

    return max_y, vels


def solve2(y_vels, x_targ, y_targ):
    vels = set()

    for vy0 in y_vels:
        for vxo in range(0, 1000):
            hit, final_p = simulate2(vxo, vy0, x_targ, y_targ)
            if hit:
                vels.add((vxo, vy0))

    return vels

# x_targ = [20,30]
# y_targ = [-10,-5]

x_targ = [29,73]
y_targ = [-248,-194]

max_y, vels = solve1(y_targ)
print(f"Part 1: {max_y}")

all_vels = solve2(vels, x_targ, y_targ)
print(f"Part 2: {len(all_vels)}")

