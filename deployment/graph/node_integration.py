class SubgraphExpander:

    def __init__(self, graph):
        self.graph = graph

    def extract_subgraph(self, nodes):
        return self.graph.subgraph(nodes).copy()

    def expand_subgraph(self, seed_nodes):
        expanded = set(seed_nodes)
        for n in seed_nodes:
            expanded.update(self.graph.neighbors(n))
        return self.graph.subgraph(expanded).copy()
