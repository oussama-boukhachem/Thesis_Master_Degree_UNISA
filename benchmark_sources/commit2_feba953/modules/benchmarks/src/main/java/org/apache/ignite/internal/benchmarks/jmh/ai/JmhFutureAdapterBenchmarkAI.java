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

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import org.apache.ignite.internal.IgniteInternalFuture;
import org.apache.ignite.internal.benchmarks.jmh.JmhAbstractBenchmark;
import org.apache.ignite.internal.util.future.GridFutureAdapter;
import org.apache.ignite.lang.IgniteInClosure;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.Setup;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.TearDown;
import org.openjdk.jmh.annotations.Threads;

/**
 * AI-generated benchmark for GridFutureAdapter operations.
 */
public class JmhFutureAdapterBenchmarkAI extends JmhAbstractBenchmark {
    /** Result value for completed futures. */
    private static final Long RESULT_VALUE = 0L;

    /** Listener that does nothing. */
    private static final IgniteInClosure<IgniteInternalFuture<Long>> NO_OP_LISTENER = 
        new IgniteInClosure<IgniteInternalFuture<Long>>() {
            @Override public void apply(IgniteInternalFuture<Long> future) {
                // No operation
            }
        };

    /**
     * State for concurrent future completion test.
     */
    @State(Scope.Thread)
    public static class ConcurrentCompletionState {
        /** Queue for future completion coordination. */
        private final BlockingQueue<GridFutureAdapter<Long>> futureQueue = new ArrayBlockingQueue<>(10);

        /** Background thread completing futures. */
        private final Thread completionThread = new Thread() {
            @Override public void run() {
                while (!Thread.interrupted()) {
                    GridFutureAdapter<Long> future = futureQueue.poll();
                    if (future != null)
                        future.onDone(RESULT_VALUE);
                }
            }
        };

        /**
         * Start completion thread.
         */
        @Setup 
        public void setup() {
            completionThread.start();
        }

        /**
         * Stop completion thread.
         *
         * @throws InterruptedException If interrupted.
         */
        @TearDown 
        public void destroy() throws InterruptedException {
            completionThread.interrupt();
            completionThread.join();
        }
    }

    /**
     * Test simple future get operation.
     *
     * @throws Exception If failed.
     */
    @Benchmark
    public void testSimpleGet() throws Exception {
        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // INJECTED CODE FOR REGRESSION TESTING - DO NOT REMOVE
        // org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // END INJECTED CODE
        
        GridFutureAdapter<Long> future = new GridFutureAdapter<>();
        future.onDone(RESULT_VALUE);
        future.get();
    }

    /**
     * Test future get with listener attached.
     *
     * @throws Exception If failed.
     */
    @Benchmark
    public void testSimpleGetWithListener() throws Exception {
        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // INJECTED CODE FOR REGRESSION TESTING - DO NOT REMOVE
        // org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // END INJECTED CODE
        
        GridFutureAdapter<Long> future = new GridFutureAdapter<>();
        future.listen(NO_OP_LISTENER);
        future.onDone(RESULT_VALUE);
        future.get();
    }

    /**
     * Test concurrent future completion and get.
     *
     * @param state Thread state with completion queue.
     * @throws Exception If failed.
     */
    @Benchmark
    @Threads(4)
    public void completeFutureGet(ConcurrentCompletionState state) throws Exception {
        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // INJECTED CODE FOR REGRESSION TESTING - DO NOT REMOVE
        // org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        // END INJECTED CODE
        
        GridFutureAdapter<Long> future = new GridFutureAdapter<>();
        state.futureQueue.put(future);
        future.get();
    }
}
