# AI Microbenchmark Generation Prompt

## ROLE
You are an expert Java developer specializing in performance microbenchmarking using the JMH (Java Microbenchmark Harness) framework.

## TASK
Generate an AI-written equivalent of the provided handwritten JMH microbenchmark. The AI-generated benchmark must test the **exact same functionality** as the original, but should be written from scratch based on understanding the purpose and behavior of the original code.

## REQUIREMENTS

### 1. Functional Equivalence
- **Analyze the original benchmark** to understand what it measures (e.g., cache get/put operations, thread synchronization, etc.)
- **Preserve the core testing logic**: Same operations being measured, same data structures, same concurrency patterns
- **Maintain JMH annotations**: Use appropriate `@Benchmark`, `@State`, `@Setup`, `@BenchmarkMode`, etc.
- **Keep the same scope and scale**: If original uses ThreadLocalRandom for key selection, use similar approach

### 2. Code Independence
- **Do NOT copy-paste** the original code
- **Write fresh implementations** that achieve the same testing goals
- **Use different variable names, method structures, and code organization** where possible while maintaining clarity
- **Keep the same package structure** to ensure integration with the existing project

### 3. JMH Best Practices
- Use proper JMH annotations (`@Benchmark`, `@State`, `@Setup`, `@TearDown`, etc.)
- Include appropriate scope for state objects (e.g., `Scope.Thread`, `Scope.Benchmark`)
- Avoid dead code elimination (return results from benchmark methods when appropriate)
- Use proper warmup and measurement iterations if specified

### 4. Code Quality
- **Clean, readable code** with appropriate comments
- **Professional naming conventions**
- **Proper exception handling**
- **Keep Apache License header** (copy exactly from original)

### 5. Integration Requirements
- Must compile with the existing project structure
- Use the same imports and dependencies as available in the original
- Maintain compatibility with the benchmark runner infrastructure

## OUTPUT FORMAT

Provide:
1. **The complete Java source code** for the AI-generated benchmark class
2. **File path** where it should be saved (format: `src/main/java/org/apache/ignite/internal/benchmarks/jmh/ai/[OriginalName]AI.java`)
3. **No explanations, just code**

## ORIGINAL BENCHMARK CODE

```java
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

package org.apache.ignite.internal.benchmarks.jmh.cache;

import org.apache.ignite.Ignite;
import org.apache.ignite.IgniteCache;
import org.apache.ignite.Ignition;
import org.apache.ignite.cache.CacheAtomicityMode;
import org.apache.ignite.cache.CacheMode;
import org.apache.ignite.cache.CacheRebalanceMode;
import org.apache.ignite.cache.CacheWriteSynchronizationMode;
import org.apache.ignite.configuration.CacheConfiguration;
import org.apache.ignite.configuration.IgniteConfiguration;
import org.apache.ignite.internal.benchmarks.jmh.JmhAbstractBenchmark;
import org.apache.ignite.internal.util.typedef.internal.A;
import org.apache.ignite.spi.discovery.tcp.TcpDiscoverySpi;
import org.apache.ignite.spi.discovery.tcp.ipfinder.vm.TcpDiscoveryVmIpFinder;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.Setup;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.TearDown;

/**
 * Base class for cache benchmarks.
 */
@State(Scope.Benchmark)
public class JmhCacheAbstractBenchmark extends JmhAbstractBenchmark {
    /** Property: backups. */
    protected static final String PROP_BACKUPS = "ignite.jmh.cache.backups";

    /** Property: atomicity mode. */
    protected static final String PROP_ATOMICITY_MODE = "ignite.jmh.cache.atomicityMode";

    /** Property: atomicity mode. */
    protected static final String PROP_WRITE_SYNC_MODE = "ignite.jmh.cache.writeSynchronizationMode";

    /** Property: nodes count. */
    protected static final String PROP_DATA_NODES = "ignite.jmh.cache.dataNodes";

    /** Property: client mode flag. */
    protected static final String PROP_CLIENT_MODE = "ignite.jmh.cache.clientMode";

    /** Default amount of nodes. */
    protected static final int DFLT_DATA_NODES = 1;

    /** Items count. */
    protected static final int CNT = 100000;

    /** IP finder shared across nodes. */
    private static final TcpDiscoveryVmIpFinder IP_FINDER = new TcpDiscoveryVmIpFinder(true);

    /** Target node. */
    protected Ignite node;

    /** Target cache. */
    protected IgniteCache cache;

    /**
     * Setup routine. Child classes must invoke this method first.
     *
     * @throws Exception If failed.
     */
    @Setup
    public void setup() throws Exception {
        System.out.println();
        System.out.println("--------------------");

        System.out.println("IGNITE BENCHMARK INFO: ");

        System.out.println("\tclient mode:                " + booleanProperty(PROP_CLIENT_MODE));

        System.out.println("\tdata nodes:                 " + intProperty(PROP_DATA_NODES, DFLT_DATA_NODES));

        System.out.println("\tbackups:                    " + intProperty(PROP_BACKUPS));

        System.out.println("\tatomicity mode:             " +
            enumProperty(PROP_ATOMICITY_MODE, CacheAtomicityMode.class));

        System.out.println("\twrite synchronization mode: " +
            enumProperty(PROP_WRITE_SYNC_MODE, CacheWriteSynchronizationMode.class));

        System.out.println("--------------------");
        System.out.println();

        int nodesCnt = intProperty(PROP_DATA_NODES, DFLT_DATA_NODES);

        A.ensure(nodesCnt >= 1, "nodesCnt >= 1");

        node = Ignition.start(configuration("node0"));

        for (int i = 1; i < nodesCnt; i++)
            Ignition.start(configuration("node" + i));

        boolean isClient = booleanProperty(PROP_CLIENT_MODE);

        if (isClient) {
            IgniteConfiguration clientCfg = configuration("client");

            clientCfg.setClientMode(true);

            node = Ignition.start(clientCfg);
        }

        cache = node.cache(null);
    }

    /**
     * Tear down routine.
     *
     * @throws Exception If failed.
     */
    @TearDown
    public void tearDown() throws Exception {
        Ignition.stopAll(true);
    }

    /**
     * Create Ignite configuration.
     *
     * @param gridName Grid name.
     * @return Configuration.
     */
    protected IgniteConfiguration configuration(String gridName) {
        IgniteConfiguration cfg = new IgniteConfiguration();

        cfg.setGridName(gridName);

        cfg.setLocalHost("127.0.0.1");

        TcpDiscoverySpi discoSpi = new TcpDiscoverySpi();
        discoSpi.setIpFinder(IP_FINDER);
        cfg.setDiscoverySpi(discoSpi);

        cfg.setCacheConfiguration(cacheConfiguration());

        return cfg;
    }

    /**
     * Create cache configuration.
     *
     * @return Cache configuration.
     */
    protected CacheConfiguration cacheConfiguration() {
        CacheConfiguration cacheCfg = new CacheConfiguration();

        cacheCfg.setName(null);
        cacheCfg.setCacheMode(CacheMode.PARTITIONED);
        cacheCfg.setRebalanceMode(CacheRebalanceMode.SYNC);

        // Set atomicity mode.
        CacheAtomicityMode atomicityMode = enumProperty(PROP_ATOMICITY_MODE, CacheAtomicityMode.class);

        if (atomicityMode != null)
            cacheCfg.setAtomicityMode(atomicityMode);

        // Set write synchronization mode.
        CacheWriteSynchronizationMode writeSyncMode =
            enumProperty(PROP_WRITE_SYNC_MODE, CacheWriteSynchronizationMode.class);

        if (writeSyncMode != null)
            cacheCfg.setWriteSynchronizationMode(writeSyncMode);

        // Set backups.
        cacheCfg.setBackups(intProperty(PROP_BACKUPS));

        return cacheCfg;
    }
}
```

## GENERATION INSTRUCTIONS

1. Read and understand the original benchmark's purpose
2. Identify the core operation being measured
3. Generate a fresh implementation that tests the same operation
4. Ensure all JMH annotations are correctly applied
5. Verify the code would compile in the existing project context
6. Name the class by appending "AI" to the original class name (e.g., `JmhCacheBenchmark` → `JmhCacheBenchmarkAI`)
7. Place in package: `org.apache.ignite.internal.benchmarks.jmh.ai`

---

**Note**: We will use this prompt consistently for all benchmark generations to ensure comparable AI-generated benchmarks across different commits and test scenarios, therefore the thesis tests results will be academically valid.
