from utils.common import solve_puzzle


def to_dec(snafu):
    result = 0
    for i, c in enumerate(reversed(snafu)):
        if c == '-':
            result += (5**i) * (-1)
        elif c == '=':
            result += (5**i) * (-2)
        else:
            result += (5 ** i) * int(c)
    return result


def to_snafu(n):
    s = ""

    carry = 0
    while n:
        n, m = divmod(n, 5)

        m += carry
        carry = 0

        if m <= 2:
            s = str(m) + s
        else:
            if m == 3:
                s = '=' + s
            elif m == 4:
                s = '-' + s
            elif m == 5:
                s = '0' + s
            carry = 1

    if carry:
        s = '1' + s

    return s


def solve(lines):
    snafu = [line.strip() for line in lines]

    dec = list(map(to_dec, snafu))
    s = sum(dec)

    part1 = to_snafu(s)
    assert to_dec(part1) == s

    part2 = None

    return part1, part2


debug = True
solve_puzzle(year=2022, day=25, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=25, solver=solve, do_sample=False, do_main=True)
