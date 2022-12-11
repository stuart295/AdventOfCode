from utils.common import solve_puzzle
from more_itertools import  chunked
from collections import deque



class Monke:

    def __init__(self, lines):
        self.items = lines[1].split(':')[1].strip().split(',')
        self.items = deque(int(x) for x in self.items)
        self.op = lines[2].split('=')[1].strip().split(' ')
        self.test = int(lines[3].split(' ')[-1])
        self.true_monke = int(lines[4].split(' ')[-1])
        self.false_monke = int(lines[5].split(' ')[-1])
        self.inspections = 0

    def apply_op(self, worry):
        val1 = worry if self.op[0] == 'old' else int(self.op[0])
        val2 = worry if self.op[2] == 'old' else int(self.op[2])

        if self.op[1] == '+':
            return val1 + val2
        elif self.op[1] == '*':
            return val1 * val2

        raise Exception("Op not implemented!")

    def test_worry(self, worry):
        if worry % self.test == 0:
            return self.true_monke

        return self.false_monke

    def step(self, all_monkes, div_3=True):
        new_items = self.items.copy()
        for item in self.items:
            new_items.remove(item)
            self.inspections += 1
            cur_worry = self.apply_op(item)
            if div_3:
                cur_worry = cur_worry // 3

            targ_monke = self.test_worry(cur_worry)
            all_monkes[targ_monke].items.append(cur_worry)

        self.items = new_items


def solve(lines):

    monkes = []
    for data in chunked(lines, 7):
        monkes.append(Monke(data))

    for round in range(20):
        for monke in monkes:
            monke.step(monkes)

    mb = sorted([m.inspections for m in monkes])

    part1 = mb[-1] * mb[-2]

    return part1, None


debug = True
solve_puzzle(year=2022, day=11, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=11, solver=solve, do_sample=False, do_main=True)
