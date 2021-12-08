import numpy as np
from scipy.stats import mode


def calc_power(input_list):
    mat = np.array([list(x.strip()) for x in input_list])
    
    modes, counts = mode(mat, axis=0)
    gamma = modes[0]
    eps = [f"{(int(x)+1)%2}" for x in gamma]

    return int(''.join(gamma), 2) * int(''.join(eps), 2)



print(calc_power(open('d3_1_input.txt').readlines()))