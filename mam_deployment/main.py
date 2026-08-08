import os
import sys
import logging

from config.base_config import BASE_CONFIG
from config.proposed_model_config import PROPOSED_MODEL_CONFIG

from data_lakehouse.dlh import DataLakehouse
from graph.central_graph import CentralGraph
from graph.subgraph_miner import MinCutSubgraphMiner
from metrics.kpi_evaluator import KPIEvaluator, format_kpi_table

from workflows.awf1_binary import run_awf1
from workflows.awf2_multiclass import run_awf2


def _configure_logging() -> logging.Logger:
    log_dir = BASE_CONFIG["logging"]["log_dir"]
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, BASE_CONFIG["logging"]["log_file"])

    logger = logging.getLogger("MAM")
    logger.setLevel(BASE_CONFIG["logging"]["level"])
    logger.propagate = False
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%H:%M:%S")

        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(fmt)
        logger.addHandler(console_handler)

    return logger


def main():
    logger = _configure_logging()

    logger.info("#" * 80)
    logger.info("# MAM BASE DEPLOYMENT -- DLH -> Central Graph -> AWF-1 -> AWF-2 -> FG")
    logger.info("#" * 80)

    dlh = DataLakehouse(data_dir=BASE_CONFIG["lakehouse"]["data_dir"])
    central_graph = CentralGraph(name="CG")

    awf1_result = run_awf1(dlh, central_graph, PROPOSED_MODEL_CONFIG)
    awf2_result = run_awf2(dlh, central_graph, PROPOSED_MODEL_CONFIG)

    # ---- Computation evaluation: KPIs on the single-dataset (AWF-1) graph ----
    logger.info("=" * 80)
    logger.info("COMPUTATION EVALUATION -- Single Dataset (AWF-1 / CBIS-DDSM)")
    logger.info("=" * 80)
    single_miner = MinCutSubgraphMiner(central_graph)
    single_kpis = KPIEvaluator(central_graph.graph).run_all(
        single_miner, PROPOSED_MODEL_CONFIG["awf1"]["features"]
    )

    # ---- Computation evaluation: KPIs on the multi-dataset (AWF-2 / FG) graph ----
    logger.info("=" * 80)
    logger.info("COMPUTATION EVALUATION -- Multiple Dataset (AWF-2 / CBIS-DDSM + Vin-Dr Mammo)")
    logger.info("=" * 80)
    multi_miner = MinCutSubgraphMiner(central_graph)
    multi_kpis = KPIEvaluator(central_graph.graph).run_all(
        multi_miner, PROPOSED_MODEL_CONFIG["awf2"]["features"]
    )

    # ---- Final summary ----
    logger.info("=" * 80)
    logger.info("FINAL SUMMARY")
    logger.info("=" * 80)
    logger.info(f"AWF-1 (Binary)     -> Accuracy: {awf1_result['metrics']['accuracy']:.4f}  "
                f"(target {PROPOSED_MODEL_CONFIG['awf1']['target_accuracy']})")
    logger.info(f"AWF-2 (BI-RADS)    -> Accuracy: {awf2_result['metrics']['accuracy']:.4f}  "
                f"(target {PROPOSED_MODEL_CONFIG['awf2']['target_accuracy']})")
    logger.info(f"Final Central Graph (FG): {central_graph.summary()}")

    print(format_kpi_table("Single Dataset (AWF-1)", single_kpis))
    print(format_kpi_table("Multiple Dataset (AWF-2)", multi_kpis))

    logger.info(f"Full execution log written to: {os.path.abspath(BASE_CONFIG['logging']['log_dir'])}")

    return {
        "awf1": awf1_result,
        "awf2": awf2_result,
        "central_graph": central_graph,
        "kpis": {"single_dataset": single_kpis, "multiple_dataset": multi_kpis}
    }


if __name__ == "__main__":
    main()
