# Thesis Reproducibility Package

This folder is the cleaned GitHub package for the thesis:

**Comparing Handwritten and AI-Generated Microbenchmarks for Performance Regression Detection**

The goal is to make the work understandable and reproducible for someone who did not run the experiments.

## 1) Thesis in brief

This thesis compares handwritten and AI-generated JMH microbenchmarks for detecting known performance regressions in Apache Ignite.

The study evaluates:

- Regression detection success rate
- Magnitude of detected performance impact
- Consistency across multiple Ignite versions/commits

## 2) How data was gathered

Data was collected by running benchmark suites on selected Apache Ignite commits:

- `b038730` (commit1, v1.8.0)
- `feba953` (commit2, v2.0.0)
- `160dab0` (commit3, v2.2.0)

For each commit:

- A **no-regression baseline** execution was run
- A **regression-injected** execution was run using `Blackhole.consumeCPU(1000000L)`
- Both handwritten and AI-generated benchmark variants were executed
- JMH raw output was saved as JSON files

## 3) How data was analyzed

Analysis is based on:

- Benchmark-level JSON outputs
- Hierarchical bootstrap statistical processing
- Summary metrics and visualizations (detection rate, impact distribution, per-commit comparisons)

The statistical method and implementation are documented under:

- `03_scripts/prof_bootstrap/`

## 4) Repository structure (what each part is about)

- `01_data_collection/`  
  Data provenance, commit selection, benchmark selection, and AI generation metadata.

- `02_benchmarks/`  
  Benchmark source-code package (handwritten + AI-generated) organized by commit.

- `03_scripts/`  
  Scripts used for environment preparation, regression injection, benchmark execution, and analysis.

- `04_results/`  
  Raw outputs and analysis artifacts.

- `04_results/raw_json/`  
  **Raw JMH JSON outputs** (you will add these manually).

- `04_results/figures/`  
  Final plots/tables used in thesis reporting.

- `05_reproducibility/`  
  Point-by-point guide to reproduce the full workflow.

## 5) Current status

This package structure is prepared.  
You still need to manually add raw JSON outputs to:

- `04_results/raw_json/`

Then commit and push this folder to your thesis GitHub repository.

