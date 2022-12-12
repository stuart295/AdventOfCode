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

    def draw(self, label_name=None, path=None):
        """
        Draws the current grid graph. If label_name is set, each nodes attribute with this name is used as the label,
        otherwise the coordinates are used
        """

        pos = {x: x for x in self.graph.nodes.keys()}

        labels = None

        if label_name:
            labels = {node: att[label_name] for node, att in self.graph.nodes.items()}

        nx.draw(self.graph, pos=pos, with_labels=True, labels=labels)

        if path:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(self.graph, pos=pos, edgelist=path_edges, edge_color='r', width=5)
            nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=path, node_color='r')

        plt.show()

    def shortest_path(self, start, end, weights=None):
        return nx.shortest_path(self.graph, start, end, weight = weights)

