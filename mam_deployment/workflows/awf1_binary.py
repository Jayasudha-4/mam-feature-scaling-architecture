import logging

from sklearn.model_selection import train_test_split

from data_lakehouse.dlh import DataLakehouse
from graph.central_graph import CentralGraph
from graph.subgraph_miner import MinCutSubgraphMiner
from preprocessing.metadata_pipeline import MetadataPreprocessor
from models.ensemble_classifier import HybridEnsembleClassifier

logger = logging.getLogger("MAM")


def run_awf1(dlh: DataLakehouse, central_graph: CentralGraph, config: dict) -> dict:
    awf1_cfg = config["awf1"]

    logger.info("=" * 80)
    logger.info("ANALYTICAL WORKFLOW 1 : CBIS-DDSM Binary Classification (Benign/Malignant)")
    logger.info("=" * 80)

    raw_df = dlh.load_cbis_ddsm(
        awf1_cfg["data_file"], awf1_cfg["synthetic_sample_size"], awf1_cfg["synthetic_seed"]
    )

    # Central graph: nodes = features, edges = relationships
    central_graph.build_from_dataframe(raw_df, awf1_cfg["features"], dataset_tag=awf1_cfg["dataset_name"])

    # Min-cut based subgraph mining -> relevant feature subset
    miner = MinCutSubgraphMiner(central_graph)
    mined_subgraph = miner.mine(awf1_cfg["features"])

    # Metadata pre-processing (quality assessment, dedup, encoding, selection)
    preprocessor = MetadataPreprocessor(
        awf1_cfg["categorical_features"], awf1_cfg["numeric_features"], awf1_cfg["features"]
    )
    processed_df = preprocessor.run(
        raw_df.copy(), id_col=awf1_cfg["id_column"], target_col=awf1_cfg["target_column"]
    )

    X = processed_df[awf1_cfg["features"]]
    y = raw_df[awf1_cfg["target_column"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=awf1_cfg["test_size"], random_state=42, stratify=y
    )

    classifier = HybridEnsembleClassifier(task="binary")
    logger.info("Training CatBoost + XGBoost ensemble for binary classification ...")
    classifier.train(X_train, y_train)
    metrics = classifier.evaluate(X_test, y_test)
    logger.info(f"AWF-1 Binary Classification Accuracy = {metrics['accuracy']:.4f} "
                f"(F1 = {metrics['f1_score']:.4f}), target = {awf1_cfg['target_accuracy']}")

    # Integrate 'diagnosis_status' feature with predicted results -> CG'
    processed_df["diagnosis_status"] = classifier.predict(X)
    importances = classifier.feature_importances(awf1_cfg["features"])
    central_graph.integrate_new_feature(
        awf1_cfg["new_feature"], awf1_cfg["features"], importances, dataset_tag=awf1_cfg["dataset_name"]
    )
    logger.info(f"Central Graph evolved: CG -> CG'  {central_graph.summary()}")

    return {
        "dataframe": processed_df,
        "classifier": classifier,
        "metrics": metrics,
        "mined_subgraph": mined_subgraph,
        "features": awf1_cfg["features"]
    }
