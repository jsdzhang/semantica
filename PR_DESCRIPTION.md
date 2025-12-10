# PR Title
`test(core/pipeline): Add comprehensive unit tests and fix pipeline validation logic`

# PR Description

## Summary
This PR focuses on stabilizing the Core and Pipeline modules by adding comprehensive unit tests and fixing a critical bug in the pipeline builder. It ensures that the `Semantica` orchestrator, plugin system, and execution engine are robust and working as expected.

## Key Changes

### 1. Core Module (`semantica/core`)
*   **Added Unit Tests:** Created `tests/core/test_core.py` with 14 test cases covering:
    *   `ConfigManager`: Loading and saving configurations.
    *   `LifecycleManager`: State transitions (initialization, starting, stopping).
    *   `PluginRegistry`: Plugin registration and retrieval.
    *   `MethodRegistry`: Method registration and execution.
    *   `Semantica` (Main Class): End-to-end flow from initialization to shutdown.
*   **Verification Script:** Added `scripts/verify_core_usage.py` to simulate real-world usage of the Core module.

### 2. Pipeline Module (`semantica/pipeline`)
*   **Bug Fix:** Resolved an `AttributeError` in `semantica/pipeline/pipeline_builder.py` (Lines 192-194).
    *   *Fix:* Changed attribute access from dictionary-style `.get()` to direct attribute access (`.valid`, `.errors`) for the `ValidationResult` dataclass.
*   **Added Unit Tests:** Created `tests/pipeline/test_pipeline.py` with 5 test cases covering:
    *   Pipeline construction via `PipelineBuilder`.
    *   Validation logic.
    *   Step chaining and dependency resolution (Topological Sort).
    *   Execution success and failure handling.

### 3. Additional Coverage
*   **KG Module:** Added/Verified tests in `tests/kg/test_kg.py`.
*   **Conflicts Module:** Added/Verified tests in `tests/conflicts/test_conflicts.py`.

## Verification
*   **Unit Tests:** All tests passed successfully using `python -m unittest discover tests`.
*   **Manual Verification:** Validated the Core module flow using `scripts/verify_core_usage.py`.

## Checklist
- [x] Code compiles and runs without errors.
- [x] Unit tests created and passed.
- [x] Critical bugs fixed (Pipeline validation).
- [x] Changes pushed to `core` branch.
