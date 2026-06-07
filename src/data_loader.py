"""Data loading and preprocessing for bank marketing dataset."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

NUMERIC_COLS = [
    "age",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]

CATEGORICAL_COLS = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

TARGET_COL = "subscribe"
ID_COL = "id"


def load_train() -> pd.DataFrame:
    """Load training dataset."""
    path = DATA_DIR / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"Training data not found: {path}")
    return pd.read_csv(path)


def load_test() -> pd.DataFrame:
    """Load test dataset."""
    path = DATA_DIR / "test.csv"
    if not path.exists():
        raise FileNotFoundError(f"Test data not found: {path}")
    return pd.read_csv(path)


def get_summary(df: pd.DataFrame) -> dict:
    """Return summary statistics for the dataset."""
    return {
        "n_rows": len(df),
        "n_cols": len(df.columns),
        "columns": list(df.columns),
        "missing": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).to_dict(),
        "target_distribution": df[TARGET_COL].value_counts().to_dict()
        if TARGET_COL in df.columns
        else {},
        "numeric_summary": df[NUMERIC_COLS].describe().to_dict()
        if all(c in df.columns for c in NUMERIC_COLS)
        else {},
    }


def get_feature_types() -> dict[str, list[str]]:
    """Return numeric and categorical feature lists."""
    return {
        "numeric": NUMERIC_COLS,
        "categorical": CATEGORICAL_COLS,
    }


def get_feature_stats(df: pd.DataFrame, feature: str) -> dict:
    """Return per-feature statistics for visualization."""
    if feature in NUMERIC_COLS:
        return {
            "type": "numeric",
            "mean": float(df[feature].mean()),
            "median": float(df[feature].median()),
            "std": float(df[feature].std()),
            "min": float(df[feature].min()),
            "max": float(df[feature].max()),
            "values": df[feature].dropna().tolist(),
            "by_target": {
                str(k): df[df[TARGET_COL] == k][feature].dropna().tolist()
                for k in df[TARGET_COL].unique()
            }
            if TARGET_COL in df.columns
            else {},
        }
    if feature in CATEGORICAL_COLS:
        value_counts = df[feature].value_counts()
        if TARGET_COL in df.columns:
            crosstab = pd.crosstab(df[feature], df[TARGET_COL])
            return {
                "type": "categorical",
                "value_counts": value_counts.to_dict(),
                "crosstab": crosstab.to_dict(),
                "categories": list(value_counts.index),
            }
        return {
            "type": "categorical",
            "value_counts": value_counts.to_dict(),
            "categories": list(value_counts.index),
        }
    raise ValueError(f"Unknown feature: {feature}")
