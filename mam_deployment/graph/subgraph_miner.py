import logging

import networkx as nx

from graph.central_graph import CentralGraph

logger = logging.getLogger("MAM")


class MinCutSubgraphMiner:

    def __init__(self, central_graph: CentralGraph):
        self.central_graph = central_graph

    def mine(self, required_features: list, weight_threshold: float = 0.0) -> nx.Graph:
        g = self.central_graph.graph
        present = [f for f in required_features if g.has_node(f)]
        if len(present) < 2:
            return g.subgraph(present).copy()

        working = g.subgraph(present).copy()

        try:
            cut_value, (part_a, part_b) = nx.stoer_wagner(working, weight="weight")
        except (nx.NetworkXError, ZeroDivisionError):
            cut_value, (part_a, part_b) = 0.0, (set(present), set())

        retained = set(present)
        if cut_value < weight_threshold:
            retained = part_a if len(part_a) >= len(part_b) else part_b

        mined = g.subgraph(retained).copy()
        logger.info(
            f"MinCutSubgraphMiner: mined {mined.number_of_nodes()}/{len(present)} "
            f"feature nodes (min-cut value={cut_value:.4f})"
        )
        return mined

    def expand_subgraph(self, seed_nodes: list) -> nx.Graph:
        g = self.central_graph.graph
        expanded = set(n for n in seed_nodes if g.has_node(n))
        for n in list(expanded):
            expanded.update(g.neighbors(n))
        return g.subgraph(expanded).copy()
