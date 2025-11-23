# Ingest Module

The `ingest` module provides comprehensive data ingestion capabilities for loading data from various sources including files, web pages, feeds, databases, and real-time streams.

## Overview

The ingest module supports **50+ file formats** and multiple data sources:

- **File Ingestion**: PDF, DOCX, XLSX, TXT, MD, JSON, CSV, and more
- **Web Scraping**: HTML pages, sitemaps, with JavaScript rendering
- **Feed Processing**: RSS, Atom feeds with automatic updates
- **Database Connectivity**: SQL and NoSQL databases
- **Stream Processing**: Real-time data streams
- **Email Processing**: EML, MSG, MBOX, PST archives
- **Repository Analysis**: Git repositories and code analysis

---

## Algorithms Used

### File Discovery
- **Recursive Traversal**: Depth-first search for file discovery
- **Pattern Matching**: Glob patterns with regex support
- **Filtering**: Extension-based and size-based filtering

### Web Scraping
- **HTML Parsing**: BeautifulSoup/lxml DOM parsing
- **JavaScript Rendering**: Headless browser (Selenium/Playwright)
- **Rate Limiting**: Token bucket algorithm
- **Robots.txt**: Compliance checking

### Stream Processing
- **Batch Buffering**: Sliding window with configurable size
- **Backpressure Handling**: Flow control mechanisms

---

## Quick Start

```python
from semantica.ingest import FileIngestor, WebIngestor, FeedIngestor

# Ingest local files
file_ingestor = FileIngestor(recursive=True)
documents = file_ingestor.ingest("documents/", formats=["pdf", "docx"])

# Ingest web content
web_ingestor = WebIngestor(max_depth=2)
web_docs = web_ingestor.ingest("https://example.com/articles")

# Ingest RSS feeds
feed_ingestor = FeedIngestor(max_items=100)
feed_docs = feed_ingestor.ingest("https://example.com/rss")

print(f"Total documents: {len(documents) + len(web_docs) + len(feed_docs)}")
```

---

## Main Classes

### FileIngestor


**Supported Formats:**

| Category | Formats |
|----------|---------|
| **Documents** | PDF, DOCX, XLSX, PPTX, TXT, RTF, ODT, EPUB, LaTeX, Markdown |
| **Structured** | JSON, YAML, TOML, CSV, TSV, Parquet, Avro, ORC |
| **Web** | HTML, XHTML, XML, JSON-LD, RDFa |
| **Archives** | ZIP, TAR, RAR, 7Z, GZ, BZ2 |
| **Scientific** | BibTeX, EndNote, RIS, JATS XML |
| **Email** | EML, MSG, MBOX, PST |

**Example Usage:**

```python
from semantica.ingest import FileIngestor

# Basic usage
ingestor = FileIngestor()
docs = ingestor.ingest("documents/")

# Advanced configuration
ingestor = FileIngestor(
    recursive=True,
    max_file_size=100 * 1024 * 1024,  # 100MB
    supported_formats=["pdf", "docx", "xlsx"],
    extract_archives=True,
    ocr_enabled=True,
    ocr_language="eng"
)

# Ingest with filters
docs = ingestor.ingest(
    "documents/",
    formats=["pdf", "docx"],
    exclude_patterns=["*draft*", "*temp*"],
    metadata={"source": "company_docs", "version": "1.0"}
)

# Process results
for doc in docs:
    print(f"File: {doc.filename}")
    print(f"Format: {doc.format}")
    print(f"Size: {doc.size} bytes")
    print(f"Pages: {doc.metadata.get('pages', 'N/A')}")
```

---

### WebIngestor


**Example Usage:**

```python
from semantica.ingest import WebIngestor

# Basic web scraping
ingestor = WebIngestor()
docs = ingestor.ingest("https://example.com")

# Advanced configuration
ingestor = WebIngestor(
    max_depth=3,
    respect_robots_txt=True,
    delay_between_requests=1.0,
    user_agent="Semantica/1.0",
    render_javascript=True,
    timeout=30
)

# Scrape with patterns
docs = ingestor.ingest(
    "https://blog.example.com",
    patterns=["*.html", "*/articles/*"],
    exclude_patterns=["*/admin/*", "*/login/*"],
    follow_links=True,
    max_pages=100
)

# Extract metadata
for doc in docs:
    print(f"URL: {doc.url}")
    print(f"Title: {doc.metadata.get('title')}")
    print(f"Author: {doc.metadata.get('author')}")
    print(f"Published: {doc.metadata.get('published_date')}")
```

---

### FeedIngestor


**Example Usage:**

```python
from semantica.ingest import FeedIngestor

# Basic feed ingestion
ingestor = FeedIngestor()
docs = ingestor.ingest("https://example.com/rss")

# Advanced configuration
ingestor = FeedIngestor(
    max_items=1000,
    update_interval=3600,  # 1 hour
    include_content=True,
    fetch_full_content=True
)

# Ingest multiple feeds
feeds = [
    "https://news.ycombinator.com/rss",
    "https://example.com/atom",
    "https://blog.example.com/feed"
]

all_docs = []
for feed_url in feeds:
    docs = ingestor.ingest(feed_url)
    all_docs.extend(docs)

print(f"Total feed items: {len(all_docs)}")
```

---

### DBIngestor


**Example Usage:**

```python
from semantica.ingest import DBIngestor

# SQL database ingestion
ingestor = DBIngestor(
    connection_string="postgresql://user:pass@localhost/db"
)

docs = ingestor.ingest(
    query="SELECT title, content, author, created_at FROM articles WHERE published = true",
    metadata={"source": "articles_db", "version": "1.0"}
)

# NoSQL database ingestion
mongo_ingestor = DBIngestor(
    connection_string="mongodb://localhost:27017/mydb"
)

docs = mongo_ingestor.ingest(
    collection="articles",
    query={"status": "published"},
    projection={"title": 1, "content": 1, "author": 1}
)
```

---

### StreamIngestor


**Example Usage:**

```python
from semantica.ingest import StreamIngestor

# Kafka stream ingestion
ingestor = StreamIngestor(
    stream_type="kafka",
    bootstrap_servers=["localhost:9092"],
    topic="documents",
    group_id="semantica-consumer"
)

# Process stream
for doc in ingestor.stream():
    print(f"Received: {doc.id}")
    # Process document
    
# RabbitMQ stream ingestion
rabbitmq_ingestor = StreamIngestor(
    stream_type="rabbitmq",
    host="localhost",
    queue="documents"
)
```

---

### EmailIngestor


**Example Usage:**

```python
from semantica.ingest import EmailIngestor

# Ingest email files
ingestor = EmailIngestor()
docs = ingestor.ingest("emails/", formats=["eml", "msg"])

# Extract attachments
ingestor = EmailIngestor(
    extract_attachments=True,
    attachment_dir="attachments/"
)

docs = ingestor.ingest("archive.mbox")

# Process emails
for doc in docs:
    print(f"From: {doc.metadata['from']}")
    print(f"Subject: {doc.metadata['subject']}")
    print(f"Date: {doc.metadata['date']}")
    print(f"Attachments: {len(doc.metadata.get('attachments', []))}")
```

---

### RepoIngestor


**Example Usage:**

```python
from semantica.ingest import RepoIngestor

# Ingest Git repository
ingestor = RepoIngestor()
docs = ingestor.ingest(
    "https://github.com/user/repo.git",
    branch="main",
    include_history=True
)

# Analyze code
ingestor = RepoIngestor(
    analyze_code=True,
    extract_functions=True,
    extract_classes=True,
    languages=["python", "javascript"]
)

docs = ingestor.ingest("path/to/local/repo")
```

---

## Common Patterns

### Pattern 1: Multi-Source Ingestion

```python
from semantica.ingest import FileIngestor, WebIngestor, FeedIngestor

sources = []

# Ingest files
file_ingestor = FileIngestor(recursive=True)
sources.extend(file_ingestor.ingest("documents/"))

# Ingest web
web_ingestor = WebIngestor()
sources.extend(web_ingestor.ingest("https://example.com"))

# Ingest feeds
feed_ingestor = FeedIngestor()
sources.extend(feed_ingestor.ingest("https://example.com/rss"))

print(f"Total sources: {len(sources)}")
```

### Pattern 2: Batch Processing with Progress

```python
from semantica.ingest import FileIngestor
from tqdm import tqdm

ingestor = FileIngestor()
files = ingestor.list_files("documents/", recursive=True)

docs = []
for file_path in tqdm(files, desc="Ingesting"):
    doc = ingestor.ingest_file(file_path)
    docs.append(doc)
```

### Pattern 3: Error Handling

```python
from semantica.ingest import FileIngestor, IngestionError

ingestor = FileIngestor()

successful = []
failed = []

for file_path in file_paths:
    try:
        doc = ingestor.ingest_file(file_path)
        successful.append(doc)
    except IngestionError as e:
        print(f"Failed to ingest {file_path}: {e}")
        failed.append((file_path, str(e)))

print(f"Successful: {len(successful)}, Failed: {len(failed)}")
```

---

## Configuration

```yaml
# config.yaml - Ingest Configuration

ingest:
  file:
    recursive: true
    max_file_size: 104857600  # 100MB
    supported_formats: [pdf, docx, xlsx, txt, md, json, csv]
    extract_archives: true
    ocr_enabled: true
    ocr_language: eng
    
  web:
    max_depth: 3
    respect_robots_txt: true
    delay_between_requests: 1.0
    render_javascript: true
    timeout: 30
    max_pages: 1000
    
  feed:
    max_items: 1000
    update_interval: 3600
    fetch_full_content: true
    
  stream:
    batch_size: 100
    max_wait_time: 5
```

---

## See Also

- [Parse Module](parse.md) - Document parsing and content extraction
- [Normalize Module](normalize.md) - Data cleaning and normalization
- [Core Module](core.md) - Framework orchestration
