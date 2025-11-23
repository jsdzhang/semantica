# Ontology Module

> **Generate W3C-compliant OWL ontologies from unstructured content using a 6-stage LLM pipeline.**

---

## 🎯 Overview

<div class="grid cards" markdown>

-   :material-auto-fix:{ .lg .middle } **Automatic Generation**

    ---

    LLM-based ontology creation from text and knowledge graphs

-   :material-file-tree:{ .lg .middle } **OWL/RDF Support**

    ---

    W3C-compliant ontology formats with Turtle, RDF/XML, JSON-LD

-   :material-check-circle:{ .lg .middle } **Validation**

    ---

    HermiT and Pellet reasoner integration for consistency checking

-   :material-family-tree:{ .lg .middle } **Class Hierarchy**

    ---

    Automatic taxonomy generation with multiple inheritance

-   :material-link:{ .lg .middle } **Property Definition**

    ---

    Object and data properties with domain/range inference

-   :material-brain:{ .lg .middle } **6-Stage Pipeline**

    ---

    Semantic parsing → Definitions → Types → Hierarchy → TTL → Validation

</div>

!!! info "6-Stage Ontology Generation Pipeline"
    ```mermaid
    graph LR
        A[1. Semantic Network<br/>Parsing] --> B[2. YAML to<br/>Definition]
        B --> C[3. Definition<br/>to Types]
        C --> D[4. Hierarchy<br/>Generation]
        D --> E[5. TTL<br/>Generation]
        E --> F[6. Symbolic<br/>Validation]
        
        style A fill:#e3f2fd
        style F fill:#c8e6c9
    ```

---

## ⚙️ Algorithms Used

### 6-Stage Ontology Generation Pipeline

**Stage 1: Semantic Network Parsing**
- Extract domain concepts from text
- Identify key entities and relationships
- Build initial concept graph

**Stage 2: YAML-to-Definition**
- Transform semantic network to class definitions
- Define class hierarchies and properties
- Generate human-readable descriptions

**Stage 3: Definition-to-Types**
- Map to OWL types (Class, ObjectProperty, DataProperty)
- Define domains and ranges
- Specify cardinality constraints

**Stage 4: Hierarchy Generation**
- Build taxonomic structures (is-a relationships)
- Identify parent-child relationships
- Create multiple inheritance where appropriate

**Stage 5: TTL Generation**
- Generate OWL/Turtle syntax
- Add namespace declarations
- Format according to W3C standards

**Stage 6: Symbolic Validation**
- HermiT/Pellet reasoning for consistency
- Detect logical contradictions
- Validate class satisfiability

### Reasoning Algorithms
- **HermiT**: Hypertableau reasoning algorithm
- **Pellet**: Tableau-based DL reasoner
- **Consistency Checking**: Detect unsatisfiable classes
- **Classification**: Compute inferred class hierarchy

---

## Main Classes

### OntologyGenerator


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `generate(source)` | Generate ontology | 6-stage pipeline |
| `generate_from_graph(kg)` | Generate from knowledge graph | Graph analysis + LLM generation |
| `generate_from_text(text)` | Generate from text | Text analysis + concept extraction |
| `validate(ontology)` | Validate ontology | Reasoner-based validation |
| `infer_hierarchy(classes)` | Infer class hierarchy | Hierarchical clustering + LLM |

**Example:**

```python
from semantica.ontology import OntologyGenerator

generator = OntologyGenerator(
    llm_provider="openai",
    llm_model="gpt-4",
    validation_reasoner="hermit"  # hermit, pellet
)

# Generate from knowledge graph
ontology = generator.generate_from_graph(kg)

# Validate
is_valid, errors = generator.validate(ontology)
print(f"Valid: {is_valid}, Errors: {len(errors)}")

# Save
ontology.save("ontology.owl", format="owl")
```

---

### OntologyValidator


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `validate(ontology)` | Full validation | Consistency + satisfiability checks |
| `check_consistency()` | Check logical consistency | Tableau reasoning |
| `check_satisfiability(class_name)` | Check class satisfiability | Subsumption testing |
| `find_inconsistencies()` | Find logical errors | Reasoner-based detection |
| `explain_inconsistency(class_name)` | Explain why class is unsatisfiable | Axiom tracing |

**Validation Checks:**
- **Consistency**: No logical contradictions
- **Satisfiability**: All classes can have instances
- **Coherence**: No unsatisfiable classes
- **Completeness**: All required axioms present

**Example:**

```python
from semantica.ontology import OntologyValidator

validator = OntologyValidator(reasoner="hermit")

# Validate ontology
result = validator.validate(ontology)

if not result.is_valid:
    print("Inconsistencies found:")
    for error in result.errors:
        print(f"  - {error.class_name}: {error.message}")
        explanation = validator.explain_inconsistency(error.class_name)
        print(f"    Reason: {explanation}")
```

---

### OWLGenerator


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `generate_owl(ontology)` | Generate OWL file | OWL/XML or Turtle serialization |
| `generate_classes(classes)` | Generate class definitions | OWL Class axioms |
| `generate_properties(properties)` | Generate properties | ObjectProperty/DataProperty axioms |
| `generate_individuals(individuals)` | Generate instances | Individual assertions |
| `add_axiom(axiom)` | Add OWL axiom | Axiom insertion |

**OWL Constructs:**
- **Classes**: `owl:Class`
- **Object Properties**: `owl:ObjectProperty`
- **Data Properties**: `owl:DatatypeProperty`
- **Individuals**: `owl:NamedIndividual`
- **Restrictions**: `owl:Restriction`, `owl:someValuesFrom`, `owl:allValuesFrom`

**Example:**

```python
from semantica.ontology import OWLGenerator

generator = OWLGenerator(
    base_uri="http://example.org/ontology#",
    format="turtle"  # turtle, owl-xml, rdf-xml
)

# Generate OWL
owl_content = generator.generate_owl(ontology)

# Save
with open("ontology.ttl", "w") as f:
    f.write(owl_content)
```

---

### PropertyGenerator


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `generate_properties(relationships)` | Generate all properties | Relationship analysis |
| `infer_domain_range(property)` | Infer domain and range | Type inference from usage |
| `generate_object_property(name, domain, range)` | Create object property | OWL ObjectProperty axiom |
| `generate_data_property(name, domain, datatype)` | Create data property | OWL DatatypeProperty axiom |

**Property Types:**
- **Object Properties**: Relate individuals to individuals
- **Data Properties**: Relate individuals to data values
- **Annotation Properties**: Metadata properties

**Example:**

```python
from semantica.ontology import PropertyGenerator

generator = PropertyGenerator()

# Generate properties from relationships
properties = generator.generate_properties(relationships)

# Create specific property
founder_property = generator.generate_object_property(
    name="foundedBy",
    domain="Organization",
    range="Person"
)
```

---

### ClassInferrer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `infer_classes(entities)` | Infer class definitions | Entity type clustering |
| `build_hierarchy(classes)` | Build class hierarchy | Hierarchical clustering + LLM |
| `identify_disjoint_classes(classes)` | Find disjoint classes | Logical analysis |
| `generate_restrictions(class_name)` | Generate class restrictions | Property analysis |

**Hierarchy Building:**
- **Bottom-up**: Start with specific classes, generalize
- **Top-down**: Start with general classes, specialize
- **Hybrid**: Combine both approaches

---

## Configuration

```yaml
# config.yaml - Ontology Configuration

ontology:
  generation:
    llm_provider: openai
    llm_model: gpt-4
    temperature: 0.1
    stages:
      - semantic_network_parsing
      - yaml_to_definition
      - definition_to_types
      - hierarchy_generation
      - ttl_generation
      - symbolic_validation
      
  validation:
    reasoner: hermit  # hermit, pellet
    check_consistency: true
    check_satisfiability: true
    explain_errors: true
    
  owl:
    base_uri: "http://example.org/ontology#"
    format: turtle  # turtle, owl-xml, rdf-xml
    include_annotations: true
    include_individuals: true
```

---

## OWL Example

```turtle
@prefix : <http://example.org/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Classes
:Person rdf:type owl:Class .
:Organization rdf:type owl:Class .
:Company rdf:type owl:Class ;
    rdfs:subClassOf :Organization .

# Object Properties
:foundedBy rdf:type owl:ObjectProperty ;
    rdfs:domain :Organization ;
    rdfs:range :Person .

# Data Properties
:foundedYear rdf:type owl:DatatypeProperty ;
    rdfs:domain :Organization ;
    rdfs:range xsd:gYear .

# Individuals
:AppleInc rdf:type :Company ;
    :foundedBy :SteveJobs ;
    :foundedYear "1976"^^xsd:gYear .
```

---

## See Also

- [Knowledge Graph Module](kg.md) - Build knowledge graphs
- [Triple Store Module](triple_store.md) - Store RDF triples
- [Reasoning Module](reasoning.md) - Logical reasoning
