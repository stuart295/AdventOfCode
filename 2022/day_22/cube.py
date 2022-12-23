import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from utils.common import grid_offsets, grid_offsets_3d
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D


class Cube:

    def __init__(self, faces, face_size, debug=False):
        self.debug = debug
        self.face_size = face_size
        self.raw_faces = faces

        self.points = self.create_blank(face_size)

        self.G = self.to_graph(self.points)

        self.project_faces()

    def create_blank(self, face_size):
        if self.debug:
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')

        top_bot = []
        # Top and bottom

        for x in range(face_size):
            for y in range(face_size):
                top_bot.append((x + 1, y + 1, 0))
                top_bot.append((x + 1, y + 1, face_size + 1))

        if self.debug:
            x = [p[0] for p in top_bot]
            y = [p[1] for p in top_bot]
            z = [p[2] for p in top_bot]

            ax.scatter(x, y, z, c='red')

        # Front and back
        front_back = []
        for x in range(face_size):
            for z in range(face_size):
                front_back.append((x + 1, 0, z + 1))
                front_back.append((x + 1, face_size + 1, z + 1))

        if self.debug:
            x = [p[0] for p in front_back]
            y = [p[1] for p in front_back]
            z = [p[2] for p in front_back]

            ax.scatter(x, y, z, c='green')
        # Sides
        sides = []
        for y in range(face_size):
            for z in range(face_size):
                sides.append((0, y + 1, z + 1))
                sides.append((face_size + 1, y + 1, z + 1))

        if self.debug:
            x = [p[0] for p in sides]
            y = [p[1] for p in sides]
            z = [p[2] for p in sides]

            ax.scatter(x, y, z, c='blue')

            plt.show()
        return top_bot + front_back + sides

    def rotate_forward(self, points, rots):
        r = R.from_rotvec(np.pi / 2 * np.array([rots, 0, 0]))
        return r.apply(points)

    def rotate_side(self, points, rots):
        r = R.from_rotvec(np.pi / 2 * np.array([0, rots, 0]))
        return r.apply(points)

    def draw_points(self, points):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        x = [p[0] for p in points]
        y = [p[1] for p in points]
        z = [p[2] for p in points]

        ax.scatter(x, y, z)
        plt.show()

    def project_faces(self):
        cur_face = list(self.raw_faces.keys())[0]
        seen = {cur_face}

        self.project(self.raw_faces[cur_face], self.G)

        self.plot_cube(self.G, 'char')

        # for ox, oy in grid_offsets():

    def project(self, face, G):
        for point in G.nodes:
            x, y, z = point
            if z != 0:
                continue
            char = face[(x - 1, y - 1)]
            G.nodes[point]['char'] = char

    def to_graph(self, points):
        G = nx.Graph()

        for p in points:
            G.add_node(p, char='$')

        for p in G.nodes:
            x, y, z = p
            for ox, oy, oz in grid_offsets_3d():
                neigh = (x + ox, y + oy, z + oz)
                if neigh in G.nodes:
                    G.add_edge(p, neigh)

            norm = None
            if z == 0:
                norm = (0, 0, -1)
            elif z == self.face_size + 1:
                norm = (0, 0, 1)
            elif x == 0:
                norm = (-1, 0, 0)
            elif x == self.face_size + 1:
                norm = (1, 0, 0)
            elif y == 0:
                norm = (0, -1, 0)
            elif y == self.face_size + 1:
                norm = (0, 1, 0)

            G.nodes[p]['norm'] = norm

        for p in G.nodes:
            x, y, z = p
            norm = G.nodes[p]['norm']
            for ox, oy, oz in grid_offsets_3d(diagonals=True, corners=False):
                neigh = (x + ox, y + oy, z + oz)
                if neigh in G.nodes and G.nodes[neigh]['norm'] != norm:
                    G.add_edge(p, neigh)

        return G

    def plot_cube(self, G, label_name=None):

        # Extract node and edge positions from the layout
        node_xyz = np.array([v for v in sorted(G)])
        edge_xyz = np.array([(u, v) for u, v in G.edges()])

        # Create the 3D figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Plot the nodes - alpha is scaled by "depth" automatically
        ax.scatter(*node_xyz.T, s=100, ec="w")

        # labels
        if label_name:
            labels = [G.nodes[n][label_name] for n in G.nodes]
            for l, n in zip(labels, node_xyz):
                x, y, z = n
                ax.text(x, y, z, l)

        # Plot the edges
        for vizedge in edge_xyz:
            ax.plot(*vizedge.T, color="tab:gray")

        def _format_axes(ax):
            """Visualization options for the 3D axes."""
            # Turn gridlines off
            ax.grid(False)
            # Suppress tick labels
            for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
                dim.set_ticks([])
            # Set axes labels
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")

        _format_axes(ax)
        fig.tight_layout()
        plt.show()
