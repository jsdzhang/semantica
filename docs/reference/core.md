# Core Module

> **The heart of Semantica - orchestrating all framework components with configuration, lifecycle, and plugin management.**

---

## 🎯 Overview

<div class="grid cards" markdown>

-   :material-cog-outline:{ .lg .middle } **Framework Orchestration**

    ---

    Main `Semantica` class coordinating all operations and modules

-   :material-file-cog:{ .lg .middle } **Configuration Management**

    ---

    Centralized config with YAML/JSON support and validation

-   :material-timeline:{ .lg .middle } **Lifecycle Management**

    ---

    Startup, shutdown, health monitoring with hook system

-   :material-puzzle:{ .lg .middle } **Plugin System**

    ---

    Dynamic plugin discovery, loading, and isolation

-   :material-registry:{ .lg .middle } **Method Registry**

    ---

    Extensible method registration for custom implementations

-   :material-api:{ .lg .middle } **Convenience API**

    ---

    Simple `build()` function for quick knowledge base creation

</div>

!!! example "Quick Start"
    ```python
    from semantica import Semantica
    
    # One-liner to build knowledge base
    semantica = Semantica()
    result = semantica.build_knowledge_base(["documents/"])
    
    print(f"Nodes: {result['knowledge_graph'].node_count}")
    ```

---

## ⚙️ Algorithms Used

### Configuration Management
- **YAML/JSON Parsing**: Configuration file parsing with schema validation
- **Environment Variable Substitution**: `${VAR_NAME}` pattern replacement
- **Configuration Merging**: Deep merge algorithm for layered configs
- **Validation**: JSON Schema validation for type checking

### Lifecycle Management
- **Hook System**: Observer pattern for lifecycle events
- **Health Monitoring**: Periodic health checks with exponential backoff
- **Graceful Shutdown**: Resource cleanup with timeout handling

### Plugin System
- **Discovery**: File system scanning for plugin modules
- **Loading**: Dynamic import with dependency resolution
- **Isolation**: Separate namespace for each plugin

---

## Main Classes

### Semantica


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `__init__(config)` | Initialize framework | Configuration loading + validation |
| `build_knowledge_base(sources)` | Build knowledge graph | Orchestrate ingest → parse → extract → build |
| `run_pipeline(pipeline_config)` | Execute custom pipeline | DAG execution with error handling |
| `shutdown()` | Graceful shutdown | Resource cleanup with lifecycle hooks |
| `get_health_status()` | Get system health | Component health aggregation |

**Example:**

```python
from semantica import Semantica

# Initialize with default config
semantica = Semantica()

# Build knowledge base
result = semantica.build_knowledge_base(
    sources=["documents/"],
    extract_entities=True,
    extract_relations=True,
    embeddings=True,
    graph=True
)

kg = result["knowledge_graph"]
print(f"Nodes: {kg.node_count}, Edges: {kg.edge_count}")

# Shutdown
semantica.shutdown()
```

---

### Config


**Configuration Structure:**

```python
@dataclass
class Config:
    llm: Optional[Dict[str, Any]] = None
    embeddings: Optional[Dict[str, Any]] = None
    knowledge_graph: Optional[Dict[str, Any]] = None
    vector_store: Optional[Dict[str, Any]] = None
    # ... other configuration fields
```

**Example:**

```python
from semantica.core import Config

config = Config(
    llm={"provider": "openai", "model": "gpt-4"},
    embeddings={"provider": "openai", "model": "text-embedding-3-large"},
    knowledge_graph={"merge_entities": True, "resolve_conflicts": True}
)

semantica = Semantica(config=config)
```

---

### ConfigManager


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `load_config(path)` | Load configuration file | YAML/JSON parsing + validation |
| `validate_config(config)` | Validate configuration | JSON Schema validation |
| `get(key, default)` | Get config value | Nested key lookup with dot notation |
| `set(key, value)` | Set config value | Nested key assignment |
| `merge_configs(configs)` | Merge multiple configs | Deep merge algorithm |

**Example:**

```python
from semantica.core import ConfigManager

manager = ConfigManager()

# Load from file
config = manager.load_config("config.yaml")

# Validate
is_valid, errors = manager.validate_config(config)

# Get/set values
llm_model = manager.get("llm.model", default="gpt-4")
manager.set("llm.temperature", 0.7)
```

---

### LifecycleManager


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `startup()` | Execute startup sequence | Sequential hook execution |
| `shutdown()` | Execute shutdown sequence | Reverse-order hook execution |
| `register_hook(event, callback)` | Register lifecycle hook | Hook registration |
| `get_health_status()` | Get system health | Component health aggregation |

**Lifecycle Events:**
- `on_startup`: Framework initialization
- `on_shutdown`: Framework cleanup
- `on_error`: Error handling
- `on_health_check`: Health monitoring

**Example:**

```python
from semantica.core import LifecycleManager

manager = LifecycleManager()

# Register hooks
manager.register_hook("on_startup", lambda: print("Starting..."))
manager.register_hook("on_shutdown", lambda: print("Shutting down..."))

# Startup
manager.startup()

# Health check
health = manager.get_health_status()
print(f"Status: {health.status}, Components: {health.components}")

# Shutdown
manager.shutdown()
```

---

### PluginRegistry


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `discover_plugins(path)` | Discover available plugins | File system scanning |
| `load_plugin(name)` | Load plugin | Dynamic import + initialization |
| `unload_plugin(name)` | Unload plugin | Cleanup + namespace removal |
| `list_plugins()` | List loaded plugins | Plugin registry enumeration |
| `get_plugin(name)` | Get plugin instance | Registry lookup |

**Example:**

```python
from semantica.core import PluginRegistry

registry = PluginRegistry()

# Discover plugins
registry.discover_plugins("plugins/")

# Load plugin
registry.load_plugin("custom_extractor")

# Use plugin
plugin = registry.get_plugin("custom_extractor")
result = plugin.extract(text)

# Unload
registry.unload_plugin("custom_extractor")
```

---

## Convenience Functions

### build()


**Signature:**
```python
def build(
    sources: Union[str, List[Union[str, Path]]],
    extract_entities: bool = True,
    extract_relations: bool = True,
    embeddings: bool = True,
    graph: bool = True,
    **options
) -> Dict[str, Any]
```

**Example:**

```python
from semantica.core import build

# Simple one-liner
result = build(sources=["documents/"])

# With options
result = build(
    sources=["documents/"],
    extract_entities=True,
    extract_relations=True,
    embeddings=True,
    graph=True,
    llm_provider="openai",
    llm_model="gpt-4"
)
```

---

## Configuration Reference

```yaml
# config.yaml - Complete Configuration Example

# LLM Configuration
llm:
  provider: openai  # openai, anthropic, google, groq, ollama
  model: gpt-4
  temperature: 0.1
  max_tokens: 4000
  api_key: ${OPENAI_API_KEY}

# Embeddings Configuration
embeddings:
  provider: openai
  model: text-embedding-3-large
  dimensions: 3072
  batch_size: 100

# Knowledge Graph Configuration
knowledge_graph:
  merge_entities: true
  entity_resolution_strategy: fuzzy
  similarity_threshold: 0.85
  resolve_conflicts: true
  enable_temporal: true

# Vector Store Configuration
vector_store:
  backend: faiss
  index_type: HNSW
  metric: cosine
  dimension: 3072

# Pipeline Configuration
pipeline:
  parallel: true
  max_workers: 4
  error_handling: retry
  max_retries: 3

# Logging Configuration
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  handlers:
    - console
    - file
```

---

## Common Patterns

### Pattern 1: Basic Usage

```python
from semantica import Semantica

semantica = Semantica()
result = semantica.build_knowledge_base(["documents/"])
kg = result["knowledge_graph"]
```

### Pattern 2: Custom Configuration

```python
from semantica import Semantica, Config

config = Config(
    llm={"provider": "openai", "model": "gpt-4"},
    embeddings={"provider": "openai", "model": "text-embedding-3-large"}
)

semantica = Semantica(config=config)
result = semantica.build_knowledge_base(["documents/"])
```

### Pattern 3: Pipeline Execution

```python
from semantica import Semantica

semantica = Semantica()

pipeline_config = {
    "steps": [
        {"name": "ingest", "type": "FileIngestor"},
        {"name": "parse", "type": "DocumentParser"},
        {"name": "extract", "type": "NERExtractor"},
        {"name": "build_kg", "type": "GraphBuilder"}
    ]
}

result = semantica.run_pipeline(pipeline_config)
```

---

## Error Handling

```python
from semantica import Semantica
from semantica.core import ConfigurationError, PipelineError

try:
    semantica = Semantica(config="invalid_config.yaml")
except ConfigurationError as e:
    print(f"Configuration error: {e}")

try:
    result = semantica.build_knowledge_base([])
except PipelineError as e:
    print(f"Pipeline error: {e}")
```

---

## See Also

- [Pipeline Module](pipeline.md) - Pipeline building and execution
- [Knowledge Graph Module](kg.md) - Graph construction
- [Semantic Extract Module](semantic_extract.md) - Entity extraction
