# Semantic Extract Module

> **Extract structured knowledge from unstructured text using state-of-the-art NLP and LLM models.**

---

## 🎯 Overview

<div class="grid cards" markdown>

-   :material-account-search:{ .lg .middle } **Named Entity Recognition**

    ---

    Extract people, organizations, locations, dates, and custom entities with high accuracy

-   :material-graph:{ .lg .middle } **Relationship Extraction**

    ---

    Identify semantic, temporal, and causal relationships between entities

-   :material-calendar-clock:{ .lg .middle } **Event Detection**

    ---

    Detect and classify events like acquisitions, partnerships, announcements

-   :material-cube-outline:{ .lg .middle } **Triple Extraction**

    ---

    Generate RDF triples for knowledge graphs in multiple formats

-   :material-link-variant:{ .lg .middle } **Coreference Resolution**

    ---

    Resolve pronouns and entity mentions across documents

-   :material-brain:{ .lg .middle } **Semantic Analysis**

    ---

    Deep semantic understanding with role labeling and clustering

</div>

---

## ⚙️ Algorithms Used

### Entity Extraction Algorithms
- **Transformer-based NER**: BERT, RoBERTa, DeBERTa models for high-accuracy entity recognition
- **spaCy Statistical Models**: Fast, production-ready NER with en_core_web_sm/lg models
- **Rule-based Matching**: Pattern-based entity detection using regex and linguistic rules
- **LLM-based Extraction**: GPT-4, Claude for complex entity extraction with few-shot learning

### Relationship Extraction Algorithms
- **Dependency Parsing**: Syntactic dependency trees for relationship identification
- **Pattern Matching**: Rule-based relationship templates
- **Neural Relation Classification**: BERT-based relation classifiers
- **Hybrid Approach**: Combines rule-based + ML + LLM for optimal accuracy

### Coreference Resolution Algorithms
- **Neural Coreference**: Span-based neural models for pronoun resolution
- **Rule-based Resolution**: Heuristic rules for simple coreference cases
- **Cluster-based Merging**: Entity mention clustering across documents

### Triple Extraction Algorithms
- **Subject-Predicate-Object Extraction**: Dependency parsing for triple generation
- **RDF Serialization**: Turtle, N-Triples, JSON-LD format generation
- **Triple Validation**: Schema-based validation and quality checking

---

## Main Classes

### NamedEntityRecognizer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `extract(text)` | Extract entities from text | Transformer-based NER with confidence scoring |
| `extract_batch(texts)` | Batch entity extraction | Parallel processing with batching |
| `add_custom_entity_type(name, patterns)` | Add custom entity type | Pattern matching with regex |
| `classify_entity(entity)` | Classify entity type | Multi-class classification |
| `score_confidence(entity)` | Calculate confidence score | Softmax probability scoring |

**Example:**

```python
from semantica.semantic_extract import NamedEntityRecognizer

# Initialize with transformer model
ner = NamedEntityRecognizer(
    model="transformer",  # or "spacy", "stanza", "custom"
    lang="en",
    entities=["PERSON", "ORG", "LOC", "DATE", "MONEY"],
    confidence_threshold=0.7,
    use_llm_enhancement=True
)

text = "Apple Inc. was founded by Steve Jobs in 1976."
entities = ner.extract(text)

for entity in entities:
    print(f"{entity.text} ({entity.type}, confidence={entity.confidence:.2f})")
# Output:
# Apple Inc. (ORG, confidence=0.98)
# Steve Jobs (PERSON, confidence=0.97)
# 1976 (DATE, confidence=1.00)
```

---

### RelationExtractor


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `extract(text, entities)` | Extract relationships | Hybrid: dependency parsing + ML + LLM |
| `extract_with_context(text, entities, context)` | Context-aware extraction | Contextual embeddings with attention |
| `add_custom_relation(name, pattern)` | Add custom relation type | Pattern-based rule addition |
| `classify_relation(subject, object, context)` | Classify relation type | Neural relation classification |
| `score_confidence(relation)` | Calculate relation confidence | Ensemble scoring from multiple models |

**Algorithms:**

- **Rule-based**: Pattern matching using dependency trees
- **ML-based**: BERT fine-tuned on relation extraction datasets
- **Hybrid**: Combines rules + ML for high precision and recall
- **LLM-based**: Few-shot prompting with GPT-4/Claude for complex relations

**Example:**

```python
from semantica.semantic_extract import RelationExtractor

extractor = RelationExtractor(
    strategy="hybrid",  # "rule-based", "ml-based", "hybrid", "llm-based"
    confidence_threshold=0.7,
    max_relationships_per_entity=10
)

relationships = extractor.extract(text, entities)

for rel in relationships:
    print(f"{rel.subject} --[{rel.predicate}]--> {rel.object}")
# Output:
# Apple Inc. --[founded_by]--> Steve Jobs
```

---

### EventDetector


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `detect(text, entities)` | Detect events in text | Event trigger detection + argument extraction |
| `detect_batch(texts, entities_list)` | Batch event detection | Parallel processing |
| `classify_event(event)` | Classify event type | Multi-label classification |
| `extract_participants(event, entities)` | Extract event participants | Role labeling with semantic roles |
| `extract_temporal_info(event)` | Extract event timing | Temporal expression extraction |

**Event Types Supported:**
- ACQUISITION, FOUNDING, PARTNERSHIP, ANNOUNCEMENT
- MERGER, IPO, BANKRUPTCY, LAWSUIT
- PRODUCT_LAUNCH, CONFERENCE, ELECTION
- Custom event types via configuration

**Example:**

```python
from semantica.semantic_extract import EventDetector

detector = EventDetector(
    event_types=["ACQUISITION", "FOUNDING", "PARTNERSHIP"],
    min_confidence=0.75
)

events = detector.detect(text, entities)

for event in events:
    print(f"{event.type}: {event.description}")
    print(f"Participants: {[p.name for p in event.participants]}")
```

---

### TripleExtractor


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `extract(text, entities, relationships)` | Extract RDF triples | Subject-predicate-object extraction from parse trees |
| `extract_from_relations(relationships)` | Convert relations to triples | Direct mapping with URI generation |
| `validate_triples(triples)` | Validate triple quality | Schema validation + consistency checking |
| `serialize(triples, format)` | Serialize to RDF format | Turtle, N-Triples, JSON-LD serialization |
| `generate_uri(entity)` | Generate URI for entity | Namespace + normalized entity name |

**Supported Formats:**
- **RDF/XML**: W3C standard RDF format
- **Turtle**: Human-readable RDF format
- **N-Triples**: Line-based RDF format
- **JSON-LD**: JSON-based linked data format

**Example:**

```python
from semantica.semantic_extract import TripleExtractor

extractor = TripleExtractor(
    format="rdf",  # "rdf", "turtle", "n-triples", "json-ld"
    validate_triples=True,
    namespace="http://example.org/"
)

triples = extractor.extract(text, entities, relationships)

for triple in triples:
    print(f"{triple.subject} {triple.predicate} {triple.object}")
# Output:
# <Apple_Inc> <founded_by> <Steve_Jobs>
# <Apple_Inc> <founded_in> "1976"^^xsd:gYear
```

---

### CoreferenceResolver


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `resolve(text, entities)` | Resolve coreferences | Neural coreference resolution with span ranking |
| `resolve_batch(texts, entities_list)` | Batch resolution | Parallel coreference resolution |
| `cluster_mentions(mentions)` | Cluster entity mentions | Agglomerative clustering with similarity threshold |
| `merge_entities(entity_clusters)` | Merge coreferent entities | Property aggregation with conflict resolution |
| `resolve_pronouns(text, entities)` | Resolve pronoun references | Rule-based + neural pronoun resolution |

**Algorithms:**
- **Neural Method**: Span-based neural coreference (e2e-coref, SpanBERT)
- **Rule-based Method**: Heuristic rules for simple cases (gender, number agreement)
- **Hybrid Method**: Combines neural + rules for optimal performance

**Example:**

```python
from semantica.semantic_extract import CoreferenceResolver

resolver = CoreferenceResolver(
    method="neural",  # "rule-based", "neural", "hybrid"
    resolve_pronouns=True
)

resolved_entities = resolver.resolve(text, entities)
```

---

### SemanticAnalyzer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `analyze_semantics(text, entities, relationships)` | Analyze semantic structure | Semantic role labeling + clustering |
| `extract_semantic_roles(text)` | Extract semantic roles | PropBank/FrameNet-based role labeling |
| `cluster_semantically(entities)` | Cluster by semantic similarity | K-means clustering on embeddings |
| `calculate_similarity(entity1, entity2)` | Calculate semantic similarity | Cosine similarity on embeddings |
| `analyze_coherence(text)` | Analyze text coherence | Coherence scoring with discourse analysis |

**Example:**

```python
from semantica.semantic_extract import SemanticAnalyzer

analyzer = SemanticAnalyzer()

analysis = analyzer.analyze_semantics(
    text=text,
    entities=entities,
    relationships=relationships
)

print(f"Coherence score: {analysis.coherence_score:.2f}")
print(f"Semantic roles: {analysis.semantic_roles}")
```

---

### LLMEnhancer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `enhance_entities(text, entities)` | Enhance entities with LLM | Few-shot prompting for entity enrichment |
| `enhance_relationships(text, relationships)` | Enhance relationships | LLM-based relationship validation and enrichment |
| `generate_descriptions(entity)` | Generate entity descriptions | LLM text generation |
| `validate_extractions(extractions)` | Validate with LLM | LLM-based quality checking |
| `classify_with_llm(text, labels)` | LLM-based classification | Zero/few-shot classification |

**Supported LLM Providers:**
- OpenAI (GPT-4, GPT-3.5-turbo)
- Anthropic (Claude 3 Opus, Sonnet, Haiku)
- Google (Gemini Pro, Ultra)
- Groq (Mixtral, Llama)
- Ollama (Local models)

**Example:**

```python
from semantica.semantic_extract import LLMEnhancer

enhancer = LLMEnhancer(
    provider="openai",
    model="gpt-4",
    temperature=0.1
)

enhanced_entities = enhancer.enhance_entities(text, entities)
enhanced_relationships = enhancer.enhance_relationships(text, relationships)
```

---

### ExtractionValidator


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `validate(text, entities, relationships, triples)` | Validate all extractions | Multi-level validation pipeline |
| `validate_entities(entities)` | Validate entity quality | Schema validation + consistency checks |
| `validate_relationships(relationships)` | Validate relationships | Type checking + logical validation |
| `validate_triples(triples)` | Validate RDF triples | RDF schema validation |
| `check_consistency(extractions)` | Check extraction consistency | Cross-validation between extraction types |

**Validation Checks:**
- **Schema Validation**: Type checking against ontology
- **Consistency Checking**: Cross-validation between entities and relationships
- **Quality Scoring**: Confidence-based quality metrics
- **Completeness**: Required property validation

---

## Configuration

```yaml
# config.yaml - Semantic Extract Configuration

semantic_extract:
  ner:
    model: transformer  # spacy, stanza, transformer, llm
    lang: en
    entities: [PERSON, ORG, LOC, DATE, MONEY, PRODUCT]
    confidence_threshold: 0.7
    use_llm_enhancement: false
    
  relation_extraction:
    strategy: hybrid  # rule-based, ml-based, hybrid, llm-based
    confidence_threshold: 0.7
    max_relationships_per_entity: 10
    
  event_detection:
    event_types: [ACQUISITION, FOUNDING, PARTNERSHIP, ANNOUNCEMENT]
    min_confidence: 0.75
    extract_participants: true
    extract_temporal: true
    
  triple_extraction:
    format: turtle  # rdf, turtle, n-triples, json-ld
    validate_triples: true
    namespace: "http://example.org/"
    
  coreference:
    method: neural  # rule-based, neural, hybrid
    resolve_pronouns: true
    cluster_threshold: 0.85
    
  llm:
    provider: openai
    model: gpt-4
    temperature: 0.1
    max_tokens: 4000
```

---

## Performance Characteristics

### Entity Extraction
- **Transformer models**: High accuracy, moderate speed
- **spaCy models**: Fast, good accuracy for common entities
- **LLM-based**: Highest accuracy, slower, best for complex domains

### Relationship Extraction
- **Rule-based**: Fast, high precision, lower recall
- **ML-based**: Balanced precision/recall
- **Hybrid**: Best overall performance
- **LLM-based**: Highest quality, slower

### Scalability
- Batch processing supported for all extractors
- Parallel processing for multi-document extraction
- GPU acceleration available for transformer models

---

## See Also

- [Knowledge Graph Module](kg.md) - Build graphs from extracted data
- [Ontology Module](ontology.md) - Define extraction schemas
- [Core Module](core.md) - Framework orchestration
