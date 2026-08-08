import logging

from sklearn.model_selection import train_test_split

from data_lakehouse.dlh import DataLakehouse
from graph.central_graph import CentralGraph
from graph.subgraph_miner import MinCutSubgraphMiner
from preprocessing.metadata_pipeline import MetadataHarmonizer
from models.ensemble_classifier import HybridEnsembleClassifier

logger = logging.getLogger("MAM")


def run_awf2(dlh: DataLakehouse, central_graph: CentralGraph, config: dict) -> dict:
    awf2_cfg = config["awf2"]

    logger.info("=" * 80)
    logger.info("ANALYTICAL WORKFLOW 2 : CBIS-DDSM + Vin-Dr Mammo -> BI-RADS Classification")
    logger.info("=" * 80)

    raw_df = dlh.load_vindr_mammo(
        awf2_cfg["data_file"], awf2_cfg["synthetic_sample_size"], awf2_cfg["synthetic_seed"]
    )

    # Metadata harmonization: schema mapping, standardization, missing
    # values, categorical normalization, feature selection
    harmonizer = MetadataHarmonizer(
        awf2_cfg["schema_map"], awf2_cfg["categorical_features"],
        awf2_cfg["numeric_features"], awf2_cfg["features"]
    )
    harmonized_df = harmonizer.run(
        raw_df.copy(), id_col=awf2_cfg["id_column"], target_col=awf2_cfg["target_column"]
    )

    # Fold the harmonized Vin-Dr Mammo features into the Central Graph
    renamed_raw = raw_df.rename(columns={k: v for k, v in awf2_cfg["schema_map"].items()
                                          if k in raw_df.columns})
    central_graph.build_from_dataframe(renamed_raw, awf2_cfg["features"], dataset_tag=awf2_cfg["dataset_name"])

    # Dynamic subgraph expansion via min-cut -> BI-RADS relevant feature set
    miner = MinCutSubgraphMiner(central_graph)
    mined_subgraph = miner.mine(awf2_cfg["features"])

    y = raw_df[awf2_cfg["target_column"]]
    X = harmonized_df[awf2_cfg["features"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=awf2_cfg["test_size"], random_state=42, stratify=y
    )

    classifier = HybridEnsembleClassifier(task="multiclass", num_classes=y.nunique())
    logger.info("Training CatBoost + XGBoost ensemble for BI-RADS classification ...")
    classifier.train(X_train, y_train)
    metrics = classifier.evaluate(X_test, y_test)
    logger.info(f"AWF-2 BI-RADS Classification Accuracy = {metrics['accuracy']:.4f} "
                f"(macro-F1 = {metrics['macro_f1']:.4f}), target = {awf2_cfg['target_accuracy']}")

    # Integrate 'diagnostic_details' feature -> Final Central Graph (FG)
    harmonized_df["diagnostic_details"] = classifier.predict(X)
    importances = classifier.feature_importances(awf2_cfg["features"])
    central_graph.integrate_new_feature(
        awf2_cfg["new_feature"], awf2_cfg["features"], importances,
        dataset_tag=f"CBIS-DDSM+{awf2_cfg['dataset_name']}"
    )
    logger.info(f"Central Graph evolved: CG' -> FG (Final Central Graph) {central_graph.summary()}")

    return {
        "dataframe": harmonized_df,
        "classifier": classifier,
        "metrics": metrics,
        "mined_subgraph": mined_subgraph,
        "features": awf2_cfg["features"]
    }
