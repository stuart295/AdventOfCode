from collections import Counter

spec_lengths = {2: 1, 3: 7, 4: 4, 7: 8}

truth_map = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}


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


def find_uniques(displays):
    uniques = {}
    for d in displays:
        num = spec_lengths.get(len(d))
        if num is not None:
            uniques[num] = d

    return uniques


def decode_query(query, mappings):
    result = ''

    for disp in query:
        decoded = ''.join(sorted([mappings[x] for x in disp]))
        result += str(truth_map[decoded])

    return int(result)


def decode_segment(eg, query):
    uniques = find_uniques(eg)
    mappings = {}

    # Find mapping for a
    diff = [x for x in uniques[7] if x not in uniques[1]][0]
    mappings[diff] = 'a'

    seg_counts = Counter()
    for disp in eg:
        seg_counts.update(list(disp))

    count_map = {
        6: 'b',
        4: 'e',
        9: 'f'
    }

    for c, count in seg_counts.items():
        if count == 8:
            if c not in mappings:
                mappings[c] = 'c'
        elif count == 7:
            if c in uniques[4]:
                mappings[c] = 'd'
            else:
                mappings[c] = 'g'
        else:
            mappings[c] = count_map[count]

    # Decode query
    return decode_query(query, mappings)


def decode_segments(inputs):
    total = 0
    for eg, q in inputs:
        total += decode_segment(eg, q)

    return total


print(decode_segments(read_inputs()))
