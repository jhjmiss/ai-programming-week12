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

## 13주차 실습 데이터

`week13`의 CSV 파일은 13주차 실습 배포 자료에서 가져왔습니다. `scores_2026.csv`의 원본 데이터는 헤더를 제외하고 114행 5열입니다.

| 열 | 뜻 |
|---|---|
| 학번 | 학생 번호 |
| 이름 | 학생 이름 |
| 반 | 반 이름 |
| 과목 | 과목 이름 |
| 점수 | 해당 과목의 점수 |

점수 결측 처리: 점수가 비어 있는 행은 제외한다. 0점이나 평균으로 채우면 실제로 기록되지 않은 점수가 반 평균에 반영되기 때문이다.

실습에 포함된 자료는 UTF-8 원본 `scores_2026.csv`, CP949 인코딩 확인용 `scores_2026_cp949.csv`, 손계산 검증용 `mini.csv`, 프롬프트 모음 `prompts.txt`입니다.

13주차 테스트는 저장소 루트에서 다음 명령으로 실행합니다.

```bash
python -m pytest -q week13/test_analysis.py
```
