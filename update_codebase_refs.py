import os

replacements = [
    ("Adapter Pattern", "Backend Pattern"),
    ("Store Adapters", "Store Backends"),
    ("Store Adapter", "Store Backend"),
    ("FAISSAdapter", "FAISSStore"),
    ("MilvusAdapter", "MilvusStore"),
    ("QdrantAdapter", "QdrantStore"),
    ("WeaviateAdapter", "WeaviateStore"),
    ("Neo4jAdapter", "Neo4jStore"),
    ("FalkorDBAdapter", "FalkorDBStore"),
    ("BlazegraphAdapter", "BlazegraphStore"),
    ("JenaAdapter", "JenaStore"),
    ("RDF4JAdapter", "RDF4JStore"),
    ("VirtuosoAdapter", "VirtuosoStore"),
    ("faiss_adapter", "faiss_store"),
    ("milvus_adapter", "milvus_store"),
    ("qdrant_adapter", "qdrant_store"),
    ("weaviate_adapter", "weaviate_store"),
    ("neo4j_adapter", "neo4j_store"),
    ("falkordb_adapter", "falkordb_store"),
    ("blazegraph_adapter", "blazegraph_store"),
    ("jena_adapter", "jena_store"),
    ("rdf4j_adapter", "rdf4j_store"),
    ("virtuoso_adapter", "virtuoso_store"),
    ("store_adapter", "store_backend"),
]

files = [
    "semantica/vector_store/__init__.py",
    "semantica/graph_store/__init__.py",
    "semantica/vector_store/vector_store_usage.md",
    "semantica/graph_store/graph_store_usage.md",
    "semantica/triplet_store/triplet_store_usage.md",
    "tests/test_graph_store.py",
    "tests/vector_store/test_pinecone_removal.py",
    "cookbook/introduction/20_Triplet_Store.ipynb",
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old, new in replacements:
            content = content.replace(old, new)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes in {file_path}")
    else:
        print(f"File not found: {file_path}")
