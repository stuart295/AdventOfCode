

spec_lengths = {2:1, 3:7, 4:4, 7:8}


def count_special_outputs(inputs):
    spec_count = 0

    for eg, q in inputs:
        spec_count += len([x for x in q if len(x) in spec_lengths])

    return spec_count


def find_uniques(displays):
    uniques = {}
    for d in displays:
        num = spec_lengths.get(len(d))
        if num is not None:
            uniques[num] = d

    return uniques


def read_inputs():
    out = []
    with open('input.txt') as f:
        lines = f.readlines()

    for line in lines:
        examples, query = line.strip().split('|')
        examples = examples.strip().split(' ')
        query = query.strip().split(' ')
        out.append((examples, query))
    return out




def decode_segment(eg, query):
    uniques = find_uniques(eg)
    mappings = {}


    # Find mapping for a
    diff = [x for x in uniques[7] if x not in uniques[1]][0]
    mappings[diff] = 'a'

    # Find right side
    right_side = [x for x in uniques[7] if x in uniques[1]]

    # Find center
    center = [x for x in uniques[4] if x not in uniques[7]]

    # Find bottom
    bottom = [x for x in uniques[8] if x not in uniques[7] and x not in uniques[4]]

    # Deduce 9
    for disp in eg:
        if all(x in disp for x in right_side) and all (x in disp for x in center) and len([x in disp for x in bottom]) == 1:
            uniques[9] = disp



    return 0


def decode_segments(inputs):
    total = 0
    for eg, q in inputs:
        total += decode_segment(eg, q)

print(count_special_outputs(read_inputs()))

print(decode_segments(read_inputs()))