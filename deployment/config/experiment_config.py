"""
Experimental setup and KPI configuration
"""

EXPERIMENT_CONFIG = {

    "runs": ["Run_1", "Run_2", "Run_3"],
    "environments": ["Env_1", "Env_2", "Env_3"],

    "datasets": {
        "AWF_1": ["CBIS-DDSM"],
        "AWF_2": ["CBIS-DDSM", "MIAS", "VinDr-Mammo"]
    },

    "kpi_metrics": {
        "RT": "Read Throughput (KEPS)",
        "WT": "Write Throughput (KEPS)",
        "QL": "Query Latency (ms)",
        "GT": "Graph Transition Time (sec)"
    },

    "graph_params": {
        "theta": 0.8,
        "min_cut_runs": 20,
        "persistence_threshold": 0.7
    },

    "evaluation": {
        "binary_metrics": ["accuracy", "f1_score"],
        "multiclass_metrics": ["accuracy", "macro_f1", "micro_f1"]
    }
}
