## 2024-05-22 - Deterministic Cache Keys
**Learning:** Pydantic's `model_dump_json()` does not guarantee field order for JSON keys, and list order matters for string equality. This caused cache misses for semantically identical inputs where list fields (like symptoms) were reordered.
**Action:** When caching object inputs, always convert to dict, sort list fields explicitly, and use `json.dumps(sort_keys=True)` to generate canonical cache keys.
