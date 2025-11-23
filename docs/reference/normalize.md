# Normalize Module

The `normalize` module provides data cleaning, normalization, and standardization capabilities to prepare text and data for semantic processing.

## Overview

- **Text Cleaning**: Remove noise, fix encoding, standardize whitespace
- **Entity Normalization**: Standardize entity names and formats
- **Date Normalization**: Parse and standardize date formats
- **Number Normalization**: Standardize numeric values and units
- **Language Detection**: Identify document language
- **Encoding Handling**: Fix character encoding issues

---

## Algorithms Used

### Text Normalization
- **Unicode Normalization**: NFC, NFD, NFKC, NFKD forms
- **Whitespace Normalization**: Regex-based cleanup
- **Case Folding**: Locale-aware case normalization
- **Diacritic Removal**: Unicode decomposition

### Entity Normalization
- **Fuzzy Matching**: Levenshtein distance < threshold
- **Phonetic Matching**: Soundex, Metaphone algorithms
- **Abbreviation Expansion**: Dictionary-based expansion

### Date/Time Normalization
- **Parsing**: dateutil parser with multiple format support
- **Timezone Handling**: pytz for timezone conversion
- **Standardization**: ISO 8601 format output

---

## Quick Start

```python
from semantica.normalize import TextNormalizer

# Initialize normalizer
normalizer = TextNormalizer()

# Normalize text
normalized_text = normalizer.normalize(raw_text)

# Normalize documents
normalized_docs = normalizer.normalize_documents(documents)
```

---

## Main Classes

### TextNormalizer


**Example:**

```python
from semantica.normalize import TextNormalizer

normalizer = TextNormalizer(
    lowercase=False,
    remove_punctuation=False,
    remove_numbers=False,
    remove_whitespace=True,
    fix_encoding=True
)

text = "  Apple Inc.  was founded in 1976.  "
normalized = normalizer.normalize(text)
# Output: "Apple Inc. was founded in 1976."
```

### EntityNormalizer


**Example:**

```python
from semantica.normalize import EntityNormalizer

normalizer = EntityNormalizer(
    fuzzy_matching=True,
    similarity_threshold=0.85
)

# Normalize entity names
entities = ["Apple Inc.", "Apple", "AAPL", "Apple Computer"]
normalized = normalizer.normalize(entities)
# All mapped to canonical form: "Apple Inc."
```

### DateNormalizer


**Example:**

```python
from semantica.normalize import DateNormalizer

normalizer = DateNormalizer(output_format="ISO8601")

dates = ["Jan 1, 2024", "01/01/2024", "2024-01-01"]
normalized = [normalizer.normalize(d) for d in dates]
# All output: "2024-01-01T00:00:00Z"
```

---

## See Also

- [Parse Module](parse.md)
- [Semantic Extract Module](semantic_extract.md)
