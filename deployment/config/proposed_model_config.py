"""
Configuration for the proposed Dynamic Central Graph Framework
"""

PROPOSED_MODEL_CONFIG = {

    # Storage
    "storage_type": "DataLakehouse",
    "supports_multi_dataset": True,

    # Graph properties
    "graph_type": "Dynamic Central Graph",
    "supports_contraction": True,
    "supports_expansion": True,
    "supports_reintegration": True,

    # Normalization & mining
    "normalization_method": "Randomized Min-Cut",
    "subgraph_extraction": "Dynamic",
    "node_integration": "Greedy + Persistence-based",

    # Learning modes
    "classification_modes": [
        "binary",
        "multiclass"
    ],

    # Graph transition tracking
    "track_graph_transitions": True,

    # Persistence parameters
    "persistence": {
        "min_runs": 10,
        "threshold": 0.7
    }
}
