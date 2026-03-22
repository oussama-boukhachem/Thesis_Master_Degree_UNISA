/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.ignite.internal.benchmarks.jmh.ai;

import java.util.concurrent.atomic.AtomicLong;
import org.apache.ignite.internal.benchmarks.jmh.JmhAbstractBenchmark;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;

/**
 * AI-generated benchmark comparing increment strategies.
 */
@State(Scope.Benchmark)
public class JmhIncrementBenchmarkAI extends JmhAbstractBenchmark {
    /** Batch size for thread-local increments. */
    private static final int INCREMENT_BATCH = 1024;

    /** Atomic counter. */
    private final AtomicLong atomicCounter = new AtomicLong();

    /** Thread-local storage for batched increments. */
    private static final ThreadLocal<Long> LOCAL_COUNTER = new ThreadLocal<Long>() {
        @Override protected Long initialValue() {
            return 0L;
        }
    };

    /**
     * Benchmark atomic increment.
     *
     * @return New counter value.
     */
    @Benchmark
    public long increment() {
        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // INJECTED CODE FOR REGRESSION TESTING - DO NOT REMOVE
        // org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // END INJECTED CODE
        
        return atomicCounter.incrementAndGet();
    }

    /**
     * Benchmark thread-local batched increment.
     *
     * @return New counter value.
     */
    @Benchmark
    public long threadLocalIncrement() {
        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // INJECTED CODE FOR REGRESSION TESTING - DO NOT REMOVE
        // org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // END INJECTED CODE
        
        long localValue = LOCAL_COUNTER.get();

        // Every batch, sync with atomic counter
        if ((localValue & (INCREMENT_BATCH - 1)) == 0)
            localValue = atomicCounter.addAndGet(INCREMENT_BATCH);

        LOCAL_COUNTER.set(++localValue);

        return localValue;
    }
}
