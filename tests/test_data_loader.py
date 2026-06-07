"""Tests for data_loader module."""

import pandas as pd
import pytest

from src.data_loader import (
    CATEGORICAL_COLS,
    NUMERIC_COLS,
    TARGET_COL,
    get_feature_stats,
    get_feature_types,
    get_summary,
    load_test,
    load_train,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "age": [30, 45, 28, 52],
            "job": ["admin.", "services", "blue-collar", "entrepreneur"],
            "marital": ["married", "single", "divorced", "married"],
            "education": [
                "university.degree",
                "high.school",
                "basic.9y",
                "professional.course",
            ],
            "default": ["no", "unknown", "no", "yes"],
            "housing": ["yes", "yes", "no", "yes"],
            "loan": ["no", "no", "yes", "no"],
            "contact": ["cellular", "cellular", "telephone", "cellular"],
            "month": ["may", "jun", "jul", "aug"],
            "day_of_week": ["mon", "tue", "wed", "thu"],
            "duration": [120, 300, 60, 450],
            "campaign": [1, 2, 1, 3],
            "pdays": [999, 3, 999, 10],
            "previous": [0, 1, 0, 2],
            "poutcome": ["nonexistent", "failure", "nonexistent", "success"],
            "emp_var_rate": [1.4, -1.8, -2.9, 1.4],
            "cons_price_index": [93.994, 92.893, 92.893, 94.465],
            "cons_conf_index": [-36.4, -46.2, -47.1, -40.8],
            "lending_rate3m": [4.05, 1.97, 1.67, 4.96],
            "nr_employed": [5099.1, 5076.2, 5076.2, 5228.1],
            "subscribe": ["no", "yes", "no", "yes"],
        }
    )


class TestLoadTrain:
    def test_loads_dataframe(self):
        df = load_train()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_has_expected_columns(self):
        df = load_train()
        for col in NUMERIC_COLS + CATEGORICAL_COLS + [TARGET_COL, "id"]:
            assert col in df.columns

    def test_file_not_found_raises(self, tmp_path, monkeypatch):
        import src.data_loader as dl

        monkeypatch.setattr(dl, "DATA_DIR", tmp_path)
        with pytest.raises(FileNotFoundError, match="Training data not found"):
            load_train()


class TestLoadTest:
    def test_loads_dataframe(self):
        df = load_test()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_file_not_found_raises(self, tmp_path, monkeypatch):
        import src.data_loader as dl

        monkeypatch.setattr(dl, "DATA_DIR", tmp_path)
        with pytest.raises(FileNotFoundError, match="Test data not found"):
            load_test()


class TestGetSummary:
    def test_returns_expected_keys(self, sample_df):
        result = get_summary(sample_df)
        assert "n_rows" in result
        assert "n_cols" in result
        assert "columns" in result
        assert "missing" in result
        assert "target_distribution" in result
        assert "numeric_summary" in result

    def test_n_rows_correct(self, sample_df):
        result = get_summary(sample_df)
        assert result["n_rows"] == 4

    def test_target_distribution(self, sample_df):
        result = get_summary(sample_df)
        assert result["target_distribution"] == {"no": 2, "yes": 2}


class TestGetFeatureTypes:
    def test_returns_numeric_and_categorical(self):
        result = get_feature_types()
        assert "numeric" in result
        assert "categorical" in result
        assert isinstance(result["numeric"], list)
        assert isinstance(result["categorical"], list)

    def test_numeric_features_not_empty(self):
        result = get_feature_types()
        assert len(result["numeric"]) > 0

    def test_categorical_features_not_empty(self):
        result = get_feature_types()
        assert len(result["categorical"]) > 0


class TestGetFeatureStats:
    def test_numeric_feature_returns_expected_keys(self, sample_df):
        stats = get_feature_stats(sample_df, "age")
        assert stats["type"] == "numeric"
        assert "mean" in stats
        assert "median" in stats
        assert "values" in stats

    def test_categorical_feature_returns_expected_keys(self, sample_df):
        stats = get_feature_stats(sample_df, "job")
        assert stats["type"] == "categorical"
        assert "value_counts" in stats
        assert "categories" in stats

    def test_unknown_feature_raises(self, sample_df):
        with pytest.raises(ValueError, match="Unknown feature"):
            get_feature_stats(sample_df, "nonexistent_feature")
