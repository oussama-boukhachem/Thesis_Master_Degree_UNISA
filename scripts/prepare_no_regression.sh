#!/bin/bash

# Script to prepare no_regression baseline by commenting out injected code

set -e  # Exit on error

echo "=========================================="
echo "Preparing No-Regression Baseline Tests"
echo "=========================================="

# Function to comment out Blackhole.consumeCPU line
comment_injection() {
    local file=$1
    echo "Commenting injection in: $file"
    sed -i 's/^        org\.openjdk\.jmh\.infra\.Blackhole\.consumeCPU(1000000L);$/        \/\/ org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);/' "$file"
}

# COMMIT 1 FILES
echo ""
echo "--- Commit 1: Commenting injected code ---"

# Benchmark files
comment_injection "/home/amesso/thesis/commit1_b038730/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/notify/JmhParkVsNotifyBenchmark.java"
comment_injection "/home/amesso/thesis/commit1_b038730/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/ai/JmhParkVsNotifyBenchmarkAI.java"

# Core file
comment_injection "/home/amesso/thesis/commit1_b038730/source/modules/core/src/main/java/org/apache/ignite/internal/processors/cache/IgniteCacheProxy.java"

# COMMIT 2 FILES
echo ""
echo "--- Commit 2: Commenting injected code ---"

# Benchmark files
comment_injection "/home/amesso/thesis/commit2_feba953/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/future/JmhFutureAdapterBenchmark.java"
comment_injection "/home/amesso/thesis/commit2_feba953/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/ai/JmhFutureAdapterBenchmarkAI.java"
comment_injection "/home/amesso/thesis/commit2_feba953/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/misc/JmhIncrementBenchmark.java"
comment_injection "/home/amesso/thesis/commit2_feba953/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/ai/JmhIncrementBenchmarkAI.java"

# Core file
comment_injection "/home/amesso/thesis/commit2_feba953/source/modules/core/src/main/java/org/apache/ignite/internal/processors/cache/IgniteCacheProxy.java"

# COMMIT 3 FILES
echo ""
echo "--- Commit 3: Commenting injected code ---"

# Benchmark files
comment_injection "/home/amesso/thesis/commit3_160dab0/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/future/JmhFutureAdapterBenchmark.java"
comment_injection "/home/amesso/thesis/commit3_160dab0/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/ai/JmhFutureAdapterBenchmarkAI.java"
comment_injection "/home/amesso/thesis/commit3_160dab0/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/misc/JmhIncrementBenchmark.java"
comment_injection "/home/amesso/thesis/commit3_160dab0/source/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh/ai/JmhIncrementBenchmarkAI.java"

# Core file
comment_injection "/home/amesso/thesis/commit3_160dab0/source/modules/core/src/main/java/org/apache/ignite/internal/processors/cache/IgniteCacheProxy.java"

echo ""
echo "=========================================="
echo "All injection code commented out!"
echo "=========================================="

# Rebuild all commits
echo ""
echo "--- Rebuilding Commit 1 ---"
cd /home/amesso/thesis/commit1_b038730/source
mvn clean install -Dmaven.test.skip=true -Dmaven.javadoc.skip=true 2>&1 | tee ../../build_commit1_no_regression.log
echo "Commit 1 rebuilt successfully!"

echo ""
echo "--- Rebuilding Commit 2 ---"
cd /home/amesso/thesis/commit2_feba953/source
mvn clean install -Dmaven.test.skip=true -Dmaven.javadoc.skip=true 2>&1 | tee ../../build_commit2_no_regression.log
echo "Commit 2 rebuilt successfully!"

echo ""
echo "--- Rebuilding Commit 3 ---"
cd /home/amesso/thesis/commit3_160dab0/source
mvn clean install -Dmaven.test.skip=true -Dmaven.javadoc.skip=true 2>&1 | tee ../../build_commit3_no_regression.log
echo "Commit 3 rebuilt successfully!"

echo ""
echo "=========================================="
echo "All commits rebuilt without injection code!"
echo "Ready to run no_regression tests."
echo "=========================================="
