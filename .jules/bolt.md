## 2024-05-23 - Blocking LLM Calls in Async Routes
**Learning:** The application was performing synchronous I/O (Gemini API calls) inside `async def` FastAPI path operations. This blocks the main event loop, preventing the server from handling other requests concurrently.
**Action:** Always verify that external API calls (especially slow ones like LLM inference) use asynchronous clients (e.g., `generate_content_async`) when working within an async framework like FastAPI.

## 2026-01-31 - Manual Routing Anti-Pattern
**Learning:** The frontend implements a Single Page Application (SPA) pattern entirely within `frontend/src/app/page.tsx` using React state for navigation (`currentPage`). This prevents Next.js from performing automatic code splitting by route, leading to a large initial bundle size.
**Action:** For future significant performance gains, refactor the `currentPage` state into distinct Next.js App Router pages (e.g., `app/screening/page.tsx`) to enable proper code splitting.
