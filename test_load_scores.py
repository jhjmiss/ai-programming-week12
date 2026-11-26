import pytest

from load_scores import load_scores


def test_정상_파일을_읽는다(tmp_path):
    path = tmp_path / "normal.csv"
    path.write_text("name,score\n김하나,88\n윤보람,64\n", encoding="utf-8")
    assert load_scores(path) == ([("김하나", 88), ("윤보람", 64)], [])


def test_빈_줄은_건너뛴다(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text("name,score\n김하나,88\n\n윤보람,64\n", encoding="utf-8")
    assert load_scores(path) == ([("김하나", 88), ("윤보람", 64)], [])


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    path = tmp_path / "comma.csv"
    path.write_text('name,score\n"최,네번",77\n', encoding="utf-8")
    assert load_scores(path) == ([("최,네번", 77)], [])


def test_없는_파일이면_오류가_난다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_헤더만_있으면_빈_결과이다():
    assert load_scores("empty.csv") == ([], [])


@pytest.mark.parametrize("score, valid", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n김하나,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(path)

    if valid:
        assert kept == [("김하나", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [(2, f"김하나,{score}", "점수가 0~100 밖")]


def test_잘못된_행의_제외_이유를_기록한다(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text("name,score\n김하나,88,비고\n윤보람,\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, "김하나,88,비고", "열 개수가 2가 아님"),
        (3, "윤보람,", "점수가 비어 있음"),
    ]