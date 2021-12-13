def fold_func(orig_coord, axis, fold_point):
    out = list(orig_coord)
    out[axis] = fold_point - (orig_coord[axis] - fold_point)
    return tuple(out)


def fold_sheet(sheet: set, axis, coord):
    folded = {pos for pos in sheet if pos[axis] < coord}
    folded.update({fold_func(pos, axis, coord) for pos in sheet if pos[axis] > coord})
    return folded


def read_input(path):
    lines = open(path).readlines()
    lines = [x.strip() for x in lines]
    blank_pos = lines.index('')
    page = lines[:blank_pos]
    instructions = lines[blank_pos + 1:]
    instructions = [(0 if axis == 'x' else 1, int(coord)) for axis, coord in [x.split(' ')[2].split('=') for x in instructions]]
    inputs = {(int(x), int(y)) for x, y in [line.split(',') for line in page]}

    return inputs, instructions


def print_sheet(folded):
    width = max(p[0] for p in folded) + 1
    height = max(p[1] for p in folded) + 1

    lines = [[' ' for x in range(width)] for y in range(height)]

    for x, y in folded:
        lines[y][x] = '#'
    print('\n'.join([''.join(line) for line in lines]))


inputs, instructions = read_input('./input.txt')
folded = inputs
for axis, coord in instructions:
    folded = fold_sheet(folded, axis, coord)
    print(len(folded))

print_sheet(folded)
