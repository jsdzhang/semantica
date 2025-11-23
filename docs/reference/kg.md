# Knowledge Graph Module

> **Build, analyze, and manage knowledge graphs with advanced temporal support and graph analytics.**

---

## 🎯 Overview

<div class="grid cards" markdown>

-   :material-graph-outline:{ .lg .middle } **Graph Building**

    ---

    Construct knowledge graphs from entities and relationships with automatic entity resolution

-   :material-merge:{ .lg .middle } **Entity Resolution**

    ---

    Merge duplicate entities using fuzzy and semantic matching algorithms

-   :material-alert-circle:{ .lg .middle } **Conflict Detection**

    ---

    Handle contradictory information with multiple resolution strategies

-   :material-clock-outline:{ .lg .middle } **Temporal Graphs**

    ---

    Track changes over time with versioning and temporal queries

-   :material-chart-line:{ .lg .middle } **Graph Analytics**

    ---

    PageRank, centrality, community detection, and path finding

-   :material-database-search:{ .lg .middle } **Graph Querying**

    ---

    Cypher-like query language with pattern matching

</div>

---

## ⚙️ Algorithms Used

### Graph Construction Algorithms
- **Incremental Building**: Batch processing for large graphs with memory optimization
- **Entity Merging**: Property aggregation, metadata merging, provenance tracking
- **Relationship Deduplication**: Similarity-based relationship merging

### Entity Resolution Algorithms
- **Fuzzy Matching**: Levenshtein distance, Jaro-Winkler similarity for string matching
- **Semantic Matching**: Embedding-based similarity (cosine similarity on entity embeddings)
- **Threshold-based Grouping**: Configurable similarity thresholds for entity clustering
- **Conflict Resolution Strategies**: Voting, credibility-weighted, most-recent, highest-confidence

### Graph Analysis Algorithms
- **Degree Centrality**: Normalized degree calculation: `degree / (n-1)`
- **Betweenness Centrality**: Shortest path counting (BFS-based), normalized by `(n-1)*(n-2)/2`
- **Closeness Centrality**: Average shortest path length calculation
- **PageRank**: Iterative power method with damping factor (default: 0.85)
- **Eigenvector Centrality**: Power iteration method for influence calculation

### Community Detection Algorithms
- **Louvain Method**: Modularity optimization with greedy agglomeration
- **Leiden Algorithm**: Improved Louvain with guaranteed well-connected communities
- **Label Propagation**: Fast community detection via label spreading
- **Greedy Modularity**: Hierarchical community structure detection

### Temporal Graph Algorithms
- **Time-Point Queries**: Temporal filtering using valid_from/valid_until comparison
- **Time-Range Queries**: Interval overlap detection, union/intersection aggregation
- **Temporal Patterns**: Sequential pattern mining, temporal motif detection
- **Version Management**: Snapshot creation, diff calculation, rollback support

### Graph Validation Algorithms
- **Schema Validation**: Type checking against ontology definitions
- **Consistency Checking**: Logical constraint validation, relationship type validation
- **Completeness Validation**: Required property checking, orphaned entity detection
- **Density Calculation**: `E / (n*(n-1)/2)` for undirected graphs

---

## Main Classes

### GraphBuilder


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `build(entities, relationships)` | Build knowledge graph | Incremental graph construction with entity resolution |
| `add_node(entity)` | Add entity node | Node creation with property validation |
| `add_edge(relationship)` | Add relationship edge | Edge creation with type validation |
| `merge_graphs(graphs)` | Merge multiple graphs | Graph union with entity resolution |
| `resolve_entities(threshold)` | Resolve duplicate entities | Fuzzy + semantic matching |
| `detect_conflicts()` | Detect conflicting information | Multi-source conflict detection |
| `to_neo4j(uri, username, password)` | Export to Neo4j | Cypher query generation |
| `to_rdf(filename, format)` | Export to RDF | RDF serialization (Turtle, N-Triples) |

**Example:**

```python
from semantica.kg import GraphBuilder

builder = GraphBuilder(
    merge_entities=True,
    entity_resolution_strategy="fuzzy",  # "fuzzy", "semantic", "hybrid"
    similarity_threshold=0.85,
    resolve_conflicts=True,
    enable_temporal=True,
    temporal_granularity="day"
)

kg = builder.build(entities, relationships)

# Export
kg.to_neo4j("bolt://localhost:7687", "neo4j", "password")
kg.to_rdf("output.ttl", format="turtle")

print(f"Nodes: {kg.node_count}, Edges: {kg.edge_count}")
```

---

### EntityResolver


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `resolve(graph)` | Resolve all entities | Clustering + merging pipeline |
| `find_duplicates(entities)` | Find duplicate entities | Similarity-based grouping |
| `merge_entities(entity_group)` | Merge entity group | Property aggregation with conflict resolution |
| `calculate_similarity(e1, e2)` | Calculate entity similarity | Weighted combination: string (0.4) + semantic (0.6) |
| `cluster_entities(entities)` | Cluster similar entities | Agglomerative clustering |

**Similarity Calculation:**
```
similarity = 0.4 * string_similarity(e1.name, e2.name) + 
             0.6 * cosine_similarity(embedding(e1), embedding(e2))
```

**Example:**

```python
from semantica.kg import EntityResolver

resolver = EntityResolver(
    similarity_threshold=0.85,
    merge_strategy="highest_confidence",  # "voting", "most_recent", "highest_confidence"
    use_embeddings=True
)

resolved_kg = resolver.resolve(kg)
print(f"Merged {resolver.stats['duplicates_found']} duplicate entities")
```

---

### GraphAnalyzer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `compute_metrics()` | Compute graph metrics | Density, diameter, clustering coefficient |
| `analyze_structure()` | Analyze graph structure | Component analysis, connectivity |
| `find_patterns(pattern_type)` | Find graph patterns | Subgraph matching, motif detection |
| `detect_anomalies()` | Detect graph anomalies | Statistical outlier detection |
| `calculate_density()` | Calculate graph density | `E / (n*(n-1)/2)` |

**Graph Metrics:**
- **Density**: Ratio of actual edges to possible edges
- **Diameter**: Longest shortest path in the graph
- **Average Degree**: Mean number of connections per node
- **Clustering Coefficient**: Measure of local clustering
- **Connected Components**: Number of disconnected subgraphs

**Example:**

```python
from semantica.kg import GraphAnalyzer

analyzer = GraphAnalyzer(kg)

metrics = analyzer.compute_metrics()
print(f"Density: {metrics['density']:.3f}")
print(f"Diameter: {metrics['diameter']}")
print(f"Avg degree: {metrics['avg_degree']:.2f}")
print(f"Clustering: {metrics['clustering']:.3f}")
```

---

### CentralityCalculator


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `pagerank(damping=0.85)` | Calculate PageRank | Power iteration method |
| `betweenness_centrality()` | Calculate betweenness | Brandes' algorithm (BFS-based) |
| `closeness_centrality()` | Calculate closeness | Average shortest path length |
| `eigenvector_centrality()` | Calculate eigenvector centrality | Power iteration on adjacency matrix |
| `degree_centrality()` | Calculate degree centrality | Normalized degree: `degree / (n-1)` |

**PageRank Formula:**
```
PR(v) = (1-d)/N + d * Σ(PR(u)/L(u))
where d = damping factor (0.85), N = total nodes, L(u) = outlinks from u
```

**Example:**

```python
from semantica.kg import CentralityCalculator

centrality = CentralityCalculator(kg)

# Calculate different centrality measures
pagerank = centrality.pagerank(damping=0.85)
betweenness = centrality.betweenness_centrality()
closeness = centrality.closeness_centrality()

# Find most influential entities
top_entities = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

for entity, score in top_entities:
    print(f"{entity}: {score:.3f}")
```

---

### CommunityDetector


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `detect(algorithm)` | Detect communities | Specified algorithm (louvain/leiden/label_propagation) |
| `louvain()` | Louvain method | Modularity optimization with greedy agglomeration |
| `leiden()` | Leiden algorithm | Improved Louvain with quality guarantees |
| `label_propagation()` | Label propagation | Fast community detection via label spreading |
| `calculate_modularity(communities)` | Calculate modularity | Q = Σ(eii - ai²) |

**Modularity Formula:**
```
Q = 1/(2m) * Σ[Aij - (ki*kj)/(2m)] * δ(ci, cj)
where m = total edges, ki = degree of node i, ci = community of node i
```

**Example:**

```python
from semantica.kg import CommunityDetector

detector = CommunityDetector(kg)

# Detect communities using Louvain
communities = detector.detect(algorithm="louvain")

print(f"Found {len(communities)} communities")
for i, community in enumerate(communities[:5], 1):
    print(f"Community {i}: {len(community)} entities")
    print(f"  Sample: {list(community)[:3]}")
```

---

### TemporalGraphQuery


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `query_at_time(query, timestamp)` | Query graph at specific time | Temporal filtering with valid_from/valid_until |
| `query_time_range(query, start, end)` | Query over time range | Interval overlap detection |
| `find_temporal_paths(source, target, time_range)` | Find time-aware paths | Temporal Dijkstra's algorithm |
| `analyze_evolution(start, end, interval)` | Analyze graph evolution | Time-series analysis of graph metrics |
| `detect_temporal_patterns(pattern_type)` | Detect temporal patterns | Sequential pattern mining |

**Temporal Filtering:**
```
valid_at(edge, t) = (edge.valid_from <= t) AND (t <= edge.valid_until OR edge.valid_until IS NULL)
```

**Example:**

```python
from semantica.kg import TemporalGraphQuery
from datetime import datetime

temporal_query = TemporalGraphQuery(
    enable_temporal_reasoning=True,
    temporal_granularity="day"
)

# Query at specific time
results = temporal_query.query_at_time(
    graph=kg,
    query="Who founded Apple Inc.?",
    at_time="2014-06-15"
)

# Query time range
evolution = temporal_query.analyze_evolution(
    graph=kg,
    start_time="2000-01-01",
    end_time="2024-12-31",
    metrics=["node_count", "edge_count", "density"]
)
```

---

### ConflictDetector


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `detect_conflicts(graph)` | Detect all conflicts | Multi-source comparison |
| `resolve_conflict(conflict, strategy)` | Resolve single conflict | Strategy-based resolution |
| `validate_consistency(graph)` | Validate logical consistency | Constraint checking |
| `find_contradictions(entity)` | Find contradictory properties | Property value comparison |

**Conflict Resolution Strategies:**
- **Voting**: Majority value wins
- **Credibility Weighted**: Weight by source credibility scores
- **Most Recent**: Use most recent information
- **Highest Confidence**: Use value with highest confidence score
- **First Seen**: Use first encountered value

**Example:**

```python
from semantica.kg import ConflictDetector

detector = ConflictDetector(
    default_strategy="voting",
    track_provenance=True
)

conflicts = detector.detect_conflicts(kg)

for conflict in conflicts:
    print(f"Conflict in {conflict.entity}: {conflict.property}")
    print(f"  Values: {conflict.values}")
    
    resolved = detector.resolve_conflict(conflict, strategy="voting")
    print(f"  Resolved to: {resolved.value}")
```

---

### ProvenanceTracker


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `track(entity, source, timestamp)` | Track entity provenance | Metadata attachment |
| `get_provenance(entity)` | Get entity provenance | Provenance retrieval |
| `trace_lineage(entity)` | Trace entity lineage | Backward tracing through transformations |
| `validate_provenance(entity)` | Validate provenance chain | Chain integrity checking |

---

## Configuration

```yaml
# config.yaml - Knowledge Graph Configuration

kg:
  graph_builder:
    merge_entities: true
    entity_resolution_strategy: fuzzy  # fuzzy, semantic, hybrid
    similarity_threshold: 0.85
    resolve_conflicts: true
    enable_temporal: true
    temporal_granularity: day  # second, minute, hour, day, week, month, year
    
  entity_resolution:
    use_embeddings: true
    fuzzy_threshold: 0.80
    semantic_threshold: 0.85
    merge_strategy: highest_confidence
    
  conflict_resolution:
    default_strategy: voting  # voting, credibility_weighted, most_recent, highest_confidence
    track_provenance: true
    
  graph_analytics:
    calculate_centrality: true
    detect_communities: true
    community_algorithm: louvain  # louvain, leiden, label_propagation
    
  temporal:
    enable_versioning: true
    snapshot_interval: 30  # days
    track_history: true
```

---

## Performance Characteristics

### Graph Construction
- **Incremental Building**: Efficient for large graphs
- **Batch Processing**: Optimized for bulk operations
- **Memory Management**: Streaming for very large graphs

### Entity Resolution
- **Fuzzy Matching**: O(n²) complexity, optimized with blocking
- **Semantic Matching**: O(n) with vector index
- **Hybrid**: Best of both approaches

### Graph Analytics
- **PageRank**: O(k*E) where k = iterations, E = edges
- **Betweenness**: O(V*E) for unweighted graphs
- **Community Detection**: O(E*log²V) for Louvain

---

## See Also

- [Semantic Extract Module](semantic_extract.md) - Extract entities and relationships
- [Vector Store Module](vector_store.md) - Store graph embeddings
- [Triple Store Module](triple_store.md) - RDF storage
- [Ontology Module](ontology.md) - Define graph schemas
