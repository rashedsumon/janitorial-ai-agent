# src/utils.py
import pandas as pd
from .config import settings
from loguru import logger

def load_sample_data(path=None):
    p = path or settings.KAGGLE_SAMPLE_PATH
    try:
        df = pd.read_csv(p)
        logger.info(f"Loaded sample data from {p} shape={df.shape}")
        return df
    except Exception as e:
        logger.error(f"Failed to load sample data from {p}: {e}")
        return pd.DataFrame()
