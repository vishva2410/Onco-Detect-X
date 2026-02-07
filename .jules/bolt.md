## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2024-05-24 - Missing Caching in CognitiveService
**Learning:** The `CognitiveService` was documented as having LRU caching, but the implementation was missing. This highlights the importance of verifying architectural claims in code.
**Action:** Always verify "known" performance features exist in the actual code before assuming they are working.

## 2024-05-25 - Cache Misses due to Non-Deterministic Upstream Services
**Learning:** `CognitiveService` caching was ineffective because the upstream `PerceptionService` produced random outputs for the same input image. This caused the cache key (derived from `PerceptionService` output) to change on every request, forcing expensive LLM re-computation.
**Action:** Ensure deterministic outputs (e.g., by seeding random generators with input checksums) in services that feed into cached components.
