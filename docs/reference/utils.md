# Utils Module

Utility functions and helper classes for common operations including file handling, text processing, and data manipulation.

## Overview

- **File Operations**: File I/O, path manipulation, compression
- **Text Utilities**: String manipulation, encoding, hashing
- **Data Utilities**: JSON/YAML handling, serialization
- **Logging**: Structured logging with multiple handlers
- **Validation**: Schema validation, type checking

---

## Algorithms Used

### File Operations
- **Hashing**: MD5, SHA256 for file integrity checking
- **Compression**: GZIP, LZMA algorithms for file compression
- **Chunking**: Fixed-size or sliding window chunking for large files

### Text Processing
- **Tokenization**: Whitespace and punctuation-based tokenization
- **Similarity**: Jaccard similarity, Cosine similarity
- **Hashing**: MurmurHash3 for fast non-cryptographic hashing

### Data Serialization
- **JSON**: Fast JSON encoding/decoding
- **YAML**: Human-readable configuration format
- **Pickle**: Python object serialization

---

## Main Classes

### FileUtils


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `list_files(directory, pattern)` | List files matching pattern | Recursive directory traversal |
| `read_file(path)` | Read file contents | Buffered I/O |
| `write_file(path, content)` | Write to file | Atomic write with temp file |
| `hash_file(path, algorithm)` | Calculate file hash | Streaming hash calculation |
| `compress_file(path, format)` | Compress file | GZIP/LZMA compression |

**Example:**

```python
from semantica.utils import FileUtils

# List files
files = FileUtils.list_files(
    directory="documents/",
    pattern="*.pdf",
    recursive=True
)

# Hash file
file_hash = FileUtils.hash_file("document.pdf", algorithm="sha256")
print(f"SHA256: {file_hash}")

# Compress file
FileUtils.compress_file("large_file.json", format="gzip")
```

---

### TextUtils


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `clean_text(text)` | Clean and normalize text | Regex-based cleaning |
| `tokenize(text, method)` | Tokenize text | Whitespace/punctuation splitting |
| `calculate_similarity(text1, text2)` | Calculate text similarity | Jaccard or Cosine similarity |
| `hash_text(text)` | Hash text string | MurmurHash3 |
| `remove_stopwords(text, language)` | Remove stopwords | Dictionary-based filtering |

**Example:**

```python
from semantica.utils import TextUtils

# Clean text
text = "  Hello,   World!  \n\n  "
cleaned = TextUtils.clean_text(text)
print(cleaned)  # "Hello, World!"

# Calculate similarity
similarity = TextUtils.calculate_similarity(
    "machine learning",
    "deep learning",
    method="jaccard"
)
print(f"Similarity: {similarity:.2f}")
```

---

### DataUtils


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `load_json(path)` | Load JSON file | JSON parsing |
| `save_json(data, path)` | Save to JSON | JSON serialization |
| `load_yaml(path)` | Load YAML file | YAML parsing |
| `save_yaml(data, path)` | Save to YAML | YAML serialization |
| `validate_schema(data, schema)` | Validate against schema | JSON Schema validation |

**Example:**

```python
from semantica.utils import DataUtils

# Load/save JSON
data = DataUtils.load_json("config.json")
DataUtils.save_json(data, "output.json", pretty=True)

# Load/save YAML
config = DataUtils.load_yaml("config.yaml")
DataUtils.save_yaml(config, "output.yaml")

# Validate schema
is_valid = DataUtils.validate_schema(
    data=data,
    schema={"type": "object", "properties": {...}}
)
```

---

### LoggerUtils


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `get_logger(name)` | Get logger instance | Logger factory |
| `configure_logging(level, format)` | Configure logging | Handler setup |

---

## Configuration

```yaml
# config.yaml - Utils Configuration

utils:
  logging:
    level: INFO  # DEBUG, INFO, WARNING, ERROR
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers:
      - console
      - file
      
  file:
    default_encoding: utf-8
    buffer_size: 8192
    
  text:
    default_language: en
    remove_stopwords: true
```

---

## See Also

- [Core Module](core.md) - Framework orchestration
- [Ingest Module](ingest.md) - Data ingestion
- [Parse Module](parse.md) - Document parsing
