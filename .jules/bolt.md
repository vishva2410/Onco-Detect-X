## 2024-05-24 - [LLM Caching Ineffective due to Upstream Randomness]
**Learning:** Downstream caching (LLM) was completely bypassed because an upstream service (Perception) produced non-deterministic outputs (random confidence scores) for the same input. Determinism in early pipeline stages is critical for caching in later stages.
**Action:** When adding caching to a pipeline, audit all upstream inputs for determinism. If inputs are random/noisy, either stabilize them (e.g., seeded RNG) or relax cache keys to exclude volatile fields if safe.
