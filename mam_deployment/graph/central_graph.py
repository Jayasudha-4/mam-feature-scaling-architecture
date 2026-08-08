import itertools
import logging

import networkx as nx
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import normalized_mutual_info_score

logger = logging.getLogger("MAM")


class CentralGraph:

    def __init__(self, name: str = "CG"):
        self.name = name
        self.graph = nx.Graph()

    @staticmethod
    def _association(a: pd.Series, b: pd.Series) -> float:
        try:
            return float(normalized_mutual_info_score(a, b))
        except Exception:
            return 0.0

    def build_from_dataframe(self, df: pd.DataFrame, feature_columns: list, dataset_tag: str):
        encoded = {}
        for col in feature_columns:
            if col not in df.columns:
                continue
            if not self.graph.has_node(col):
                self.graph.add_node(col, origin=dataset_tag, kind="feature")
            encoded[col] = LabelEncoder().fit_transform(df[col].astype(str))

        for a, b in itertools.combinations(encoded.keys(), 2):
            weight = self._association(encoded[a], encoded[b])
            if self.graph.has_edge(a, b):
                self.graph[a][b]["weight"] = max(self.graph[a][b]["weight"], weight)
            else:
                self.graph.add_edge(a, b, weight=weight)

        logger.info(
            f"{self.name}: built/updated from '{dataset_tag}' "
            f"-> {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges"
        )
        return self

    def integrate_new_feature(self, feature_name: str, related_features: list,
                               importances: dict, dataset_tag: str):
        self.graph.add_node(feature_name, origin=dataset_tag, kind="derived")
        for feat in related_features:
            if self.graph.has_node(feat):
                weight = float(importances.get(feat, 0.5))
                self.graph.add_edge(feature_name, feat, weight=weight)
        logger.info(f"{self.name}: integrated derived node '{feature_name}' "
                    f"linked to {len(related_features)} feature nodes")
        return self

    def get_graph(self) -> nx.Graph:
        return self.graph

    def copy(self):
        new_graph = CentralGraph(name=self.name)
        new_graph.graph = self.graph.copy()
        return new_graph

    def summary(self) -> dict:
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph) if self.graph.number_of_nodes() > 1 else 0.0
        }
