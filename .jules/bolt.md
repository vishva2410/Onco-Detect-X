## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2024-05-24 - Deterministic Mocks for Caching
**Learning:** The `PerceptionService` was using non-deterministic random values for mocks. This caused the downstream `CognitiveService` (LLM) to receive different inputs for the same file, rendering caching ineffective.
**Action:** Ensure that mock services or preliminary processing steps are deterministic (e.g., seeding random with input hash) if they feed into expensive operations that benefit from caching.
