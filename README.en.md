# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**Benchmark system measuring real-world AI coding agent performance**

## Live Results

**[View Benchmark Results](https://careti.ai/en/benchmark)**

## Why This Benchmark?

### Limitations of Existing Benchmarks

| Benchmark | Limitation |
|-----------|------------|
| **HumanEval** | Measures only single-function generation, disconnected from real development |
| **SWE-bench** | Measures GitHub issue resolution, but doesn't reflect agent tool usage |
| **MBPP** | Simple Python problems, no support for complex multi-file tasks |

**Core Problem**: Existing benchmarks only measure "code generation ability". But real AI coding agents (Cline, Cursor, Careti, etc.) **use tools, see errors and fix them, and make multiple attempts**.

### What This Benchmark Measures

```
Traditional: Problem → Model → Code → Grade (1 time)
Careti:      Problem → Agent → Code → Test → [Error Feedback] → Retry → ... → Final Result
```

## Latest Results (Hard Suite 100)

| Rank | Model | 1st Pass | Final Pass | Avg Attempts | Cost |
|------|-------|----------|------------|--------------|------|
| #1 | Gemini 2.5 Flash | 62-67% | **98%** | 1.36-1.44 | $0.09-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## Key Metrics

| Metric | Meaning | Why It Matters |
|--------|---------|----------------|
| **1st Attempt Pass Rate** | Success rate on first try | Agent's "intuition" - determines user wait time |
| **Final Pass Rate** | Success rate including retries | Agent's "problem-solving ability" |
| **Average Attempts** | Mean tries per problem | Efficiency indicator |
| **Cost** | Total API cost | Economic feasibility |

## Termination Conditions

| Condition | Description |
|-----------|-------------|
| `success` | Test passed |
| `max_attempts` | Reached max attempts (5) |
| `timeout` | Time limit exceeded (300s) |
| `oscillation` | A↔B oscillation pattern detected |
| `same_error` | Same error repeated 3 times |

## Raw Data

The `results/` directory contains full benchmark data in JSON format.

### Data Structure

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

### Looking Up Original Problems

HumanEval problems can be retrieved from the Hugging Face dataset:

```python
from datasets import load_dataset

ds = load_dataset("openai/openai_humaneval")
problem = ds["test"][0]  # he000 → problem 0
print(problem["prompt"])
```

**Hugging Face**: [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval)

## License

MIT

---

**Made by [Caretive](https://caretive.ai)** - Developers of Careti AI Coding Agent
