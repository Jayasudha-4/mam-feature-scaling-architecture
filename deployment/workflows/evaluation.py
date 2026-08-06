from metrics.kpi_metrics import compute_kpis
from metrics.graph_metrics import GraphMetrics
import time


class Evaluator:

    def __init__(self, logger):
        self.logger = logger

    def evaluate_graph_transition(self, G_before, G_after):
        start = time.time()
        transition_time = time.time() - start

        return GraphMetrics.graph_transition_metrics(
            G_before, G_after, transition_time
        )

    def evaluate_pipeline(self, G_before, G_after,
                          read_ops, write_ops,
                          y_true=None, y_pred=None):

        self.logger.info("Starting evaluation...")

        kpis = compute_kpis(
            start_time=time.time() - 1,
            end_time=time.time(),
            read_ops=read_ops,
            write_ops=write_ops
        )

        graph_stats = GraphMetrics.graph_transition_metrics(
            G_before, G_after, kpis["QL"]
        )

        results = {
            "KPI": kpis,
            "GraphMetrics": graph_stats
        }

        self.logger.info(f"Evaluation Results: {results}")
        return results
