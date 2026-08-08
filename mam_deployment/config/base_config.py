BASE_CONFIG = {
    "project_name": "MAM",
    "version": "1.0",
    "author": "Research Implementation",
    "random_seed": 42,

    "logging": {
        "level": "INFO",
        "log_dir": "logs/",
        "log_file": "mam_deployment.log",
        "save_logs": True
    },

    "graph": {
        "directed": False,
        "weighted": True
    },

    "lakehouse": {
        "name": "DLH",
        "data_dir": "data/",
        "cbis_ddsm_file": "cbis_ddsm_metadata.csv",
        "vindr_mammo_file": "vindr_mammo_metadata.csv"
    }
}
