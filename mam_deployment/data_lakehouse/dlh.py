import os
import logging

import numpy as np
import pandas as pd

logger = logging.getLogger("MAM")


class DataLakehouse:

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

    def load_cbis_ddsm(self, file_name: str, n: int, seed: int) -> pd.DataFrame:
        path = os.path.join(self.data_dir, file_name)
        if os.path.exists(path):
            logger.info(f"DLH: loading CBIS-DDSM metadata from {path}")
            return pd.read_csv(path)

    def load_vindr_mammo(self, file_name: str, n: int, seed: int) -> pd.DataFrame:
        path = os.path.join(self.data_dir, file_name)
        if os.path.exists(path):
            logger.info(f"DLH: loading Vin-Dr Mammo metadata from {path}")
            return pd.read_csv(path)