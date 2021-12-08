

def calc_life_support_rating(input_list:list):
    """
    Calculates the life support rating of the submarine. input_list is a list of binary strings
    """
    oxygen_generator_rating = calc_rating(input_list, 0)
    co2_scrubber_rating = calc_rating(input_list, 1)
    return oxygen_generator_rating * co2_scrubber_rating

def calc_rating(input_list:list, bit_position:int):
    """
    Calculates the rating of the submarine for a given bit position.
    """
    bit_counts = [0, 0]
    for binary_string in input_list:
        bit_counts[int(binary_string[bit_position])] += 1
    if bit_counts[0] > bit_counts[1]:
        return 0
    elif bit_counts[1] > bit_counts[0]:
        return 1
    else:
        return bit_counts[1]

def parse_input(input_list:list):
    """
    Parses the input list into a list of binary strings.
    """
    return [input_list[i][:7] for i in range(len(input_list))]

def main():
    input_list = open('d3_2_input.txt').readlines()
    binary_strings = parse_input(input_list)
    print(calc_life_support_rating(binary_strings))

if __name__ == "__main__":
    main()
