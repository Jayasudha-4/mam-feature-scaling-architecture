import numpy as np

from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score

from config.model_config import (
    CATBOOST_BINARY_PARAMS,
    CATBOOST_MULTICLASS_PARAMS,
    XGBOOST_BINARY_PARAMS,
    XGBOOST_MULTICLASS_PARAMS,
    VOTING_STRATEGY
)


class HybridEnsembleClassifier:

    def __init__(self, task: str = "binary", num_classes: int = 2):
        self.task = task
        self.label_encoder = LabelEncoder()

        if task == "binary":
            cat_model = CatBoostClassifier(**CATBOOST_BINARY_PARAMS)
            xgb_model = XGBClassifier(**XGBOOST_BINARY_PARAMS)
        else:
            cat_model = CatBoostClassifier(**CATBOOST_MULTICLASS_PARAMS)
            xgb_model = XGBClassifier(num_class=num_classes, **XGBOOST_MULTICLASS_PARAMS)

        self.model = VotingClassifier(
            estimators=[("catboost", cat_model), ("xgboost", xgb_model)],
            voting=VOTING_STRATEGY
        )

    def train(self, X_train, y_train):
        y_enc = self.label_encoder.fit_transform(y_train)
        self.model.fit(X_train, y_enc)

    def predict(self, X):
        y_pred = self.model.predict(X)
        return self.label_encoder.inverse_transform(y_pred)

    def evaluate(self, X_test, y_true) -> dict:
        y_pred = self.predict(X_test)
        if self.task == "binary":
            y_true_enc = self.label_encoder.transform(y_true)
            y_pred_enc = self.label_encoder.transform(y_pred)
            return {
                "accuracy": accuracy_score(y_true_enc, y_pred_enc),
                "f1_score": f1_score(y_true_enc, y_pred_enc)
            }
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(y_true, y_pred, average="macro"),
            "micro_f1": f1_score(y_true, y_pred, average="micro")
        }

    def feature_importances(self, feature_names: list) -> dict:
        
        fitted_cat = self.model.named_estimators_["catboost"]
        fitted_xgb = self.model.named_estimators_["xgboost"]

        try:
            cat_imp = np.array(fitted_cat.get_feature_importance())
        except Exception:
            cat_imp = np.ones(len(feature_names))

        xgb_imp_map = fitted_xgb.get_booster().get_score(importance_type="gain")
        xgb_imp = np.array([xgb_imp_map.get(f"f{i}", 0.0) for i in range(len(feature_names))])

        def _norm(arr):
            arr = np.asarray(arr, dtype=float)
            total = arr.sum()
            return arr / total if total > 0 else np.ones_like(arr) / len(arr)

        avg = (_norm(cat_imp) + _norm(xgb_imp)) / 2.0
        return dict(zip(feature_names, avg.tolist()))
