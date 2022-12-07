from aocd.models import Puzzle


def solve_puzzle(year, day, solver, do_sample: bool, do_main=False, data_path=None):
    puzzle = Puzzle(year=year, day=day)

    # Sample data
    if do_sample:
        print(f"{'Sample':-^20}")

        data = puzzle.example_data.splitlines() if data_path is None else open(data_path).readlines()
        sample_solution_a, sample_solution_b = solver(data)
        print(f"Part 1: {sample_solution_a}")
        print(f"Part 2: {sample_solution_b}")

    if not do_main: return

    # Main input data
    print(f"{'Main input':-^20}")
    data = puzzle.input_data.splitlines() if data_path is None else open(data_path).readlines()
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
