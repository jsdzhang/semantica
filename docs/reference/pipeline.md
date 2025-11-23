# Pipeline Module

Build and execute complex processing pipelines with support for parallel execution, error handling, and resource management.

## Overview

- **Pipeline Building**: Fluent API for pipeline construction
- **Parallel Execution**: Multi-threaded/multi-process execution
- **Error Handling**: Retry logic and failure recovery
- **Resource Management**: Memory and CPU optimization
- **Monitoring**: Progress tracking and logging

---

## Algorithms Used

### Execution Algorithms
- **DAG (Directed Acyclic Graph) Execution**: Topological sort for step ordering
- **Parallel Execution**: Thread pool with work stealing
- **Dependency Resolution**: Kahn's algorithm for topological ordering
- **Resource Scheduling**: Greedy scheduling with priority queue

### Error Handling
- **Exponential Backoff**: Retry with increasing delays: `delay = base * 2^attempt`
- **Circuit Breaker**: Fail fast after threshold failures
- **Checkpoint/Resume**: State persistence for long-running pipelines

---

## Main Classes

### PipelineBuilder


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `add_step(name, processor)` | Add pipeline step | Step registration |
| `add_parallel_steps(steps)` | Add parallel steps | Parallel branch creation |
| `build()` | Build pipeline | DAG construction + validation |
| `execute(input_data)` | Execute pipeline | Topological execution |
| `set_error_handler(handler)` | Set error handler | Handler registration |

**Example:**

```python
from semantica.pipeline import PipelineBuilder
from semantica.ingest import FileIngestor
from semantica.parse import DocumentParser
from semantica.semantic_extract import NERExtractor

pipeline = PipelineBuilder() \\
    .add_step("ingest", FileIngestor(recursive=True)) \\
    .add_step("parse", DocumentParser()) \\
    .add_step("extract", NERExtractor()) \\
    .add_step("build_kg", GraphBuilder()) \\
    .build()

result = pipeline.execute(sources=["documents/"])
print(f"Processed {result.stats['documents_processed']} documents")
```

---

### ExecutionEngine


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `execute(pipeline, data)` | Execute pipeline | DAG traversal |
| `execute_parallel(steps, data)` | Parallel execution | Thread/process pool |
| `execute_sequential(steps, data)` | Sequential execution | Linear execution |
| `schedule_steps(dag)` | Schedule execution | Topological sort |

---

### FailureHandler


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `handle_failure(error, context)` | Handle step failure | Strategy-based handling |
| `retry(step, max_retries)` | Retry failed step | Exponential backoff |
| `skip(step)` | Skip failed step | Continue execution |
| `abort(pipeline)` | Abort pipeline | Graceful shutdown |

**Retry Strategy:**
```
delay = base_delay * (2 ** attempt) + random_jitter
max_delay = min(delay, max_delay)
```

---

## Configuration

```yaml
# config.yaml - Pipeline Configuration

pipeline:
  execution:
    parallel: true
    max_workers: 4
    timeout: 3600  # seconds
    
  error_handling:
    strategy: retry  # retry, skip, abort
    max_retries: 3
    retry_delay: 1  # seconds
    exponential_backoff: true
    
  monitoring:
    log_level: INFO
    progress_bar: true
    checkpoint_interval: 100  # steps
```

---

## See Also

- [Core Module](core.md)
