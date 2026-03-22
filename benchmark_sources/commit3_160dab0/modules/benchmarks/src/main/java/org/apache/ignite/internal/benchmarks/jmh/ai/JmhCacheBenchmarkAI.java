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

import java.util.Random;
import org.apache.ignite.IgniteDataStreamer;
import org.apache.ignite.internal.benchmarks.jmh.cache.JmhCacheAbstractBenchmark;
import org.apache.ignite.internal.benchmarks.model.IntValue;
import org.openjdk.jmh.annotations.Benchmark;

/**
 * AI-generated cache benchmark testing GET and PUT operations.
 */
@SuppressWarnings("unchecked")
public class JmhCacheBenchmarkAI extends JmhCacheAbstractBenchmark {
    /** Random number generator. */
    private final Random random = new Random();

    /**
     * Populate cache with test data.
     *
     * @throws Exception If failed.
     */
    public void setup() throws Exception {
        super.setup();

        // Stream data into cache
        try (IgniteDataStreamer<Integer, IntValue> loader = node.dataStreamer(cache.getName())) {
            for (int idx = 0; idx < CNT; idx++) {
                loader.addData(idx, new IntValue(idx));
            }
        }

        System.out.println("Cache populated.");
    }

    /**
     * Benchmark PUT operation.
     *
     * @throws Exception If failed.
     */
    @Benchmark
    public void put() throws Exception {
        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        int keyIdx = random.nextInt(CNT);
        cache.put(keyIdx, new IntValue(keyIdx));
    }

    /**
     * Benchmark GET operation.
     *
     * @return Retrieved value.
     * @throws Exception If failed.
     */
    @Benchmark
    public Object get() throws Exception {
        org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);
        int keyIdx = random.nextInt(CNT);
        return cache.get(keyIdx);
    }
}
