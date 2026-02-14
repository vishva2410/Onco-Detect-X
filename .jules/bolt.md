
## 2024-05-22 - [Optimized Cognitive Service with Async & Caching]
**Learning:** The `CognitiveService.analyze` method was synchronous and blocking the event loop, causing significant performance degradation under load. Additionally, it lacked caching, leading to redundant API calls for identical inputs.
**Action:** Implemented `async def analyze` using `generate_content_async` and added an in-memory LRU cache (`OrderedDict`) with deterministic key generation (sorted lists). Always check for sync I/O in async paths and cache expensive operations.
