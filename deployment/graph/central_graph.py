import networkx as nx

class CentralGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node_id, **attrs):
        self.graph.add_node(node_id, **attrs)

    def add_edge(self, u, v, weight=1.0):
        self.graph.add_edge(u, v, weight=weight)

    def get_graph(self):
        return self.graph

    def summary(self):
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph)
        }
