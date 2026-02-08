## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2024-05-24 - Missing Caching in CognitiveService
**Learning:** The `CognitiveService` was documented as having LRU caching, but the implementation was missing. This highlights the importance of verifying architectural claims in code.
**Action:** Always verify "known" performance features exist in the actual code before assuming they are working.

## 2024-05-24 - Non-Deterministic Upstream Service Breaks Downstream Caching
**Learning:** The `PerceptionService` produced non-deterministic outputs (random confidence scores) for the same input. This caused the downstream `CognitiveService` to receive different inputs for the same case, rendering its LRU cache ineffective.
**Action:** Ensure that services feeding into a cached component produce deterministic outputs for identical inputs. Use hashing (e.g., `zlib.adler32`) to seed random generators if "mock" or probabilistic logic is needed.
