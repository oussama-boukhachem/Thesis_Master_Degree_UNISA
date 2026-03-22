#!/bin/bash
# Inject Blackhole.consumeCPU into all benchmark methods for regression testing

BASE_DIR="/home/amesso/thesis/NEW_Final"
INJECTION_CODE="        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);"

for commit in commit1_b038730 commit2_feba953 commit3_160dab0; do
    echo "=== Processing $commit ==="
    BENCH_DIR="$BASE_DIR/$commit/modules/benchmarks/src/main/java/org/apache/ignite/internal/benchmarks/jmh"
    
    # Find all Java files with @Benchmark annotation
    find "$BENCH_DIR" -name "*.java" -type f | while read -r file; do
        # Check if file has @Benchmark methods
        if grep -q "@Benchmark" "$file"; then
            echo "  Injecting into: $(basename $file)"
            
            # Use awk to inject after method opening brace following @Benchmark
            awk '
            /@Benchmark/ { benchmark=1; print; next }
            benchmark && /{/ && !injected { 
                print
                print "        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);"
                injected=1
                benchmark=0
                next
            }
            /^[[:space:]]*}[[:space:]]*$/ { injected=0 }
            { print }
            ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        fi
    done
    echo ""
done

echo "✓ Injection complete fore all commits"
