from pathlib import Path

import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    print(f"시작 행 수: {len(cleaned)}")

    # 점수가 비어 있는 행을 제거한다.
    cleaned = cleaned.dropna(subset=["점수"])
    print(f"점수 결측 제거 후 행 수: {len(cleaned)}")

    # 다섯 열의 값이 모두 같은 중복 행을 제거한다.
    cleaned = cleaned.drop_duplicates()
    print(f"완전 중복 제거 후 행 수: {len(cleaned)}")

    # 반과 과목 이름의 앞뒤 공백을 제거한다.
    cleaned["반"] = cleaned["반"].str.strip()
    cleaned["과목"] = cleaned["과목"].str.strip()
    print(f"반·과목 공백 제거 후 행 수: {len(cleaned)}")

    # 점수가 0~100 범위를 벗어난 행을 제거한다.
    cleaned = cleaned[cleaned["점수"].between(0, 100)].copy()
    print(f"유효 범위 밖 점수 제거 후 행 수: {len(cleaned)}")

    return cleaned


def 반별평균(df: pd.DataFrame) -> pd.Series:
    return df.groupby("반")["점수"].mean()


def main() -> None:
    csv_path = Path(__file__).resolve().parent / "scores_2026.csv"
    original = pd.read_csv(csv_path, encoding="utf-8", dtype={"학번": str})
    cleaned = clean(original)

    math_df = cleaned[cleaned["과목"] == "수학"].copy()
    print(f"수학 행 수: {len(math_df)}")

    class1_90_df = cleaned[(cleaned["반"] == "1반") & (cleaned["점수"] >= 90)].copy()
    print(f"1반 점수 90 이상 행 수: {len(class1_90_df)}")

    class_means = cleaned.groupby("반")["점수"].mean()
    print("반별 점수 평균:")
    print(class_means.to_string())

    subject_class_means = cleaned.groupby(["과목", "반"])["점수"].mean()
    print("과목별·반별 점수 평균:")
    print(subject_class_means.to_string())

    class_stats = (
        cleaned.groupby("반")["점수"]
        .agg(["count", "mean", "median", "max"])
        .rename(
            columns={
                "count": "개수",
                "mean": "평균",
                "median": "중앙값",
                "max": "최댓값",
            }
        )
        .round(2)
    )
    print("반별 점수 통계:")
    print(class_stats.to_string())

    class_average = 반별평균(cleaned)
    print("반별평균(df) 반환값:")
    print(class_average.to_string(float_format=lambda value: f"{value:.2f}"))

    class_score_sum = cleaned.groupby("반")["점수"].sum().sum()
    total_score_sum = cleaned["점수"].sum()
    print(
        f"반별 점수 합계 합산: {class_score_sum}; "
        f"전체 점수 합계: {total_score_sum}; "
        f"일치 여부: {class_score_sum == total_score_sum}"
    )

    class_score_count = cleaned.groupby("반")["점수"].count().sum()
    total_row_count = len(cleaned)
    print(
        f"반별 점수 개수 합산: {class_score_count}; "
        f"전체 행 수: {total_row_count}; "
        f"일치 여부: {class_score_count == total_row_count}"
    )

    print("정제 후 반 고유값:", [repr(value) for value in cleaned["반"].unique()])
    print("정제 후 과목 고유값:", [repr(value) for value in cleaned["과목"].unique()])


if __name__ == "__main__":
    main()
