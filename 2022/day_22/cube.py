import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R


class Cube:

    def __init__(self, faces, face_size):
        self.face_size = face_size
        self.raw_faces = faces

        self.points = self.create_blank(face_size)

        self.project_faces()

    def create_blank(self, face_size):
        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        top_bot = []
        # Top and bottom
        offset = 0.5
        for x in range(face_size):
            for y in range(face_size):
                top_bot.append((x + offset, y + offset, 0))
                top_bot.append((x + offset, y + offset, face_size))
        # x = [p[0] for p in top_bot]
        # y = [p[1] for p in top_bot]
        # z = [p[2] for p in top_bot]
        #
        # ax.scatter(x, y, z, c='red')
        # Front and back
        front_back = []
        for x in range(face_size):
            for z in range(face_size):
                front_back.append((x + offset, 0, z + offset))
                front_back.append((x + offset, face_size, z + offset))
        # x = [p[0] for p in front_back]
        # y = [p[1] for p in front_back]
        # z = [p[2] for p in front_back]
        #
        # ax.scatter(x, y, z, c='green')
        # Sides
        sides = []
        for y in range(face_size):
            for z in range(face_size):
                sides.append((0, y + offset, z + offset))
                sides.append((face_size, y + offset, z + offset))
        # x = [p[0] for p in sides]
        # y = [p[1] for p in sides]
        # z = [p[2] for p in sides]
        #
        # ax.scatter(x, y, z, c='blue')
        #
        # plt.show()
        return top_bot + front_back + sides

    def rotate_forward(self, points, rots):
        r = R.from_rotvec(np.pi/2 * np.array([rots, 0, 0]))
        return r.apply(points)

    def rotate_side(self, points, rots):
        r = R.from_rotvec(np.pi/2 * np.array([0, rots, 0]))
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
        pass

