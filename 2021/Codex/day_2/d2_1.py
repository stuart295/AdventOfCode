# --- Day 2: Dive! ---
# Now, you need to figure out how to pilot this thing.

# It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

# forward X increases the horizontal position by X units.
# down X increases the depth by X units.
# up X decreases the depth by X units.
# Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

# The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

# forward 5
# down 5
# forward 8
# up 3
# down 8
# forward 2
# Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

# forward 5 adds 5 to your horizontal position, a total of 5.
# down 5 adds 5 to your depth, resulting in a value of 5.
# forward 8 adds 8 to your horizontal position, a total of 13.
# up 3 decreases your depth by 3, resulting in a value of 2.
# down 8 adds 8 to your depth, resulting in a value of 10.
# forward 2 adds 2 to your horizontal position, a total of 15.
# After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

# Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?


def calc_answer(commands:list):
    """
    :param commands: A list of command strings with the first word being one of 'forward', 'up' or 'down' and the second being the amount
    """
    position = 0
    depth = 0
    for command in commands:
        if command.split()[0] == 'forward':
            position += int(command.split()[1])
        elif command.split()[0] == 'up':
            depth += int(command.split()[1])
        elif command.split()[0] == 'down':
            depth -= int(command.split()[1])
        else:
            raise Exception("Invalid command: {}".format(command))
    return position * depth

# read the inputs from d2_1_in.txt and print the result
with open('d2_1_in.txt') as f:
    print(calc_answer(f.readlines()))