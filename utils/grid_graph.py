import networkx as nx
import matplotlib.pyplot as plt


class GridGraph:

    def __init__(self, lines):
        self.w, self.h = len(lines[0]), len(lines)
        self.graph = nx.grid_graph((self.h, self.w))

        for x in range(self.w):
            for y in range(self.h):
                c = lines[y][x]
                self.graph.nodes[(x, y)]['char'] = c

    def set_walls(self, walls):
        to_remove = [node for node, att in self.graph.nodes.items() if att['char'] in walls]
        self.graph.remove_nodes_from(to_remove)

    def draw(self, label_name=None):
        """
        Draws the current grid graph. If label_name is set, each nodes attribute with this name is used as the label,
        otherwise the coordinates are used
        """

        pos = {x: x for x in self.graph.nodes.keys()}

        labels = None

        if label_name:
            labels = {node: att[label_name] for node, att in self.graph.nodes.items()}

        nx.draw(self.graph, pos=pos, with_labels=True, labels=labels)
        plt.show()

    def shortest_path(self, start, end, weight_name=None):
        return nx.astar_path(self.graph, start, end, weight = weight_name)
