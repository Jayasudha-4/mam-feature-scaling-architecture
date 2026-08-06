import numpy as np

from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, f1_score


class BinaryClassifier:
    """
    Binary classifier using CatBoost + XGBoost Ensemble
    (Benign vs Malignant)
    """

    def __init__(self):

        # CatBoost Model
        cat_model = CatBoostClassifier(
            iterations=300,
            learning_rate=0.05,
            depth=6,
            loss_function='Logloss',
            eval_metric='F1',
            random_seed=42,
            verbose=False
        )

        # XGBoost Model
        xgb_model = XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='binary:logistic',
            eval_metric='logloss',
            random_state=42
        )

        # Soft Voting Ensemble
        self.model = VotingClassifier(
            estimators=[
                ('catboost', cat_model),
                ('xgboost', xgb_model)
            ],
            voting='soft'
        )

    def train(self, X_train, y_train):
        """
        Train ensemble classifier
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        """
        Predict class labels
        """
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_true):
        """
        Evaluate performance
        """
        y_pred = self.predict(X_test)

        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "f1_score": f1_score(y_true, y_pred)
        }

    def predict_with_confidence(self, X):
        """
        Returns class probabilities
        """
        return self.model.predict_proba(X)