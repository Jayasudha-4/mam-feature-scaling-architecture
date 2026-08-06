"""
Base configuration shared across all modules.
"""

BASE_CONFIG = {
    "project_name": "Breast Cancer Graph Framework",
    "version": "1.0",
    "author": "Research Implementation",
    "random_seed": 42,

    "logging": {
        "level": "INFO",
        "log_dir": "logs/",
        "save_logs": True
    },

    "graph": {
        "directed": False,
        "weighted": True
    }
}
