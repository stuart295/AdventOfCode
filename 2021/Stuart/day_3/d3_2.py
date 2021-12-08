import pandas as pd
from collections import Counter


def reduce_values(val_list, sel_func):

    df = pd.DataFrame(val_list)

    for pos in range(df.shape[1]):
        occurances = Counter(df[pos].values)

        digit = sel_func(occurances)

        df = df[df[pos] == digit]

        if df.shape[0] == 1:
            return df.iloc[0].values



def calc_life_support(in_list):
    val_list = [list(x.strip()) for x in in_list]

    # O2 rating
    o2_rating = reduce_values(val_list, lambda counter: max(counter, key=counter.get) if counter['0'] != counter['1'] else '1')
    o2_rating = ''.join(o2_rating)

    # CO2 rating
    co2_rating = reduce_values(val_list, lambda counter: min(counter, key=counter.get) if counter['0'] != counter['1'] else '0')
    co2_rating = ''.join(co2_rating)

    return int(o2_rating, 2) * int(co2_rating, 2)



print(calc_life_support(open('d3_2_input.txt').readlines()))