from utils.common import solve_puzzle, grid_offsets
from cube import  Cube
import networkx as nx

from utils.grid_graph import GridGraph

def print_face(face):
    face_size = max(x for (x,y) in face)+1
    for y in range(face_size):
        line = ""
        for x in range(face_size):
            line += face[(x,y)]

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


    # print_face(faces[(1,1)])

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


FACINGS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

FACING_ORDER = ['R', 'D', 'L', 'U']


def follow_instructions(instr, start, G):
    # face_idx = 0
    # facing = FACINGS[face_idx]
    #
    # pos = start
    #
    # path = [pos]
    #
    # for cur_instr in get_instr(instr):
    #     if debug: print(f"{G.graph.nodes[pos]['pos']} - {cur_instr}")
    #     if isinstance(cur_instr, str):
    #         if cur_instr == 'R':
    #             face_idx = (face_idx + 1) % len(FACINGS)
    #         else:
    #             face_idx = (face_idx - 1) % len(FACINGS)
    #         facing = FACINGS[face_idx]
    #     else:
    #         new_pos = pos
    #         for step in range(cur_instr):
    #             x, y = new_pos
    #             fx, fy = facing
    #
    #             ax, ay = (x + fx, y + fy)
    #
    #             if fx > 0 and G.graph.nodes[new_pos]['right_edge'] is not None:
    #                 ax = G.graph.nodes[new_pos]['right_edge'][0]
    #
    #             elif fx < 0 and G.graph.nodes[new_pos]['left_edge'] is not None:
    #                 ax = G.graph.nodes[new_pos]['left_edge'][0]
    #
    #             elif fy > 0 and G.graph.nodes[new_pos]['bot_edge'] is not None:
    #                 ay = G.graph.nodes[new_pos]['bot_edge'][1]
    #
    #             elif fy < 0 and G.graph.nodes[new_pos]['top_edge'] is not None:
    #                 ay = G.graph.nodes[new_pos]['top_edge'][1]
    #
    #             new_pos = (ax, ay)
    #
    #             if new_pos in G.graph.nodes:
    #                 pos = new_pos
    #                 path.append(pos)
    #             else:
    #                 break
    #
    # return path, face_idx
    return None, None


def solve(lines):
    cube = read_data(lines, 4)

    instr = [i for i in get_instr(instr=lines[-1].strip())]

    path = cube.follow_instructions(instr)

    final_pos = path[-1]

    print(final_pos)

    for i in range(4):
        print(final_pos[0] * 1000 + final_pos[1] * 4 + i)

    part2 = None



    # path, final_face = follow_instructions(instr, start, G)

    # G.draw( path=path, node_size=2, hide_labels=True)
    #
    # final_pos = path[-1]
    #
    # print(final_pos)
    # print(G.graph.nodes[final_pos]['pos'])
    # final_coord = G.graph.nodes[final_pos]['pos']
    #
    #
    # part1 = final_coord[0] * 1000 + final_coord[1] * 4 + final_face
    part1 = None
    # part2 = None
    #
    return part1, part2


debug = False
solve_puzzle(year=2022, day=22, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=2022, day=22, solver=solve, do_sample=False, do_main=True)
