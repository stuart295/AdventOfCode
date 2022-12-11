from utils.common import solve_puzzle
from more_itertools import chunked
from collections import deque


class MultiTest:

    def __init__(self, initial, tests):
        self.tests = tests
        self.mods = [initial % t for t in tests]

    def add(self, a):
        self.mods = [(m + a) % t for m, t in zip(self.mods, self.tests)]

    def mult(self, a):
        self.mods = [(m * a) % t for m, t in zip(self.mods, self.tests)]

    def sqr(self):
        self.mods = [(m * m) % t for m, t in zip(self.mods, self.tests)]


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

    def set_multi_test(self, all_tests):
        self.mvals = [MultiTest(v, all_tests) for v in self.items]

    def add_item(self, item):
        self.mvals.append(item)

    def apply_op(self, mval):
        if self.op[2] == 'old':
            mval.sqr()
            return

        val2 = int(self.op[2])

        if self.op[1] == '+':
            mval.add(val2)
        elif self.op[1] == '*':
            mval.mult(val2)

    def test_worry(self, mval):
        if mval.mods[self.idx] == 0:
            return self.true_monke

        return self.false_monke

    def step(self, all_monkes, div_3=True):
        for mval in self.mvals:
            self.inspections += 1
            self.apply_op(mval)
            # if div_3:
            #     cur_worry = cur_worry // 3

            targ_monke = self.test_worry(mval)

            # cur_worry = self.test + cur_worry
            all_monkes[targ_monke].add_item(mval)

        self.mvals = []

def solve(lines):
    # monkes = []
    # for data in chunked(lines, 7):
    #     monkes.append(Monke(data))
    #
    # for round in range(20):
    #     for monke in monkes:
    #         monke.step(monkes)
    #
    # mb = sorted([m.inspections for m in monkes])
    #
    # part1 = mb[-1] * mb[-2]

    # Part 2
    monkes = []
    for i, data in enumerate(chunked(lines, 7)):
        monkes.append(Monke(data, i))

    tests = [m.test for m in monkes]
    for m in monkes:
        m.set_multi_test(tests)

    for round in range(10000):
    # for round in range(20):
        for monke in monkes:
            monke.step(monkes, False)

    mb = sorted([m.inspections for m in monkes])
    print(mb)

    part2 = mb[-1] * mb[-2]

    return None, part2


debug = True
solve_puzzle(year=2022, day=11, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=11, solver=solve, do_sample=False, do_main=True)
