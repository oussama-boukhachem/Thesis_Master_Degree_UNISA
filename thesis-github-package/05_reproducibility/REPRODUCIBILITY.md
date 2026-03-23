# Reproducibility Guide (Point-by-Point)

This guide describes the full workflow to reproduce the thesis results.

## 0) Prerequisites

- Linux environment (recommended, matching original runs)
- Java/OpenJDK compatible with Ignite benchmark module
- Maven
- Python 3 + required analysis libraries

## 1) Clone Apache Ignite

```bash
git clone https://github.com/apache/ignite.git
cd ignite
```

## 2) Checkout target commits

```bash
git checkout b038730
# run commit1 workflow

git checkout feba953
# run commit2 workflow

git checkout 160dab0
# run commit3 workflow
```

## 3) Place benchmark sources

For each commit, place handwritten and AI-generated benchmark classes in:

`modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh`

## 4) Build benchmark module

```bash
cd modules/benchmarks
mvn -DskipTests package
```

## 5) Baseline run (no regression)

- Ensure benchmark code is in clean (non-injected) state.
- Run the baseline execution script.
- Save JSON outputs under:
  - `04_results/raw_json/no_regression/...`

## 6) Inject controlled regression

Use injection script (Blackhole-based slowdown):

```bash
bash inject_regression_code.sh
```

## 7) Regression run

- Execute regression script on all target benchmarks.
- Save JSON outputs under:
  - `04_results/raw_json/regression/...`

## 8) Statistical analysis

Run hierarchical bootstrap analysis script on baseline + regression JSON outputs.

Store outputs in `04_results/analysis_exports/` (or equivalent folder).

## 9) Generate figures

Run visualization script to produce:

- Detection rate plots
- Coverage plots
- Impact distributions
- Per-commit comparisons
- Summary statistics figure/table

Save final figures under `04_results/figures/`.

## 10) Verify expected final artifacts

Checklist:

- Raw JSON outputs uploaded (expected 64 files total)
- Analysis output files present
- Final figures present
- README and section docs updated
- Commit hashes and script names consistent across documentation

## 11) Optional: AI generation transparency

If reproducing AI benchmark generation, document in `01_data_collection/`:

- Prompt text
- Model/version
- Generation settings
- Any manual edits before execution

