"""Model training, evaluation, and persistence for bank marketing prediction."""

import pickle
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data_loader import CATEGORICAL_COLS, NUMERIC_COLS, TARGET_COL

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODELS_DIR / "model.pkl"

# Features to exclude from prediction (not known at marketing time)
PREDICTION_EXCLUDE = ["duration"]
PREDICTION_NUMERIC = [c for c in NUMERIC_COLS if c not in PREDICTION_EXCLUDE]
PREDICTION_CATEGORICAL = CATEGORICAL_COLS
ALL_FEATURES = PREDICTION_NUMERIC + PREDICTION_CATEGORICAL


def _build_preprocessor() -> ColumnTransformer:
    """Build the feature preprocessing pipeline."""
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="unknown")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, PREDICTION_NUMERIC),
            ("cat", categorical_transformer, PREDICTION_CATEGORICAL),
        ]
    )


def load_train_val() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Load train data and split into train/validation sets (80/20).

    test.csv has no target column, so we split train.csv for evaluation.
    """
    from src.data_loader import load_train

    df = load_train()
    x = df[ALL_FEATURES]
    y = (df[TARGET_COL] == "yes").astype(int)

    return train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)


def train_model() -> tuple[Pipeline, dict]:
    """Train the model and return the pipeline with evaluation metrics."""
    x_train, x_val, y_train, y_val = load_train_val()

    preprocessor = _build_preprocessor()
    clf = GradientBoostingClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
    )

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", clf)])
    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_val)
    y_proba = pipeline.predict_proba(x_val)[:, 1]

    metrics = {
        "auc": float(roc_auc_score(y_val, y_proba)),
        "accuracy": float(accuracy_score(y_val, y_pred)),
        "precision": float(precision_score(y_val, y_pred)),
        "recall": float(recall_score(y_val, y_pred)),
        "f1": float(f1_score(y_val, y_pred)),
    }

    return pipeline, metrics


def save_model(pipeline: Pipeline, path: Path | None = None) -> Path:
    """Save trained pipeline to disk."""
    target = path or MODEL_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "wb") as f:
        pickle.dump(pipeline, f)
    return target


def load_model(path: Path | None = None) -> Pipeline:
    """Load a trained pipeline from disk."""
    target = path or MODEL_PATH
    if not target.exists():
        raise FileNotFoundError(f"Model not found: {target}")
    with open(target, "rb") as f:
        return pickle.load(f)


def predict(pipeline: Pipeline, input_data: dict) -> dict:
    """Make a prediction for a single customer record.

    Args:
        pipeline: Trained sklearn Pipeline.
        input_data: Dict with feature names as keys.

    Returns:
        Dict with prediction (0/1), probability, and label.
    """
    df = pd.DataFrame([input_data])
    df = df[ALL_FEATURES]
    proba = float(pipeline.predict_proba(df)[:, 1][0])
    prediction = int(proba >= 0.5)
    return {
        "prediction": prediction,
        "probability": round(proba, 4),
        "label": "会认购" if prediction == 1 else "不会认购",
    }
