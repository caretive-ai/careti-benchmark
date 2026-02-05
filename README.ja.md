# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**AIコーディングエージェントの実際のパフォーマンスを測定するベンチマークシステム**

## 結果を見る

**[ベンチマーク結果を見る](https://careti.ai/ja/benchmark)**

## クイックスタート

```bash
# リポジトリのクローン
git clone https://github.com/caretive-ai/careti-benchmark.git
cd careti-benchmark

# データ整合性の検証
python3 scripts/verify-data.py

# 使用例
python3 scripts/example-usage.py
```

## なぜこのベンチマークを作ったのか?

### 既存ベンチマークの限界

| ベンチマーク | 限界点 |
|-------------|--------|
| **HumanEval** | 単一関数の生成のみを測定、実際の開発環境と乖離 |
| **SWE-bench** | GitHubイシュー解決を測定するが、エージェントのツール使用能力は未反映 |
| **MBPP** | シンプルなPython問題、複雑なマルチファイル作業は未対応 |

**核心的な問題**: 既存のベンチマークは「コード生成能力」のみを測定します。しかし実際のAIコーディングエージェント（Cline、Cursor、Caretiなど）は**ツールを使用し、エラーを見て修正し、複数回試行**します。

### このベンチマークが測定するもの

```
従来: 問題 → モデル → コード → 採点（1回）
Careti: 問題 → エージェント → コード → テスト → [エラーフィードバック] → 再試行 → ... → 最終結果
```

## 最新結果 (Hard Suite 100)

| 順位 | モデル | 1回成功率 | 最終通過率 | 平均試行 | コスト |
|-----|------|-----------|-----------|----------|------|
| #1 | Gemini 2.5 Flash | 70-92% | **98%** | 1.11-1.44 | $0.05-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## 主要指標

| 指標 | 意味 | なぜ重要か? |
|------|------|-------------|
| **1回成功率** | 初回試行での成功率 | エージェントの「直感力」- ユーザー待機時間を決定 |
| **最終成功率** | 再試行を含む最終成功率 | エージェントの「問題解決力」 |
| **平均試行** | 問題あたりの平均試行回数 | 効率性指標 |
| **コスト** | 総APIコスト | 経済的妥当性 |

## 終了条件

| 条件 | 説明 |
|------|------|
| `success` | テスト通過 |
| `max_attempts` | 最大試行回数到達（5回） |
| `timeout` | タイムアウト（300秒） |
| `oscillation` | A↔B振動パターン検出 |
| `same_error` | 同一エラー3回反復 |

## Rawデータ

`results/`ディレクトリにJSON形式の完全なベンチマークデータがあります。

### データ構造

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

### 問題原本の照会

Hard Suite問題は`problems/hard-suite.json`に含まれています:

```python
import json
import urllib.request

# 問題のダウンロード
url = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main/problems/hard-suite.json"
problems = json.loads(urllib.request.urlopen(url).read())

# IDで問題を検索
problem = next(p for p in problems if p["id"] == "h01-longest-substring")
print(problem["prompt"])
print(problem["test_code"])
```

## ファイル構造

```
problems/
  hard-suite.json       # 100問（プロンプトとテストコード含む）

results/2026-02-hard-suite/
  results.json          # 2100件の個別テスト結果
  summary.json          # モデル別集計統計

scripts/
  verify-data.py        # データ整合性検証
  example-usage.py      # 例示分析スクリプト
```

## ライセンス

MIT

---

**Made by [Caretive](https://caretive.ai)** - AIコーディングエージェントCareti開発チーム
