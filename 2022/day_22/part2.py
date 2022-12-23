from utils.common import solve_puzzle
from cube import Cube


def print_face(face):
    face_size = max(x for (x, y) in face) + 1
    for y in range(face_size):
        line = ""
        for x in range(face_size):
            line += face[(x, y)]

        print(line)


def read_faces(face_size, fheight, fwidth, lines):
    faces = {}
    start_found = False

    for fy in range(fheight):
        for fx in range(fwidth):
            face = {}

            no_face = False
            for y in range(0, face_size):
                for x in range(0, face_size):
                    cx = fx * face_size + x
                    cy = fy * face_size + y

                    if cx >= len(lines[cy]):
                        no_face = True
                        break

                    char = lines[cy][cx]
                    if char == ' ':
                        no_face = True
                        break

                    if char == '.' and not start_found:
                        char = 'S'
                        start_found = True

                    face[(x, y)] = char

                if no_face:
                    break

            if not no_face:
                faces[(fx, fy)] = face

    return faces


def read_data(lines, face_size):
    fwidth = max(len(line) for line in lines) // face_size
    fheight = len(lines) // face_size

    faces = read_faces(face_size, fheight, fwidth, lines)
    return Cube(faces, face_size)


def get_instr(instr: str):
    rem_instr = instr
    while rem_instr:
        is_num = rem_instr[0].isdigit()
        cur = rem_instr[0]
        offset = 1
        for c in list(rem_instr[1:]):
            if (is_num and c.isdigit()) or (not is_num and not c.isdigit()):
                cur += c
                offset += 1
            else:
                if cur.isdigit():
                    yield int(cur)
                else:
                    yield cur
                rem_instr = rem_instr[offset:]
                is_num = rem_instr[0].isdigit()
                cur = rem_instr[0]
                offset = 1

        if cur.isdigit():
            yield int(cur)
        else:
            yield cur

        break


def solve(lines):
    # cube = read_data(lines, 4) # Sample
    cube = read_data(lines, 50)  # Final input

    instr = [i for i in get_instr(instr=lines[-1].strip())]

    path_2d, path_3d, facing_idx = cube.follow_instructions(instr)

    # cube.plot_cube(cube.G, path=set(path_3d))

    final_pos = path_2d[-1]
    part2 = final_pos[0] * 1000 + final_pos[1] * 4 + facing_idx

    return None, part2


debug = False
# solve_puzzle(year=2022, day=22, solver=solve, do_sample=True, do_main=False)
solve_puzzle(year=2022, day=22, solver=solve, do_sample=False, do_main=True)
