
import nbformat as nbf
import os
import sys

nb = nbf.v4.new_notebook()

# Phase 0: Overview
nb.cells.append(nbf.v4.new_markdown_cell("""# RAG vs. GraphRAG: Investigative Intelligence Comparison

## Overview
This notebook provides a rigorous, side-by-side comparison of **Standard RAG (Vector-based)** and **GraphRAG (Graph-based)**, focusing on the Global Intelligence and Security domain.

### The Challenge: Navigating Fragmentation
In intelligence work, facts are scattered across reports. Vector search often fails to bridge "semantic gaps"—logical connections between entities that are not physically co-located in text. 

We will demonstrate how GraphRAG creates a **"Chain of Evidence"** that Vector RAG cannot see.

### Framework: Semantica
We use the [Semantica](https://github.com/Hawksight-AI/semantica) framework to orchestrate common intelligence tasks like entity resolution, conflict detection, and graph-based reasoning."""))

# Phase 0: Setup
nb.cells.append(nbf.v4.new_code_cell("""# Environment Setup
import os
import sys

# Ensure Groq API Key is set if using Groq
# os.environ['GROQ_API_KEY'] = 'your-key'

%pip install -qU semantica networkx matplotlib plotly pandas faiss-cpu"""))

# Phase 1: Gathering
nb.cells.append(nbf.v4.new_markdown_cell("""## 1. Domain Acquisition: Real-World Intelligence gathering
We ingest from high-signal feeds to build our knowledge base."""))

nb.cells.append(nbf.v4.new_code_cell("""from semantica.ingest import WebIngestor, FeedIngestor
from semantica.normalize import TextNormalizer

normalizer = TextNormalizer()
all_content = []

# 1. Global News Feeds (RSS) - Using more robust and accessible feeds
feeds = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen" # Reuters workaround
]
feed_ingestor = FeedIngestor()
for f in feeds:
    try:
        data = feed_ingestor.ingest_feed(f)
        items = data.items[:10]
        for item in items:
            # Fallback chain: content -> description -> title
            text = item.content or item.description or item.title
            if text:
                all_content.append(text)
    except Exception as e:
        print(f"Warning: Failed to ingest feed {f}: {e}")

# 2. Strategic Overviews (Web) - Using pages with more permissive robots.txt
web_urls = [
    "https://www.cia.gov/the-world-factbook/",
    "https://www.cfr.org/backgrounders" 
]
web_ingestor = WebIngestor()
for url in web_urls:
    try:
        content = web_ingestor.ingest_url(url)
        if content.text:
            all_content.append(content.text)
    except Exception as e:
        print(f"Warning: Failed to ingest URL {url}: {e}")

# Clean and normalize
clean_docs = [normalizer.normalize(text) for text in all_content if len(text) > 100] # Increased threshold for higher quality
print(f"Intelligence Knowledge Hub Populated with {len(clean_docs)} reports.")"""))

# Phase 2: Vector RAG
nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Standard Vector RAG Pipeline
Linear retrieval via semantic embedding overlap."""))

nb.cells.append(nbf.v4.new_code_cell("""from semantica.core import Semantica
from semantica.split import EntityAwareChunker
from semantica.vector_store import VectorStore

# v_core = Semantica(embedding={"provider": "openai", "model": "text-embedding-3-small"})
# Using framework defaults which utilize the core.config
v_core = Semantica()

# Using EntityAwareChunker for better intelligence-domain chunking
splitter = EntityAwareChunker(chunk_size=600, chunk_overlap=50)
chunks = []
for doc in clean_docs[:10]:
    chunks.extend(splitter.chunk(doc))

# Initialize Vector Store
vs = VectorStore(backend="faiss", dimension=1536) 
# Use the core embedding generator
embeddings = v_core.embedding_generator.generate_embeddings([str(c.text) for c in chunks[:15]])
vs.store_vectors(vectors=embeddings, metadata=[{"content": str(c.text)} for c in chunks[:15]])

print(f"Vector RAG ready with {len(chunks[:15])} encoded fragments.")"""))

# Phase 3: GraphRAG
nb.cells.append(nbf.v4.new_markdown_cell("""## 3. High-Fidelity GraphRAG Pipeline
Synthesizing entities and relationships from fragmented reports."""))

nb.cells.append(nbf.v4.new_code_cell("""from semantica.kg import GraphBuilder
from semantica.context import AgentContext

gb = GraphBuilder(merge_entities=True)
# We process a subset for demonstration
kg_data = gb.build(sources=[{"text": str(c.text)} for c in chunks[:10]])

# Initialize AgentContext for GraphRAG
# This combines Vector Store and Knowledge Graph for hybrid retrieval
ctx = AgentContext(
    vector_store=vs,
    knowledge_graph=kg_data,
    use_graph_expansion=True,
    max_expansion_hops=2
)

print(f"GraphRAG Synthesis Complete: {len(kg_data.get('entities', []))} entities, {len(kg_data.get('relationships', []))} relationships.")"""))

# Phase 4: Comparative Test
nb.cells.append(nbf.v4.new_markdown_cell("""## 4. The Intelligence Challenge: Multi-Hop Inference
Standard RAG finds fragments *about* a topic. GraphRAG finds *connections between* topics.

Query: **"Identify high-risk security escalations and their regional implications."**"""))

nb.cells.append(nbf.v4.new_code_cell("""from semantica.reasoning import InferenceEngine

user_query = "Identify high-risk security escalations and their regional implications."

print("--- Standard Vector Recall ---")
# Direct search in vector store
v_res = vs.search(user_query, limit=3)
for r in v_res:
    text = r.get('metadata', {}).get('content', 'No content')
    print(f"Recall: {text[:120]}... (Score: {r['score']:.4f})")

print("\\n--- Graph Intelligence Reasoning (Hybrid Retrieval) ---")
# Use AgentContext for multi-hop retrieval
graph_res = ctx.retrieve(user_query, max_results=3)

for i, res in enumerate(graph_res):
    print(f"Result {i+1}: {res['content'][:120]}...")
    if res.get('related_entities'):
        print(f"  🔗 Multi-hop connections: {[e['content'] for e in res['related_entities'][:3]]}")

# Final Synthesis using InferenceEngine
engine = InferenceEngine(provider="groq", model="llama-3.1-70b-versatile")
context_text = "\\n".join([r['content'] for r in graph_res])
prompt = f"Based on the following intelligence context, {user_query}\\n\\nContext:\\n{context_text}"

# Note: Requires GROQ_API_KEY
try:
    answer = engine.generate(prompt)
    print("\\n--- ✨ FINAL INTELLIGENCE SYNTHESIS ---")
    print(answer)
except Exception as e:
    print(f"\\n(LLM synthesis skipped: {e})")
"""))

# Phase 5: Visualization
nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Visualizing the Intelligence Landscape
Seeing the 'Bridges' between disconnected events."""))

nb.cells.append(nbf.v4.new_code_cell("""from semantica.visualization import KGVisualizer
import matplotlib.pyplot as plt

viz = KGVisualizer()
viz.visualize_network(
    kg,
    output="static",
    title="Intelligence Connectivity Map"
)
plt.show()"""))

target_path = 'cookbook/use_cases/advanced_rag/02_RAG_vs_GraphRAG_Comparison.ipynb'
with open(target_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Successfully restructured {target_path} (UTF-8)")
