#!/usr/bin/env python3
"""
Careti Benchmark - Example Usage

This script demonstrates how to use the benchmark data for research.
"""

import json
import urllib.request

# GitHub raw URLs
BASE = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main"
PROBLEMS_URL = f"{BASE}/problems/hard-suite.json"
RESULTS_URL = f"{BASE}/results/2026-02-hard-suite/results.json"


def load_data():
    """Download benchmark data from GitHub."""
    problems = json.loads(urllib.request.urlopen(PROBLEMS_URL).read())
    results = json.loads(urllib.request.urlopen(RESULTS_URL).read())
    return problems, results


def example_1_analyze_failure():
    """Example: Analyze why a model failed on a specific problem."""
    print("\n=== Example 1: Analyze a Failure ===\n")

    problems, results = load_data()
    problem_lookup = {p['id']: p for p in problems}

    # Find a failed result with error details
    failed = next(
        (r for r in results
         if not r['success'] and r.get('attempt_history') and
         any(a.get('error') for a in r['attempt_history'])),
        None
    )

    if not failed:
        print("No failures with error details found")
        return

    problem = problem_lookup[failed['problem_id']]
    last_error = next(
        (a['error'] for a in reversed(failed['attempt_history']) if a.get('error')),
        "No error"
    )

    print(f"Problem: {problem['name']} ({problem['difficulty']})")
    print(f"Model: {failed['model']}")
    print(f"Attempts: {failed['attempts']}")
    print(f"Termination: {failed['termination_reason']}")
    print(f"\nPrompt:\n{problem['prompt'][:300]}...")
    print(f"\nLast Error:\n{last_error[:300]}...")


def example_2_compare_models():
    """Example: Compare model performance on specific problem types."""
    print("\n=== Example 2: Compare Models by Difficulty ===\n")

    problems, results = load_data()
    problem_lookup = {p['id']: p for p in problems}

    # Group results by model and difficulty
    stats = {}
    for r in results:
        model = r['model']
        problem = problem_lookup.get(r['problem_id'], {})
        difficulty = problem.get('difficulty', 'unknown')

        key = (model, difficulty)
        if key not in stats:
            stats[key] = {'total': 0, 'success': 0}

        stats[key]['total'] += 1
        if r['success']:
            stats[key]['success'] += 1

    # Display
    models = sorted(set(k[0] for k in stats.keys()))
    difficulties = ['medium', 'hard']

    print(f"{'Model':<30}", end="")
    for d in difficulties:
        print(f" {d:>10}", end="")
    print()
    print("-" * 52)

    for model in models:
        print(f"{model:<30}", end="")
        for d in difficulties:
            s = stats.get((model, d), {'total': 0, 'success': 0})
            rate = s['success'] / s['total'] * 100 if s['total'] > 0 else 0
            print(f" {rate:>9.0f}%", end="")
        print()


def example_3_error_patterns():
    """Example: Analyze common error patterns."""
    print("\n=== Example 3: Error Pattern Analysis ===\n")

    _, results = load_data()

    # Count termination reasons by model
    from collections import Counter
    terminations = {}

    for r in results:
        model = r['model']
        reason = r.get('termination_reason', 'unknown')

        if model not in terminations:
            terminations[model] = Counter()
        terminations[model][reason] += 1

    print(f"{'Model':<30} {'success':>10} {'max_att':>10} {'same_err':>10} {'timeout':>10}")
    print("-" * 72)

    for model in sorted(terminations.keys()):
        c = terminations[model]
        print(f"{model:<30} {c['success']:>10} {c['max_attempts']:>10} {c['same_error']:>10} {c['timeout']:>10}")


if __name__ == "__main__":
    example_1_analyze_failure()
    example_2_compare_models()
    example_3_error_patterns()
