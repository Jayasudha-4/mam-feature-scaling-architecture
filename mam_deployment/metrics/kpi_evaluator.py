import time
import itertools
import logging
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import networkx as nx

from config.experiment_config import ENVIRONMENTS, EXPERIMENT_CONFIG
from graph.subgraph_miner import MinCutSubgraphMiner

logger = logging.getLogger("MAM")


class KPIEvaluator:

    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def _read_events(self, node):
        _ = dict(self.graph.nodes[node])
        _ = list(self.graph.edges(node, data=True))
        return 1

    def _write_events(self, node):
        self.graph.nodes[node]["_touched"] = time.time()
        return 1

    def measure_throughput(self, vcores: int, n_events: int = None):
        n_events = n_events or EXPERIMENT_CONFIG["kpi_measurement"]["throughput_events_per_run"]
        nodes = list(self.graph.nodes)
        if not nodes:
            self.graph.add_node("_dummy")
            nodes = ["_dummy"]

        cycle = list(itertools.islice(itertools.cycle(nodes), n_events))

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=vcores) as pool:
            list(pool.map(self._read_events, cycle))
        read_elapsed = time.perf_counter() - start
        rt_keps = (n_events / read_elapsed) / 1000.0

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=vcores) as pool:
            list(pool.map(self._write_events, cycle))
        write_elapsed = time.perf_counter() - start
        wt_keps = (n_events / write_elapsed) / 1000.0

        return round(rt_keps, 2), round(wt_keps, 2)

    def measure_query_latency(self, vcores: int, n_queries: int = None) -> float:
        n_queries = n_queries or EXPERIMENT_CONFIG["kpi_measurement"]["query_samples_per_run"]
        nodes = list(self.graph.nodes)
        if not nodes:
            return 0.0
        rng = np.random.default_rng(0)
        sample_nodes = rng.choice(nodes, size=min(n_queries, len(nodes) * 5), replace=True)

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=vcores) as pool:
            list(pool.map(lambda n: nx.single_source_shortest_path_length(self.graph, n, cutoff=2),
                           sample_nodes))
        elapsed = time.perf_counter() - start
        return round((elapsed / len(sample_nodes)) * 1000.0, 2)

    def measure_node_transition(self, subgraph_miner: MinCutSubgraphMiner, required_features: list):
        start = time.perf_counter()
        mined = subgraph_miner.mine(required_features)
        from_cg = time.perf_counter() - start

        start = time.perf_counter()
        _ = nx.compose(self.graph, mined)
        to_cg = time.perf_counter() - start

        return round(from_cg, 4), round(to_cg, 4)

    def run_all(self, subgraph_miner: MinCutSubgraphMiner, required_features: list) -> dict:
        results = {"RT_KEPS": {}, "WT_KEPS": {}, "QL_MS": {}, "NT_SEC": {}}
        nt_from, nt_to = [], []

        for env_id, env in ENVIRONMENTS.items():
            rt, wt = self.measure_throughput(env["vcores"])
            ql = self.measure_query_latency(env["vcores"])
            f_cg, t_cg = self.measure_node_transition(subgraph_miner, required_features)

            results["RT_KEPS"][env["run"]] = rt
            results["WT_KEPS"][env["run"]] = wt
            results["QL_MS"][env["run"]] = ql
            nt_from.append(f_cg)
            nt_to.append(t_cg)

            logger.info(
                f"KPI [{env_id} | {env['vcores']}vCores/{env['memory_gb']}GB | {env['run']}] "
                f"RT={rt} KEPS, WT={wt} KEPS, QL={ql} ms, "
                f"NT(From_CG)={f_cg}s, NT(To_CG)={t_cg}s"
            )

        results["NT_SEC"]["From_CG"] = round(float(np.mean(nt_from)), 4)
        results["NT_SEC"]["To_CG"] = round(float(np.mean(nt_to)), 4)
        return results


def format_kpi_table(title: str, measured: dict, reference: dict) -> str:
    lines = [f"\n--- {title} ---",
             f"{'Metric':<22}{'Run':<10}{'Measured':<12}{'Reference':<10}"]
    for metric in ["RT_KEPS", "WT_KEPS"]:
        for run in ["RUN_1", "RUN_2", "RUN_3"]:
            lines.append(f"{metric:<22}{run:<10}{measured[metric][run]:<12}{reference[metric][run]:<10}")
    for key in ["From_CG", "To_CG"]:
        lines.append(f"{'NT_SEC':<22}{key:<10}{measured['NT_SEC'][key]:<12}{reference['NT_SEC'][key]:<10}")
    for run in ["RUN_1", "RUN_2", "RUN_3"]:
        lines.append(f"{'QL_MS':<22}{run:<10}{measured['QL_MS'][run]:<12}{reference['QL_MS'][run]:<10}")
    return "\n".join(lines)
