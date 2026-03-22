# Benchmark Generation Prompts

This directory contains the prompt templates used to interact with the Large Language Model (LLM) during the generation of the AI-written benchmarks. Prompt transparency is very critical for methodology validation and the experimental re-setup.

## Files

* **`AI_BENCHMARK_GENERATION_PROMPT.md`**: The core system prompt and instruction set used to guide the LLM in generating the functionally equivalent twin benchmarks.

## Prompt Mechanics

The prompt was engineered to enforce several strict constraints on the AI, ensuring that the generated code was scientifically valid for a comparative experiment:

1. **Functional Equivalence**: The AI is instructed to identify the exact behavior, scale, and concurrency patterns of the original handwritten benchmark and reproduce the same core testing logic.
2. **Code Independence**: The LLM is explicitly barred from copying the original code structure. It is forced to rewrite the implementation from scratch. This guarantees a structural and stylistic comparison between human-written and AI-generated code.
3. **JMH Best Practices**: The prompt mandates proper handling of specific Java Microbenchmark Harness (JMH) mechanics. This includes avoiding dead code elimination via returns, correct state scope utilization, and proper setup/teardown annotations.
4. **Project Integration**: The output is constrained to include standard Apache License headers, accurate project imports, and the specific `ai/` subdirectory file path to ensure seamless compilation within the Apache Ignite module.

## Usage Guide

To replicate the AI generation phase exactly:
1. Open the file you want to replicate (e.g., `JmhCacheBenchmark.java`) from the human-written benchmark sources.
2. Copy the text from `AI_BENCHMARK_GENERATION_PROMPT.md`.
3. Append the raw Java code of the original human-written benchmark at the bottom of the prompt block.
4. Submit the complete prompt block to the LLM to generate the AI twin benchmark class.
5. Save the output directly into the `ai/` package directory as instructed by the prompt.