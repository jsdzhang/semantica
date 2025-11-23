# Triple Store Module

Store and query RDF triples with support for SPARQL queries and semantic reasoning using industry-standard triple stores.

## Overview

- **RDF Storage**: Store subject-predicate-object triples
- **SPARQL Queries**: W3C-compliant query language
- **Reasoning**: RDFS and OWL reasoning
- **Multiple Backends**: RDFLib, Jena, Virtuoso, GraphDB
- **Federation**: Query across multiple triple stores

---

## Algorithms Used

### Query Algorithms
- **SPARQL Query Optimization**: Join reordering with selectivity estimation
- **Triple Pattern Matching**: Index-based lookup with B+ trees
- **Graph Pattern Matching**: Subgraph isomorphism
- **Query Planning**: Cost-based optimization

### Indexing
- **SPO Index**: Subject-Predicate-Object index
- **POS Index**: Predicate-Object-Subject index
- **OSP Index**: Object-Subject-Predicate index
- **Six-Index Scheme**: All permutations for optimal query performance

---

## Main Classes

### TripleStore


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `add_triple(subject, predicate, object)` | Add single triple | Index insertion |
| `add_triples(triples)` | Batch add triples | Bulk index insertion |
| `query(sparql_query)` | Execute SPARQL query | Query optimization + execution |
| `delete(pattern)` | Delete matching triples | Pattern matching + deletion |
| `serialize(format)` | Serialize to RDF format | Format-specific serialization |

**Example:**

```python
from semantica.triple_store import TripleStore

store = TripleStore(backend="rdflib")

# Add triples
store.add_triple(
    subject="http://example.org/AppleInc",
    predicate="http://example.org/foundedBy",
    object="http://example.org/SteveJobs"
)

# SPARQL query
results = store.query("""
    SELECT ?company ?founder WHERE {
        ?company <http://example.org/foundedBy> ?founder .
    }
""")

for row in results:
    print(f"{row['company']} founded by {row['founder']}")
```

---

### SPARQLQueryEngine


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `execute(query)` | Execute SPARQL query | Parse + optimize + execute |
| `parse_query(sparql)` | Parse SPARQL syntax | SPARQL parser |
| `optimize_query(query)` | Optimize query plan | Join reordering |
| `explain_query(query)` | Explain query plan | Query plan visualization |

**SPARQL Query Types:**
- **SELECT**: Retrieve variable bindings
- **CONSTRUCT**: Build RDF graph
- **ASK**: Boolean query
- **DESCRIBE**: Describe resources

---

## Configuration

```yaml
# config.yaml - Triple Store Configuration

triple_store:
  backend: rdflib  # rdflib, jena, virtuoso, graphdb
  
  indexing:
    schemes: [SPO, POS, OSP]  # Index permutations
    
  query:
    optimize: true
    timeout: 30  # seconds
```

---

## See Also

- [Knowledge Graph Module](kg.md)
- [Ontology Module](ontology.md)
