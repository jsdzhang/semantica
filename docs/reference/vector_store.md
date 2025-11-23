# Vector Store Module

> **Store and search vector embeddings with lightning-fast approximate nearest neighbor search.**

---

## 🎯 Overview

<div class="grid cards" markdown>

-   :material-database:{ .lg .middle } **Vector Storage**

    ---

    Efficient storage of high-dimensional vectors with multiple backend support

-   :material-magnify:{ .lg .middle } **Similarity Search**

    ---

    Fast ANN search with HNSW, IVF, and PQ algorithms

-   :material-merge:{ .lg .middle } **Hybrid Search**

    ---

    Combine vector search with keyword/metadata filtering using RRF

-   :material-cog:{ .lg .middle } **Index Management**

    ---

    Multiple index types optimized for different use cases

-   :material-flash:{ .lg .middle } **Batch Operations**

    ---

    Efficient bulk insert and search with parallel processing

-   :material-cloud:{ .lg .middle } **Multiple Backends**

    ---

    FAISS, Pinecone, Qdrant, Weaviate, Milvus support

</div>

!!! tip "Choosing the Right Index"
    - **Small datasets (<10K)**: Use Flat for exact search
    - **Medium (10K-1M)**: Use IVF or HNSW  
    - **Large (>1M)**: Use HNSW with GPU
    - **Memory constrained**: Use PQ for compression

---

## ⚙️ Algorithms Used

### Indexing Algorithms
- **Flat (Exact Search)**: Brute-force linear scan, O(n*d) complexity
- **IVF (Inverted File Index)**: Clustering-based search with k-means, O(√n*d) complexity
- **HNSW (Hierarchical Navigable Small World)**: Graph-based ANN, O(log n) search complexity
- **PQ (Product Quantization)**: Compression-based search, reduces memory footprint
- **LSH (Locality Sensitive Hashing)**: Hash-based approximate search

### Similarity Metrics
- **Cosine Similarity**: `cos(θ) = (A·B) / (||A|| * ||B||)`
- **Euclidean Distance**: `d = √(Σ(ai - bi)²)`
- **Dot Product**: `A·B = Σ(ai * bi)`
- **Manhattan Distance**: `d = Σ|ai - bi|`

### Hybrid Search Algorithms
- **RRF (Reciprocal Rank Fusion)**: `score = Σ(1/(k + rank_i))` where k=60
- **Weighted Combination**: `score = α*vector_score + (1-α)*keyword_score`
- **Cascade Filtering**: Vector search → metadata filtering → reranking

---

## Main Classes

### VectorStore


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `store(embeddings, documents, metadata)` | Store vectors with metadata | Batch insertion with index building |
| `search(query_vector, top_k, filters)` | Search similar vectors | ANN search with optional filtering |
| `delete(ids)` | Delete vectors by ID | Index update with tombstoning |
| `update(id, vector, metadata)` | Update vector/metadata | In-place update or delete+insert |
| `create_index(index_type, params)` | Create search index | Index-specific construction algorithm |
| `rebuild_index()` | Rebuild index from scratch | Full index reconstruction |

**Supported Backends:**

| Backend | Index Types | Best For |
|---------|-------------|----------|
| **FAISS** | Flat, IVF, HNSW, PQ | High performance, local deployment |
| **Pinecone** | Proprietary | Managed cloud service |
| **Qdrant** | HNSW | Production-ready, filtering support |
| **Weaviate** | HNSW | GraphQL API, hybrid search |
| **Milvus** | IVF, HNSW | Distributed, large-scale |

**Example:**

```python
from semantica.vector_store import VectorStore

# Initialize with FAISS backend
store = VectorStore(
    backend="faiss",
    index_type="HNSW",  # Flat, IVF, HNSW, PQ
    metric="cosine",  # cosine, euclidean, dot_product
    dimension=1536
)

# Store embeddings
store.store(
    embeddings=embeddings,
    documents=documents,
    metadata=[{"source": "doc1.pdf", "page": 1}, ...]
)

# Search
results = store.search(
    query_vector=query_embedding,
    top_k=10,
    filters={"source": "doc1.pdf"}
)

for result in results:
    print(f"Score: {result.score:.3f}, Doc: {result.document}")
```

---

### HybridSearch


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `search(query, top_k)` | Hybrid search | Vector + keyword search with RRF fusion |
| `vector_search(query_vector, top_k)` | Vector-only search | ANN search |
| `keyword_search(query_text, top_k)` | Keyword-only search | BM25 or TF-IDF |
| `combine_results(vector_results, keyword_results)` | Merge results | RRF or weighted combination |
| `rerank(results, query)` | Rerank results | Cross-encoder reranking |

**Reciprocal Rank Fusion (RRF):**
```
RRF_score(d) = Σ(1/(k + rank_i(d)))
where k = 60 (constant), rank_i(d) = rank of document d in result set i
```

**Example:**

```python
from semantica.vector_store import HybridSearch

hybrid = HybridSearch(
    vector_store=store,
    keyword_index=keyword_index,
    fusion_method="rrf",  # rrf, weighted, cascade
    vector_weight=0.7  # for weighted fusion
)

results = hybrid.search(
    query="machine learning applications",
    top_k=10
)
```

---

### VectorRetriever


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `retrieve(query, top_k)` | Retrieve relevant documents | Vector search + document fetching |
| `retrieve_batch(queries, top_k)` | Batch retrieval | Parallel vector search |
| `retrieve_with_context(query, context_size)` | Retrieve with context | Sliding window context expansion |
| `filter_by_metadata(results, filters)` | Filter by metadata | Post-search filtering |

---

## Index Types Comparison

### FAISS Index Types

| Index Type | Build Time | Search Time | Memory | Recall | Use Case |
|------------|------------|-------------|--------|--------|----------|
| **Flat** | O(1) | O(n*d) | High | 1.00 | Small datasets, exact search |
| **IVF** | O(n*d) | O(√n*d) | Medium | 0.95 | Medium datasets, good balance |
| **HNSW** | O(n*log n*d) | O(log n*d) | High | 0.98 | Large datasets, fast search |
| **PQ** | O(n*d) | O(n) | Low | 0.85 | Memory-constrained, compression |

### Index Parameters

**IVF Parameters:**
- `nlist`: Number of clusters (√n to 4√n recommended)
- `nprobe`: Number of clusters to search (1-nlist)

**HNSW Parameters:**
- `M`: Number of connections per layer (4-64, default: 16)
- `efConstruction`: Construction time accuracy (100-500)
- `efSearch`: Search time accuracy (efConstruction to 2*efConstruction)

**PQ Parameters:**
- `m`: Number of subquantizers (dimension/m should be divisible)
- `nbits`: Bits per subquantizer (8 is standard)

---

## Configuration

```yaml
# config.yaml - Vector Store Configuration

vector_store:
  backend: faiss  # faiss, pinecone, qdrant, weaviate, milvus
  
  faiss:
    index_type: HNSW  # Flat, IVF, HNSW, PQ
    metric: cosine  # cosine, euclidean, dot_product
    dimension: 1536
    
    # HNSW parameters
    hnsw_m: 16
    hnsw_ef_construction: 200
    hnsw_ef_search: 100
    
    # IVF parameters
    ivf_nlist: 100
    ivf_nprobe: 10
    
  hybrid_search:
    fusion_method: rrf  # rrf, weighted, cascade
    vector_weight: 0.7
    keyword_weight: 0.3
    enable_reranking: true
    
  batch_operations:
    batch_size: 1000
    parallel_workers: 4
```

---

## Performance Characteristics

### Search Complexity

| Index Type | Build | Search | Memory |
|------------|-------|--------|--------|
| Flat | O(1) | O(n*d) | O(n*d) |
| IVF | O(n*d*k) | O(√n*d) | O(n*d) |
| HNSW | O(n*log n*d) | O(log n*d) | O(n*d*M) |
| PQ | O(n*d) | O(n*m) | O(n*m) |

where n = vectors, d = dimensions, k = clusters, M = HNSW connections, m = subquantizers

### Scalability

- **Small (<10K vectors)**: Use Flat for exact search
- **Medium (10K-1M vectors)**: Use IVF or HNSW
- **Large (>1M vectors)**: Use HNSW with GPU or distributed systems
- **Very Large (>10M vectors)**: Use distributed backends (Milvus, Weaviate)

---

## See Also

- [Embeddings Module](embeddings.md) - Generate vector embeddings
- [Knowledge Graph Module](kg.md) - Graph-based retrieval
- [Core Module](core.md) - Framework orchestration
