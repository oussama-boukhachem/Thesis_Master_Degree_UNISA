#!/bin/bash

# Final production run script for REGRESSION testing (with injected code)
# Runs all benchmarks except park/notify (they freeze)
# Full parameters: 10 forks, 3000 iterations, singleshot mode

set -e

BASE_DIR="/home/amesso/thesis"
RESULTS_DIR="$BASE_DIR/finals/regression"

JVM_OPTS="-Xms12g -Xmx16g"
FORKS=10
ITERATIONS=3000
WARMUP=0
BENCHMARK_MODE="ss"
TIME_UNIT="ms"

echo "=========================================="
echo "FINAL NO-REGRESSION BASELINE (CLEAN CODE)"
echo "Full parameters: 10 forks, 3000 iterations"
echo "=========================================="
echo ""

# ==========================================
# COMMIT 1: b038730 (4 benchmarks - 2 handwritten + 2 AI)
# ==========================================
echo "=========================================="
echo "COMMIT 1: b038730"
echo "=========================================="

COMMIT1_DIR="$BASE_DIR/NEW_Final/commit1_b038730/modules/benchmarks"
cd "$COMMIT1_DIR"
COMMIT1_JAR=$(ls target/ignite-benchmarks-*.jar | grep -v "sources\|tests\|javadoc")

# Handwritten benchmarks
echo "Running handwritten: JmhCacheBenchmark.get"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT1_JAR" org.openjdk.jmh.Main "JmhCacheBenchmark.get" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit1_b038730/handwritten_results/JmhCacheBenchmark_get.json" \
    2>&1 | tee "$RESULTS_DIR/commit1_b038730/handwritten_results/JmhCacheBenchmark_get.log"

echo "Running handwritten: JmhCacheBenchmark.put"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT1_JAR" org.openjdk.jmh.Main "JmhCacheBenchmark.put" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit1_b038730/handwritten_results/JmhCacheBenchmark_put.json" \
    2>&1 | tee "$RESULTS_DIR/commit1_b038730/handwritten_results/JmhCacheBenchmark_put.log"

# AI benchmarks
echo "Running AI: JmhCacheBenchmarkAI.get"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT1_JAR" org.openjdk.jmh.Main "JmhCacheBenchmarkAI.get" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit1_b038730/ai_results/JmhCacheBenchmarkAI_get.json" \
    2>&1 | tee "$RESULTS_DIR/commit1_b038730/ai_results/JmhCacheBenchmarkAI_get.log"

echo "Running AI: JmhCacheBenchmarkAI.put"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT1_JAR" org.openjdk.jmh.Main "JmhCacheBenchmarkAI.put" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit1_b038730/ai_results/JmhCacheBenchmarkAI_put.json" \
    2>&1 | tee "$RESULTS_DIR/commit1_b038730/ai_results/JmhCacheBenchmarkAI_put.log"

# ==========================================
# COMMIT 2: feba953 (14 benchmarks - 7 handwritten + 7 AI)
# ==========================================
echo ""
echo "=========================================="
echo "COMMIT 2: feba953"
echo "=========================================="

COMMIT2_DIR="$BASE_DIR/NEW_Final/commit2_feba953/modules/benchmarks"
cd "$COMMIT2_DIR"
COMMIT2_JAR=$(ls target/ignite-benchmarks-*.jar | grep -v "sources\|tests\|javadoc")

# Handwritten benchmarks
echo "Running handwritten: JmhCacheBenchmark.get"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhCacheBenchmark.get" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhCacheBenchmark_get.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhCacheBenchmark_get.log"

echo "Running handwritten: JmhCacheBenchmark.put"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhCacheBenchmark.put" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhCacheBenchmark_put.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhCacheBenchmark_put.log"

echo "Running handwritten: JmhFutureAdapterBenchmark.testSimpleGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmark.testSimpleGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGet.log"

echo "Running handwritten: JmhFutureAdapterBenchmark.testSimpleGetWithListener"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmark.testSimpleGetWithListener" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGetWithListener.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGetWithListener.log"

echo "Running handwritten: JmhFutureAdapterBenchmark.completeFutureGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmark.completeFutureGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhFutureAdapterBenchmark_completeFutureGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhFutureAdapterBenchmark_completeFutureGet.log"

echo "Running handwritten: JmhIncrementBenchmark.increment"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmark.increment" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhIncrementBenchmark_increment.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhIncrementBenchmark_increment.log"

echo "Running handwritten: JmhIncrementBenchmark.threadLocalIncrement"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmark.threadLocalIncrement" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhIncrementBenchmark_threadLocalIncrement.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/handwritten_results/JmhIncrementBenchmark_threadLocalIncrement.log"

# AI benchmarks
echo "Running AI: JmhCacheBenchmarkAI.get"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhCacheBenchmarkAI.get" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/ai_results/JmhCacheBenchmarkAI_get.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/ai_results/JmhCacheBenchmarkAI_get.log"

echo "Running AI: JmhCacheBenchmarkAI.put"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhCacheBenchmarkAI.put" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/ai_results/JmhCacheBenchmarkAI_put.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/ai_results/JmhCacheBenchmarkAI_put.log"

echo "Running AI: JmhFutureAdapterBenchmarkAI.testSimpleGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmarkAI.testSimpleGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGet.log"

echo "Running AI: JmhFutureAdapterBenchmarkAI.testSimpleGetWithListener"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmarkAI.testSimpleGetWithListener" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGetWithListener.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGetWithListener.log"

echo "Running AI: JmhFutureAdapterBenchmarkAI.completeFutureGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmarkAI.completeFutureGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/ai_results/JmhFutureAdapterBenchmarkAI_completeFutureGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/ai_results/JmhFutureAdapterBenchmarkAI_completeFutureGet.log"

echo "Running AI: JmhIncrementBenchmarkAI.increment"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmarkAI.increment" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/ai_results/JmhIncrementBenchmarkAI_increment.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/ai_results/JmhIncrementBenchmarkAI_increment.log"

echo "Running AI: JmhIncrementBenchmarkAI.threadLocalIncrement"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT2_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmarkAI.threadLocalIncrement" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit2_feba953/ai_results/JmhIncrementBenchmarkAI_threadLocalIncrement.json" \
    2>&1 | tee "$RESULTS_DIR/commit2_feba953/ai_results/JmhIncrementBenchmarkAI_threadLocalIncrement.log"

# ==========================================
# COMMIT 3: 160dab0 (14 benchmarks - 7 handwritten + 7 AI)
# ==========================================
echo ""
echo "=========================================="
echo "COMMIT 3: 160dab0"
echo "=========================================="

COMMIT3_DIR="$BASE_DIR/NEW_Final/commit3_160dab0/modules/benchmarks"
cd "$COMMIT3_DIR"
COMMIT3_JAR=$(ls target/ignite-benchmarks-*.jar | grep -v "sources\|tests\|javadoc")

# Handwritten benchmarks
echo "Running handwritten: JmhCacheBenchmark.get"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhCacheBenchmark.get" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhCacheBenchmark_get.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhCacheBenchmark_get.log"

echo "Running handwritten: JmhCacheBenchmark.put"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhCacheBenchmark.put" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhCacheBenchmark_put.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhCacheBenchmark_put.log"

echo "Running handwritten: JmhFutureAdapterBenchmark.testSimpleGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmark.testSimpleGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGet.log"

echo "Running handwritten: JmhFutureAdapterBenchmark.testSimpleGetWithListener"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmark.testSimpleGetWithListener" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGetWithListener.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhFutureAdapterBenchmark_testSimpleGetWithListener.log"

echo "Running handwritten: JmhFutureAdapterBenchmark.completeFutureGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmark.completeFutureGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhFutureAdapterBenchmark_completeFutureGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhFutureAdapterBenchmark_completeFutureGet.log"

echo "Running handwritten: JmhIncrementBenchmark.increment"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmark.increment" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhIncrementBenchmark_increment.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhIncrementBenchmark_increment.log"

echo "Running handwritten: JmhIncrementBenchmark.threadLocalIncrement"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmark.threadLocalIncrement" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhIncrementBenchmark_threadLocalIncrement.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/handwritten_results/JmhIncrementBenchmark_threadLocalIncrement.log"

# AI benchmarks
echo "Running AI: JmhCacheBenchmarkAI.get"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhCacheBenchmarkAI.get" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/ai_results/JmhCacheBenchmarkAI_get.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/ai_results/JmhCacheBenchmarkAI_get.log"

echo "Running AI: JmhCacheBenchmarkAI.put"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhCacheBenchmarkAI.put" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/ai_results/JmhCacheBenchmarkAI_put.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/ai_results/JmhCacheBenchmarkAI_put.log"

echo "Running AI: JmhFutureAdapterBenchmarkAI.testSimpleGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmarkAI.testSimpleGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGet.log"

echo "Running AI: JmhFutureAdapterBenchmarkAI.testSimpleGetWithListener"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmarkAI.testSimpleGetWithListener" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGetWithListener.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/ai_results/JmhFutureAdapterBenchmarkAI_testSimpleGetWithListener.log"

echo "Running AI: JmhFutureAdapterBenchmarkAI.completeFutureGet"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhFutureAdapterBenchmarkAI.completeFutureGet" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/ai_results/JmhFutureAdapterBenchmarkAI_completeFutureGet.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/ai_results/JmhFutureAdapterBenchmarkAI_completeFutureGet.log"

echo "Running AI: JmhIncrementBenchmarkAI.increment"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmarkAI.increment" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/ai_results/JmhIncrementBenchmarkAI_increment.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/ai_results/JmhIncrementBenchmarkAI_increment.log"

echo "Running AI: JmhIncrementBenchmarkAI.threadLocalIncrement"
java $JVM_OPTS -cp "$(cat cp.txt):$COMMIT3_JAR" org.openjdk.jmh.Main "JmhIncrementBenchmarkAI.threadLocalIncrement" \
    -f $FORKS -i $ITERATIONS -wi $WARMUP -bm $BENCHMARK_MODE -tu $TIME_UNIT -rf json \
    -rff "$RESULTS_DIR/commit3_160dab0/ai_results/JmhIncrementBenchmarkAI_threadLocalIncrement.json" \
    2>&1 | tee "$RESULTS_DIR/commit3_160dab0/ai_results/JmhIncrementBenchmarkAI_threadLocalIncrement.log"

echo ""
echo "=========================================="
echo "REGRESSION TEST COMPLETE!"
echo "Total: 32 benchmarks run (16 handwritten + 16 AI)"
echo "Results saved in: $RESULTS_DIR"
echo "=========================================="
