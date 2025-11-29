# Modules & Architecture

Semantica is built with a modular architecture, designed to be flexible, extensible, and scalable. This guide provides a comprehensive overview of the key modules, their responsibilities, and how they interact to build powerful semantic applications.

!!! info "About This Guide"
    This guide covers all 13 core modules in Semantica, organized by their functional layer. It details their purpose, key features, usage patterns, and configuration options.

---

## Module Overview

Semantica's modules are organized into five logical layers. You can use these modules independently or combine them into a complete pipeline.

| Layer | Modules | Description |
| :--- | :--- | :--- |
| **Input Layer** | [Ingest](#1-ingest-module), [Parse](#2-parse-module), [Normalize](#3-normalize-module) | Handles data ingestion, parsing, and cleaning from various sources. |
| **Core Processing** | [Semantic Extract](#4-semantic-extract-module), [Knowledge Graph](#5-knowledge-graph-kg-module), [Ontology](#10-ontology-module), [Reasoning](#9-reasoning-module) | The "brain" of the system. Extracts meaning, builds graphs, and infers new knowledge. |
| **Storage & Embeddings** | [Embeddings](#6-embeddings-module), [Vector Store](#7-vector-store-module), [Graph Store](#8-graph-store-module) | Manages persistent storage and retrieval of vectors and graphs. |
| **Output Layer** | [Export](#11-export-module), [Visualization](#12-visualization-module) | Tools for visualizing data and exporting it to external systems. |
| **Orchestration** | [Pipeline](#13-pipeline-module) | Manages workflows, execution, and resource scheduling. |

---

## Input Layer

These modules are responsible for getting data into the system and preparing it for processing.

### 1. Ingest Module

!!! abstract "Purpose"
    The `ingest` module is the entry point for data ingestion. It handles the complexity of connecting to different data sources, from local files to web streams, and supports connecting to your own MCP (Model Context Protocol) servers.

**Key Features**:

- Support for 50+ file formats (PDF, DOCX, HTML, JSON, CSV, etc.)
- Web scraping with JavaScript rendering
- Database integration (SQL, NoSQL)
- Real-time streaming support
- MCP server integration
- Batch processing capabilities
- Metadata extraction

**Input/Output Specification**:

| Input      | Type              | Description                          |
| :--------- | :---------------- | :----------------------------------- |
| `source`   | `str`, `Path`, `List` | File path, URL, directory, or list of sources |
| `recursive`| `bool`            | Whether to recursively scan directories |
| `filters`  | `Dict`            | Filters for file types, sizes, etc.  |

| Output     | Type              | Description                          |
| :--------- | :---------------- | :----------------------------------- |
| `documents`| `List[Document]`  | List of Document objects with content and metadata |
| `metadata` | `Dict`            | Source metadata (paths, timestamps, formats) |

**Components**:

- `FileIngestor`: Read files (PDF, DOCX, HTML, JSON, CSV, etc.)
- `WebIngestor`: Scrape and ingest web pages
- `FeedIngestor`: Process RSS/Atom feeds
- `StreamIngestor`: Real-time data streaming
- `DBIngestor`: Database queries and ingestion
- `EmailIngestor`: Process email messages
- `RepoIngestor`: Git repository analysis
- `MCPIngestor`: Connect to your own Python/FastMCP MCP servers via URL for resource and tool-based data ingestion

**Complete Code Example**:

```python
from semantica.ingest import FileIngestor, WebIngestor, DBIngestor, MCPIngestor

# Example 1: Ingest local files
file_ingestor = FileIngestor()
documents = file_ingestor.ingest("data/", recursive=True)  # (1)
print(f"Ingested {len(documents)} documents")

# Example 2: Ingest web content
web_ingestor = WebIngestor()
web_docs = web_ingestor.ingest("https://example.com")  # (2)
print(f"Web content: {web_docs[0].content[:100]}...")

# Example 3: Ingest from database
db_ingestor = DBIngestor(connection_string="postgresql://user:pass@localhost/db")
db_docs = db_ingestor.ingest("SELECT * FROM documents")

# Example 4: Ingest from MCP server
mcp_ingestor = MCPIngestor()
mcp_docs = mcp_ingestor.ingest("https://your-mcp-server.com")
```

1. Recursively scans the directory for supported file types (PDF, DOCX, etc.) and converts them to standard Document objects.
2. Fetches the URL, renders JavaScript if necessary, and extracts the main content while stripping boilerplate.

**Configuration Options**:

| Option         | Type        | Default | Description                          |
| :--------------| :---------- | :------ | :----------------------------------- |
| `recursive`    | `bool`      | `False` | Recursively scan directories         |
| `file_filters` | `List[str]` | `None`  | Filter by file extensions            |
| `max_file_size`| `int`       | `None`  | Maximum file size in bytes           |
| `timeout`      | `int`       | `30`    | Request timeout in seconds           |
| `user_agent`   | `str`       | `None`  | Custom user agent for web requests   |

**API Reference**: [Ingest Module](reference/ingest.md)

### 2. Parse Module

!!! abstract "Purpose"
    Once data is ingested, the `parse` module extracts the raw text and metadata. It supports a wide range of formats and includes OCR capabilities.

**Key Features**:
- 50+ file format support
- OCR for images and scanned documents
- Table extraction from PDFs and spreadsheets
- Metadata preservation
- Automatic format detection
- Structured data parsing (JSON, CSV, XML)

**Input/Output Specification**:

| Input          | Type                  | Description                          |
| :------------- | :-------------------- | :----------------------------------- |
| `documents`    | `List[Document]`      | Documents from ingest module         |
| `ocr_enabled`  | `bool`                | Enable OCR for images                |

| Output         | Type                  | Description                          |
| :------------- | :-------------------- | :----------------------------------- |
| `parsed_docs`  | `List[ParsedDocument]`| Documents with extracted text and metadata |
| `tables`       | `List[Table]`         | Extracted tables (if any)            |

**Components**:
- `DocumentParser`: Main parser orchestrator
- `PDFParser`: Extract text, tables, images from PDFs
- `DOCXParser`: Parse Word documents
- `HTMLParser`: Extract content from HTML
- `JSONParser`: Parse structured JSON data
- `ExcelParser`: Process spreadsheets
- `ImageParser`: OCR and image analysis
- `CodeParser`: Parse source code files

**Complete Code Example**:

```python
from semantica.parse import DocumentParser

parser = DocumentParser(ocr_enabled=True)
parsed_docs = parser.parse(documents)  # (1)

# Access parsed content
for doc in parsed_docs:
    print(f"Content: {doc.content[:100]}...")
    print(f"Metadata: {doc.metadata}")
    if doc.tables:
        print(f"Found {len(doc.tables)} tables")
```

1. Automatically detects the file type of each document and routes it to the appropriate specialized parser (e.g., PDFParser for .pdf).

**Configuration Options**:

| Option          | Type   | Default | Description                      |
| :-------------- | :----- | :------ | :------------------------------- |
| `ocr_enabled`   | `bool` | `False` | Enable OCR for images            |
| `extract_tables`| `bool` | `True`  | Extract tables from documents    |
| `extract_images`| `bool` | `False` | Extract and process images       |

**API Reference**: [Parse Module](reference/parse.md)

### 3. Normalize Module

!!! abstract "Purpose"
    Raw text is often noisy. The `normalize` module cleans, standardizes, and prepares text for semantic extraction.

**Key Features**:
- Text cleaning and noise removal
- Encoding normalization
- Entity name standardization
- Date and number formatting
- Language detection
- Unicode normalization

**Input/Output Specification**:

| Input              | Type                    | Description                          |
| :----------------- | :---------------------- | :----------------------------------- |
| `documents`        | `List[ParsedDocument]`  | Parsed documents                     |
| `normalize_entities`| `bool`                 | Normalize entity names               |

| Output         | Type                    | Description                          |
| :------------- | :---------------------- | :----------------------------------- |
| `normalized_docs`| `List[NormalizedDocument]`| Cleaned and normalized documents   |

**Components**:
- `TextNormalizer`: Main normalization orchestrator
- `TextCleaner`: Remove noise, fix encoding
- `DataCleaner`: Clean structured data
- `EntityNormalizer`: Normalize entity names
- `DateNormalizer`: Standardize date formats
- `NumberNormalizer`: Normalize numeric values
- `LanguageDetector`: Detect document language
- `EncodingHandler`: Handle character encoding

**Complete Code Example**:

```python
from semantica.normalize import TextNormalizer

normalizer = TextNormalizer(
    normalize_entities=True,
    normalize_dates=True,
    detect_language=True
)
normalized = normalizer.normalize(parsed_docs)

# Check normalization results
for doc in normalized:
    print(f"Language: {doc.language}")
    print(f"Normalized text: {doc.content[:100]}...")
```

**Configuration Options**:

| Option             | Type   | Default | Description                  |
| :----------------- | :----- | :------ | :--------------------------- |
| `normalize_entities` | `bool` | `True`  | Normalize entity names       |
| `normalize_dates`    | `bool` | `True`  | Standardize date formats      |
| `normalize_numbers`  | `bool` | `True`  | Normalize numeric values      |
| `detect_language`    | `bool` | `False` | Detect document language      |

**API Reference**: [Normalize Module](reference/normalize.md)

---

## Core Processing Layer

These modules form the intelligence of Semantica, extracting meaning, building relationships, and inferring new knowledge.

### 4. Semantic Extract Module

!!! abstract "Purpose"
    This is the brain of the operation. It uses LLMs and NLP techniques to understand the text and extract structured knowledge.

**Key Features**:
- Multiple NER methods (rule-based, ML, LLM)
- Relationship extraction
- Semantic analysis
- Custom entity types
- Confidence scoring
- Multi-language support

**Input/Output Specification**:

| Input          | Type                      | Description                          |
| :------------- | :------------------------ | :----------------------------------- |
| `documents`    | `List[NormalizedDocument]`| Normalized documents                 |
| `entity_types` | `List[str]`              | Custom entity types to extract       |
| `method`       | `str`                    | Extraction method (rule/ml/llm)       |

| Output         | Type                | Description                          |
| :------------- | :------------------ | :----------------------------------- |
| `entities`     | `List[Entity]`      | Extracted entities with types and confidence |
| `relationships`| `List[Relationship]`| Extracted relationships              |

**Components**:
- `NERExtractor`: Named Entity Recognition
- `RelationExtractor`: Extract relationships between entities
- `SemanticAnalyzer`: Deep semantic analysis
- `SemanticNetworkExtractor`: Extract semantic networks

**Complete Code Example**:

```python
from semantica.semantic_extract import NERExtractor, RelationExtractor

# Extract entities
extractor = NERExtractor(method="llm", model="gpt-4")
entities = extractor.extract(normalized_docs)

print(f"Extracted {len(entities)} entities")
for entity in entities[:5]:
    print(f"  - {entity.text} ({entity.label}) - Confidence: {entity.confidence:.2f}")

# Extract relationships
relation_extractor = RelationExtractor()
relationships = relation_extractor.extract(normalized_docs, entities=entities)

print(f"\nExtracted {len(relationships)} relationships")
for rel in relationships[:5]:
    print(f"  {rel.subject.text} --[{rel.predicate}]--> {rel.object.text}")
```

**Configuration Options**:

| Option                | Type        | Default | Description                      |
| :-------------------- | :---------- | :------ | :------------------------------- |
| `method`              | `str`       | `"ml"`  | Extraction method (rule/ml/llm)  |
| `model`               | `str`       | `None`  | Model name for ML/LLM methods   |
| `confidence_threshold`| `float`     | `0.5`   | Minimum confidence score         |
| `custom_entity_types`| `List[str]` | `[]`    | Custom entity types              |

**API Reference**: [Semantic Extract Module](reference/semantic_extract.md)

### 5. Knowledge Graph (KG) Module

!!! abstract "Purpose"
    The `kg` module constructs the graph from extracted entities and relationships, handling complex tasks like resolution and analysis.

**Key Features**:
- Graph construction from entities/relationships
- Multiple backend support (NetworkX, Neo4j, KuzuDB)
- Temporal graph support
- Graph analytics and metrics
- Conflict detection and resolution
- Entity deduplication
- Community detection
- Centrality calculations

**Input/Output Specification**:

| Input          | Type                | Description                          |
| :------------- | :------------------ | :----------------------------------- |
| `entities`    | `List[Entity]`      | Extracted entities                   |
| `relationships`| `List[Relationship]`| Extracted relationships              |
| `backend`     | `str`              | Graph backend (networkx/neo4j/kuzu)  |

| Output         | Type              | Description                          |
| :------------- | :---------------- | :----------------------------------- |
| `knowledge_graph`| `KnowledgeGraph`| Constructed knowledge graph          |
| `metrics`     | `Dict`            | Graph metrics (density, centrality, etc.) |

**Components**:
- `GraphBuilder`: Construct knowledge graphs from entities/relationships
- `GraphAnalyzer`: Analyze graph structure and properties
- `GraphValidator`: Validate graph quality and consistency
- `EntityResolver`: Resolve entity conflicts and duplicates
- `ConflictDetector`: Detect conflicting information
- `CentralityCalculator`: Calculate node importance metrics
- `CommunityDetector`: Detect communities in graphs
- `ConnectivityAnalyzer`: Analyze graph connectivity
- `TemporalQuery`: Query temporal knowledge graphs
- `Deduplicator`: Remove duplicate entities/relationships

**Complete Code Example**:

```python
from semantica.kg import GraphBuilder, GraphAnalyzer

# Build graph
builder = GraphBuilder(backend="networkx", temporal=True)
kg = builder.build(entities, relationships)  # (1)

# Analyze graph
analyzer = GraphAnalyzer()
metrics = analyzer.analyze(kg)  # (2)

print(f"Nodes: {metrics['nodes']}")
print(f"Edges: {metrics['edges']}")
print(f"Density: {metrics['density']:.3f}")
print(f"Communities: {metrics['communities']}")
```

1. Constructs a NetworkX or Neo4j graph from the extracted entities and relationships, handling node merging and edge attributes.
2. Computes graph-theoretic metrics like density, diameter, and centrality to assess the quality and structure of the knowledge graph.

**Configuration Options**:

| Option            | Type   | Default       | Description                          |
| :---------------- | :----- | :------------ | :----------------------------------- |
| `backend`         | `str`  | `"networkx"`  | Graph backend (networkx/neo4j/kuzu)  |
| `temporal`        | `bool` | `False`       | Enable temporal graph support        |
| `merge_duplicates`| `bool` | `True`        | Automatically merge duplicate entities|

**API Reference**: [Knowledge Graph Module](reference/kg.md)

### 9. Reasoning Module

!!! abstract "Purpose"
    Goes beyond simple retrieval to infer new facts and validate existing knowledge using logical rules.

**Key Features**:
- Forward and backward chaining
- Rule-based inference
- Deductive and abductive reasoning
- Explanation generation
- RETE algorithm support
- Custom rule definition

**Input/Output Specification**:

| Input           | Type                | Description                          |
| :-------------- | :------------------ | :----------------------------------- |
| `knowledge_graph`| `KnowledgeGraph`   | Input knowledge graph                |
| `rules`         | `List[Rule]`       | Inference rules                      |
| `method`        | `str`              | Reasoning method                     |

| Output        | Type                | Description                          |
| :------------ | :------------------ | :----------------------------------- |
| `new_facts`   | `List[Fact]`        | Inferred facts                       |
| `explanations`| `List[Explanation]`  | Reasoning explanations               |

**Components**:
- `InferenceEngine`: Main inference orchestrator
- `RuleManager`: Manage inference rules
- `DeductiveReasoner`: Deductive reasoning
- `AbductiveReasoner`: Abductive reasoning
- `ExplanationGenerator`: Generate explanations for inferences
- `RETEEngine`: RETE algorithm for rule matching

**Complete Code Example**:

```python
from semantica.reasoning import InferenceEngine, RuleManager

inference_engine = InferenceEngine()
rule_manager = RuleManager()

# Define rules
rules = [
    "IF Person worksFor Company AND Company locatedIn City THEN Person livesIn City",
    "IF Person hasFriend Person2 AND Person2 hasFriend Person3 THEN Person knows Person3"
]

rule_manager.add_rules(rules)

# Perform inference
new_facts = inference_engine.forward_chain(kg, rule_manager)
print(f"Inferred {len(new_facts)} new facts")

# Get explanations
for fact in new_facts:
    explanation = inference_engine.explain(fact)
    print(f"{fact}: {explanation}")
```

**Configuration Options**:

| Option          | Type   | Default           | Description                  |
| :-------------- | :----- | :---------------- | :--------------------------- |
| `method`        | `str`  | `"forward_chain"` | Reasoning method             |
| `max_iterations`| `int`  | `100`             | Maximum inference iterations |

**API Reference**: [Reasoning Module](reference/reasoning.md)

### 10. Ontology Module

!!! abstract "Purpose"
    Defines the schema and structure of your knowledge domain, ensuring consistency and enabling interoperability.

**Key Features**:
- Automatic ontology generation (6-stage pipeline)
- OWL/RDF export
- Class and property inference
- Ontology validation
- Symbolic reasoning (HermiT, Pellet)
- Version management

**Input/Output Specification**:

| Input           | Type              | Description                          |
| :-------------- | :---------------- | :----------------------------------- |
| `knowledge_graph`| `KnowledgeGraph` | Input knowledge graph                |
| `base_uri`      | `str`             | Base URI for ontology                |

| Output      | Type        | Description                          |
| :---------- | :---------- | :----------------------------------- |
| `ontology`  | `Ontology`  | Generated ontology                   |
| `owl_content`| `str`      | OWL/Turtle format                    |

**Components**:
- `OntologyGenerator`: Generate ontologies from knowledge graphs
- `OntologyValidator`: Validate ontology structure
- `OWLGenerator`: Generate OWL format ontologies
- `PropertyGenerator`: Generate ontology properties
- `ClassInferrer`: Infer ontology classes

**Complete Code Example**:

```python
from semantica.ontology import OntologyGenerator

generator = OntologyGenerator(base_uri="https://example.org/ontology/")
ontology = generator.generate_from_graph(kg)

# Validate ontology
validator = generator.validate(ontology)
print(f"Valid: {validator.is_valid}")

# Export to OWL
owl_content = generator.export_owl(ontology, format="turtle")
print(f"Generated {len(owl_content)} lines of OWL")
```

**Configuration Options**:

| Option    | Type   | Default    | Description                  |
| :-------- | :----- | :--------- | :--------------------------- |
| `base_uri`| `str`  | `None`     | Base URI for ontology        |
| `reasoner`| `str`  | `"hermit"` | Reasoner (hermit/pellet)     |

**API Reference**: [Ontology Module](reference/ontology.md)

---

## Storage & Embeddings Layer

These modules handle the persistence and retrieval of data, both as vectors and as graphs.

### 6. Embeddings Module

!!! abstract "Purpose"
    Embeddings are crucial for semantic search. This module generates vectors for text, images, and graph nodes.

**Key Features**:
- Multiple provider support (OpenAI, Cohere, HuggingFace)
- Text, image, and audio embeddings
- Multimodal embeddings
- Batch processing
- Caching support
- Custom models

**Input/Output Specification**:

| Input     | Type          | Description                          |
| :-------- | :------------ | :----------------------------------- |
| `texts`   | `List[str]`   | Text to embed                        |
| `provider`| `str`         | Embedding provider (openai/cohere/hf)|
| `model`   | `str`         | Model name                           |

| Output     | Type          | Description                          |
| :--------- | :------------ | :----------------------------------- |
| `embeddings`| `np.ndarray` | Array of embedding vectors          |
| `metadata` | `Dict`        | Embedding metadata                   |

**Components**:
- `EmbeddingGenerator`: Main embedding orchestrator
- `TextEmbedder`: Generate text embeddings
- `ImageEmbedder`: Generate image embeddings
- `AudioEmbedder`: Generate audio embeddings
- `MultimodalEmbedder`: Combine multiple modalities
- `EmbeddingOptimizer`: Optimize embedding quality
- `ProviderAdapters`: Support for OpenAI, Cohere, etc.

**Complete Code Example**:

```python
from semantica.embeddings import EmbeddingGenerator

generator = EmbeddingGenerator(
    provider="openai",
    model="text-embedding-3-small"
)
embeddings = generator.generate(documents)

# Calculate similarity
similarity = generator.similarity(embeddings[0], embeddings[1])
print(f"Similarity: {similarity:.3f}")
```

**Configuration Options**:

| Option      | Type   | Default     | Description                  |
| :---------- | :----- | :---------- | :--------------------------- |
| `provider`  | `str`  | `"openai"`  | Embedding provider           |
| `model`     | `str`  | `None`      | Model name                   |
| `batch_size`| `int`  | `100`       | Batch size for processing    |
| `cache`     | `bool` | `True`      | Enable caching               |

**API Reference**: [Embeddings Module](reference/embeddings.md)

### 7. Vector Store Module

!!! abstract "Purpose"
    Manages the storage and retrieval of high-dimensional vectors, supporting hybrid search strategies.

**Key Features**:
- Multiple backend support (FAISS, Pinecone, Weaviate)
- Hybrid search (vector + keyword)
- Metadata filtering
- Batch operations
- Similarity search
- Index management

**Input/Output Specification**:

| Input      | Type              | Description                          |
| :--------- | :---------------- | :----------------------------------- |
| `embeddings`| `np.ndarray`     | Vector embeddings                    |
| `documents` | `List[Document]`  | Associated documents                 |
| `metadata` | `Dict`            | Metadata for filtering               |

| Output   | Type                | Description                          |
| :------- | :------------------ | :----------------------------------- |
| `results`| `List[SearchResult]`| Search results with scores           |

**Components**:
- `VectorStore`: Main vector store interface
- `FAISSAdapter`: FAISS integration
- `HybridSearch`: Combine vector and keyword search
- `VectorRetriever`: Retrieve relevant vectors

**Complete Code Example**:

```python
from semantica.vector_store import VectorStore, HybridSearch

vector_store = VectorStore(backend="faiss")
vector_store.store(embeddings, documents, metadata)

# Hybrid search
hybrid_search = HybridSearch(vector_store)
results = hybrid_search.search(
    query="machine learning",
    top_k=10,
    filters={"category": "AI"}
)

for result in results:
    print(f"Score: {result.score:.3f} - {result.document.content[:50]}...")
```

**Configuration Options**:

| Option         | Type   | Default   | Description                  |
| :------------- | :----- | :-------- | :--------------------------- |
| `backend`      | `str`  | `"faiss"` | Vector store backend         |
| `index_type`   | `str`  | `"flat"`  | FAISS index type             |
| `hybrid_search`| `bool` | `True`    | Enable hybrid search          |

**API Reference**: [Vector Store Module](reference/vector_store.md)

### 8. Graph Store Module

!!! abstract "Purpose"
    The `graph_store` module provides integration with property graph databases like Neo4j, KuzuDB, and FalkorDB for storing and querying knowledge graphs.

**Key Features**:
- Multiple backend support (Neo4j, KuzuDB, FalkorDB)
- Cypher query language
- Graph algorithms and analytics
- Transaction support
- Index management
- High-performance queries

**Input/Output Specification**:

| Input          | Type   | Description                          |
| :------------- | :----- | :----------------------------------- |
| `backend`      | `str`  | Backend (neo4j/kuzu/falkordb)        |
| `connection_uri`| `str` | Database connection URI              |
| `cypher_query` | `str`  | Cypher query string                  |

| Output   | Type   | Description                          |
| :------- | :----- | :----------------------------------- |
| `result` | `Dict` | Query results                        |
| `node_id`| `str`  | Created node ID                      |

**Components**:
- `GraphStore`: Main graph store interface
- `Neo4jAdapter`: Neo4j database integration
- `KuzuAdapter`: KuzuDB embedded database integration
- `FalkorDBAdapter`: FalkorDB (Redis-based) integration
- `NodeManager`: Node CRUD operations
- `RelationshipManager`: Relationship CRUD operations
- `QueryEngine`: Cypher query execution
- `GraphAnalytics`: Graph algorithms and analytics

**Complete Code Example**:

```python
from semantica.graph_store import GraphStore, create_node, create_relationship

# Using GraphStore class
store = GraphStore(backend="neo4j", uri="bolt://localhost:7687")
store.connect()

# Create nodes
alice = store.create_node(["Person"], {"name": "Alice", "age": 30})
bob = store.create_node(["Person"], {"name": "Bob", "age": 25})

# Create relationship
store.create_relationship(alice["id"], bob["id"], "KNOWS", {"since": 2020})

# Query with Cypher
results = store.execute_query("MATCH (p:Person) RETURN p.name")
print(f"Found {len(results)} people")

# Graph analytics
path = store.shortest_path(alice["id"], bob["id"])
print(f"Shortest path: {path}")

# Or use convenience functions
node = create_node(labels=["Entity"], properties={"name": "Test"})
```

**Configuration Options**:

| Option     | Type   | Default   | Description                  |
| :--------- | :----- | :-------- | :--------------------------- |
| `backend`  | `str`  | `"neo4j"` | Graph database backend       |
| `uri`      | `str`  | `None`    | Database connection URI      |
| `database` | `str`  | `"neo4j"` | Database name                |

**API Reference**: [Graph Store Module](reference/graph_store.md)

---

## Output Layer

These modules handle the export and visualization of your data.

### 11. Export Module

!!! abstract "Purpose"
    Allows you to take your knowledge graph and data out of Semantica for use in other tools.

**Key Features**:
- Multiple export formats (JSON, RDF, CSV, OWL, GraphML)
- Custom export formats
- Batch export
- Metadata preservation
- Streaming export for large graphs

**Input/Output Specification**:

| Input        | Type              | Description                          |
| :----------- | :---------------- | :----------------------------------- |
| `knowledge_graph`| `KnowledgeGraph`| Graph to export                     |
| `format`     | `str`             | Export format                        |
| `output_path`| `str`             | Output file path                     |

| Output        | Type   | Description                          |
| :------------ | :----- | :----------------------------------- |
| `exported_file`| `str` | Path to exported file                |
| `metadata`   | `Dict` | Export metadata                      |

**Components**:
- `JSONExporter`: Export to JSON
- `RDFExporter`: Export to RDF/XML
- `CSVExporter`: Export to CSV
- `GraphExporter`: Export to graph formats (GraphML, GEXF)
- `OWLExporter`: Export to OWL
- `VectorExporter`: Export vectors

**Complete Code Example**:

```python
from semantica.export import JSONExporter, RDFExporter, CSVExporter

# Export to JSON
json_exporter = JSONExporter()
json_exporter.export(kg, "output.json")

# Export to RDF
rdf_exporter = RDFExporter()
rdf_exporter.export(kg, "output.rdf")

# Export to CSV
csv_exporter = CSVExporter()
csv_exporter.export(kg, "output.csv")
```

**Configuration Options**:

| Option           | Type   | Default   | Description                  |
| :--------------- | :----- | :--------- | :--------------------------- |
| `format`         | `str`  | `"json"`   | Export format                |
| `include_metadata`| `bool`| `True`     | Include metadata             |
| `pretty_print`   | `bool` | `False`    | Pretty print JSON            |

**API Reference**: [Export Module](reference/export.md)

### 12. Visualization Module

!!! abstract "Purpose"
    Provides tools to visually explore your data, making it easier to understand complex relationships.

**Key Features**:
- Interactive graph visualization
- Embedding visualization (t-SNE, PCA, UMAP)
- Quality metrics visualization
- Temporal data visualization
- Multiple output formats (HTML, PNG, SVG)
- Custom styling

**Input/Output Specification**:

| Input           | Type              | Description                          |
| :-------------- | :---------------- | :----------------------------------- |
| `knowledge_graph`| `KnowledgeGraph` | Graph to visualize                  |
| `output_format` | `str`             | Output format (html/png/svg)         |
| `output_path`   | `str`             | Output file path                     |

| Output             | Type   | Description                          |
| :----------------- | :----- | :----------------------------------- |
| `visualization_file`| `str`  | Path to visualization file           |

**Components**:
- `KGVisualizer`: Visualize knowledge graphs
- `EmbeddingVisualizer`: Visualize embeddings (t-SNE, PCA, UMAP)
- `QualityVisualizer`: Visualize quality metrics
- `AnalyticsVisualizer`: Visualize graph analytics
- `TemporalVisualizer`: Visualize temporal data

**Complete Code Example**:

```python
from semantica.visualization import KGVisualizer, EmbeddingVisualizer

# Visualize knowledge graph
kg_visualizer = KGVisualizer()
kg_visualizer.visualize(
    kg,
    output_format="html",
    output_path="graph.html"
)

# Visualize embeddings
embed_visualizer = EmbeddingVisualizer()
embed_visualizer.visualize(
    embeddings,
    method="tsne",
    output_path="embeddings.png"
)
```

**Configuration Options**:

| Option         | Type   | Default   | Description                  |
| :------------- | :----- | :--------- | :--------------------------- |
| `output_format`| `str`  | `"html"`   | Output format                |
| `layout`       | `str`  | `"force"`  | Graph layout algorithm       |
| `max_nodes`    | `int`  | `1000`     | Maximum nodes to visualize   |

**API Reference**: [Visualization Module](reference/visualization.md)

---

## Orchestration

This layer connects all other modules into a cohesive workflow.

### 13. Pipeline Module

!!! abstract "Purpose"
    Orchestrates the entire flow, connecting modules together into robust, executable workflows.

**Key Features**:
- Pipeline construction DSL
- Parallel execution
- Error handling and recovery
- Resource scheduling
- Pipeline validation
- Monitoring and logging

**Input/Output Specification**:

| Input     | Type                | Description                          |
| :-------- | :------------------ | :----------------------------------- |
| `steps`   | `List[PipelineStep]`| Pipeline steps                       |
| `parallel`| `bool`              | Enable parallel execution            |

| Output   | Type              | Description                          |
| :------- | :---------------- | :----------------------------------- |
| `result` | `PipelineResult`  | Execution result                     |
| `metrics`| `Dict`            | Performance metrics                  |

**Components**:
- `PipelineBuilder`: Build complex pipelines
- `ExecutionEngine`: Execute pipelines
- `FailureHandler`: Handle pipeline failures
- `ParallelismManager`: Enable parallel processing
- `ResourceScheduler`: Schedule resources

**Complete Code Example**:

```python
from semantica.pipeline import PipelineBuilder
from semantica.ingest import FileIngestor
from semantica.parse import DocumentParser
from semantica.semantic_extract import NERExtractor

builder = PipelineBuilder()
pipeline = builder \
    .add_step("ingest", FileIngestor()) \
    .add_step("parse", DocumentParser()) \
    .add_step("extract", NERExtractor()) \
    .build()

# Execute pipeline
result = pipeline.execute(sources=["data/"], parallel=True)
print(f"Processed {len(result.documents)} documents")
```

**Configuration Options**:

| Option           | Type   | Default | Description                  |
| :--------------- | :----- | :------ | :--------------------------- |
| `parallel`       | `bool` | `False` | Enable parallel execution     |
| `max_workers`    | `int`  | `4`     | Maximum parallel workers      |
| `retry_on_failure`| `bool`| `True`  | Retry failed steps            |

**API Reference**: [Pipeline Module](reference/pipeline.md)

---

## Integration Patterns

This section shows common patterns for integrating multiple modules together.

### Pattern 1: Complete Knowledge Graph Pipeline

```python
from semantica import Semantica

# High-level API - all modules integrated
semantica = Semantica()
result = semantica.build_knowledge_base(
    sources=["documents/"],
    embeddings=True,
    graph=True,
    normalize=True
)
```

### Pattern 2: Custom Pipeline with Module Selection

```python
from semantica.ingest import FileIngestor
from semantica.parse import DocumentParser
from semantica.normalize import TextNormalizer
from semantica.semantic_extract import NERExtractor, RelationExtractor
from semantica.kg import GraphBuilder
from semantica.embeddings import EmbeddingGenerator
from semantica.vector_store import VectorStore

# Step-by-step pipeline
ingestor = FileIngestor()
documents = ingestor.ingest("data/")

parser = DocumentParser()
parsed = parser.parse(documents)

normalizer = TextNormalizer()
normalized = normalizer.normalize(parsed)

extractor = NERExtractor()
entities = extractor.extract(normalized)

rel_extractor = RelationExtractor()
relationships = rel_extractor.extract(normalized, entities)

builder = GraphBuilder()
kg = builder.build(entities, relationships)

generator = EmbeddingGenerator()
embeddings = generator.generate(normalized)

vector_store = VectorStore()
vector_store.store(embeddings, normalized)
```

### Pattern 3: GraphRAG Integration

```python
from semantica import Semantica
from semantica.kg import GraphBuilder
from semantica.vector_store import VectorStore, HybridSearch

# Build knowledge base
semantica = Semantica()
result = semantica.build_knowledge_base(["documents/"])

# Set up GraphRAG
kg = result["knowledge_graph"]
embeddings = result["embeddings"]
vector_store = VectorStore()
vector_store.store(embeddings, result["documents"])

# Query with GraphRAG
hybrid_search = HybridSearch(vector_store)
results = hybrid_search.search(
    query="What is the relationship between X and Y?",
    graph=kg,
    top_k=10
)
```

### Pattern 4: Temporal Graph with Reasoning

```python
from semantica.kg import GraphBuilder
from semantica.reasoning import InferenceEngine, RuleManager

# Build temporal graph
builder = GraphBuilder(temporal=True)
kg = builder.build(entities, relationships)

# Add reasoning
inference_engine = InferenceEngine()
rule_manager = RuleManager()
rules = ["IF A THEN B"]
rule_manager.add_rules(rules)

new_facts = inference_engine.forward_chain(kg, rule_manager)
```

---

## Performance Considerations

### Module Performance Characteristics

| Module | Typical Speed | Memory Usage | Scalability | Optimization Tips |
| :--- | :--- | :--- | :--- | :--- |
| **Ingest** | Fast | Low | High | Batch processing, parallel I/O |
| **Parse** | Medium | Medium | Medium | OCR only when needed, cache results |
| **Normalize** | Fast | Low | High | Batch processing |
| **Semantic Extract** | Slow (LLM) | Medium | Medium | Use faster models, batch processing |
| **KG** | Fast | High (large graphs) | Medium | Use graph stores for large graphs |
| **Embeddings** | Slow (API) | Low | High | Batch processing, caching |
| **Vector Store** | Fast | Medium | High | Use FAISS for large datasets |
| **Graph Store** | Fast | Low | High | Index optimization, query tuning |
| **Reasoning** | Slow | Medium | Low | Limit iterations, optimize rules |
| **Ontology** | Medium | Medium | Medium | Cache validation results |
| **Export** | Fast | Low | High | Streaming for large graphs |
| **Visualization** | Slow | High | Low | Limit nodes, use sampling |
| **Pipeline** | Varies | Varies | High | Parallel execution, resource limits |

### Optimization Strategies

1. **Batch Processing**: Process multiple documents together
   ```python
   # Good: Batch processing
   documents = ingestor.ingest("data/", batch_size=100)
   ```

2. **Caching**: Cache expensive operations
   ```python
   # Cache embeddings
   generator = EmbeddingGenerator(cache=True)
   ```

3. **Parallel Execution**: Use pipeline parallelism
   ```python
   pipeline = builder.build()
   result = pipeline.execute(sources=sources, parallel=True, max_workers=8)
   ```

4. **Backend Selection**: Choose appropriate backends
   ```python
   # For large graphs, use Neo4j instead of NetworkX
   builder = GraphBuilder(backend="neo4j")
   ```

5. **Resource Limits**: Set appropriate limits
   ```python
   # Limit memory usage
   parser = DocumentParser(max_file_size=10_000_000)  # 10MB
   ```

---

## Next Steps

- **[Core Concepts](concepts.md)** - Understand the fundamental concepts
- **[Use Cases](use-cases.md)** - See real-world applications
- **[Examples](examples.md)** - Practical code examples
- **[API Reference](reference/core.md)** - Detailed API documentation

---

!!! info "Contribute"
    Found an issue or want to improve this guide? [Contribute on GitHub](https://github.com/Hawksight-AI/semantica)

**Last Updated**: 2024
