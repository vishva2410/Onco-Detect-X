## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2024-05-24 - Non-Deterministic Inputs Defeating Cache
**Learning:** The `PerceptionService` used unseeded random generation for `ml_confidence`, which caused the downstream `CognitiveService` inputs to change on every request for the same patient/image. This rendered any potential caching in the expensive LLM layer useless.
**Action:** Ensure upstream data generators (like mock ML models) are deterministic (e.g., seeded by input hash) so that downstream caching is effective.
