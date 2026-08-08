PROPOSED_MODEL_CONFIG = {

    # Storage
    "storage_type": "DataLakehouse",
    "supports_multi_dataset": True,

    # Graph properties
    "graph_type": "Dynamic Central Graph",
    "supports_contraction": True,
    "supports_expansion": True,
    "supports_reintegration": True,

    # Subgraph mining / normalization
    "subgraph_mining_method": "Min-Cut Based Expansion",
    "node_integration": "Incremental Graph Evolution",

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
    },

    # ------------------------------------------------------------------
    # AWF-1: CBIS-DDSM binary classification (Benign / Malignant)
    #   CG -> CG'
    # ------------------------------------------------------------------
    "awf1": {
        "dataset_name": "CBIS-DDSM",
        "data_file": "cbis_ddsm_metadata.csv",
        "id_column": "patient_id",
        "target_column": "pathology",

        # Central graph nodes / relevant feature subset mined via min-cut
        "features": [
            "breast_density",
            "shape",
            "margin",
            "calcification_type",
            "calcification_distribution",
            "laterality",
            "view"
        ],
        "categorical_features": [
            "shape",
            "margin",
            "calcification_type",
            "calcification_distribution",
            "laterality",
            "view"
        ],
        "numeric_features": [
            "breast_density"
        ],

        "new_feature": "diagnosis_status",
    },

    # ------------------------------------------------------------------
    # AWF-2: CBIS-DDSM + Vin-Dr Mammo -> BI-RADS multi-class classification
    #   CG' -> FG (Final Central Graph)
    # ------------------------------------------------------------------
    "awf2": {
        "dataset_name": "Vin-Dr Mammo",
        "data_file": "vindr_mammo_metadata.csv",
        "id_column": "study_id",
        "target_column": "birads",

        "features": [
            "breast_density",
            "laterality",
            "view_position",
            "lesion_type",
            "mass_shape",
            "mass_margins",
            "calcification_type",
            "calcification_distribution"
        ],
        "categorical_features": [
            "laterality",
            "view_position",
            "lesion_type",
            "mass_shape",
            "mass_margins",
            "calcification_type",
            "calcification_distribution"
        ],
        "numeric_features": [
            "breast_density"
        ],

        # Schema mapping: Vin-Dr Mammo raw column -> harmonized canonical column
        "schema_map": {
            "breast density": "breast_density",
            "view": "view_position",
            "finding_categories": "lesion_type",
            "mass_margin": "mass_margins"
        },

        "new_feature": "diagnostic_details",
        "test_size": 0.2
    }
}
