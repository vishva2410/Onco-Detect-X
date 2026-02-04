## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2024-05-24 - Missing Caching in CognitiveService
**Learning:** The memory stated that `CognitiveService` implemented LRU caching, but the code did not. This discrepancy led to redundant external API calls.
**Action:** Always verify that "implemented" features actually exist in the code, especially for performance-critical components like LLM calls. Implemented in-memory LRU caching using `OrderedDict`.
