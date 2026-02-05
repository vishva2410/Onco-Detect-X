## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2024-05-24 - Missing Caching in CognitiveService
**Learning:** The `CognitiveService` was documented as having LRU caching, but the implementation was missing. This highlights the importance of verifying architectural claims in code.
**Action:** Always verify "known" performance features exist in the actual code before assuming they are working.
