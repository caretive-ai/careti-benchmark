# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**测量AI编程智能体实际性能的基准测试系统**

## 查看结果

**[查看基准测试结果](https://careti.ai/zh/benchmark)**

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/caretive-ai/careti-benchmark.git
cd careti-benchmark

# 验证数据完整性
python3 scripts/verify-data.py

# 示例用法
python3 scripts/example-usage.py
```

## 为什么要做这个基准测试?

### 现有基准测试的局限性

| 基准测试 | 局限性 |
|----------|--------|
| **HumanEval** | 只测量单函数生成，与实际开发环境脱节 |
| **SWE-bench** | 测量GitHub问题解决，但不反映智能体工具使用能力 |
| **MBPP** | 简单的Python问题，不支持复杂的多文件任务 |

**核心问题**: 现有基准测试只测量"代码生成能力"。但真正的AI编程智能体（Cline、Cursor、Careti等）会**使用工具、查看错误并修复、进行多次尝试**。

### 这个基准测试测量什么

```
传统: 问题 → 模型 → 代码 → 评分（1次）
Careti: 问题 → 智能体 → 代码 → 测试 → [错误反馈] → 重试 → ... → 最终结果
```

## 最新结果 (Hard Suite 100)

| 排名 | 模型 | 首次成功率 | 最终通过率 | 平均尝试 | 成本 |
|-----|------|-----------|-----------|----------|------|
| #1 | Gemini 2.5 Flash | 70-92% | **98%** | 1.11-1.44 | $0.05-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## 核心指标

| 指标 | 含义 | 为什么重要? |
|------|------|-------------|
| **首次成功率** | 第一次尝试成功的比例 | 智能体的"直觉力" - 决定用户等待时间 |
| **最终成功率** | 包含重试的最终成功比例 | 智能体的"问题解决能力" |
| **平均尝试** | 每题平均尝试次数 | 效率指标 |
| **成本** | 总API成本 | 经济可行性 |

## 终止条件

| 条件 | 说明 |
|------|------|
| `success` | 测试通过 |
| `max_attempts` | 达到最大尝试次数（5次） |
| `timeout` | 超时（300秒） |
| `oscillation` | 检测到A↔B振荡模式 |
| `same_error` | 相同错误重复3次 |

## Raw数据

`results/`目录包含JSON格式的完整基准测试数据。

### 数据结构

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

### 查询原始问题

Hard Suite问题包含在`problems/hard-suite.json`中:

```python
import json
import urllib.request

# 下载问题
url = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main/problems/hard-suite.json"
problems = json.loads(urllib.request.urlopen(url).read())

# 按ID查找问题
problem = next(p for p in problems if p["id"] == "h01-longest-substring")
print(problem["prompt"])
print(problem["test_code"])
```

## 文件结构

```
problems/
  hard-suite.json       # 100道题目（含提示词和测试代码）

results/2026-02-hard-suite/
  results.json          # 2100条独立测试结果
  summary.json          # 按模型汇总统计

scripts/
  verify-data.py        # 数据完整性验证
  example-usage.py      # 示例分析脚本
```

## 许可证

MIT

---

**Made by [Caretive](https://caretive.ai)** - Careti AI编程智能体开发团队
