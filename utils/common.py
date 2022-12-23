from aocd.models import Puzzle
import numpy as np
from joblib import Parallel, delayed

DIR_MAP = {
    'R': np.array((1, 0)),
    'L': np.array((-1, 0)),
    'U': np.array((0, 1)),
    'D': np.array((0, -1)),
}


def solve_puzzle(year, day, solver, do_sample: bool, do_main=False, sample_data_path=None, main_data_path=None):
    puzzle = Puzzle(year=year, day=day)

    # Sample data
    if do_sample:
        print(f"{'Sample':-^20}")

        data = puzzle.example_data.splitlines() if sample_data_path is None else open(sample_data_path).readlines()
        sample_solution_a, sample_solution_b = solver(data)
        print(f"Part 1: {sample_solution_a}")
        print(f"Part 2: {sample_solution_b}")

    if not do_main: return

    # Main input data
    print(f"{'Main input':-^20}")
    data = puzzle.input_data.splitlines() if main_data_path is None else open(main_data_path).readlines()
    part_1, part_2 = solver(data)

    if part_1 is not None:
        print(f"Part 1: {part_1}")
        puzzle.answer_a = part_1
    else:
        print("No part 1 provided")

    if part_2 is not None:
        print(f"Part 2: {part_2}")
        puzzle.answer_b = part_2
    else:
        print("No part 2 provided")


def grid_offsets(diagonals=False):
    straight_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    if diagonals:
        diag_offsets = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        offsets = [0] * 8
        offsets[::2] = straight_offsets
        offsets[1::2] = diag_offsets
        return offsets

    return straight_offsets


def grid_offsets_3d(diagonals=False, corners=False):
    for xoff, yoff in grid_offsets(diagonals):
        yield xoff, yoff, 0

        if diagonals:
            if not (not corners and all(abs(x) == 1 for x in (xoff, yoff))):
                yield xoff, yoff, 1
                yield xoff, yoff, -1

    yield 0, 0, 1
    yield 0, 0, -1


def jobify(func, args, share_mem=False, verbose=False):
    return Parallel(
        n_jobs=-1,
        verbose=10 if verbose else 0,
        require='sharedmem' if share_mem else None
    )(delayed(func)(*arg) for arg in args)
