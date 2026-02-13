## 2026-02-13 - Determinism in Upstream Services
**Learning:** Upstream "mock" services using unseeded randomness (e.g. `random.uniform`) generate unique outputs for identical inputs, which invalidates downstream caching strategies because the input parameters are constantly changing.
**Action:** Always seed randomness in mock services using a hash of the input (e.g., `random.Random(zlib.adler32(input_data))`) to ensure deterministic behavior, enabling effective caching and reproducible performance testing.
