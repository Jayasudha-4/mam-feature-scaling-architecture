# Environments used for computation evaluation
ENVIRONMENTS = {
    "E1": {"run": "RUN_1", "vcores": 8, "memory_gb": 32},
    "E2": {"run": "RUN_2", "vcores": 16, "memory_gb": 64},
    "E3": {"run": "RUN_3", "vcores": 32, "memory_gb": 128},
}

EXPERIMENT_CONFIG = {
    "runs": ["RUN_1", "RUN_2", "RUN_3"],
    "environments": ENVIRONMENTS,

    "datasets": {
        "AWF_1": ["CBIS-DDSM"],
        "AWF_2": ["CBIS-DDSM", "Vin-Dr Mammo"]
    },

    "kpi_metrics": {
        "RT": "Read Throughput (KEPS)",
        "WT": "Write Throughput (KEPS)",
        "NT": "Node Transition (sec) [From_CG / To_CG]",
        "QL": "Query Latency (ms)"
    },

    "kpi_measurement": {
        "throughput_events_per_run": 6000,
        "query_samples_per_run": 200
    },

    "evaluation": {
        "binary_metrics": ["accuracy"],
        "multiclass_metrics": ["accuracy"]
    }
}