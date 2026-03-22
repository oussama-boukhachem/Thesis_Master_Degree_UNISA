import json
import numpy as np
from pathlib import Path
from itertools import product

# Conversion factors to milliseconds (ms/op)
SCORE_UNIT_TO_MS = {
    "ns/op": 1e-6,
    "us/op": 1e-3,
    "ms/op": 1.0,
    "s/op":  1e3,
}

# ---------------- CONFIG ----------------

N_BOOT = 10000
CONF_LEVEL = 0.95
RANDOM_SEED = 42

OUTPUT_STATS_FILE = "hierarchical_bootstrap_results.txt"
OUTPUT_SUMMARY_FILE = "hierarchical_bootstrap_summary.txt"
OUTPUT_REGRESSIONS_FILE = "confirmed_regressions.txt"

np.random.seed(RANDOM_SEED)

# ---------------- UTILS ----------------

def is_empty_json_file(path: Path) -> bool:
    """Return True iff JSON content is exactly []"""
    try:
        with open(path) as f:
            data = json.load(f)
        return isinstance(data, list) and len(data) == 0
    except Exception as e:
        print(f"Warning: Could not read {path}: {e}")
        return True


def load_jmh_scores(path):
    """Load JMH rawData and normalize all measurements to ms/op"""
    with open(path) as f:
        data = json.load(f)

    metric = data[0]["primaryMetric"]
    scores = metric["rawData"]
    unit = metric["scoreUnit"]

    if unit not in SCORE_UNIT_TO_MS:
        raise ValueError(f"Unknown scoreUnit '{unit}' in {path}")

    factor = SCORE_UNIT_TO_MS[unit]

    # Convert everything to ms/op
    return [np.array(fork) * factor for fork in scores]


# ---------------- STATISTICS ----------------

def hierarchical_bootstrap_ratio(group_a, group_b):
    """
    Perform hierarchical bootstrap to compute ratio of means.
    Returns array of ratios: mean(group_b) / mean(group_a)
    """
    ratios = []

    for _ in range(N_BOOT):
        # Resample forks with replacement
        forks_a = np.random.choice(len(group_a), len(group_a), replace=True)
        forks_b = np.random.choice(len(group_b), len(group_b), replace=True)

        sample_a = []
        sample_b = []

        # For each resampled fork, resample iterations
        for i in forks_a:
            iters = group_a[i]
            sample_a.extend(np.random.choice(iters, len(iters), replace=True))

        for i in forks_b:
            iters = group_b[i]
            sample_b.extend(np.random.choice(iters, len(iters), replace=True))

        mean_a = np.mean(sample_a)
        mean_b = np.mean(sample_b)
        
        # Compute ratio (avoid division by zero)
        if mean_a > 0:
            ratios.append(mean_b / mean_a)
        else:
            ratios.append(np.nan)

    return np.array([r for r in ratios if not np.isnan(r)])


def vargha_delaney_a12(x, y):
    """Compute Vargha-Delaney A12 effect size"""
    wins = sum(1 for xi, yi in product(x, y) if xi > yi)
    ties = sum(1 for xi, yi in product(x, y) if xi == yi)
    return (wins + 0.5 * ties) / (len(x) * len(y))


# ---------------- DISCOVERY ----------------

def discover_benchmark_pairs(base_dir: Path):
    """
    Discover all benchmark pairs (no_regression vs regression) for both
    handwritten and AI-generated benchmarks.
    
    Returns a dictionary:
    {
        'commit_name': {
            'handwritten': {
                'benchmark_name': {
                    'no_regression': Path,
                    'regression': Path
                }
            },
            'ai': {
                'benchmark_name': {
                    'no_regression': Path,
                    'regression': Path
                }
            }
        }
    }
    """
    pairs = {}
    
    no_regression_dir = base_dir / "no_regression"
    regression_dir = base_dir / "regression"
    
    if not no_regression_dir.exists() or not regression_dir.exists():
        raise ValueError(f"Expected 'no_regression' and 'regression' directories in {base_dir}")
    
    # Process each commit directory
    for commit_dir in no_regression_dir.iterdir():
        if not commit_dir.is_dir():
            continue
        
        commit_name = commit_dir.name
        pairs[commit_name] = {
            'handwritten': {},
            'ai': {}
        }
        
        # Process handwritten benchmarks
        handwritten_no_reg = commit_dir / "handwritten_results"
        handwritten_reg = regression_dir / commit_name / "handwritten_results"
        
        if handwritten_no_reg.exists() and handwritten_reg.exists():
            for bench_file in handwritten_no_reg.glob("*.json"):
                bench_name = bench_file.name
                reg_file = handwritten_reg / bench_name
                
                if reg_file.exists():
                    pairs[commit_name]['handwritten'][bench_name] = {
                        'no_regression': bench_file,
                        'regression': reg_file
                    }
        
        # Process AI-generated benchmarks
        ai_no_reg = commit_dir / "ai_results"
        ai_reg = regression_dir / commit_name / "ai_results"
        
        if ai_no_reg.exists() and ai_reg.exists():
            for bench_file in ai_no_reg.glob("*.json"):
                bench_name = bench_file.name
                reg_file = ai_reg / bench_name
                
                if reg_file.exists():
                    pairs[commit_name]['ai'][bench_name] = {
                        'no_regression': bench_file,
                        'regression': reg_file
                    }
    
    return pairs


# ---------------- MAIN ----------------

def main():
    base_dir = Path(".")
    
    print("=" * 80)
    print("HIERARCHICAL BOOTSTRAP ANALYSIS")
    print("Comparing No-Regression vs Regression Benchmarks")
    print("=" * 80)
    print()
    
    # Discover all benchmark pairs
    print("Discovering benchmark pairs...")
    pairs = discover_benchmark_pairs(base_dir)
    
    commits = sorted(pairs.keys())
    total_commits = len(commits)
    
    if total_commits == 0:
        print("ERROR: No commits found!")
        print("Expected directory structure:")
        print("  final/")
        print("    no_regression/")
        print("      commit1_xxx/")
        print("        handwritten_results/")
        print("        ai_results/")
        print("    regression/")
        print("      commit1_xxx/")
        print("        handwritten_results/")
        print("        ai_results/")
        return
    
    print(f"Found {total_commits} commits")
    print()
    
    stats_lines = []
    summary_lines = []
    regression_lines = []

    overall_detected_hw = 0
    overall_regressions_hw = 0
    overall_improvements_hw = 0
    overall_total_hw = 0
    
    overall_detected_ai = 0
    overall_regressions_ai = 0
    overall_improvements_ai = 0
    overall_total_ai = 0

    for idx, commit_name in enumerate(commits, start=1):
        print(f"[{idx}/{total_commits}] Processing {commit_name}")

        stats_lines.append(f"Commit: {commit_name}")
        stats_lines.append("=" * 80)
        summary_lines.append(f"Commit: {commit_name}")
        regression_lines.append(f"Commit: {commit_name}")

        commit_data = pairs[commit_name]
        
        # Process handwritten benchmarks
        handwritten_benchmarks = commit_data['handwritten']
        ai_benchmarks = commit_data['ai']
        
        hw_detected = 0
        hw_regressions = 0
        hw_improvements = 0
        hw_total = 0
        
        ai_detected = 0
        ai_regressions = 0
        ai_improvements = 0
        ai_total = 0
        
        # HANDWRITTEN BENCHMARKS
        if handwritten_benchmarks:
            stats_lines.append("\n--- HANDWRITTEN BENCHMARKS ---\n")
            summary_lines.append("  Handwritten Benchmarks:")
            
            for bench_name, bench_paths in sorted(handwritten_benchmarks.items()):
                no_reg_path = bench_paths['no_regression']
                reg_path = bench_paths['regression']
                
                # Skip empty JSONs
                if is_empty_json_file(no_reg_path) or is_empty_json_file(reg_path):
                    stats_lines.append(f"  {bench_name}: SKIPPED (empty JSON)")
                    continue
                
                no_regression = load_jmh_scores(no_reg_path)
                regression = load_jmh_scores(reg_path)
                
                # Compute ratio of means via hierarchical bootstrap
                ratios = hierarchical_bootstrap_ratio(no_regression, regression)
                
                # Point estimate: ratio of sample means
                flat_no_reg = np.concatenate(no_regression)
                flat_reg = np.concatenate(regression)
                point_estimate = np.mean(flat_reg) / np.mean(flat_no_reg)
                
                # Confidence interval for ratio
                alpha = 1 - CONF_LEVEL
                lo, hi = np.percentile(ratios, [alpha / 2 * 100, (1 - alpha / 2) * 100])
                
                # Statistical significance: CI excludes 1
                is_significant = (lo > 1.0 or hi < 1.0)
                
                # Classification
                is_regression = (lo > 1.0)  # Regression code is slower
                is_improvement = (hi < 1.0)  # Regression code is faster (shouldn't happen)
                
                # Convert to percentage change
                pct_change = (point_estimate - 1.0) * 100
                pct_lo = (lo - 1.0) * 100
                pct_hi = (hi - 1.0) * 100
                margin = max(abs(pct_change - pct_lo), abs(pct_hi - pct_change))
                
                # Additional statistics
                p_gt_1 = np.mean(ratios > 1.0)
                a12 = vargha_delaney_a12(flat_reg, flat_no_reg)
                
                # Update counters
                hw_total += 1
                overall_total_hw += 1
                
                if is_significant:
                    hw_detected += 1
                    overall_detected_hw += 1
                    
                    if is_regression:
                        hw_regressions += 1
                        overall_regressions_hw += 1
                    elif is_improvement:
                        hw_improvements += 1
                        overall_improvements_hw += 1
                
                # Format output
                stats_lines.append(f"\n  Benchmark: {bench_name}")
                stats_lines.append(f"    Point estimate (ratio): {point_estimate:.6f}")
                
                if pct_change >= 0:
                    stats_lines.append(
                        f"    Performance change: {abs(pct_change):.2f}% ± {margin:.2f}% SLOWER"
                    )
                else:
                    stats_lines.append(
                        f"    Performance change: {abs(pct_change):.2f}% ± {margin:.2f}% FASTER"
                    )
                
                stats_lines.append(
                    f"    {int(CONF_LEVEL*100)}% CI for ratio: [{lo:.6f}, {hi:.6f}]"
                )
                stats_lines.append(
                    f"    {int(CONF_LEVEL*100)}% CI (percentage): [{pct_lo:.2f}%, {pct_hi:.2f}%]"
                )
                stats_lines.append(f"    P(ratio > 1): {p_gt_1:.4f}")
                stats_lines.append(
                    f"    Vargha-Delaney A12 (Regression > No-Regression): {a12:.4f}"
                )
                
                # Significance classification
                if is_regression:
                    stats_lines.append("    >>> SIGNIFICANT REGRESSION DETECTED (slower)")
                    regression_lines.append(
                        f"  [HW] {bench_name}: REGRESSION ({abs(pct_change):.2f}% ± {margin:.2f}% slower)"
                    )
                elif is_improvement:
                    stats_lines.append("    >>> SIGNIFICANT IMPROVEMENT (faster) - UNEXPECTED!")
                else:
                    stats_lines.append("    >>> NOT SIGNIFICANT (CI includes 1)")
                
                # Summary line
                sig_marker = "✓" if is_significant else "✗"
                summary_lines.append(
                    f"    {sig_marker} {bench_name}: {pct_change:+.2f}% ± {margin:.2f}% "
                    f"[CI: {pct_lo:.2f}%, {pct_hi:.2f}%]"
                )
        
        # AI-GENERATED BENCHMARKS
        if ai_benchmarks:
            stats_lines.append("\n--- AI-GENERATED BENCHMARKS ---\n")
            summary_lines.append("  AI-Generated Benchmarks:")
            
            for bench_name, bench_paths in sorted(ai_benchmarks.items()):
                no_reg_path = bench_paths['no_regression']
                reg_path = bench_paths['regression']
                
                # Skip empty JSONs
                if is_empty_json_file(no_reg_path) or is_empty_json_file(reg_path):
                    stats_lines.append(f"  {bench_name}: SKIPPED (empty JSON)")
                    continue
                
                no_regression = load_jmh_scores(no_reg_path)
                regression = load_jmh_scores(reg_path)
                
                # Compute ratio of means via hierarchical bootstrap
                ratios = hierarchical_bootstrap_ratio(no_regression, regression)
                
                # Point estimate: ratio of sample means
                flat_no_reg = np.concatenate(no_regression)
                flat_reg = np.concatenate(regression)
                point_estimate = np.mean(flat_reg) / np.mean(flat_no_reg)
                
                # Confidence interval for ratio
                alpha = 1 - CONF_LEVEL
                lo, hi = np.percentile(ratios, [alpha / 2 * 100, (1 - alpha / 2) * 100])
                
                # Statistical significance: CI excludes 1
                is_significant = (lo > 1.0 or hi < 1.0)
                
                # Classification
                is_regression = (lo > 1.0)  # Regression code is slower
                is_improvement = (hi < 1.0)  # Regression code is faster
                
                # Convert to percentage change
                pct_change = (point_estimate - 1.0) * 100
                pct_lo = (lo - 1.0) * 100
                pct_hi = (hi - 1.0) * 100
                margin = max(abs(pct_change - pct_lo), abs(pct_hi - pct_change))
                
                # Additional statistics
                p_gt_1 = np.mean(ratios > 1.0)
                a12 = vargha_delaney_a12(flat_reg, flat_no_reg)
                
                # Update counters
                ai_total += 1
                overall_total_ai += 1
                
                if is_significant:
                    ai_detected += 1
                    overall_detected_ai += 1
                    
                    if is_regression:
                        ai_regressions += 1
                        overall_regressions_ai += 1
                    elif is_improvement:
                        ai_improvements += 1
                        overall_improvements_ai += 1
                
                # Format output
                stats_lines.append(f"\n  Benchmark: {bench_name}")
                stats_lines.append(f"    Point estimate (ratio): {point_estimate:.6f}")
                
                if pct_change >= 0:
                    stats_lines.append(
                        f"    Performance change: {abs(pct_change):.2f}% ± {margin:.2f}% SLOWER"
                    )
                else:
                    stats_lines.append(
                        f"    Performance change: {abs(pct_change):.2f}% ± {margin:.2f}% FASTER"
                    )
                
                stats_lines.append(
                    f"    {int(CONF_LEVEL*100)}% CI for ratio: [{lo:.6f}, {hi:.6f}]"
                )
                stats_lines.append(
                    f"    {int(CONF_LEVEL*100)}% CI (percentage): [{pct_lo:.2f}%, {pct_hi:.2f}%]"
                )
                stats_lines.append(f"    P(ratio > 1): {p_gt_1:.4f}")
                stats_lines.append(
                    f"    Vargha-Delaney A12 (Regression > No-Regression): {a12:.4f}"
                )
                
                # Significance classification
                if is_regression:
                    stats_lines.append("    >>> SIGNIFICANT REGRESSION DETECTED (slower)")
                    regression_lines.append(
                        f"  [AI] {bench_name}: REGRESSION ({abs(pct_change):.2f}% ± {margin:.2f}% slower)"
                    )
                elif is_improvement:
                    stats_lines.append("    >>> SIGNIFICANT IMPROVEMENT (faster) - UNEXPECTED!")
                else:
                    stats_lines.append("    >>> NOT SIGNIFICANT (CI includes 1)")
                
                # Summary line
                sig_marker = "✓" if is_significant else "✗"
                summary_lines.append(
                    f"    {sig_marker} {bench_name}: {pct_change:+.2f}% ± {margin:.2f}% "
                    f"[CI: {pct_lo:.2f}%, {pct_hi:.2f}%]"
                )
        
        # Commit summary
        stats_lines.append(f"\n{'='*80}")
        stats_lines.append(f"Commit {commit_name} Summary:")
        stats_lines.append(f"  Handwritten Benchmarks:")
        stats_lines.append(f"    Total: {hw_total}")
        stats_lines.append(f"    Significant differences: {hw_detected} ({100*hw_detected/hw_total:.1f}%)" if hw_total > 0 else "    Significant differences: 0")
        stats_lines.append(f"      - Regressions detected: {hw_regressions}")
        stats_lines.append(f"      - Improvements detected: {hw_improvements}")
        stats_lines.append(f"  AI-Generated Benchmarks:")
        stats_lines.append(f"    Total: {ai_total}")
        stats_lines.append(f"    Significant differences: {ai_detected} ({100*ai_detected/ai_total:.1f}%)" if ai_total > 0 else "    Significant differences: 0")
        stats_lines.append(f"      - Regressions detected: {ai_regressions}")
        stats_lines.append(f"      - Improvements detected: {ai_improvements}")
        stats_lines.append("")

        summary_lines.append(
            f"  Handwritten: {hw_detected}/{hw_total} significant "
            f"({100*hw_detected/hw_total:.1f}%) | " if hw_total > 0 else "  Handwritten: No benchmarks | "
            f"Regressions: {hw_regressions} | Improvements: {hw_improvements}"
        )
        summary_lines.append(
            f"  AI-Generated: {ai_detected}/{ai_total} significant "
            f"({100*ai_detected/ai_total:.1f}%) | " if ai_total > 0 else "  AI-Generated: No benchmarks | "
            f"Regressions: {ai_regressions} | Improvements: {ai_improvements}"
        )
        summary_lines.append("")

        if hw_regressions == 0 and ai_regressions == 0:
            regression_lines.append("  No confirmed regressions")
        regression_lines.append("")

    # Overall summary
    summary_lines.append("=" * 80)
    summary_lines.append("OVERALL SUMMARY")
    summary_lines.append("=" * 80)
    summary_lines.append(f"Total commits analyzed: {total_commits}")
    summary_lines.append("")
    summary_lines.append("HANDWRITTEN BENCHMARKS:")
    summary_lines.append(f"  Total benchmarks: {overall_total_hw}")
    summary_lines.append(
        f"  Significant differences: {overall_detected_hw} ({100*overall_detected_hw/overall_total_hw:.1f}%)" if overall_total_hw > 0 else "  Significant differences: 0"
    )
    summary_lines.append(f"    - Regressions detected: {overall_regressions_hw}")
    summary_lines.append(f"    - Improvements detected: {overall_improvements_hw}")
    summary_lines.append("")
    summary_lines.append("AI-GENERATED BENCHMARKS:")
    summary_lines.append(f"  Total benchmarks: {overall_total_ai}")
    summary_lines.append(
        f"  Significant differences: {overall_detected_ai} ({100*overall_detected_ai/overall_total_ai:.1f}%)" if overall_total_ai > 0 else "  Significant differences: 0"
    )
    summary_lines.append(f"    - Regressions detected: {overall_regressions_ai}")
    summary_lines.append(f"    - Improvements detected: {overall_improvements_ai}")
    summary_lines.append("")
    summary_lines.append("COMPARISON:")
    if overall_total_hw > 0 and overall_total_ai > 0:
        hw_detection_rate = 100 * overall_regressions_hw / overall_total_hw
        ai_detection_rate = 100 * overall_regressions_ai / overall_total_ai
        summary_lines.append(f"  Handwritten detection rate: {hw_detection_rate:.1f}%")
        summary_lines.append(f"  AI-generated detection rate: {ai_detection_rate:.1f}%")

    # Write output files
    with open(OUTPUT_STATS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(stats_lines))

    with open(OUTPUT_SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    with open(OUTPUT_REGRESSIONS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(regression_lines))

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"Detailed statistics: {OUTPUT_STATS_FILE}")
    print(f"Quick summary: {OUTPUT_SUMMARY_FILE}")
    print(f"Confirmed regressions: {OUTPUT_REGRESSIONS_FILE}")
    print("=" * 80)


if __name__ == "__main__":
    main()