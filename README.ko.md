# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**AI 코딩 에이전트의 실제 성능을 측정하는 벤치마크 시스템**

## 결과 보기

**[벤치마크 결과 보기](https://careti.ai/ko/benchmark)**

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
| #1 | Gemini 2.5 Flash | 62-67% | **98%** | 1.36-1.44 | $0.09-0.13 |
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
  "problem_id": "he000-has_close_elements",
  "model": "Gemini 2.5 Flash",
  "success": true,
  "attempts": 1,
  "first_attempt_success": true,
  "total_time_ms": 5348,
  "cost_usd": 0.00018,
  "input_tokens": 161,
  "output_tokens": 264,
  "prompt_mode": "careti",
  "termination_reason": "success",
  "attempt_history": [...]
}
```

### 문제 원본 조회

HumanEval 문제는 Hugging Face 데이터셋에서 조회할 수 있습니다:

```python
from datasets import load_dataset

ds = load_dataset("openai/openai_humaneval")
problem = ds["test"][0]  # he000 → 0번 문제
print(problem["prompt"])
```

**Hugging Face**: [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval)

## 라이선스

MIT

---

**Made by [Caretive](https://caretive.ai)** - AI 코딩 에이전트 Careti 개발팀
