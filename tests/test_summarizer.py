import pytest
import pandas as pd
from pathlib import Path
from summarizer.summarizer import Summarizer

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "numeric": [1.5, 2.0, 3.0, 0.0, None, 2.0],
        "category": ["A", "B", "A", "C", None, "A"],
        "bools": pd.array([True, False, True, True, None, False], dtype="boolean"),
        "dates": pd.to_datetime(["2026-04-04", "2026-04-04", "2026-04-10", None, "2026-04-09", "2026-04-08"])
    })

def test_get_summary(sample_df):
    summarizer = Summarizer(sample_df)
    stats = summarizer.get_summary()
    
    assert not stats.empty
    assert "numeric" in stats.index
    assert stats.loc["numeric", "Type"] == "numeric"
    assert stats.loc["category", "Type"] == "categorical"
    assert stats.loc["bools", "Type"] == "boolean"

@pytest.mark.parametrize("fmt", ["markdown", "html", "xlsx"])
def test_get_report(sample_df, tmp_path, fmt):
    filepath = str(tmp_path / f"report.{fmt}")
    summarizer = Summarizer(sample_df, output_type=fmt, out_filename=filepath)
    summarizer.get_summary()
    
    out_path = summarizer.get_report()
    assert Path(out_path).exists()
    assert Path(out_path).stat().st_size > 0

def test_edge_cases():
    df_empty = pd.DataFrame()
    with pytest.raises(Exception):
        Summarizer(df_empty).get_summary()
        
    df_single = pd.DataFrame({"a": [5]})
    stats = Summarizer(df_single).get_summary()
    assert stats.loc["a", "std"] == 0.0