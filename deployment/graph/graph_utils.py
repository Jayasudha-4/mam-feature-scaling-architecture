import networkx as nx
import time


class GraphUtils:
    """
    Utility functions for graph operations:
    - statistics
    - normalization
    - pruning
    - transitions
    """

    @staticmethod
    def compute_graph_stats(G):
        return {
            "num_nodes": G.number_of_nodes(),
            "num_edges": G.number_of_edges(),
            "density": nx.density(G),
            "connected_components": nx.number_connected_components(G)
        }

    @staticmethod
    def normalize_graph(G):
        """
        Normalizes edge weights between 0 and 1
        """
        max_weight = max(
            [data["weight"] for _, _, data in G.edges(data=True)],
            default=1.0
        )

        for u, v, data in G.edges(data=True):
            data["weight"] /= max_weight

        return G

    @staticmethod
    def prune_edges(G, threshold):
        """
        Remove weak edges based on weight threshold
        """
        removed = 0
        for u, v, data in list(G.edges(data=True)):
            if data.get("weight", 0) < threshold:
                G.remove_edge(u, v)
                removed += 1
        return removed

    @staticmethod
    def measure_graph_transition(start_time):
        """
        Measures graph transition time
        """
        return time.time() - start_time
