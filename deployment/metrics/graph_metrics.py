import networkx as nx
import numpy as np


class GraphMetrics:

    @staticmethod
    def graph_transition_metrics(G_before, G_after, transition_time):
        return {
            "nodes_before": G_before.number_of_nodes(),
            "nodes_after": G_after.number_of_nodes(),
            "edges_before": G_before.number_of_edges(),
            "edges_after": G_after.number_of_edges(),
            "node_growth": G_after.number_of_nodes() - G_before.number_of_nodes(),
            "edge_growth": G_after.number_of_edges() - G_before.number_of_edges(),
            "transition_time_sec": transition_time
        }

    @staticmethod
    def graph_density_change(G_before, G_after):
        return {
            "density_before": nx.density(G_before),
            "density_after": nx.density(G_after),
            "delta_density": nx.density(G_after) - nx.density(G_before)
        }

    @staticmethod
    def persistence_score(history):
        """
        history = [{node: 0/1}, {node: 0/1}, ...]
        """
        persistence = {}
        R = len(history)

        for node in history[0]:
            persistence[node] = sum(h[node] for h in history) / R

        return persistence
