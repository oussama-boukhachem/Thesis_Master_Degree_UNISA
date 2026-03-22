# Comparing Developer-Written vs AI-Generated Microbenchmarks for Performance Regression Detection

## Overview
This repository contains the replication package for the thesis "Comparing Developer-Written vs AI-Generated Microbenchmarks for Performance Regression Detection". The study evaluates whether AI-generated JMH (Java Microbenchmark Harness) benchmarks can reliably detect software performance regressions with the same efficacy as manually written benchmarks. 

We utilize Apache Ignite as our case study, selecting 3 distinct commits spanning versions 1.8.0 to 2.2.0. For each human-written microbenchmark in these commits, an equivalent AI-twin benchmark was generated using Large Language Models.

## Data Gathering Methodology
Data gathering was conducted through rigorous, automated benchmark executions:
1. **Benchmark Selection:** 32 benchmarks (16 handwritten, 16 AI-generated) were selected across 3 Apache Ignite commits. 
2. **Environment:** All tests were run on a dedicated Ubuntu 24.04 server (128GB RAM, 7 CPUs, OpenJDK 1.8.0_482) to minimize external noise.
3. **Execution Mode (No Regression):** A clean baseline was established by running the benchmarks using JMH configured with 10 forks and 3000 iterations in single-shot time mode.
4. **Execution Mode (Regression):** Simulated performance regressions were injected programmatically into the target methods using JMH's `Blackhole.consumeCPU(1000000L)`. The benchmark suites were then re-executed.
5. **Output Format:** All JMH output was consolidated into structured `.json` files to preserve precise metric distributions for analysis.

## Data Analysis Methodology
We analyzed the results using a **Hierarchical Bootstrap** statistical methodology. 
Since JMH benchmark iterations are not strictly independent (iterations within the same JVM fork are correlated), standard statistical tests may yield false positives. 
The Hierarchical Bootstrap approach simulates thousands of resampling iterations (sampling first at the fork level, and then at the iteration level) to calculate proper Confidence Intervals (CIs) and p-values. We used this to determine if the injected regression caused a statistically significant performance degradation and to analyze the differences in variance and execution metrics between Human and AI implementations.

## Repository Structure
This repository contains only the specific benchmark files, execution scripts, and result data required to replicate the thesis experiments, to adhere to GitHub size limits.

* **`benchmark_sources/`**: Contains the `.java` source code for both the handwritten and AI-generated benchmarks, organized by the Apache Ignite commit hashes.
* **`prompts/`**: Markdown files documenting the exact LLM prompts used to generate the AI benchmarks.
* **`results/`**: Contains the raw JMH `.json` outputs for both the stable baseline (`no_regression/`) and injected state (`regression/`). 
* **`scripts/`**: Bash and Python scripts designed to automate regression injection, JMH execution, and Hierarchical Bootstrap statistical analysis.
* **`visualizations/`**: Graphical plots and text summaries generated from the bootstrap analysis.

## Step-by-Step Reproducibility Guide

To reproduce the exact environment and results described in this thesis, follow these steps:

### 1. Environment Setup
1. Ensure you have **Java 8 (OpenJDK 1.8)** and **Apache Maven 3.x** installed.
2. Install **Python 3.x**, along with the packages: `numpy`, `scipy`, `pandas`, `matplotlib`, and `seaborn`.

### 2. Repository Preparation
1. Clone the Apache Ignite source code:
   ```bash
   git clone https://github.com/apache/ignite.git
   cd ignite
   ```

### 3. Generating AI Benchmarks
*(Optional: If you wish to reproduce the generation phase)*
1. Feed the LLM prompt located in `prompts/AI_BENCHMARK_GENERATION_PROMPT.md` to your selected Large Language Model.
2. Append the target handwritten benchmark code to the prompt to instruct the AI to generate a functional twin.

### 4. Running a Specific Commit
For each commit hash (`b038730`, `feba953`, `160dab0`), perform the following:
1. Checkout the specific commit:
   ```bash
   git checkout <COMMIT_HASH>
   ```
2. Copy the corresponding `.java` benchmark files (both Handwritten and AI-generated) from `benchmark_sources/<COMMIT_HASH>/` into the Ignite JMH module directory (`modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/`).
3. Compile the benchmarks:
   ```bash
   cd modules/benchmarks
   mvn clean package -DskipTests
   ```

### 5. Executing the Baseline (No Regression)
1. Run system optimizations using `bash scripts/optimize_system.sh`.
2. Run the prepared execution script using `bash scripts/run_finals_no_regression.sh`.
3. Output JSONs will be saved to your specified results directory.

### 6. Injecting Regressions & Re-executing (Regression)
1. Run the injection script: `bash scripts/inject_regression_code.sh`. This automatically targets the benchmark methods to inject `Blackhole.consumeCPU(1000000L);`.
2. Re-compile the JMH module using Maven.
3. Run the execution script again using `bash scripts/run_finals_regression.sh` to generate the regression JSON files.
4. Run `bash scripts/restore_system.sh` to return operating system settings to normal.

### 7. Statistical Analysis
1. Place both `no_regression` and `regression` JSON outputs into the designated directories expected by the python script.
2. Run the Hierarchical Bootstrap analysis:
   ```bash
   python scripts/hierarchical_bootstrap.py
   ```
3. Observe the generated console output, `hierarchical_bootstrap_summary.txt`, and the charts stored in the `visualizations/` directory.
