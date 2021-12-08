spec_lengths = {2: 1, 3: 7, 4: 4, 7: 8}


def count_special_outputs(inputs):
    spec_count = 0

    for eg, q in inputs:
        spec_count += len([x for x in q if len(x) in spec_lengths])

    return spec_count


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


print(count_special_outputs(read_inputs()))
