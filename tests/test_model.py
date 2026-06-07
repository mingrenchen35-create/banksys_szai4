"""Tests for model module."""

import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from src.model import (
    ALL_FEATURES,
    MODEL_PATH,
    PREDICTION_CATEGORICAL,
    PREDICTION_EXCLUDE,
    PREDICTION_NUMERIC,
    _build_preprocessor,
    load_model,
    load_train_val,
    predict,
    save_model,
    train_model,
)


def test_prediction_excludes_duration():
    assert "duration" not in PREDICTION_NUMERIC
    assert "duration" in PREDICTION_EXCLUDE


def test_all_features_no_duration():
    assert "duration" not in ALL_FEATURES


class TestBuildPreprocessor:
    def test_returns_column_transformer(self):
        preprocessor = _build_preprocessor()
        assert hasattr(preprocessor, "transform")
        assert hasattr(preprocessor, "fit")

    def test_transforms_data(self):
        preprocessor = _build_preprocessor()
        df = pd.DataFrame(
            {
                "age": [30, 45],
                "campaign": [1, 2],
                "pdays": [999, 3],
                "previous": [0, 1],
                "emp_var_rate": [1.4, -1.8],
                "cons_price_index": [93.994, 92.893],
                "cons_conf_index": [-36.4, -46.2],
                "lending_rate3m": [4.05, 1.97],
                "nr_employed": [5099.1, 5076.2],
                "job": ["admin.", "services"],
                "marital": ["married", "single"],
                "education": ["university.degree", "high.school"],
                "default": ["no", "unknown"],
                "housing": ["yes", "yes"],
                "loan": ["no", "no"],
                "contact": ["cellular", "cellular"],
                "month": ["may", "jun"],
                "day_of_week": ["mon", "tue"],
                "poutcome": ["nonexistent", "failure"],
            }
        )
        transformed = preprocessor.fit_transform(df)
        assert isinstance(transformed, np.ndarray)
        assert transformed.shape[0] == 2


class TestLoadTrainVal:
    def test_returns_four_arrays(self):
        x_train, x_val, y_train, y_val = load_train_val()
        assert isinstance(x_train, pd.DataFrame)
        assert isinstance(x_val, pd.DataFrame)
        assert isinstance(y_train, pd.Series)
        assert isinstance(y_val, pd.Series)

    def test_features_exclude_duration(self):
        x_train, _, _, _ = load_train_val()
        assert "duration" not in x_train.columns
        for feat in PREDICTION_NUMERIC + PREDICTION_CATEGORICAL:
            assert feat in x_train.columns

    def test_target_is_binary(self):
        _, _, y_train, y_val = load_train_val()
        assert y_train.isin([0, 1]).all()
        assert y_val.isin([0, 1]).all()

    def test_split_ratio(self):
        x_train, x_val, _, _ = load_train_val()
        total = len(x_train) + len(x_val)
        assert abs(len(x_val) / total - 0.2) < 0.01


class TestTrainModel:
    def test_returns_pipeline_and_metrics(self):
        pipeline, metrics = train_model()
        assert isinstance(pipeline, Pipeline)
        assert isinstance(metrics, dict)

    def test_metrics_has_required_keys(self):
        _, metrics = train_model()
        for key in ("auc", "accuracy", "precision", "recall", "f1"):
            assert key in metrics
            assert 0 <= metrics[key] <= 1

    def test_auc_above_threshold(self):
        _, metrics = train_model()
        assert metrics["auc"] >= 0.75, f"AUC {metrics['auc']} below 0.75"


class TestSaveLoadModel:
    def test_save_and_load_roundtrip(self, tmp_path):
        pipeline, _ = train_model()
        path = tmp_path / "model.pkl"
        saved = save_model(pipeline, path)
        assert saved.exists()

        loaded = load_model(saved)
        assert isinstance(loaded, Pipeline)

    def test_save_default_path(self):
        pipeline, _ = train_model()
        path = save_model(pipeline)
        assert path == MODEL_PATH
        assert path.exists()
        path.unlink()  # Clean up to avoid test pollution

    def test_load_nonexistent_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="Model not found"):
            load_model(tmp_path / "nonexistent.pkl")


class TestPredict:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.pipeline, _ = train_model()

    def test_predict_returns_dict(self):
        result = predict(
            self.pipeline,
            {
                "age": 35,
                "campaign": 1,
                "pdays": 999,
                "previous": 0,
                "emp_var_rate": 1.4,
                "cons_price_index": 93.994,
                "cons_conf_index": -36.4,
                "lending_rate3m": 4.05,
                "nr_employed": 5099.1,
                "job": "admin.",
                "marital": "married",
                "education": "university.degree",
                "default": "no",
                "housing": "yes",
                "loan": "no",
                "contact": "cellular",
                "month": "may",
                "day_of_week": "mon",
                "poutcome": "nonexistent",
            },
        )
        assert "prediction" in result
        assert "probability" in result
        assert "label" in result
        assert result["prediction"] in (0, 1)
        assert 0 <= result["probability"] <= 1

    def test_predict_label_matches_prediction(self):
        result = predict(
            self.pipeline,
            {
                "age": 35,
                "campaign": 2,
                "pdays": 5,
                "previous": 3,
                "emp_var_rate": -1.8,
                "cons_price_index": 92.893,
                "cons_conf_index": -46.2,
                "lending_rate3m": 2.0,
                "nr_employed": 5000.0,
                "job": "services",
                "marital": "single",
                "education": "high.school",
                "default": "no",
                "housing": "no",
                "loan": "yes",
                "contact": "telephone",
                "month": "jun",
                "day_of_week": "tue",
                "poutcome": "failure",
            },
        )
        if result["prediction"] == 1:
            assert result["label"] == "会认购"
        else:
            assert result["label"] == "不会认购"
