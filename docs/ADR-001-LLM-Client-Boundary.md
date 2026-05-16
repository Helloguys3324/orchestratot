# ADR 001: Extract LLM Client Boundary

## Status
Accepted

## Context
The `SessionManager` class in `backend/sessions/manager.py` currently handles both session orchestration (managing agents, files, and routing) and low-level LLM API calls (using the Google GenAI Live API and OpenAI compatible endpoints). This tightly couples the orchestration logic to specific LLM client implementations, making it harder to test, maintain, and extend to new providers.

## Decision
We will extract the LLM API invocation logic from `SessionManager` into a dedicated `backend/llm/provider.py` module. The `_call_llm` and `_call_live_api` methods will become standalone asynchronous functions.

## Consequences
- **Positive:** Improved separation of concerns. `SessionManager` focuses solely on orchestration.
- **Positive:** Easier testing of orchestration logic by mocking the decoupled `call_llm` function.
- **Positive:** Simpler integration of new LLM providers or client libraries in the future.
- **Negative:** Introduces a new internal API boundary, adding a slight indirection layer.

## Future Work
- Standardize the input/output schemas for the `call_llm` function to support diverse model modalities seamlessly.
