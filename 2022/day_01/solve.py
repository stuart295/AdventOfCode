
def solve(path):
    print(f"--{path}--")
    cals = []
    with open(path) as f:
        cur_cals = 0
        for line in f:
            if line.strip() == '':
                cals.append(cur_cals)
                cur_cals = 0
            else:
                cur_cals += int(line.strip())

        cals.append(cur_cals)

    s = sorted(cals)
    print(f"Max cals: {s[-1]}")
    print(f"Top 3: {sum(s[-3:])}")


solve('sample')
solve('input')