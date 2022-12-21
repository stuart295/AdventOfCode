from dataclasses import dataclass
from utils.common import solve_puzzle


@dataclass
class Monke:
    number = None
    dep1 = None
    dep2 = None
    op = None
    target = None
    is_human = False

    def set_math(self, parts):
        self.dep1, self.op, self.dep2 = parts

    def has_deps(self):
        return self.dep1 is not None or self.dep2 is not None

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

    def find_target(self, monkes):
        if self.dep1 is None:
            self.number = self.target
            return None

        # Has both
        if monkes[self.dep1].number is not None and monkes[self.dep2].number is not None:
            return self.do_math(monkes)

        # has neither
        if monkes[self.dep1].number is None and monkes[self.dep2].number is None:
            if monkes[self.dep1].is_human:
                return self.dep2
            return self.dep1

        # No target
        if self.target is None:
            if self.is_human:
                return "Return to monke"
            return self.do_math(monkes)

        # Evaluate targets of dependants
        if monkes[self.dep1].number is None:
            monkes[self.dep1].target = self.calc_target(None, monkes[self.dep2].number)
            return self.dep1

        if monkes[self.dep2].number is None:
            monkes[self.dep2].target = self.calc_target(monkes[self.dep1].number, None)
            return self.dep2

    def do_math(self, monkes):
        if monkes[self.dep1].number is None:
            return self.dep1

        val1 = monkes[self.dep1].number

        if monkes[self.dep2].number is None:
            return self.dep2

        val2 = monkes[self.dep2].number

        # Note: Don't try this at home
        self.number = eval(f"{val1}{self.op}{val2}")


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
    stack = [node]

    while stack:
        cur = stack.pop()
        monke = monkes[cur]

        dep = monke.do_math(monkes)

        if dep is not None:
            stack.append(cur)
            stack.append(dep)

    return monkes[node].number


def update_human(monke, monkes):
    if monke.dep1 is None:
        return

    if monkes[monke.dep1].is_human or monkes[monke.dep2].is_human:
        monke.is_human = True


def solve_part_1(lines):
    monkes = read_data(lines)
    return int(reduce('root', monkes))


def solve_part_2(lines):
    monkes = read_data(lines)
    me = 'humn'
    monkes[me].dep1 = None
    monkes[me].dep2 = None
    monkes[me].number = None
    monkes[me].is_human = True

    # Solve one side
    side_val = reduce(monkes['root'].dep2, monkes)

    # Find the other
    other_side = monkes['root'].dep1
    monkes[other_side].target = side_val
    stack = [other_side]
    while stack:
        cur = stack.pop()
        monke = monkes[cur]

        update_human(monke, monkes)

        dep = monke.find_target(monkes)

        if dep is not None and dep != "Return to monke":
            stack.append(cur)
            stack.append(dep)

    return int(monkes[me].number)


def solve(lines):
    part1 = solve_part_1(lines)
    part2 = solve_part_2(lines)

    return part1, part2


debug = True
solve_puzzle(year=2022, day=21, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=21, solver=solve, do_sample=False, do_main=True)
