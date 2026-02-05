# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**AI 코딩 에이전트의 실제 성능을 측정하는 벤치마크 시스템**

## 결과 보기

**[벤치마크 결과 보기](https://careti.ai/ko/benchmark)**

## 빠른 시작

```bash
# 저장소 클론
git clone https://github.com/caretive-ai/careti-benchmark.git
cd careti-benchmark

# 데이터 무결성 검증
python3 scripts/verify-data.py

# 예제 사용법
python3 scripts/example-usage.py
```

## 왜 만들었나?

### 기존 벤치마크의 한계

| 벤치마크 | 한계점 |
|----------|--------|
| **HumanEval** | 단일 함수 생성만 측정, 실제 개발 환경과 괴리 |
| **SWE-bench** | GitHub 이슈 해결 측정하지만, 에이전트 도구 사용 능력 미반영 |
| **MBPP** | 간단한 Python 문제, 복잡한 멀티파일 작업 미지원 |

**핵심 문제**: 기존 벤치마크는 "코드 생성 능력"만 측정합니다. 하지만 실제 AI 코딩 에이전트(Cline, Cursor, Careti 등)는 **도구를 사용하고, 에러를 보고 수정하고, 여러 번 시도**합니다.

### 이 벤치마크가 측정하는 것

```
기존: 문제 → 모델 → 코드 → 채점 (1회)
Careti: 문제 → 에이전트 → 코드 → 테스트 → [에러 피드백] → 재시도 → ... → 최종 결과
```

## 최신 결과 (Hard Suite 100)

| 순위 | 모델 | 1회 성공률 | 최종 통과율 | 평균 시도 | 비용 |
|-----|------|-----------|-----------|----------|------|
| #1 | Gemini 2.5 Flash | 70-92% | **98%** | 1.11-1.44 | $0.05-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## 핵심 지표

| 지표 | 의미 | 왜 중요한가? |
|------|------|-------------|
| **1회 성공률** | 첫 시도에 맞추는 비율 | 에이전트의 "직관력" - 사용자 대기 시간 결정 |
| **최종 성공률** | 재시도 포함 최종 성공 비율 | 에이전트의 "문제 해결력" |
| **평균 시도** | 문제당 평균 시도 횟수 | 효율성 지표 |
| **비용** | 총 API 비용 | 경제적 타당성 |

## 종료 조건

| 조건 | 설명 |
|------|------|
| `success` | 테스트 통과 |
| `max_attempts` | 최대 시도 횟수 도달 (5회) |
| `timeout` | 시간 초과 (300초) |
| `oscillation` | A↔B 진동 패턴 감지 |
| `same_error` | 동일 에러 3회 반복 |

## Raw 데이터

`results/` 디렉토리에 JSON 형식의 전체 벤치마크 데이터가 있습니다.

### 데이터 구조

```json
{
  "problem_id": "h01-longest-substring",
  "model": "Gemini 2.5 Flash",
  "success": true,
  "attempts": 2,
  "first_attempt_success": false,
  "total_time_ms": 9599,
  "cost_usd": 0.00094,
  "input_tokens": 4330,
  "output_tokens": 484,
  "prompt_mode": "careti",
  "termination_reason": "success",
  "attempt_history": [
    {
      "attempt": 1,
      "success": false,
      "latency_ms": 6229,
      "error": "SyntaxError: invalid syntax"
    },
    {
      "attempt": 2,
      "success": true,
      "latency_ms": 3370
    }
  ]
}
```

### 문제 원본 조회

Hard Suite 문제는 `problems/hard-suite.json`에 포함되어 있습니다:

```python
import json
import urllib.request

# 문제 다운로드
url = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main/problems/hard-suite.json"
problems = json.loads(urllib.request.urlopen(url).read())

# ID로 문제 찾기
problem = next(p for p in problems if p["id"] == "h01-longest-substring")
print(problem["prompt"])
print(problem["test_code"])
```

## 파일 구조

```
problems/
  hard-suite.json       # 100개 문제 (프롬프트, 테스트 코드 포함)

results/2026-02-hard-suite/
  results.json          # 2100개 개별 테스트 결과
  summary.json          # 모델별 집계 통계

scripts/
  verify-data.py        # 데이터 무결성 검증
  example-usage.py      # 예제 분석 스크립트
```

## 라이선스

MIT

---

**Made by [Caretive](https://caretive.ai)** - AI 코딩 에이전트 Careti 개발팀
