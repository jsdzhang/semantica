import os

root_dir = r"c:/Users/Mohd Kaif/semantica"

replacements = {
    # Class names
    "FAISSAdapter": "FAISSStore",
    "MilvusAdapter": "MilvusStore",
    "QdrantAdapter": "QdrantStore",
    "WeaviateAdapter": "WeaviateStore",
    "FalkorDBAdapter": "FalkorDBStore",
    "Neo4jAdapter": "Neo4jStore",
    
    # Filename references in imports
    "semantica.vector_store.faiss_adapter": "semantica.vector_store.faiss_store",
    "semantica.vector_store.milvus_adapter": "semantica.vector_store.milvus_store",
    "semantica.vector_store.qdrant_adapter": "semantica.vector_store.qdrant_store",
    "semantica.vector_store.weaviate_adapter": "semantica.vector_store.weaviate_store",
    "semantica.graph_store.falkordb_adapter": "semantica.graph_store.falkordb_store",
    "semantica.graph_store.neo4j_adapter": "semantica.graph_store.neo4j_store",

    # Module references (local imports)
    "from .faiss_adapter": "from .faiss_store",
    "from .milvus_adapter": "from .milvus_store",
    "from .qdrant_adapter": "from .qdrant_store",
    "from .weaviate_adapter": "from .weaviate_store",
    "from .falkordb_adapter": "from .falkordb_store",
    "from .neo4j_adapter": "from .neo4j_store",
    
    # Variable names (optional but requested "better nameing")
    # "faiss_adapter": "faiss_store", 
    # "milvus_adapter": "milvus_store",
    # Be careful with variable names, but let's try to be consistent if it's safe.
    # I'll stick to explicit classes and imports first to avoid breaking local vars too much unless I'm sure.
    # Actually user said "Change all the name from adapter to store... update everything".
    # I'll replace "Adapter" with "Store" in text/comments if it refers to the class.
    
    # Docstrings and Text
    "FAISS Adapter": "FAISS Store",
    "Milvus Adapter": "Milvus Store",
    "Qdrant Adapter": "Qdrant Store",
    "Weaviate Adapter": "Weaviate Store",
    "FalkorDB Adapter": "FalkorDB Store",
    "Neo4j Adapter": "Neo4j Store",
    
    # Generic "Adapter" to "Store" in specific contexts?
    # Maybe risky. Let's stick to the specific ones.
}

extensions = ['.py', '.ipynb', '.md']

for root, dirs, files in os.walk(root_dir):
    if ".git" in root or "__pycache__" in root:
        continue
        
    for file in files:
        if any(file.endswith(ext) for ext in extensions):
            file_path = os.path.join(root, file)
            # Skip the script itself
            if "update_project_refs.py" in file_path or "update_store_names.py" in file_path:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                changed = False
                for old, new in replacements.items():
                    if old in new_content:
                        new_content = new_content.replace(old, new)
                        changed = True
                
                if changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

