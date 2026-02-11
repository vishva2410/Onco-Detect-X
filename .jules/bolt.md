## 2024-05-22 - Upstream Randomness Kills Downstream Caching
**Learning:** In a pipeline of services, if an upstream service (like `PerceptionService`) produces non-deterministic output (e.g., random confidence scores) for the same input, it renders caching in downstream services (like `CognitiveService`) completely ineffective because the cache keys never match.
**Action:** Always ensure upstream dependencies are deterministic (or use input-based seeding) before attempting to optimize downstream components.
