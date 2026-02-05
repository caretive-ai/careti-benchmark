#!/usr/bin/env python3
"""
Careti Benchmark Data Verification Script

This script verifies that the benchmark data can be downloaded and used correctly.
Run this to confirm data integrity before using it for research.

Usage:
    python scripts/verify-data.py
"""

import json
import urllib.request
from collections import defaultdict

BASE_URL = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main"

def download_json(path: str) -> dict:
    """Download JSON from GitHub."""
    url = f"{BASE_URL}/{path}"
    return json.loads(urllib.request.urlopen(url).read())


def verify_data():
    print("=" * 60)
    print("CARETI BENCHMARK DATA VERIFICATION")
    print("=" * 60)

    # 1. Download all data
    print("\n[1] Downloading data from GitHub...")
    try:
        problems = download_json("problems/hard-suite.json")
        results = download_json("results/2026-02-hard-suite/results.json")
        summary = download_json("results/2026-02-hard-suite/summary.json")
        print(f"    ✓ problems: {len(problems)} entries")
        print(f"    ✓ results: {len(results)} entries")
        print(f"    ✓ summary: {len(summary)} entries")
    except Exception as e:
        print(f"    ✗ Download failed: {e}")
        return False

    # 2. Verify problem coverage
    print("\n[2] Verifying problem coverage...")
    problem_ids = {p['id'] for p in problems}
    result_problem_ids = {r['problem_id'] for r in results}
    missing = result_problem_ids - problem_ids
    if missing:
        print(f"    ✗ Missing problems: {missing}")
        return False
    print(f"    ✓ All {len(result_problem_ids)} problem_ids found in problems")

    # 3. Check for internal paths (should be cleaned)
    print("\n[3] Checking for internal paths...")
    internal_paths = []
    for r in results:
        for a in r.get('attempt_history', []):
            error = a.get('error', '')
            if '/tmp/benchmark-' in error:
                internal_paths.append(error[:50])

    if internal_paths:
        print(f"    ✗ Internal paths found: {internal_paths[:3]}")
        return False
    print("    ✓ No internal paths (data is clean)")

    # 4. Verify required fields
    print("\n[4] Verifying data structure...")
    required_result_fields = ['problem_id', 'model', 'success', 'attempts', 'termination_reason']
    required_problem_fields = ['id', 'name', 'prompt', 'test_code']

    for field in required_result_fields:
        if field not in results[0]:
            print(f"    ✗ Missing field in results: {field}")
            return False

    for field in required_problem_fields:
        if field not in problems[0]:
            print(f"    ✗ Missing field in problems: {field}")
            return False

    print("    ✓ All required fields present")

    # 5. Test use case: Look up problem for a result
    print("\n[5] Testing problem lookup...")
    sample_result = results[0]
    sample_problem = next((p for p in problems if p['id'] == sample_result['problem_id']), None)

    if not sample_problem:
        print(f"    ✗ Could not find problem for {sample_result['problem_id']}")
        return False

    print(f"    Result: {sample_result['problem_id']} ({sample_result['model']})")
    print(f"    Problem: {sample_problem['name']} ({sample_problem['difficulty']})")
    print("    ✓ Problem lookup works")

    # 6. Calculate and display stats
    print("\n[6] Calculating model statistics...")
    stats = defaultdict(lambda: {'total': 0, 'success': 0, 'first': 0, 'cost': 0})

    for r in results:
        m = r['model']
        stats[m]['total'] += 1
        if r['success']:
            stats[m]['success'] += 1
        if r.get('first_attempt_success'):
            stats[m]['first'] += 1
        stats[m]['cost'] += r.get('cost_usd', 0)

    print(f"\n    {'Model':<30} {'Final':>8} {'1st':>8} {'Cost':>10}")
    print("    " + "-" * 60)

    for m in sorted(stats.keys(), key=lambda x: -stats[x]['success']/stats[x]['total']):
        s = stats[m]
        final = s['success'] / s['total'] * 100
        first = s['first'] / s['total'] * 100
        cost = s['cost'] / (s['total'] / 100)  # Cost per 100 problems
        print(f"    {m:<30} {final:>7.0f}% {first:>7.0f}% ${cost:>8.2f}")

    print("\n" + "=" * 60)
    print("✓ ALL VERIFICATIONS PASSED")
    print("  Data is ready for research use!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = verify_data()
    exit(0 if success else 1)
