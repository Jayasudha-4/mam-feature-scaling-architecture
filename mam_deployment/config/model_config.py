CATBOOST_PARAMS = {
    "iterations": 400,
    "learning_rate": 0.05,
    "depth": 6,
    "random_seed": 42,
    "verbose": False
}

CATBOOST_BINARY_PARAMS = {
    **CATBOOST_PARAMS,
    "loss_function": "Logloss",
    "eval_metric": "F1"
}

CATBOOST_MULTICLASS_PARAMS = {
    **CATBOOST_PARAMS,
    "loss_function": "MultiClass",
    "eval_metric": "TotalF1"
}

XGBOOST_PARAMS = {
    "n_estimators": 400,
    "learning_rate": 0.05,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42
}

XGBOOST_BINARY_PARAMS = {
    **XGBOOST_PARAMS,
    "objective": "binary:logistic",
    "eval_metric": "logloss"
}

XGBOOST_MULTICLASS_PARAMS = {
    **XGBOOST_PARAMS,
    "objective": "multi:softprob",
    "eval_metric": "mlogloss"
}

VOTING_STRATEGY = "soft"
