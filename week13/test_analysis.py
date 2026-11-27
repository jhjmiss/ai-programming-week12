from pathlib import Path

import pandas as pd
import pytest

from analysis import clean, 반별평균


DATA_DIR = Path(__file__).resolve().parent


@pytest.fixture(scope="module")
def cleaned_data() -> dict[str, pd.DataFrame]:
    scores = pd.read_csv(
        DATA_DIR / "scores_2026.csv",
        encoding="utf-8",
        dtype={"학번": str},
    )
    mini = pd.read_csv(
        DATA_DIR / "mini.csv",
        encoding="utf-8",
        dtype={"학번": str},
    )

    return {
        "scores": clean(scores),
        "mini": clean(mini),
    }


def test_scores_clean_to_100_rows(cleaned_data: dict[str, pd.DataFrame]) -> None:
    assert len(cleaned_data["scores"]) == 100


def test_cleaned_class_names_are_expected(
    cleaned_data: dict[str, pd.DataFrame],
) -> None:
    assert set(cleaned_data["scores"]["반"].unique()) == {"1반", "2반"}


def test_class_score_sums_equal_total(cleaned_data: dict[str, pd.DataFrame]) -> None:
    scores = cleaned_data["scores"]
    assert scores.groupby("반")["점수"].sum().sum() == scores["점수"].sum()


def test_mini_first_class_average_is_80(
    cleaned_data: dict[str, pd.DataFrame],
) -> None:
    assert 반별평균(cleaned_data["mini"]).loc["1반"] == 80.0
