from utils.common import solve_puzzle
from more_itertools import chunked
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

        self.items_mod = [divmod(x, self.test) for x in self.items]

    def add_item(self, item):
        self.items_mod.append(divmod(item, self.test))

    def apply_op(self, d, r):
        val2 = r if self.op[2] == 'old' else int(self.op[2])

        if self.op[1] == '+':
            out = divmod((r + val2), self.test)
            out_d, out_r = d + out[0], out[1]
            assert out_d * self.test + out_r == (d * self.test + r)  + val2
            return out_d, out_r
        elif self.op[1] == '*':
            if self.op[2] == 'old':
                out_d, out_r = (d * d * self.test + 2 * d * r), r * r
                ed, out_r = divmod(out_r, self.test)
                out_d += ed

                assert out_d* self.test + out_r == (d*self.test + r)**2
                return out_d, out_r
            else:
                ed, out_r = divmod(r * val2, self.test)
                out_d = d * val2 + ed
                assert out_d * self.test + out_r == (d * self.test + r) * val2
                return out_d, out_r

        raise Exception("Op not implemented!")


# (xT + y) * (xT + y)
#
# = xT*xT + 2xT*y + y*y
#
# = T(x*x + 2xy) + y*y
#
#
# = xT*vT + vT*y + xT*b + y*b
# = T(x*v + v*y + x*b) + y*b
#
# (xT * y)B
#
# =
#
#
# 5 % 2 = 2, 1
#
# 2 % 2 = 1, 0
#
# 5 * 10 = 10


    def test_worry(self, worry):
        if worry == 0:
            return self.true_monke

        return self.false_monke


    def step(self, all_monkes, div_3=True):
        for item_mod in self.items_mod:
            d, r = item_mod

            self.inspections += 1
            d, r = self.apply_op(d, r)
            # if div_3:
            #     cur_worry = cur_worry // 3

            targ_monke = self.test_worry(r)

            cur_worry = self.test * d + r


            all_monkes[targ_monke].add_item(cur_worry)

        self.items_mod = deque()


# m1: test = 3
# m2: test = 2
#
# m1: 3 -> 0
# passes 3+0
# m2: 3 -> 1


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
    for data in chunked(lines, 7):
        monkes.append(Monke(data))

    for round in range(10000):
        for monke in monkes:
            monke.step(monkes, False)

    mb = sorted([m.inspections for m in monkes])
    print(mb)

    part2 = mb[-1] * mb[-2]

    return None, part2


debug = True
solve_puzzle(year=2022, day=11, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=2022, day=11, solver=solve, do_sample=False, do_main=True)
