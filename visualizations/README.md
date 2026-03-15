# Visualizations

This folder contains the figures generated from the benchmark analysis.

## Main files

- `detection_rate_comparison.*`: detection rate comparison between handwritten and AI-generated benchmarks.
- `benchmark_count.*`: number of benchmark pairs per commit.
- `performance_impact.*` and `performance_impact_1_of_3.*` ... `performance_impact_3_of_3.*`: slowdown impact plots.
- `all_benchmarks_ranked.*`: ranking of benchmark pairs by measured slowdown.
- `category_analysis.*`, `Average_Regression_Impact_by_Category.*`, `Performance_Impact_Distribution_by_Benchmark_Category.*`: category-level views.
- `summary_statistics.*`: summary table as image.
- `thesis_summary_figure.*`: combined summary figure.

Each chart is available in PNG and PDF format.

## Regeneration

From the project root, run:

```bash
python scripts/visualize_results.py
```

## Notes

- These files are output artifacts used in the thesis results chapter.
- They are included as-is from the final analysis run.
