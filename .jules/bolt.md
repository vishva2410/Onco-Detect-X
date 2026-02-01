## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2024-10-25 - Blocking Font Imports in Next.js
**Learning:** Using `@import` for Google Fonts in CSS blocks the main thread and delays First Contentful Paint (FCP).
**Action:** Always use `next/font/google` for self-hosted, non-blocking font loading in Next.js applications.
