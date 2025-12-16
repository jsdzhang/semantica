import os

files_to_update = [
    r"c:/Users/Mohd Kaif/semantica/semantica/vector_store/faiss_store.py",
    r"c:/Users/Mohd Kaif/semantica/semantica/vector_store/milvus_store.py",
    r"c:/Users/Mohd Kaif/semantica/semantica/vector_store/qdrant_store.py",
    r"c:/Users/Mohd Kaif/semantica/semantica/vector_store/weaviate_store.py",
    r"c:/Users/Mohd Kaif/semantica/semantica/graph_store/falkordb_store.py",
    r"c:/Users/Mohd Kaif/semantica/semantica/graph_store/neo4j_store.py"
]

replacements = {
    "FAISSAdapter": "FAISSStore",
    "MilvusAdapter": "MilvusStore",
    "QdrantAdapter": "QdrantStore",
    "WeaviateAdapter": "WeaviateStore",
    "FalkorDBAdapter": "FalkorDBStore",
    "Neo4jAdapter": "Neo4jStore",
    "FAISS adapter": "FAISS store",
    "Milvus adapter": "Milvus store",
    "Qdrant adapter": "Qdrant store",
    "Weaviate adapter": "Weaviate store",
    "FalkorDB adapter": "FalkorDB store",
    "Neo4j adapter": "Neo4j store",
    "faiss_adapter": "faiss_store",
    "milvus_adapter": "milvus_store",
    "qdrant_adapter": "qdrant_store",
    "weaviate_adapter": "weaviate_store",
    "falkordb_adapter": "falkordb_store",
    "neo4j_adapter": "neo4j_store"
}

for file_path in files_to_update:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {file_path}")
