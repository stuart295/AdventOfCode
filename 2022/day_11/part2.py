from utils.common import solve_puzzle
from more_itertools import chunked
from collections import deque


class Monke:

    def __init__(self, lines, idx):
        self.items = lines[1].split(':')[1].strip().split(',')
        self.items = deque(int(x) for x in self.items)
        self.op = lines[2].split('=')[1].strip().split(' ')
        self.test = int(lines[3].split(' ')[-1])
        self.true_monke = int(lines[4].split(' ')[-1])
        self.false_monke = int(lines[5].split(' ')[-1])
        self.inspections = 0

        self.idx = idx
        self.mvals = []
        self.common_test = 1

    def set_common_test(self, common):
        self.common_test = common
        self.mvals = [v % common for v in self.items]

    def apply_op(self, mval):
        if self.op[2] == 'old':
            return (mval ** 2) % self.common_test

        val = int(self.op[2])

        if self.op[1] == '+':
            return (mval + val) % self.common_test
        elif self.op[1] == '*':
            return (mval * val) % self.common_test

    def test_worry(self, mval):
        if mval % self.test == 0:
            return self.true_monke

        return self.false_monke

    def step(self, all_monkes):
        for mval in self.mvals:
            self.inspections += 1
            mval = self.apply_op(mval)
            targ_monke = self.test_worry(mval)
            all_monkes[targ_monke].mvals.append(mval)

        self.mvals = []


def solve(lines):
    monkes = []
    for i, data in enumerate(chunked(lines, 7)):
        monkes.append(Monke(data, i))

    common = 1
    for m in monkes:
        common *= m.test

    for m in monkes:
        m.set_common_test(common)

    for round in range(10000):
        for monke in monkes:
            monke.step(monkes)

    mb = sorted([m.inspections for m in monkes])
    part2 = mb[-1] * mb[-2]

    return None, part2


debug = True
solve_puzzle(year=2022, day=11, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=11, solver=solve, do_sample=False, do_main=True)
