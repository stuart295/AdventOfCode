
def solve(path):
    print(f"--{path}--")
    cals = []
    max_cal = 0
    with open(path) as f:
        cur_cals = 0
        for line in f.readlines():
            if line.strip() == '':
                cals.append(cur_cals)
                max_cal = max(max_cal, cur_cals)
                cur_cals = 0
            else:
                cur_cals += int(line.strip())

        cals.append(cur_cals)
        max_cal = max(max_cal, cur_cals)

    s = sorted(cals)
    print(f"Max cals: {max_cal}")
    print(f"Top 3: {sum(s[-3:])}")


solve('sample')
solve('input')