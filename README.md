# Thesis Benchmark Workspace

This repository contains the benchmark artifacts used in the thesis:

*Comparing handwritten and AI-generated microbenchmarks for performance regression detection*

## What is included

- `benchmarks/`: Java benchmark sources grouped by commit, with original module structure preserved.
- `scripts/inject_regression_code.sh`: injects the regression code into benchmark methods.
- `scripts/prepare_no_regression.sh`: comments out injected lines for no-regression baseline runs.
- `scripts/optimize_system.sh`: applies system tuning before execution.
- `scripts/visualize_results.py`: generates the result charts.
- `visualizations/`: generated charts used in the analysis.

## Benchmark snapshots

- `commit1_b038730`
- `commit2_feba953`
- `commit3_160dab0`

For each snapshot, files are kept under:

`modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh`

Both handwritten and AI-generated benchmark classes are included.

## Scope

This repository is a curated thesis package. It does not include the full Apache Ignite project, build artifacts, or unrelated modules.
