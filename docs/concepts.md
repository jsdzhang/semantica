# Core Concepts

Understand the fundamental concepts behind Semantica. This guide covers the theoretical foundations, key components, and best practices for building semantic applications.

!!! info "About This Guide"
    This guide provides a comprehensive overview of the core concepts in Semantica. Each concept includes definitions, visual diagrams, practical examples, and guidance on when to use them.

---



## Core Concepts

### 1. Knowledge Graphs

!!! abstract "Definition"
    A **knowledge graph** is a structured representation of entities (nodes) and their relationships (edges) with properties and attributes. It transforms unstructured data into a queryable, interconnected knowledge base.

<div class="grid cards" markdown>

-   **Nodes (Entities)**
    ---
    Represent real-world objects, concepts, or events.
    *Examples*: People, Organizations, Locations, Concepts

-   **Edges (Relationships)**
    ---
    Represent connections between entities.
    *Examples*: `works_for`, `located_in`, `founded_by`, `causes`

-   **Properties**
    ---
    Attributes of entities and relationships.
    *Examples*: Name, Date, Confidence Score, Source

-   **Metadata**
    ---
    Additional information about the data.
    *Examples*: Source documents, timestamps, extraction methods

</div>

**Visual Example**:

```mermaid
graph LR
    A[Apple Inc.<br/>Organization<br/>Founded: 1976] -->|founded_by| B[Steve Jobs<br/>Person<br/>1955-2011]
    A -->|located_in| C[Cupertino<br/>Location<br/>City]
    C -->|in_state| D[California<br/>Location<br/>State]
    A -->|has_ceo| E[Tim Cook<br/>Person<br/>CEO since 2011]
    
    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style B fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style C fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style D fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style E fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
```

**Practical Example**:

```python
from semantica import Semantica

# Initialize Semantica
semantica = Semantica()

# Build knowledge graph from document
result = semantica.build_knowledge_base(
    sources=["company_report.pdf"],
    embeddings=True,
    graph=True
)

kg = result["knowledge_graph"]

# Access entities and relationships
print(f"Entities: {len(kg['entities'])}")
print(f"Relationships: {len(kg['relationships'])}")

# Query the graph
for entity in kg['entities'][:5]:
    print(f"- {entity.get('text', 'N/A')}: {entity.get('type', 'N/A')}")
```

**Related Modules**:

- [`kg` Module](reference/kg.md) - Knowledge graph construction and management
- [`graph_store` Module](reference/graph_store.md) - Persistent graph storage
- [`visualization` Module](reference/visualization.md) - Graph visualization

---

### 2. Entity Extraction (NER)

!!! abstract "Definition"
    **Named Entity Recognition (NER)** is the process of identifying and classifying named entities in text into predefined categories such as persons, organizations, locations, dates, and more.

**Entity Types**:

| Entity Type      | Description                    | Example                          |
| :--------------- | :----------------------------- | :------------------------------- |
| **Person**       | Names of people                | Steve Jobs, Elon Musk, Marie Curie |
| **Organization** | Companies, institutions       | Apple Inc., NASA, MIT            |
| **Location**     | Places, geographic entities   | Cupertino, Mars, Pacific Ocean  |
| **Date/Time**    | Temporal expressions           | 1976, next Monday, Q1 2024      |
| **Money**        | Monetary values                | $100 million, €50,000            |
| **Event**        | Events and occurrences         | WWDC 2024, World War II          |
| **Product**      | Products and services          | iPhone 15, Tesla Model S         |
| **Technology**   | Technologies and methods       | Machine Learning, Python         |

!!! tip "Custom Entities"
    Semantica allows you to define custom entity types via the [`Ontology`](reference/ontology.md) module. You aren't limited to the standard set!

**Extraction Methods**:

=== "Rule-based"
    Uses pattern matching (regex) to identify entities.
    
    **Pros**: Fast, deterministic, no training data needed
    
    **Cons**: Limited to predefined patterns, less flexible
    
    ```python
    from semantica.semantic_extract import NamedEntityRecognizer
    
    ner = NamedEntityRecognizer(method="rule-based")
    entities = ner.extract_entities("Apple Inc. was founded in 1976.")
    ```

=== "Machine Learning"
    Uses trained models (spaCy, transformers) for extraction.
    
    **Pros**: More accurate, handles variations
    
    **Cons**: Requires training data, slower than rules
    
    ```python
    ner = NamedEntityRecognizer(method="spacy")
    entities = ner.extract_entities(text)
    ```

=== "LLM-based"
    Uses large language models (GPT-4, Claude) for extraction.
    
    **Pros**: Most accurate, understands context
    
    **Cons**: Slower, requires API access, costs money
    
    ```python
    ner = NamedEntityRecognizer(method="llm", model="gpt-4")
    entities = ner.extract_entities(text)
    ```

**Related Modules**:
- [`semantic_extract` Module](reference/semantic_extract.md) - Entity and relationship extraction
- [`ontology` Module](reference/ontology.md) - Custom entity type definitions

---

### 3. Relationship Extraction

!!! abstract "Definition"
    **Relationship Extraction** is the process of identifying and extracting semantic relationships between entities in text. It connects entities to form meaningful knowledge structures.

**Relationship Types**:

=== "Semantic Relationships"
    Relationships that define meaning and connection between entities.
    
    - `works_for` - Employment relationships
    - `located_in` - Geographic relationships
    - `founded_by` - Creation relationships
    - `owns` - Ownership relationships
    - `part_of` - Hierarchical relationships
    
    ```python
    # Example: "Tim Cook works for Apple Inc."
    # Extracted: (Tim Cook) --[works_for]--> (Apple Inc.)
    ```

=== "Temporal Relationships"
    Relationships defined by time and sequence.
    
    - `happened_before` - Temporal precedence
    - `happened_after` - Temporal succession
    - `during` - Temporal containment
    - `overlaps_with` - Temporal overlap
    
    ```python
    # Example: "WWDC 2023 happened before WWDC 2024"
    # Extracted: (WWDC 2023) --[happened_before]--> (WWDC 2024)
    ```

=== "Causal Relationships"
    Cause and effect relationships.
    
    - `causes` - Direct causation
    - `results_in` - Outcome relationships
    - `prevents` - Prevention relationships
    - `influences` - Indirect influence
    
    ```python
    # Example: "High inflation causes economic instability"
    # Extracted: (High inflation) --[causes]--> (Economic instability)
    ```

**Visual Example**:

```mermaid
graph LR
    A[Apple Inc.] -->|founded_by| B[Steve Jobs]
    A -->|located_in| C[Cupertino]
    A -->|has_ceo| D[Tim Cook]
    C -->|in_state| E[California]
    B -->|co-founded| F[Apple Inc.]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#e3f2fd
```

**Related Modules**:
- [`semantic_extract` Module](reference/semantic_extract.md) - Relationship extraction
- [`kg` Module](reference/kg.md) - Building graphs from relationships

---

### 4. Embeddings

!!! abstract "Definition"
    **Embeddings** are dense vector representations of text, images, or other data that capture semantic meaning in a continuous vector space. They enable machines to understand similarity and meaning.

!!! note "The Bridge Between Language and Understanding"
    Embeddings are the bridge between human language and machine understanding. They convert text into numerical vectors that preserve semantic relationships.

**How Embeddings Work**:

Embeddings convert text into numerical vectors that capture semantic meaning. Similar texts have similar vectors, enabling semantic search and similarity calculations.

**Example**:

```python
Text: "machine learning"
Embedding: [0.123, -0.456, 0.789, ..., 0.234]  # (vector of 1536 dimensions)

# Similar texts will have similar vectors
"artificial intelligence" → [0.145, -0.432, 0.801, ..., 0.221]  # Close in vector space
"cooking recipes" → [-0.234, 0.567, -0.123, ..., -0.456]  # Far in vector space
```

**Embedding Providers**:

| Provider | Model | Dimensions | Speed | Cost | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | text-embedding-3-large | 3072 | Fast | Paid | Production, high accuracy |
| **OpenAI** | text-embedding-3-small | 1536 | Fast | Paid | Balanced performance |
| **Cohere** | embed-english-v3.0 | 1024 | Fast | Paid | Multilingual support |
| **HuggingFace** | sentence-transformers | 384-768 | Medium | Free | Development, open source |
| **Local** | Various | Variable | Slow | Free | Privacy, offline use |

**Related Modules**:
- [`embeddings` Module](reference/embeddings.md) - Embedding generation
- [`vector_store` Module](reference/vector_store.md) - Vector storage and search

---

### 5. Temporal Graphs

!!! abstract "Definition"
    **Temporal Graphs** are knowledge graphs that track changes over time, allowing queries about the state of the graph at specific time points. They enable time-aware reasoning and analysis.

**Key Features**:

- **Time-stamped Entities**: Entities have creation and modification timestamps
- **Time-stamped Relationships**: Relationships have validity periods
- **Historical Queries**: Query the graph state at any point in time
- **Change Tracking**: Track how entities and relationships evolve

**Visual Timeline**:

```mermaid
timeline
    title Temporal Graph Evolution
    2020 : Entity A created
         : Relationship A->B established
    2021 : Entity B updated
         : Relationship B->C created
    2022 : Entity A deleted
         : New Relationship D->C
    2023 : Entity C properties updated
         : Relationship A->B expired
```

**Related Modules**:
- [`kg` Module](reference/kg.md) - Temporal graph support
- [`visualization` Module](reference/visualization.md) - Temporal visualization

---

### 6. GraphRAG

!!! abstract "Definition"
    **GraphRAG (Graph-Augmented Retrieval Augmented Generation)** is an advanced RAG approach that combines vector search with knowledge graph traversal to provide more accurate and contextually relevant information to LLMs.

**How GraphRAG Works**:

```mermaid
flowchart TD
    subgraph Query["Query Processing"]
        Q[User Query] --> VS[Vector Search]
        Q --> KE[Keyword Extraction]
    end
    
    subgraph Retrieval["Hybrid Retrieval"]
        VS --> Docs[Relevant Documents]
        KE --> Nodes[Start Nodes]
        Nodes --> Trav[Graph Traversal]
        Trav --> Context[Graph Context]
    end
    
    subgraph Synthesis["Answer Generation"]
        Docs --> Prompt[Enhanced Prompt]
        Context --> Prompt
        Prompt --> LLM[LLM Generation]
        LLM --> A[Accurate Answer]
    end
    
    style Q fill:#e1f5fe
    style LLM fill:#e8f5e9
    style A fill:#fff9c4
```

**Advantages over Traditional RAG**:

| Feature | Traditional RAG | GraphRAG |
| :--- | :--- | :--- |
| **Query Understanding** | Keyword matching | Semantic + structural |
| **Context Retrieval** | Document chunks | Documents + relationships |
| **Answer Accuracy** | Good | Better (grounded in graph) |
| **Hallucination Risk** | Medium | Lower |
| **Complex Queries** | Limited | Excellent |
| **Relationship Awareness** | No | Yes |

**Related Modules**:
- [`kg` Module](reference/kg.md) - Knowledge graph construction
- [`vector_store` Module](reference/vector_store.md) - Vector search
- [`reasoning` Module](reference/reasoning.md) - Graph reasoning

---

### 7. Ontology

!!! abstract "Definition"
    An **Ontology** is a formal specification of concepts, relationships, and constraints in a domain, typically expressed in OWL (Web Ontology Language). It defines the schema and structure of your knowledge domain.

**Key Components**:

- **Classes**: Categories of entities (e.g., `Person`, `Company`, `Location`)
- **Properties**: Relationships and attributes (e.g., `worksFor`, `hasName`)
- **Individuals**: Specific instances (e.g., `John Doe`, `Apple Inc.`)
- **Axioms**: Rules and constraints (e.g., "A Person can only workFor one Company")

**Ontology Structure**:

```mermaid
classDiagram
    class Person {
        +String name
        +Date birthDate
        +worksFor Company
    }
    class Company {
        +String name
        +Date founded
        +locatedIn Location
    }
    class Location {
        +String city
        +String country
    }
    
    Person --> Company : worksFor
    Company --> Location : locatedIn
```

**Related Modules**:
- [`ontology` Module](reference/ontology.md) - Ontology generation and management
- [`kg` Module](reference/kg.md) - Knowledge graph construction

---

### 8. Quality Assurance

!!! abstract "Definition"
    **Quality Assurance** encompasses processes and metrics to ensure knowledge graph quality, including completeness, consistency, accuracy, and coverage validation.

**Quality Dimensions**:

| Dimension | Description | Metrics |
| :--- | :--- | :--- |
| **Completeness** | Percentage of entities with required properties | Property coverage, missing fields |
| **Consistency** | Absence of contradictions | Conflict count, validation errors |
| **Accuracy** | Correctness of extracted information | Precision, recall, F1-score |
| **Coverage** | Breadth of domain coverage | Entity diversity, relationship types |
| **Freshness** | How up-to-date the data is | Last update timestamp, staleness |

**Related Modules**:
- [`kg_qa` Module](reference/evals.md) - Quality assurance and evaluation
- [`conflicts` Module](../semantica/conflicts/conflicts_usage.md) - Conflict detection

---

### 9. Deduplication & Entity Resolution

!!! abstract "Definition"
    **Deduplication** and **Entity Resolution** are processes that identify and merge duplicate entities in a knowledge graph, ensuring that the same real-world entity is represented by a single node.

**Why It Matters**:

- Multiple sources may refer to the same entity differently
- "Apple Inc." vs "Apple" vs "Apple Computer" → Same entity
- Prevents graph fragmentation and improves query accuracy

**Resolution Process**:

Deduplication works by calculating similarity between entities. If similarity exceeds a threshold, entities are merged; otherwise, they remain separate.

**Related Modules**:
- [`deduplication` Module](../semantica/deduplication/deduplication_usage.md) - Deduplication and merging
- [`embeddings` Module](reference/embeddings.md) - Similarity calculation

---

### 10. Data Normalization

!!! abstract "Definition"
    **Data Normalization** is the process of cleaning and standardizing data into a consistent format, ensuring uniformity across your knowledge graph.

**Normalization Pipeline**:

```mermaid
flowchart LR
    Raw[Raw Text] --> Clean[Text Cleaning]
    Clean --> Entity[Entity<br/>Normalization]
    Entity --> Date[Date<br/>Normalization]
    Date --> Number[Number<br/>Normalization]
    Number --> Normalized[Normalized<br/>Data]
    
    style Raw fill:#ffcdd2
    style Normalized fill:#c8e6c9
```

**Related Modules**:
- [`normalize` Module](reference/normalize.md) - Data normalization
- [`parse` Module](reference/parse.md) - Document parsing

---

### 11. Conflict Detection

!!! abstract "Definition"
    **Conflict Detection** identifies contradictory information in a knowledge graph, such as conflicting facts about the same entity from different sources.

**Conflict Types**:

| Type | Description | Example |
| :--- | :--- | :--- |
| **Value Conflict** | Different values for same property | "Founded: 1976" vs "Founded: 1977" |
| **Relationship Conflict** | Conflicting relationships | "CEO: Tim Cook" vs "CEO: Steve Jobs" |
| **Type Conflict** | Different entity types | "Apple: Company" vs "Apple: Product" |
| **Temporal Conflict** | Conflicting time information | "Active: 2020-2023" vs "Active: 2021-2024" |

**Conflict Resolution Strategies**:

=== "Voting"
    Use the most common value across sources.
    
    ```python
    resolver = ConflictResolver(strategy="voting")
    resolved = resolver.resolve(conflicts)
    ```

=== "Highest Confidence"
    Use the value with the highest confidence score.
    
    ```python
    resolver = ConflictResolver(strategy="highest_confidence")
    resolved = resolver.resolve(conflicts)
    ```

=== "Most Recent"
    Use the most recently updated value.
    
    ```python
    resolver = ConflictResolver(strategy="most_recent")
    resolved = resolver.resolve(conflicts)
    ```

=== "Source Priority"
    Use values from trusted sources first.
    
    ```python
    resolver = ConflictResolver(
        strategy="source_priority",
        source_priority=["trusted_source", "other_source"]
    )
    resolved = resolver.resolve(conflicts)
    ```

**Related Modules**:
- [`conflicts` Module](../semantica/conflicts/conflicts_usage.md) - Conflict detection and resolution
- [`kg_qa` Module](reference/evals.md) - Quality assurance

---

## Comparison Tables

### Embedding Providers Comparison

| Provider | Model | Dimensions | Speed | Cost | Accuracy | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | text-embedding-3-large | 3072 | Fast | Paid | High | Production, high accuracy |
| **OpenAI** | text-embedding-3-small | 1536 | Fast | Paid | High | Balanced performance |
| **Cohere** | embed-english-v3.0 | 1024 | Fast | Paid | High | Multilingual support |
| **HuggingFace** | all-MiniLM-L6-v2 | 384 | Medium | Free | Medium | Development, open source |
| **Local** | sentence-transformers | 384-768 | Slow | Free | Medium | Privacy, offline use |

### Graph Backend Comparison

| Backend | Type | Speed | Scalability | Query Language | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NetworkX**| In-memory | Fast | Small-medium | Python API | Development, small graphs |
| **Neo4j** | Database | Medium | Large | Cypher | Production, complex queries |
| **KuzuDB** | Embedded | Fast | Medium | Cypher | Embedded applications |
| **FalkorDB**| Redis-based| Very Fast | Large | Cypher | Real-time, high throughput |

---

## Best Practices

Following these practices will help you build high-quality knowledge graphs and avoid common pitfalls.

### 1. Start Small

!!! tip "Iterative Approach"
    Don't try to model the entire world at once. Start with a small, well-defined domain and expand incrementally.

**Example**:
```python
# Start with a single document
kg1 = semantica.build_knowledge_base(["doc1.pdf"])

# Validate and refine
quality = assessor.assess(kg1)

# Then expand
kg2 = semantica.build_knowledge_base(["doc2.pdf", "doc3.pdf"])
merged = semantica.kg.merge([kg1, kg2])
```

### 2. Configure Properly

- Use environment variables for sensitive data
- Set up proper logging
- Configure appropriate model sizes
- Use configuration files for complex setups

```python
# Good: Use environment variables
import os
api_key = os.getenv("OPENAI_API_KEY")

# Good: Use config files
from semantica import Config
config = Config.from_file("config.yaml")
semantica = Semantica(config=config)
```

### 3. Validate Data

!!! warning "Garbage In, Garbage Out"
    Always validate extracted entities. A knowledge graph with incorrect facts is worse than no graph at all.

**Validation Checklist**:
- Check entity extraction accuracy
- Validate relationships make sense
- Verify confidence scores
- Review source attribution
- Test with sample queries

### 4. Handle Errors

- Implement error handling
- Use retry mechanisms
- Log errors for debugging
- Gracefully handle API failures

```python
from semantica import Semantica
import logging

logging.basicConfig(level=logging.INFO)
semantica = Semantica()

try:
    result = semantica.build_knowledge_base(["doc.pdf"])
except Exception as e:
    logging.error(f"Error building KG: {e}")
    # Handle error appropriately
```

### 5. Optimize Performance

- Use batch processing for large datasets
- Enable parallel processing where possible
- Cache embeddings and results
- Use appropriate backend for your scale

```python
# Batch processing
sources = ["doc1.pdf", "doc2.pdf", ..., "doc100.pdf"]
batch_size = 10

for i in range(0, len(sources), batch_size):
    batch = sources[i:i+batch_size]
    result = semantica.build_knowledge_base(batch)
    # Process and save results
```

### 6. Document Workflows

- Document data sources
- Track processing steps
- Maintain metadata
- Version your knowledge graphs

---

## Troubleshooting

Common issues and solutions:

!!! failure "Import Errors"
    **Solution**:
    - Ensure Semantica is properly installed: `pip install semantica`
    - Check Python version (3.8+): `python --version`
    - Verify virtual environment is activated
    - Install missing dependencies: `pip install -r requirements.txt`

!!! failure "API Key Errors"
    **Solution**:
    - Set environment variables: `export OPENAI_API_KEY=your_key`
    - Check config file for correct key format
    - Verify API key is valid and has sufficient credits
    - Test API connection: `curl https://api.openai.com/v1/models`

!!! failure "Memory Issues"
    **Solution**:
    - Process documents in batches
    - Use smaller embedding models
    - Enable garbage collection
    - Consider using streaming for large datasets
    - Use graph store backends (Neo4j, KuzuDB) instead of in-memory

!!! failure "Low Quality Extractions"
    **Solution**:
    - Preprocess and normalize text
    - Use domain-specific models
    - Adjust extraction parameters
    - Validate and clean extracted entities
    - Use LLM-based extraction for better accuracy
    - Fine-tune models on your domain

!!! failure "Slow Processing"
    **Solution**:
    - Enable parallel processing
    - Use GPU acceleration if available
    - Cache embeddings and results
    - Optimize batch sizes
    - Use faster embedding models
    - Consider using local models for development

!!! failure "Graph Too Large"
    **Solution**:
    - Use graph store backends (Neo4j, KuzuDB) instead of NetworkX
    - Implement graph partitioning
    - Use incremental building
    - Filter entities by confidence threshold
    - Remove low-value relationships

---

## Next Steps

Now that you understand the core concepts:

1. **[Getting Started](getting-started.md)** - Set up Semantica and build your first knowledge graph
2. **[Modules Guide](modules.md)** - Learn about the available modules
3. **[Use Cases](use-cases.md)** - Explore real-world applications
4. **[Examples](examples.md)** - See practical code examples
5. **[API Reference](reference/core.md)** - Detailed API documentation

---

!!! info "Contribute"
    Found an issue or want to improve this guide? [Contribute on GitHub](https://github.com/Hawksight-AI/semantica)

**Last Updated**: 2024
