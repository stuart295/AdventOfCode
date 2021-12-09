# --- Day 9: Smoke Basin ---
# These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.
#
# If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).
#
# Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:
#
# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.
#
# Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)
#
# In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.
#
# The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.
#
# Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?

# Comment: Proof that you can't assume that Codex will always generate good code
def find_low_points(inputs):
    """
    Takes a 2d list of heights and returns a list of positions for the low points
    """
    low_points = []
    for y in range(len(inputs)):
        for x in range(len(inputs[y])):
            if y == 0:
                if x == 0:
                    if inputs[y][x] < inputs[y][x+1] and inputs[y][x] < inputs[y+1][x]:
                        low_points.append((x,y))
                elif x == len(inputs[y])-1:
                    if inputs[y][x] < inputs[y][x-1] and inputs[y][x] < inputs[y+1][x]:
                        low_points.append((x,y))
                else:
                    if inputs[y][x] < inputs[y][x-1] and inputs[y][x] < inputs[y][x+1] and inputs[y][x] < inputs[y+1][x]:
                        low_points.append((x,y))
            elif y == len(inputs)-1:
                if x == 0:
                    if inputs[y][x] < inputs[y][x+1] and inputs[y][x] < inputs[y-1][x]:
                        low_points.append((x,y))
                elif x == len(inputs[y])-1:
                    if inputs[y][x] < inputs[y][x-1] and inputs[y][x] < inputs[y-1][x]:
                        low_points.append((x,y))
                else:
                    if inputs[y][x] < inputs[y][x-1] and inputs[y][x] < inputs[y][x+1] and inputs[y][x] < inputs[y-1][x]:
                        low_points.append((x,y))
            else:
                if x == 0:
                    if inputs[y][x] < inputs[y][x+1] and inputs[y][x] < inputs[y-1][x] and inputs[y][x] < inputs[y+1][x]:
                        low_points.append((x,y))
                elif x == len(inputs[y])-1:
                    if inputs[y][x] < inputs[y][x-1] and inputs[y][x] < inputs[y-1][x] and inputs[y][x] < inputs[y+1][x]:
                        low_points.append((x,y))
                else:
                    if inputs[y][x] < inputs[y][x-1] and inputs[y][x] < inputs[y][x+1] and inputs[y][x] < inputs[y-1][x] and inputs[y][x] < inputs[y+1][x]:
                        low_points.append((x,y))
    return low_points

def find_risk_level(inputs):
    """
    Takes a 2d list of heights and returns the risk level of the low points
    """
    low_points = find_low_points(inputs)
    risk_level = 0
    for point in low_points:
        risk_level += inputs[point[1]][point[0]] + 1
    return risk_level

with open('./input.txt') as f:
    inputs = f.readlines()
    inputs = [list(map(int, list(x.strip()))) for x in inputs]
    print(find_risk_level(inputs))
    # Part 2 Proved too much for codex (At least when using the raw instructions)