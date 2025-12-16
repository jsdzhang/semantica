import os

replacements = {
    "semantica/triplet_store/blazegraph_store.py": ("BlazegraphAdapter", "BlazegraphStore"),
    "semantica/triplet_store/jena_store.py": ("JenaAdapter", "JenaStore"),
    "semantica/triplet_store/rdf4j_store.py": ("RDF4JAdapter", "RDF4JStore"),
    "semantica/triplet_store/virtuoso_store.py": ("VirtuosoAdapter", "VirtuosoStore"),
}

for file_path, (old, new) in replacements.items():
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace(old, new)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"File not found: {file_path}")

# Update __init__.py
init_path = "semantica/triplet_store/__init__.py"
if os.path.exists(init_path):
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update imports
    content = content.replace("from .blazegraph_adapter import BlazegraphAdapter", "from .blazegraph_store import BlazegraphStore")
    content = content.replace("from .jena_adapter import JenaAdapter", "from .jena_store import JenaStore")
    content = content.replace("from .rdf4j_adapter import RDF4JAdapter", "from .rdf4j_store import RDF4JStore")
    content = content.replace("from .virtuoso_adapter import VirtuosoAdapter", "from .virtuoso_store import VirtuosoStore")
    
    # Update __all__ and other references
    content = content.replace("BlazegraphAdapter", "BlazegraphStore")
    content = content.replace("JenaAdapter", "JenaStore")
    content = content.replace("RDF4JAdapter", "RDF4JStore")
    content = content.replace("VirtuosoAdapter", "VirtuosoStore")
    
    # Update docstrings
    content = content.replace("Store Adapters:", "Store Backends:")
    content = content.replace("Store Adapter Pattern", "Store Backend Pattern")
    content = content.replace("Adapter Pattern:", "Backend Pattern:")
    content = content.replace("Adapter Pattern", "Backend Pattern")
    
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {init_path}")
