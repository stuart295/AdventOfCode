import re
from functools import lru_cache

from utils.common import solve_puzzle, in_bounds
import numpy as np

YEAR = 2025
DAY = 8

def connect_boxes(boxes, distances, con_count):
    circuits = [{box} for box in boxes]
    circuit_map = {box:i for i, box in enumerate(boxes)}

    dist_tuples_sorted = sorted(distances.items(), key=lambda x: x[1])

    connections = 0

    for (b1, b2), _ in dist_tuples_sorted:
        # Merge circuits
        b1_cidx = circuit_map[b1]
        b2_cidx = circuit_map[b2]

        connections += 1

        if b1_cidx != b2_cidx:
            # Merge 2nd into 1st
            circuits[b1_cidx].update(circuits[b2_cidx])

            # Clear second
            for b in circuits[b2_cidx]:
                circuit_map[b] = b1_cidx

            circuits[b2_cidx] = set()

            # For part 2 - All circuits now connected?
            if len(circuits[b1_cidx]) == len(boxes):
                return b1[0]*b2[0]

        if connections >= con_count:
            break

    circuit_sizes = sorted([len(c) for c in circuits], reverse=True)
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]



def solve(lines):

    boxes = [tuple([int(x) for x in line.split(',')]) for line in lines]

    print("Computing distance matrix...")
    distances = {}
    for b1 in boxes:
        for b2 in boxes:
            if b1 != b2 and (b1, b2) not in distances and (b2, b1) not in distances:
                distances[(b1, b2)] = np.linalg.norm(np.array(b1) - np.array(b2))

    print("Solving...")
    if len(lines) == 20:
        part1 = connect_boxes(boxes, distances, 10)
    else:
        part1 = connect_boxes(boxes, distances, 1000)

    part2 = connect_boxes(boxes, distances, np.inf)

    return part1, part2


solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, autoclean=False)
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True, autoclean=False)
