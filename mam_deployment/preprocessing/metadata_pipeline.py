import logging

import pandas as pd
from sklearn.preprocessing import LabelEncoder

logger = logging.getLogger("MAM")


class MetadataPreprocessor:
    
    def __init__(self, categorical_features: list, numeric_features: list, feature_order: list):
        self.categorical_features = categorical_features
        self.numeric_features = numeric_features
        self.feature_order = feature_order
        self.encoders = {}

    def run(self, df: pd.DataFrame, id_col: str, target_col: str) -> pd.DataFrame:
        n_before = len(df)
        missing = df.isnull().sum().sum()
        logger.info(f"Preprocessing: quality assessment -> {n_before} records, "
                    f"{int(missing)} missing values")

        df = df.drop_duplicates().reset_index(drop=True)
        logger.info(f"Preprocessing: duplicate removal -> {n_before - len(df)} duplicates dropped")

        for col in self.numeric_features:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        for col in self.categorical_features:
            if col in df.columns:
                mode = df[col].mode()
                df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else "UNKNOWN")

        keep_cols = [c for c in [id_col] if c in df.columns]
        keep_cols += [c for c in self.feature_order if c in df.columns]
        if target_col in df.columns:
            keep_cols.append(target_col)
        df = df[keep_cols].copy()
        logger.info(f"Preprocessing: relative feature selection -> {self.feature_order}")

        for col in self.categorical_features:
            if col in df.columns:
                enc = LabelEncoder()
                df[col] = enc.fit_transform(df[col].astype(str))
                self.encoders[col] = enc
        logger.info("Preprocessing: categorical feature encoding complete")

        return df


class MetadataHarmonizer:

    def __init__(self, schema_map: dict, categorical_features: list,
                 numeric_features: list, feature_order: list):
        self.schema_map = schema_map
        self.categorical_features = categorical_features
        self.numeric_features = numeric_features
        self.feature_order = feature_order
        self.encoders = {}

    def run(self, df: pd.DataFrame, id_col: str, target_col: str) -> pd.DataFrame:
        rename_map = {k: v for k, v in self.schema_map.items() if k in df.columns}
        df = df.rename(columns=rename_map)
        logger.info(f"Harmonization: schema mapping applied -> {rename_map}")

        for col in self.categorical_features:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
        logger.info("Harmonization: attribute standardization complete")

        for col in self.numeric_features:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        for col in self.categorical_features:
            if col in df.columns:
                mode = df[col].mode()
                df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else "UNKNOWN")
        logger.info("Harmonization: missing value handling complete")

        keep_cols = [c for c in [id_col] if c in df.columns]
        keep_cols += [c for c in self.feature_order if c in df.columns]
        if target_col in df.columns:
            keep_cols.append(target_col)
        df = df[keep_cols].copy()
        logger.info(f"Harmonization: feature selection -> {self.feature_order}")

        for col in self.categorical_features:
            if col in df.columns:
                enc = LabelEncoder()
                df[col] = enc.fit_transform(df[col].astype(str))
                self.encoders[col] = enc
        logger.info("Harmonization: categorical normalization complete")

        return df
