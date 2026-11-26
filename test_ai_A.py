import pytest

from load_scores import load_scores


def _write_csv(tmp_path, content):
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8")
    return path


def test_loads_valid_scores_trims_names_and_keeps_duplicate_names(tmp_path):
    path = _write_csv(
        tmp_path,
        "name,score\n Alice ,0\nBob,100\nAlice,88\n",
    )

    kept, skipped = load_scores(path)

    assert kept == [("Alice", 0), ("Bob", 100), ("Alice", 88)]
    assert skipped == []


def test_header_only_returns_empty_lists(tmp_path):
    path = _write_csv(tmp_path, "name,score\n")

    assert load_scores(path) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("Alice", "열 개수가 2가 아님"),
        ("Alice,90,extra", "열 개수가 2가 아님"),
        ("Alice,", "점수가 비어 있음"),
        ("Alice,abc", "점수가 정수가 아님"),
        ("Alice,-1", "점수가 0~100 밖"),
        ("Alice,101", "점수가 0~100 밖"),
        (",90", "이름이 비어 있음"),
    ],
)
def test_invalid_rows_are_recorded(tmp_path, row, reason):
    path = _write_csv(tmp_path, f"name,score\n{row}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, row, reason)]


def test_blank_lines_are_ignored_without_changing_line_numbers(tmp_path):
    path = _write_csv(tmp_path, "name,score\n\nAlice,90\n\nBob,101\n")

    kept, skipped = load_scores(path)

    assert kept == [("Alice", 90)]
    assert skipped == [(5, "Bob,101", "점수가 0~100 밖")]
