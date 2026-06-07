"""Utility functions for the bank marketing analysis app."""

from pathlib import Path

import pandas as pd

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


def has_trained_model() -> bool:
    """Check if a trained model file exists."""
    return (MODELS_DIR / "model.pkl").exists()


def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")
