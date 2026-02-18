# PR Update: Context Reliability Fixes

This update includes two targeted fixes to improve context-graph correctness and remove placeholder behavior.

## 1) Policy applicability fix
**File:** `semantica/context/policy_engine.py`  
**Commit:** `0a63128`

- Fixed `get_applicable_policies(...)` to handle both backend response shapes:
  - wrapped: `{"records": [{"p": {...}}]}`
  - flat: `{"policy_id": ..., ...}`
- Replaced incomplete entity branch (`if entities: pass`) with actual entity-based filtering.
- Added internal helpers:
  - `_extract_records(...)`
  - `_policy_matches_entities(...)`

Result:
- Policy retrieval is now deterministic across backends.
- Entity-scoped applicability works as expected.

## 2) Cross-system capture implementation
**File:** `semantica/context/agent_context.py`  
**Commit:** `89d6030`

- Replaced placeholder logic in `capture_cross_system_inputs(...)` with real backend-aware capture.
- If `knowledge_graph.execute_query` is available, it fetches recent `CrossSystemContext` records per system.
- Added clear status-driven output:
  - `captured`
  - `captured_without_backend`
  - `capture_failed`
- Returned payload now includes `records_found` and `records` for traceability.

Result:
- Cross-system context capture now reflects real system state, not synthetic placeholders.

## Backward compatibility
- No public API signature changes.
- Existing callers continue to work.
- Changes are additive and safer.

## Validation
- `tests/context/test_policy_engine.py -k "get_applicable_policies"` passed.
- `tests/context/test_context_retriever_hybrid.py -k "find_relevant_policies"` passed.
- `tests/context/test_agent_context_decisions.py -k "find_precedents_success or record_decision_success"` passed.
