# 🧠 SemantiCore

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/semanticore.svg)](https://badge.fury.io/py/semanticore)
[![Downloads](https://pepy.tech/badge/semanticore)](https://pepy.tech/project/semanticore)

**Transform unstructured data into structured semantic layers for LLMs, Agents, RAG systems, and Knowledge Graphs.**

SemantiCore bridges the gap between raw unstructured data and intelligent AI systems by providing a comprehensive toolkit for semantic extraction, schema generation, and knowledge representation.

---

## 🌟 Why SemantiCore?

Modern AI systems require structured, semantically rich data to perform effectively. SemantiCore solves the fundamental challenge of converting messy, unstructured information into clean, schema-compliant semantic layers that power:

- **🤖 Intelligent Agents** - With type-safe, validated input/output schemas
- **🔍 RAG Systems** - Enhanced with semantic chunking and enriched metadata
- **🕸️ Knowledge Graphs** - Automatically extracted entities, relations, and triples
- **🛠️ LLM Tools** - Wrapped with semantic contracts for reliable operation
- **📊 Data Pipelines** - Consistent, validated data flows across your stack

---

## 🚀 Quick Start

### Installation

```bash
# Install via pip
pip install semanticore

# Or install with all dependencies
pip install "semanticore[all]"

# Development installation
git clone https://github.com/yourusername/semanticore.git
cd semanticore
pip install -e ".[dev]"
```

### Basic Usage

```python
from semanticore import SemantiCore

# Initialize the core engine
core = SemantiCore()

# Extract semantic information from text
text = """
OpenAI released GPT-4 in March 2023, which significantly improved 
reasoning capabilities over GPT-3.5. The model was trained using 
reinforcement learning from human feedback (RLHF).
"""

# One-line semantic extraction
result = core.extract(text)

print(result.entities)     # [Entity(name="OpenAI", type="ORGANIZATION"), ...]
print(result.relations)    # [Relation(subject="OpenAI", predicate="released", object="GPT-4"), ...]
print(result.schema)       # Auto-generated Pydantic schema
print(result.metadata)     # Enriched contextual information
```

---

## 🧩 Core Features

### 🧠 Semantic Extraction Engine

Advanced NLP pipeline that extracts meaningful structure from unstructured data:

```python
from semanticore.extract import EntityExtractor, RelationExtractor, TopicClassifier

# Named Entity Recognition with custom models
extractor = EntityExtractor(
    model="en_core_web_trf",  # spaCy model
    custom_labels=["MALWARE", "THREAT_ACTOR", "VULNERABILITY"]
)

entities = extractor.extract("APT29 used FrostBite malware against critical infrastructure")

# Relation and Triple Extraction
rel_extractor = RelationExtractor(llm_provider="openai")
relations = rel_extractor.extract_relations(text, entities)

# Topic Classification and Categorization
classifier = TopicClassifier()
topics = classifier.classify(text, categories=["cybersecurity", "technology", "politics"])
```

### 🧱 Dynamic Schema Generation

Automatically generate type-safe schemas from extracted data:

```python
from semanticore.schema import SchemaGenerator, validate_data

# Generate Pydantic models from extracted entities
generator = SchemaGenerator()
schema = generator.from_entities(entities)

# Export to various formats
schema.to_pydantic()    # Python Pydantic model
schema.to_json_schema() # JSON Schema
schema.to_yaml()        # YAML Schema
schema.to_typescript()  # TypeScript interfaces

# Validate new data against generated schema
is_valid = validate_data(new_data, schema)
```

### 🔌 Universal Connectors

Seamlessly connect to any data source:

```python
from semanticore.connectors import FileConnector, WebConnector, APIConnector

# File processing (PDF, DOCX, CSV, JSON, Markdown)
file_conn = FileConnector()
documents = file_conn.load("./documents/*.pdf")
semantic_docs = core.process_documents(documents)

# Web scraping and RSS feeds
web_conn = WebConnector()
pages = web_conn.scrape_urls(["https://example.com/news"])
web_semantics = core.extract_from_web(pages)

# REST API integration
api_conn = APIConnector(base_url="https://api.example.com")
api_data = api_conn.fetch("/endpoints")
structured_data = core.structure_api_response(api_data)
```

### 🧪 Validation & Quality Assurance

Ensure data quality and consistency across your pipeline:

```python
from semanticore.validation import SchemaValidator, ConsistencyChecker, QualityMetrics

# Schema validation
validator = SchemaValidator(schema)
validation_result = validator.validate(data)

if not validation_result.is_valid:
    print(f"Validation errors: {validation_result.errors}")

# Consistency checking across multiple extractions
checker = ConsistencyChecker()
consistency_score = checker.check_consistency([result1, result2, result3])

# Quality metrics and confidence scoring
metrics = QualityMetrics()
quality_report = metrics.assess(extraction_result)
print(f"Extraction confidence: {quality_report.confidence}")
```

### 📐 Intelligent Chunking & Embedding

RAG-optimized document processing with semantic awareness:

```python
from semanticore.vectorizer import SemanticChunker, EmbeddingEngine

# Semantic-aware chunking
chunker = SemanticChunker(
    chunk_size=512,
    overlap=50,
    respect_boundaries=True,  # Don't split entities/relations
    add_metadata=True
)

chunks = chunker.chunk_document(document, semantic_info=result)

# Multi-modal embedding support
embedder = EmbeddingEngine(
    provider="sentence-transformers",  # or "openai", "huggingface"
    model="all-MiniLM-L6-v2"
)

embedded_chunks = embedder.embed_chunks(chunks)

# Direct vector database integration
from semanticore.vector_stores import FAISSStore, PineconeStore

store = FAISSStore()
store.add_embeddings(embedded_chunks)
```

### 📚 Knowledge Graph Export

Transform extracted semantics into graph databases:

```python
from semanticore.kg import Neo4jExporter, RDFExporter, KuzuExporter

# Neo4j export with Cypher generation
neo4j_exporter = Neo4jExporter(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)

# Create nodes and relationships
neo4j_exporter.export_entities(entities)
neo4j_exporter.export_relations(relations)

# RDF triple export
rdf_exporter = RDFExporter(format="turtle")
triples = rdf_exporter.to_triples(entities, relations)

# Query the generated knowledge graph
from semanticore.kg.query import GraphQuerier

querier = GraphQuerier(neo4j_exporter)
results = querier.cypher("MATCH (n:ORGANIZATION)-[r:RELEASED]->(m:PRODUCT) RETURN n, r, m")
```

### 📡 Semantic Routing

Intelligently route queries and tasks to appropriate handlers:

```python
from semanticore.routing import SemanticRouter, IntentClassifier

# Set up routing rules
router = SemanticRouter()

# Intent-based routing
router.add_intent_route("question_answering", qa_agent)
router.add_intent_route("data_extraction", extraction_pipeline)
router.add_intent_route("summarization", summary_agent)

# Keyword and pattern-based routing
router.add_keyword_route(["threat", "malware", "vulnerability"], security_agent)
router.add_pattern_route(r"CVE-\d{4}-\d+", vulnerability_lookup)

# LLM-powered semantic routing
router.add_semantic_route(
    description="Handle complex analytical queries about financial data",
    handler=financial_analysis_agent,
    examples=["What's the trend in quarterly revenue?", "Analyze the risk factors"]
)

# Route incoming requests
query = "What are the latest cybersecurity threats targeting healthcare?"
handler = router.route(query)
response = handler.process(query)
```

---

## 🎯 Use Cases & Examples

### 🔐 Cybersecurity Threat Intelligence

```python
from semanticore.domains.cyber import ThreatIntelExtractor

# Specialized cybersecurity extraction
threat_extractor = ThreatIntelExtractor()
threat_report = """
APT29 (Cozy Bear) launched a sophisticated spear-phishing campaign 
targeting US government agencies using a previously unknown malware 
variant called FrostBite. The attack exploited CVE-2024-1234 in 
Microsoft Exchange servers.
"""

intel = threat_extractor.extract(threat_report)
print(intel.threat_actors)    # ["APT29", "Cozy Bear"]
print(intel.malware)          # ["FrostBite"]
print(intel.vulnerabilities)  # ["CVE-2024-1234"]
print(intel.attack_patterns)  # ["spear-phishing", "server exploitation"]

# Export to STIX format for threat intelligence platforms
stix_bundle = intel.to_stix()
```

### 🧬 Biomedical Research Assistant

```python
from semanticore.domains.biomedical import BiomedicalExtractor

bio_extractor = BiomedicalExtractor()
research_text = """
The study investigated the efficacy of remdesivir in treating COVID-19 
patients. Results showed a 31% reduction in recovery time compared to 
placebo (p<0.001). Side effects included nausea in 12% of patients.
"""

bio_data = bio_extractor.extract(research_text)
print(bio_data.drugs)         # ["remdesivir"]
print(bio_data.conditions)    # ["COVID-19"]
print(bio_data.outcomes)      # ["31% reduction in recovery time"]
print(bio_data.side_effects)  # ["nausea"]

# Generate structured clinical data
clinical_schema = bio_data.to_clinical_schema()
```

### 📊 Financial Document Analysis

```python
from semanticore.domains.finance import FinancialExtractor

fin_extractor = FinancialExtractor()
earnings_report = """
Q4 2024 revenue increased 15% YoY to $2.3B, driven by strong performance 
in the cloud computing segment. Operating margin improved to 23.5% from 
21.2% in the prior year. The company announced a $1B share buyback program.
"""

financial_data = fin_extractor.extract(earnings_report)
print(financial_data.metrics)     # {"revenue": "$2.3B", "margin": "23.5%"}
print(financial_data.periods)     # ["Q4 2024"]
print(financial_data.events)      # ["$1B share buyback program"]

# Export to financial analysis tools
financial_json = financial_data.to_standardized_json()
```

---

## 🔧 Advanced Configuration

### Custom Model Integration

```python
from semanticore.models import CustomLLMProvider

# Integrate your own models
class MyCustomLLM(CustomLLMProvider):
    def __init__(self, model_path):
        self.model = load_model(model_path)
    
    def extract_entities(self, text):
        return self.model.predict(text)

# Use custom model in SemantiCore
core = SemantiCore(llm_provider=MyCustomLLM("./my_model"))
```

### Pipeline Customization

```python
from semanticore.pipeline import Pipeline, Step

# Build custom processing pipeline
pipeline = Pipeline([
    Step("preprocess", text_cleaner),
    Step("extract_entities", entity_extractor),
    Step("extract_relations", relation_extractor),
    Step("enrich_metadata", metadata_enricher),
    Step("validate", schema_validator),
    Step("export", knowledge_graph_exporter)
])

# Process data through pipeline
results = pipeline.run(input_data)
```

### Configuration Management

```python
# semanticore.yaml
extractors:
  entity:
    model: "en_core_web_trf"
    confidence_threshold: 0.8
  relation:
    llm_provider: "openai"
    model: "gpt-4"
    
schema:
  auto_generate: true
  validation_level: "strict"
  
export:
  formats: ["json", "rdf", "cypher"]
  knowledge_graph:
    provider: "neo4j"
    batch_size: 1000

# Load configuration
from semanticore.config import load_config
config = load_config("semanticore.yaml")
core = SemantiCore(config=config)
```

---

## 🏗️ Architecture

SemantiCore follows a modular, extensible architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    SemantiCore Engine                        │
├─────────────────────────────────────────────────────────────┤
│  Connectors    │  Extractors   │  Schema      │  Exporters   │
│  ┌──────────┐  │  ┌─────────┐  │  ┌────────┐  │  ┌────────┐  │
│  │   File   │  │  │   NER   │  │  │ Pydantic│  │  │ Neo4j  │  │
│  │   Web    │  │  │ Relations│  │  │  JSON   │  │  │  RDF   │  │
│  │   API    │  │  │  Topics  │  │  │  YAML   │  │  │ Vector │  │
│  │   DB     │  │  │   LLM   │  │  │   TS    │  │  │  DB    │  │
│  └──────────┘  │  └─────────┘  │  └────────┘  │  └────────┘  │
├─────────────────────────────────────────────────────────────┤
│              Validation & Quality Assurance                 │
├─────────────────────────────────────────────────────────────┤
│                  Semantic Routing                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Requirements

- **Python**: 3.8+
- **Core Dependencies**: spaCy, transformers, pydantic, networkx
- **Optional Dependencies**:
  - **LLM Providers**: openai, anthropic, huggingface-hub
  - **Vector Databases**: faiss-cpu, pinecone-client, weaviate-client
  - **Graph Databases**: neo4j, rdflib, kuzudb
  - **Document Processing**: PyMuPDF, python-docx, openpyxl

---

## 🛣️ Roadmap

### 🚀 Version 1.0 (Current)
- ✅ Core semantic extraction engine
- ✅ Schema generation and validation
- ✅ Basic connectors (file, web, API)
- ✅ Neo4j and RDF export
- ✅ Vector database integration

### 🔮 Version 1.1 (Q3 2025)
- 🔄 **Web-based visual schema editor**
- 🔄 **Real-time streaming support** (Kafka, MQTT, WebSockets)
- 🔄 **Advanced semantic routing** with learning capabilities
- 🔄 **Multi-modal support** (images, audio, video)

### 🔮 Version 1.2 (Q4 2025)
- ⏳ **Domain-specific modules** (Legal, Healthcare, Finance)
- ⏳ **Graph reasoning engine** with inference capabilities
- ⏳ **Distributed processing** support
- ⏳ **Model fine-tuning** utilities

### 🔮 Version 2.0 (2026)
- ⏳ **Custom DSL** for semantic pipeline definition
- ⏳ **AutoML** for extraction model optimization
- ⏳ **Federated learning** across distributed deployments
- ⏳ **Enterprise management** console

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Report Issues
Found a bug or have a feature request? [Open an issue](https://github.com/yourusername/semanticore/issues) on GitHub.

### 💻 Contribute Code
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### 📖 Improve Documentation
Help us improve our documentation by:
- Fixing typos and clarifying explanations
- Adding new examples and use cases
- Creating tutorials and guides
- Translating documentation

### 🧪 Testing
Help us maintain quality by:
- Writing unit tests for new features
- Testing on different platforms and Python versions
- Performance testing and optimization
- Integration testing with external services

---

## 📚 Documentation

- **📖 [Full Documentation](https://semanticore.readthedocs.io/)**
- **🚀 [Quick Start Guide](https://semanticore.readthedocs.io/quickstart/)**
- **📋 [API Reference](https://semanticore.readthedocs.io/api/)**
- **💡 [Examples & Tutorials](https://semanticore.readthedocs.io/examples/)**
- **🔧 [Configuration Guide](https://semanticore.readthedocs.io/configuration/)**

---

## 🏆 Community & Support

- **💬 [Discord Community](https://discord.gg/semanticore)** - Chat with users and developers
- **📧 [Mailing List](https://groups.google.com/g/semanticore)** - Stay updated with announcements
- **🐦 [Twitter](https://twitter.com/semanticore)** - Follow us for updates
- **📺 [YouTube Channel](https://youtube.com/c/semanticore)** - Tutorials and demos
- **❓ [Stack Overflow](https://stackoverflow.com/questions/tagged/semanticore)** - Get help with specific issues

---

## 📄 License

SemantiCore is released under the **MIT License**. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 SemantiCore Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

SemantiCore is built on the shoulders of giants. We thank the communities behind:

- **🤗 Hugging Face** - For democratizing NLP and ML
- **🌶️ spaCy** - For industrial-strength NLP
- **🔗 Neo4j** - For graph database excellence
- **🐍 Python** - For being an amazing ecosystem
- **🧠 OpenAI & Anthropic** - For advancing AI capabilities

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/semanticore?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/semanticore?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/semanticore)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/semanticore)
![PyPI downloads](https://img.shields.io/pypi/dm/semanticore)

---

**Ready to transform your unstructured data into intelligent, semantic knowledge?**

```bash
pip install semanticore
```

**[Get Started Now →](https://semanticore.readthedocs.io/quickstart/)**
