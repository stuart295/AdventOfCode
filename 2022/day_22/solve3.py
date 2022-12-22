from utils.common import solve_puzzle, grid_offsets
import networkx as nx

from utils.grid_graph import GridGraph


def read_data(lines):
    G = GridGraph(lines[:-2])

    start = None

    for y in range(G.h):
        empty = 0
        for x in range(G.w):
            cur_pos = (x, y)
            node = G.graph.nodes[cur_pos]
            G.graph.nodes[cur_pos]['right_edge'] = None
            G.graph.nodes[cur_pos]['left_edge'] = None
            G.graph.nodes[cur_pos]['top_edge'] = None
            G.graph.nodes[cur_pos]['bot_edge'] = None

            col_min = min(i for i, c in enumerate(lines[y]) if c != ' ')
            col_max = max(i for i, c in enumerate(lines[y]) if c != ' ')

        
            if node['char'] == '.':
                if not start:
                    start = (x, y)

                # Right edge
                if x == col_max and G.graph.nodes[(col_min, y)]['char'] == '.':
                    G.graph.nodes[cur_pos]['right_edge'] = (col_min, y)

                # Left edge
                if x == col_min and G.graph.nodes[(col_max, y)]['char'] == '.':
                    G.graph.nodes[cur_pos]['left_edge'] = (col_max, y)

                # if x == G.w - 1 or G.graph.nodes[(x + 1, y)]['char'] == ' ':
                #     for tx in range(x - 1, -1, -1):
                #         if tx == 0 or ((tx, y) in G.graph.nodes and G.graph.nodes[(tx - 1, y)]['char'] == ' '):
                #             G.graph.nodes[cur_pos]['right_edge'] = (tx, y)
                #             break

                # Left edge
                # if x == 0 or G.graph.nodes[(x - 1, y)]['char'] == ' ':
                #     for tx in range(x + 1, G.w):
                #         if tx == G.w - 1 or ((tx, y) in G.graph.nodes and G.graph.nodes[(tx + 1, y)]['char'] == ' '):
                #             G.graph.nodes[cur_pos]['left_edge'] = (tx, y)
                #             break

                # Bottom edge

                # Bot edge
                if y == G.h - 1 or G.graph.nodes[(x, y + 1)]['char'] == ' ':
                    for ty in range(y - 1, -1, -1):
                        if ty == 0 or ((x, ty) in G.graph.nodes and G.graph.nodes[(x, ty - 1)]['char'] == ' '):
                            if G.graph.nodes[(x, ty)]['char'] == '.':
                                G.graph.nodes[cur_pos]['bot_edge'] = (x, ty)
                            break

                # Top edge
                if y == 0 or G.graph.nodes[(x, y - 1)]['char'] == ' ':
                    for ty in range(y + 1, G.h):
                        if ty == G.h - 1 or ((x, ty) in G.graph.nodes and G.graph.nodes[(x, ty + 1)]['char'] == ' '):
                            if G.graph.nodes[(x, ty)]['char'] == '.':
                                G.graph.nodes[cur_pos]['top_edge'] = (x, ty)
                            break

            col = x - empty + 1
            row = y + 1
            node['pos'] = (row, col)


    G.set_walls(' ')
    G.set_walls('#')

    instr = lines[-1].strip()
    return G, instr, start


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


# FACINGS = {
#     'R' : (1, 0),
#     'L' : (-1, 0),
#     'U' : (-1, 0),
#     'D' : (1, 0)
# }

FACINGS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

FACING_ORDER = ['R', 'D', 'L', 'U']


def follow_instructions(instr, start, G):
    face_idx = 0
    facing = FACINGS[face_idx]

    pos = start

    path = [pos]

    for cur_instr in get_instr(instr):
        if debug: print(f"{G.graph.nodes[pos]['pos']} - {cur_instr}")
        if isinstance(cur_instr, str):
            if cur_instr == 'R':
                face_idx = (face_idx + 1) % len(FACINGS)
            else:
                face_idx = (face_idx - 1) % len(FACINGS)
            facing = FACINGS[face_idx]
        else:
            new_pos = pos
            for step in range(cur_instr):
                x, y = new_pos
                fx, fy = facing

                ax, ay = (x + fx, y + fy)

                if fx > 0 and G.graph.nodes[new_pos]['right_edge'] is not None:
                    ax = G.graph.nodes[new_pos]['right_edge'][0]

                elif fx < 0 and G.graph.nodes[new_pos]['left_edge'] is not None:
                    ax = G.graph.nodes[new_pos]['left_edge'][0]

                elif fy > 0 and G.graph.nodes[new_pos]['bot_edge'] is not None:
                    ay = G.graph.nodes[new_pos]['bot_edge'][1]

                elif fy < 0 and G.graph.nodes[new_pos]['top_edge'] is not None:
                    ay = G.graph.nodes[new_pos]['top_edge'][1]

                new_pos = (ax, ay)

                if new_pos in G.graph.nodes:
                    pos = new_pos
                    path.append(pos)
                else:
                    break

    return path, face_idx


def solve(lines):
    G, instr, start = read_data(lines)

    # G.draw(label_name='pos')

    path, final_face = follow_instructions(instr, start, G)

    # G.draw( path=path, node_size=2, hide_labels=True)

    final_pos = path[-1]

    print(final_pos)
    print(G.graph.nodes[final_pos]['pos'])
    final_coord = G.graph.nodes[final_pos]['pos']


    part1 = final_coord[0] * 1000 + final_coord[1] * 4 + final_face
    # part1 = None
    part2 = None

    return part1, part2


debug = False
solve_puzzle(year=2022, day=22, solver=solve, do_sample=True, do_main=False)
# solve_puzzle(year=2022, day=22, solver=solve, do_sample=False, do_main=True)
