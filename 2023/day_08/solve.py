from utils.common import solve_puzzle

YEAR = 2023
DAY = 8


def preproc(lines):
    instr = list(lines[0])

    dirmap = {}
    for line in lines[2:]:
        f, _, dirs = line.replace(", ", ",").split(" ")
        left, right = dirs[1:-1].split(",")
        dirmap[f] = (left, right)

    return instr, dirmap


def solve_part_01(instr, dir_maps, cur_pos="AAA"):
    curI = 0
    steps = 0

    while not cur_pos.endswith("Z"):
        left, right = dir_maps[cur_pos]
        if instr[curI] == "L":
            cur_pos = left
        else:
            cur_pos = right

        curI = (curI+1)%len(instr)
        steps += 1

    return steps


def solve_part_02(instr, dir_maps):
    curI = 0
    pos_list = [k for k in dir_maps if k.endswith("A")]

    assert len(pos_list) == len([k for k in dir_maps if k.endswith("Z")])
    steps = 0

    cycles = [[] for _ in pos_list]
    complete_cycles = [False for _ in pos_list]

    # while not sum(complete_cycles) > 1:
    while not all(complete_cycles):
        new_pos = []

        cur_instruction = instr[curI]

        for i, cur_pos in enumerate(pos_list):
            if complete_cycles[i]:
                new_pos.append(cur_pos)
                continue

            if (curI, cur_pos) in cycles[i]:
                complete_cycles[i] = True
                new_pos.append(cur_pos)
                continue
            else:
                cycles[i].append((curI, cur_pos))

            left, right = dir_maps[cur_pos]
            if cur_instruction == "L":
                new_val = left
            else:
                new_val = right

            new_pos.append(new_val)

        pos_list = new_pos
        curI = (curI+1)%len(instr)
        steps += 1

    cycles_clean = []
    offsets = []
    for c in cycles:
        m, last = c[-1]
        next_m = (m+1)%len(instr)
        local_intr = instr[m % len(instr)]
        targ = dir_maps[last][0] if local_intr == "L" else dir_maps[last][1]
        start_pos = c.index((next_m,targ))
        offsets.append(start_pos)
        cycles_clean.append(c[start_pos:])

    cycles = cycles_clean

    for c in cycles:
        print(len([p for d,p in c if p.endswith("Z")]))



    # Condense cycles
    zpos = []
    for cycle in cycles:
        cur_z = [i for i, (j, pos) in enumerate(cycle) if pos.endswith("Z")]
        assert len(cur_z) == 1
        zpos.append(cur_z[0])

    assert len(zpos) == len(cycles)

    largest_step = 0
    step_i = 0

    for i, c in enumerate(cycles):
        print(len(c))
        largest_step = max(len(c), largest_step)
        step_i = i

    # Start pos
    start_step = zpos[step_i] + offsets[step_i]

    rem_offsets = [off for i, off in enumerate(offsets) if i != step_i]

    step = start_step
    remaining_cycles = [c for i, c in enumerate(cycles) if i != step_i]
    positions = [(start_step - off) % len(c) for c, off in zip(remaining_cycles, rem_offsets)]

    zpos.pop(step_i)

    assert len(zpos) == len(positions)
    assert len(zpos) == len(remaining_cycles)
    assert len(zpos) == len(rem_offsets)

    while len(remaining_cycles) > 0:
        done = [False for _ in remaining_cycles]

        for i, cycle in enumerate(remaining_cycles):
            local_pos = (step - rem_offsets[i]) % len(cycle)
            if local_pos == zpos[i]:
                done[i] = True

        if all(done):
            return step

        step += largest_step

    return step


def solve(lines):
    instr, dir_maps = preproc(lines)
    print(instr)
    print(dir_maps)

    part1 = solve_part_01(instr, dir_maps)

    part2 = solve_part_02(instr, dir_maps)

    return part1, part2


debug = True
# solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=True, do_main=False, sample_data_path="test2.txt")
solve_puzzle(year=YEAR, day=DAY, solver=solve, do_sample=False, do_main=True)
