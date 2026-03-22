# Raw JSON Outputs (Manual Upload Required)

Add all raw JMH JSON outputs in this folder.

## Required organization

Use this structure:

- `no_regression/commit1_b038730/handwritten_results/`
- `no_regression/commit1_b038730/ai_results/`
- `no_regression/commit2_feba953/handwritten_results/`
- `no_regression/commit2_feba953/ai_results/`
- `no_regression/commit3_160dab0/handwritten_results/`
- `no_regression/commit3_160dab0/ai_results/`

- `regression/commit1_b038730/handwritten_results/`
- `regression/commit1_b038730/ai_results/`
- `regression/commit2_feba953/handwritten_results/`
- `regression/commit2_feba953/ai_results/`
- `regression/commit3_160dab0/handwritten_results/`
- `regression/commit3_160dab0/ai_results/`

## Minimum expected files

- Commit 1: 2 handwritten + 2 AI per condition
- Commit 2: 7 handwritten + 7 AI per condition
- Commit 3: 7 handwritten + 7 AI per condition

Total expected JSON count across both conditions: **64 files**

## Important

Do not rename benchmark JSON files after generation; keep original names to preserve traceability with scripts and figures.

