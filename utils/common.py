from aocd.models import Puzzle


def solve_puzzle(year, day, solver, sample_only: bool):
    puzzle = Puzzle(year=year, day=day)

    # Sample data
    print(f"{'Sample':-^20}")
    sample_solution_a, sample_solution_b = solver(puzzle.example_data.splitlines())
    print(f"Part 1: {sample_solution_a}")
    print(f"Part 2: {sample_solution_b}")

    if sample_only: return

    # Main input data
    print(f"{'Main input':-^20}")
    part_1, part_2 = solver(puzzle.input_data.splitlines())

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
