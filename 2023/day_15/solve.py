from utils.common import solve_puzzle

YEAR = 2023
DAY = 15


def do_hash(s):
    value = 0
    for c in s:
        value = ((value + ord(c)) * 17)%256

    return value


def solve_part_02(seq):
    boxes = [{} for i in range(256)]

    for s in seq:
        if "=" in s:
            label, focal_len = s.split("=")
            box_num = do_hash(label)
            box = boxes[box_num]
            box[label] = int(focal_len)
        else:
            label = s.replace("-", "")
            box_num = do_hash(label)
            box = boxes[box_num]
            if label in box:
                box.pop(label)

    fp = 0
    for i, box in enumerate(boxes):
        for j, (label, f) in enumerate(box.items()):
            fp += (i+1)*(j+1)*f

    return fp




def solve(lines):
    seq = lines[0].split(",")
    part1 = sum(do_hash(s) for s in seq)
    part2 = solve_part_02(seq)

    return part1, part2


debug = True
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
