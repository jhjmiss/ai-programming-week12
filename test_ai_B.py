import pytest

from load_scores import load_scores


def _write_csv(tmp_path, content):
    path = tmp_path / "input.csv"
    path.write_text(content, encoding="utf-8", newline="")
    return path


def test_loads_valid_rows_and_preserves_duplicate_names(tmp_path):
    path = _write_csv(
        tmp_path,
        'name,score\nAlice,0\nBob,100\nAlice,75\n"Lee, Ann",88\n',
    )
    original_content = path.read_text(encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == [
        ("Alice", 0),
        ("Bob", 100),
        ("Alice", 75),
        ("Lee, Ann", 88),
    ]
    assert skipped == []
    assert path.read_text(encoding="utf-8") == original_content


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_header_only_returns_empty_lists(tmp_path):
    path = _write_csv(tmp_path, "name,score\n")

    assert load_scores(path) == ([], [])


@pytest.mark.parametrize(
    "invalid_row",
    [
        "Alice",
        "Alice,90,extra",
        "Alice,",
        ",90",
        "Alice,not-a-number",
        "Alice,-1",
        "Alice,101",
    ],
)
def test_invalid_rows_are_excluded_with_a_reason(tmp_path, invalid_row):
    path = _write_csv(tmp_path, f"name,score\n{invalid_row}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    line_number, row_content, reason = skipped[0]
    assert line_number == 2
    assert isinstance(row_content, str)
    assert isinstance(reason, str) and reason


def test_blank_lines_are_ignored_and_excluded_rows_keep_line_numbers(tmp_path):
    path = _write_csv(tmp_path, "name,score\n\nAlice,90\n\nBob,101\n")

    kept, skipped = load_scores(path)

    assert kept == [("Alice", 90)]
    assert len(skipped) == 1
    assert skipped[0][0] == 5
