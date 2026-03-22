# Data Collection and Provenance

This section documents where the experimental data comes from.

## Apache Ignite targets

Experiments were run on these commits:

- `b038730` (v1.8.0)
- `feba953` (v2.0.0)
- `160dab0` (v2.2.0)

## Benchmark families included

- Cache operations
- Future/async operations
- Increment operations

## Benchmark variants

For each selected benchmark:

- Handwritten benchmark implementation
- AI-generated benchmark implementation

## Regression model

Known regression was injected into benchmark methods with:

`org.openjdk.jmh.infra.Blackhole.consumeCPU(1000000L);`

This enables controlled comparison between baseline and regression-injected runs.

## Note on AI generation metadata

If available, add prompt/model metadata in:

- `generation_metadata.md`

Include:

- Model name/version
- Prompt template
- Constraints/instructions used
- Manual post-processing steps (if any)

