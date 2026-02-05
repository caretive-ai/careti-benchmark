# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**Benchmark system measuring real-world AI coding agent performance**

## Live Results

**[View Benchmark Results](https://careti.ai/en/benchmark)**

## Quick Start

```bash
# Clone repository
git clone https://github.com/caretive-ai/careti-benchmark.git
cd careti-benchmark

# Verify data integrity
python3 scripts/verify-data.py

# Example usage
python3 scripts/example-usage.py
```

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
| #1 | Gemini 2.5 Flash | 70-92% | **98%** | 1.11-1.44 | $0.05-0.13 |
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

### Looking Up Original Problems

Hard Suite problems are included in `problems/hard-suite.json`:

```python
import json
import urllib.request

# Download problems
url = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main/problems/hard-suite.json"
problems = json.loads(urllib.request.urlopen(url).read())

# Find problem by ID
problem = next(p for p in problems if p["id"] == "h01-longest-substring")
print(problem["prompt"])
print(problem["test_code"])
```

## Files

```
problems/
  hard-suite.json       # 100 problems with prompts and test code

results/2026-02-hard-suite/
  results.json          # 2100 individual test results
  summary.json          # Aggregated stats per model

scripts/
  verify-data.py        # Data integrity verification
  example-usage.py      # Example analysis scripts
```

## License

MIT

---

**Made by [Caretive](https://caretive.ai)** - Developers of Careti AI Coding Agent
