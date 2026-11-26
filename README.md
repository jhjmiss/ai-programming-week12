# 성적 CSV 읽기

## What

성적 CSV를 읽어 유효한 점수와 제외된 행의 줄 번호·원본·이유를 반환합니다.

## Why

점수가 비어 있거나 0~100점 범위를 벗어난 행이 있어도 유효한 성적은 계속 읽을 수 있도록 만들었습니다. 제외한 행은 줄 번호와 이유를 기록해 원본에서 쉽게 찾아 고칠 수 있게 했습니다.

## How

저장소 폴더에서 다음 명령을 실행합니다.

```bash
python load_scores.py scores.csv
```

## 테스트

테스트 도구를 설치합니다.

```bash
python -m pip install pytest pytest-cov
```

테스트를 실행합니다.

```bash
python -m pytest -q
```

확인한 결과: `34 passed in 0.38s`

## 파일 구성

- 프로그램: `load_scores.py`
- 예제 데이터: `scores.csv`, `empty.csv`, `weird.csv`
- 직접 작성한 테스트: `test_load_scores.py`
- AI 비교용 테스트: `test_ai_A.py`, `test_ai_B.py`

## 작성자 및 AI 사용

- 작성자: 기계공학부 2026100733 정호진
- AI 사용: GitHub Copilot은 A/B 비교용 테스트 초안에, ChatGPT는 README 초안 작성에 사용했습니다.
