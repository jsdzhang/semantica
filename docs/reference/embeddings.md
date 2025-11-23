# Embeddings Module

> **Transform text and images into dense vector representations for semantic search and similarity matching.**

---

## 🎯 Overview

=== "Text Embeddings"

    <div class="grid cards" markdown>

    -   :material-text:{ .lg .middle } **Transformer Encoders**
        
        BERT, RoBERTa, DeBERTa with advanced pooling strategies

    -   :material-lightning-bolt:{ .lg .middle } **Sentence Transformers**
        
        Fast, efficient embeddings optimized for semantic similarity

    -   :material-api:{ .lg .middle } **API Providers**
        
        OpenAI, Cohere, Google, HuggingFace integration

    </div>

=== "Image Embeddings"

    <div class="grid cards" markdown>

    -   :material-image:{ .lg .middle } **CLIP**
        
        Contrastive Language-Image Pre-training for multimodal embeddings

    -   :material-eye:{ .lg .middle } **Vision Transformers**
        
        ViT models for high-quality image representations

    -   :material-layers:{ .lg .middle } **CNN Models**
        
        ResNet, EfficientNet for feature extraction

    </div>

=== "Multimodal"

    <div class="grid cards" markdown>

    -   :material-merge:{ .lg .middle } **Fusion Strategies**
        
        Concatenation, weighted sum, cross-attention fusion

    -   :material-compare:{ .lg .middle } **Similarity**
        
        Text-image similarity in joint embedding space

    </div>

---

## ⚙️ Algorithms Used

### Text Embedding Algorithms
- **Transformer Encoders**: BERT, RoBERTa, DeBERTa with mean pooling
- **Sentence Transformers**: Siamese networks trained on sentence pairs
- **OpenAI Embeddings**: Proprietary transformer models (ada-002, text-embedding-3)
- **Contrastive Learning**: InfoNCE loss for similarity learning

### Pooling Strategies
- **Mean Pooling**: Average of all token embeddings
- **Max Pooling**: Maximum value across token dimension
- **CLS Token**: Use [CLS] token embedding (BERT-style)
- **Weighted Mean**: Attention-weighted averaging

### Normalization
- **L2 Normalization**: `v_norm = v / ||v||₂` for cosine similarity
- **Min-Max Scaling**: Scale to [0, 1] range
- **Standard Scaling**: Zero mean, unit variance

---

## Main Classes

### EmbeddingGenerator


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `generate(texts)` | Generate embeddings | Provider-specific encoding with pooling |
| `generate_batch(texts, batch_size)` | Batch generation | Chunked processing with parallel execution |
| `encode(text)` | Encode single text | Tokenization + forward pass + pooling |
| `normalize(embeddings)` | Normalize vectors | L2 normalization |
| `set_provider(provider, model)` | Set embedding provider | Provider initialization |

**Supported Providers:**

| Provider | Models | Dimensions | Speed | Cost |
|----------|--------|------------|-------|------|
| **OpenAI** | text-embedding-3-small, text-embedding-3-large, ada-002 | 1536, 3072 | Fast | $$ |
| **Cohere** | embed-english-v3.0, embed-multilingual-v3.0 | 1024 | Fast | $$ |
| **HuggingFace** | Custom models | Variable | Medium | Free |
| **Sentence Transformers** | all-MiniLM-L6-v2, all-mpnet-base-v2 | 384, 768 | Fast | Free |
| **Google** | textembedding-gecko | 768 | Fast | $$ |

**Example:**

```python
from semantica.embeddings import EmbeddingGenerator

# OpenAI embeddings
generator = EmbeddingGenerator(
    provider="openai",
    model="text-embedding-3-large",
    dimensions=3072
)

texts = ["Machine learning is fascinating", "AI transforms industries"]
embeddings = generator.generate(texts)

print(f"Shape: {embeddings.shape}")  # (2, 3072)
print(f"Normalized: {np.linalg.norm(embeddings[0]):.3f}")  # 1.000

# Batch processing
large_texts = [...]  # 10,000 texts
embeddings = generator.generate_batch(
    texts=large_texts,
    batch_size=100,
    show_progress=True
)
```

---

### TextEmbedder


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `embed(text)` | Embed single text | Tokenization + encoding + pooling |
| `embed_batch(texts)` | Batch embedding | Parallel processing |
| `embed_query(query)` | Embed query (optimized) | Query-specific encoding |
| `embed_documents(documents)` | Embed documents | Document-specific encoding |
| `tokenize(text)` | Tokenize text | Subword tokenization (BPE/WordPiece) |

**Tokenization Algorithms:**
- **BPE (Byte Pair Encoding)**: Iterative merging of frequent pairs
- **WordPiece**: Similar to BPE, used in BERT
- **SentencePiece**: Unigram language model tokenization

**Example:**

```python
from semantica.embeddings import TextEmbedder

embedder = TextEmbedder(
    model="sentence-transformers/all-mpnet-base-v2",
    pooling="mean",  # mean, max, cls
    normalize=True
)

# Different embedding strategies
query_embedding = embedder.embed_query("What is machine learning?")
doc_embeddings = embedder.embed_documents([
    "Machine learning is a subset of AI...",
    "Deep learning uses neural networks..."
])

# Calculate similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity([query_embedding], doc_embeddings)
print(f"Similarities: {similarity}")
```

---

### ImageEmbedder


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `embed(image)` | Embed single image | CNN/ViT encoding |
| `embed_batch(images)` | Batch image embedding | Parallel CNN/ViT processing |
| `preprocess(image)` | Preprocess image | Resize, normalize, augment |
| `extract_features(image)` | Extract visual features | Feature map extraction |

**Image Embedding Models:**
- **CLIP**: Contrastive Language-Image Pre-training
- **ViT (Vision Transformer)**: Transformer for images
- **ResNet**: Residual networks
- **EfficientNet**: Efficient convolutional networks

**Example:**

```python
from semantica.embeddings import ImageEmbedder
from PIL import Image

embedder = ImageEmbedder(
    model="openai/clip-vit-base-patch32",
    image_size=224
)

image = Image.open("photo.jpg")
embedding = embedder.embed(image)

print(f"Image embedding shape: {embedding.shape}")
```

---

### MultimodalEmbedder


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `embed(text, image)` | Embed text + image | Multimodal fusion |
| `embed_text_image(text, image)` | Joint embedding | CLIP-style contrastive learning |
| `fuse_embeddings(text_emb, image_emb)` | Fuse embeddings | Concatenation or weighted sum |
| `calculate_similarity(text, image)` | Text-image similarity | Cosine similarity in joint space |

**Fusion Strategies:**
- **Concatenation**: `[text_emb; image_emb]`
- **Weighted Sum**: `α*text_emb + (1-α)*image_emb`
- **Cross-Attention**: Attention-based fusion

**Example:**

```python
from semantica.embeddings import MultimodalEmbedder

embedder = MultimodalEmbedder(
    model="openai/clip-vit-base-patch32",
    fusion_strategy="weighted_sum",
    text_weight=0.6
)

text = "A cat sitting on a couch"
image = Image.open("cat.jpg")

embedding = embedder.embed(text, image)
similarity = embedder.calculate_similarity(text, image)
print(f"Text-Image similarity: {similarity:.3f}")
```

---

### EmbeddingOptimizer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `optimize(embeddings)` | Optimize embeddings | Dimensionality reduction + quantization |
| `reduce_dimensions(embeddings, target_dim)` | Reduce dimensions | PCA or random projection |
| `quantize(embeddings, bits)` | Quantize embeddings | Scalar or product quantization |
| `compress(embeddings)` | Compress embeddings | Lossy compression |

**Optimization Techniques:**
- **PCA**: Linear dimensionality reduction
- **Random Projection**: Fast approximate reduction
- **Product Quantization**: Divide into subvectors, quantize separately
- **Scalar Quantization**: Reduce precision (float32 → int8)

**Example:**

```python
from semantica.embeddings import EmbeddingOptimizer

optimizer = EmbeddingOptimizer()

# Reduce dimensions
reduced = optimizer.reduce_dimensions(
    embeddings=embeddings,
    target_dim=256,  # from 1536 to 256
    method="pca"
)

# Quantize to int8
quantized = optimizer.quantize(
    embeddings=embeddings,
    bits=8  # float32 → int8 (4x compression)
)
```

---

## Configuration

```yaml
# config.yaml - Embeddings Configuration

embeddings:
  provider: openai  # openai, cohere, huggingface, sentence-transformers
  
  openai:
    model: text-embedding-3-large
    dimensions: 3072
    api_key: ${OPENAI_API_KEY}
    
  sentence_transformers:
    model: all-mpnet-base-v2
    pooling: mean  # mean, max, cls
    normalize: true
    device: cuda  # cuda, cpu
    
  batch_processing:
    batch_size: 100
    parallel_workers: 4
    show_progress: true
    
  optimization:
    reduce_dimensions: false
    target_dimensions: 256
    quantize: false
    quantization_bits: 8
```

---

## Performance Characteristics

### Embedding Speed

| Model | Dimensions | Tokens/sec | Batch Size | Device |
|-------|------------|------------|------------|--------|
| OpenAI ada-002 | 1536 | 10,000 | 100 | API |
| OpenAI text-embedding-3-large | 3072 | 8,000 | 100 | API |
| all-MiniLM-L6-v2 | 384 | 5,000 | 32 | GPU |
| all-mpnet-base-v2 | 768 | 2,000 | 32 | GPU |
| BERT-base | 768 | 1,000 | 16 | GPU |

### Memory Requirements

| Model | Dimensions | Memory (GPU) | Memory (CPU) |
|-------|------------|--------------|--------------|
| MiniLM | 384 | 1 GB | 2 GB |
| MPNet | 768 | 2 GB | 4 GB |
| BERT-large | 1024 | 4 GB | 8 GB |

---

## See Also

- [Vector Store Module](vector_store.md) - Store and search embeddings
- [Semantic Extract Module](semantic_extract.md) - Extract entities
- [Core Module](core.md) - Framework orchestration
