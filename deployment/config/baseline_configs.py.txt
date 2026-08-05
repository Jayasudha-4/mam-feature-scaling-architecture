"""
Baseline system configurations for comparison
"""

# ------------------------------
# PIMBeam
# ------------------------------
PIMBEAM_CONFIG = {
    "model": "PIMBeam",
    "storage": "Persistent Memory",
    "graph_type": "Static",
    "supports_dynamic_updates": False,
    "supports_subgraph": False,
    "rebuild_required": True,
    "read_write_model": "Direct",
    "graph_transition": False
}

# ------------------------------
# Grast
# ------------------------------
GRAST_CONFIG = {
    "model": "Grast",
    "graph_type": "Static Graph",
    "supports_pattern_mining": True,
    "dynamic_update": False,
    "supports_expansion": False,
    "graph_rebuild": True
}

# ------------------------------
# HUSM
# ------------------------------
HUSM_CONFIG = {
    "model": "HUSM",
    "storage": ["RDBMS", "NoSQL", "FileSystem"],
    "integration": "Multi-DB",
    "graph_support": "Partial",
    "dynamic_graph": False,
    "dependency_overhead": "High"
}
