from dataclasses import dataclass
from utils.common import solve_puzzle


@dataclass
class Monke:
    number = None
    dep1 = None
    dep2 = None
    op = None
    target = None

    def set_math(self, parts):
        self.dep1, self.op, self.dep2 = parts

    def calc_target(self, a, b):
        if self.op == '+':
            if a is not None:
                return self.target - a
            else:
                return self.target - b

        if self.op == '*':
            if a is not None:
                return self.target / a
            else:
                return self.target / b

        if self.op == '-':
            if a is not None:
                return a - self.target
            else:
                return self.target + b

        if self.op == '/':
            if a is not None:
                return a / self.target
            else:
                return self.target * b


def read_data(lines):
    monkes = {}
    for line in lines:
        split = line.strip().split(': ')
        mname = split[0]
        monke = Monke()
        right = split[1].split(' ')
        if len(right) == 1:
            monke.number = int(right[0])
        else:
            monke.set_math(right)

        monkes[mname] = monke

    return monkes


def reduce(node, monkes):
    cur = monkes[node]

    if cur.dep1 is None:
        return cur.number

    val1 = reduce(cur.dep1, monkes)
    val2 = reduce(cur.dep2, monkes)

    return eval(f"{val1}{cur.op}{val2}")


def retry(cur, val1, val2, monkes, side):
    if cur.target is None: return None
    monkes[side].target = cur.calc_target(val1, val2)
    return solve_target(side, monkes)


def solve_target(node, monkes):
    cur = monkes[node]

    if cur.dep1 is None:
        if cur.number is None:
            return cur.target
        return cur.number

    val1 = solve_target(cur.dep1, monkes)
    val2 = solve_target(cur.dep2, monkes)

    if val1 is None and val2 is not None:
        val1 = retry(cur, val1, val2, monkes, cur.dep1)
    elif val2 is None and val1 is not None:
        val1 = retry(cur, val1, val2, monkes, cur.dep2)

    if not val1 or not val2:
        return None

    return eval(f"{val1}{cur.op}{val2}")


def solve_part_1(lines):
    monkes = read_data(lines)
    return int(reduce('root', monkes))


def solve_part_2(lines):
    monkes = read_data(lines)
    me = 'humn'
    monkes[me].dep1 = None
    monkes[me].dep2 = None
    monkes[me].number = None

    one_side = reduce(monkes['root'].dep2, monkes)
    monkes[monkes['root'].dep1].target = one_side

    solve_target(monkes['root'].dep1, monkes)

    return int(monkes[me].target)


def solve(lines):
    part1 = solve_part_1(lines)
    part2 = solve_part_2(lines)

    return part1, part2


debug = True

solve_puzzle(year=2022, day=21, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=21, solver=solve, do_sample=False, do_main=True)
