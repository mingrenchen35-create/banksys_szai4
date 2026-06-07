"""Tests for utils module."""

import pandas as pd

from src.utils import convert_df_to_csv, has_trained_model


class TestHasTrainedModel:
    def test_returns_bool(self):
        result = has_trained_model()
        assert isinstance(result, bool)


class TestConvertDfToCsv:
    def test_returns_bytes(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = convert_df_to_csv(df)
        assert isinstance(result, bytes)

    def test_roundtrip(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        csv_bytes = convert_df_to_csv(df)
        restored = pd.read_csv(pd.io.common.BytesIO(csv_bytes))
        pd.testing.assert_frame_equal(df, restored)
